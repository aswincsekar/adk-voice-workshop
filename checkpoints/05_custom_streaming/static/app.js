const button = document.querySelector("#connect");
const status = document.querySelector("#status");
const events = document.querySelector("#events");

let socket;
let stream;
let audioContext;
let processor;
let source;
let nextPlaybackTime = 0;
const playbackNodes = new Set();

function addEvent(text, className = "") {
  const row = document.createElement("div");
  row.className = `event ${className}`;
  row.textContent = text;
  events.prepend(row);
}

function base64FromBytes(bytes) {
  let binary = "";
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary);
}

function bytesFromBase64(value) {
  const binary = atob(value);
  return Uint8Array.from(binary, character => character.charCodeAt(0));
}

function downsampleToPcm16(input, inputRate, outputRate = 16000) {
  const ratio = inputRate / outputRate;
  const length = Math.round(input.length / ratio);
  const output = new Int16Array(length);
  for (let i = 0; i < length; i++) {
    const start = Math.round(i * ratio);
    const end = Math.min(Math.round((i + 1) * ratio), input.length);
    let total = 0;
    for (let j = start; j < end; j++) total += input[j];
    const sample = Math.max(-1, Math.min(1, total / Math.max(1, end - start)));
    output[i] = sample < 0 ? sample * 0x8000 : sample * 0x7fff;
  }
  return new Uint8Array(output.buffer);
}

function sampleRateFromMimeType(mimeType, fallback = 24000) {
  const match = /(?:^|;)\s*rate=(\d+)/i.exec(mimeType || "");
  return match ? Number(match[1]) : fallback;
}

function playPcm(base64, mimeType) {
  const sampleRate = sampleRateFromMimeType(mimeType);
  const bytes = bytesFromBase64(base64);
  const samples = new Int16Array(bytes.buffer, bytes.byteOffset, bytes.byteLength / 2);
  const buffer = audioContext.createBuffer(1, samples.length, sampleRate);
  const channel = buffer.getChannelData(0);
  for (let i = 0; i < samples.length; i++) channel[i] = samples[i] / 32768;
  const node = audioContext.createBufferSource();
  node.buffer = buffer;
  node.connect(audioContext.destination);
  playbackNodes.add(node);
  node.addEventListener("ended", () => playbackNodes.delete(node));
  nextPlaybackTime = Math.max(nextPlaybackTime, audioContext.currentTime);
  node.start(nextPlaybackTime);
  nextPlaybackTime += buffer.duration;
}

async function connect() {
  audioContext = new AudioContext();
  await audioContext.resume();
  stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true } });
  socket = new WebSocket(`${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws`);
  socket.addEventListener("open", () => {
    status.textContent = "Listening — try: Find a room after three";
    button.textContent = "Disconnect";
    button.classList.add("connected");
    source = audioContext.createMediaStreamSource(stream);
    processor = audioContext.createScriptProcessor(4096, 1, 1);
    processor.onaudioprocess = event => {
      if (socket.readyState !== WebSocket.OPEN) return;
      const pcm = downsampleToPcm16(event.inputBuffer.getChannelData(0), audioContext.sampleRate);
      socket.send(JSON.stringify({ type: "audio", mime_type: "audio/pcm;rate=16000", data: base64FromBytes(pcm) }));
    };
    source.connect(processor);
    processor.connect(audioContext.destination);
  });
  socket.addEventListener("message", event => {
    const message = JSON.parse(event.data);
    if (message.type === "audio") playPcm(message.data, message.mime_type);
    if (message.type === "transcript") addEvent(`${message.speaker}: ${message.text}`, message.speaker);
    if (message.type === "tool") addEvent(`tool ${message.phase}: ${message.name}`, "tool");
    if (message.type === "interrupted") {
      playbackNodes.forEach(node => { try { node.stop(); } catch (_) {} });
      playbackNodes.clear();
      nextPlaybackTime = audioContext.currentTime;
      addEvent("agent interrupted");
    }
    if (message.type === "error") addEvent(message.message);
  });
  socket.addEventListener("close", disconnect);
}

function disconnect() {
  if (socket?.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ type: "audio_stream_end" }));
    socket.close();
  }
  processor?.disconnect(); source?.disconnect();
  stream?.getTracks().forEach(track => track.stop());
  audioContext?.close();
  playbackNodes.clear();
  socket = stream = audioContext = processor = source = null;
  nextPlaybackTime = 0;
  status.textContent = "Disconnected";
  button.textContent = "Connect microphone";
  button.classList.remove("connected");
}

button.addEventListener("click", async () => {
  try { socket ? disconnect() : await connect(); }
  catch (error) { status.textContent = error.message; disconnect(); }
});
