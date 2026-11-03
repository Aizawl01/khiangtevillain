const canvas = document.querySelector('#runner-canvas');
const ctx = canvas.getContext('2d');
const screen = document.querySelector('#game-screen');
const startButton = document.querySelector('#start-run');
const restartButton = document.querySelector('#restart-run');
const soundButton = document.querySelector('#sound-toggle');
const scoreNode = document.querySelector('#score');
const bestNode = document.querySelector('#best-score');
const statusNode = document.querySelector('#run-status');
const seedNode = document.querySelector('#daily-seed');

const W = canvas.width;
const H = canvas.height;
const ground = 842;
const storeKey = 'kv-frequency-zero-v1';
const dailyKey = new Date().toISOString().slice(0, 10);
seedNode.textContent = dailyKey.replaceAll('-', '.');

function readStore() {
  try { return JSON.parse(localStorage.getItem(storeKey)) || {best:0, badges:[]}; }
  catch { return {best:0, badges:[]}; }
}
function saveStore() { try { localStorage.setItem(storeKey, JSON.stringify(store)); } catch { /* no persistence available */ } }
const store = readStore();
bestNode.textContent = String(store.best).padStart(4, '0');

function hash(value) { return [...value].reduce((total, char) => ((total << 5) - total + char.charCodeAt(0)) | 0, 0) >>> 0; }
function mulberry32(seed) { return () => { seed += 0x6D2B79F5; let t = seed; t = Math.imul(t ^ t >>> 15, t | 1); t ^= t + Math.imul(t ^ t >>> 7, t | 61); return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
let random = mulberry32(hash(dailyKey));
let state = 'idle';
let score = 0;
let signals = 0;
let elapsed = 0;
let spawnIn = 0;
let beatIn = 0;
let items = [];
let rain = Array.from({length:80}, (_, index) => ({x:(index * 89) % W, y:(index * 137) % H, speed:240 + (index % 7) * 34}));
let lastFrame = performance.now();
let audioContext;
let soundOn = false;
const player = {x:138, y:ground - 94, vy:0, jumps:0, tilt:0};

function tone(frequency, length=.09, type='sine', gain=.025) {
  if (!soundOn) return;
  audioContext ||= new AudioContext();
  if (audioContext.state === 'suspended') audioContext.resume();
  const oscillator = audioContext.createOscillator();
  const volume = audioContext.createGain();
  oscillator.type = type; oscillator.frequency.value = frequency;
  volume.gain.setValueAtTime(gain, audioContext.currentTime);
  volume.gain.exponentialRampToValueAtTime(.0001, audioContext.currentTime + length);
  oscillator.connect(volume).connect(audioContext.destination);
  oscillator.start(); oscillator.stop(audioContext.currentTime + length);
}

function jump() {
  if (state === 'idle' || state === 'over') { startRun(); return; }
  if (state !== 'running' || player.jumps >= 2) return;
  player.vy = player.jumps ? -720 : -820;
  player.jumps += 1;
  tone(player.jumps === 1 ? 196 : 294, .08, 'square', .018);
}

function startRun() {
  // Each day uses one repeatable course, so a restart is a fair attempt at the same run.
  random = mulberry32(hash(dailyKey));
  state = 'running'; score = 0; signals = 0; elapsed = 0; spawnIn = .85; beatIn = .15; items = [];
  Object.assign(player, {y:ground - 94, vy:0, jumps:0, tilt:0});
  screen.classList.add('is-hidden');
  statusNode.textContent = 'RUN LIVE — jump crates, catch frequency signals, stay off the drone grid.';
  tone(98, .16, 'sawtooth', .035);
}

function endRun() {
  if (state !== 'running') return;
  state = 'over';
  store.best = Math.max(store.best, Math.floor(score));
  if (score >= 500 && !store.badges.includes('MONSOON')) store.badges.push('MONSOON');
  if (signals >= 10 && !store.badges.includes('FREQUENCY')) store.badges.push('FREQUENCY');
  saveStore();
  bestNode.textContent = String(store.best).padStart(4, '0');
  screen.querySelector('.screen-kicker').textContent = `RUN SCORE // ${String(Math.floor(score)).padStart(4, '0')}`;
  screen.querySelector('h2').innerHTML = 'SIGNAL<br><em>LOST.</em>';
  screen.querySelector('.game-screen > p:not(.screen-kicker)').innerHTML = `Signals captured: ${signals}.<br>Best: ${store.best}. Beat your own ghost next run.`;
  startButton.textContent = 'Run Again ↗';
  screen.classList.remove('is-hidden');
  statusNode.textContent = signals >= 8 ? 'Clean run. The beat is getting louder.' : 'Run ended. Learn the rooftop rhythm and go again.';
  tone(73, .32, 'sawtooth', .04);
}

function spawn() {
  const isSignal = random() < .45;
  const isTall = !isSignal && random() < .42;
  items.push({
    kind: isSignal ? 'signal' : 'obstacle',
    x: W + 55,
    y: isSignal ? ground - 175 - random() * 95 : ground - (isTall ? 125 : 68),
    w: isSignal ? 42 : isTall ? 54 : 68,
    h: isSignal ? 42 : isTall ? 125 : 68,
    phase: random() * Math.PI * 2
  });
}

function hit(a, b) { return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y; }

function update(dt) {
  rain.forEach(drop => { drop.y += drop.speed * dt; drop.x -= drop.speed * .18 * dt; if (drop.y > H + 20) { drop.y = -20; drop.x = random() * W; } });
  if (state !== 'running') return;
  elapsed += dt; score += dt * (18 + signals * 1.5);
  const speed = 350 + Math.min(160, elapsed * 5.5);
  spawnIn -= dt;
  if (spawnIn <= 0) { spawn(); spawnIn = .74 + random() * .72 - Math.min(.18, elapsed / 180); }
  player.vy += 2050 * dt;
  player.y += player.vy * dt;
  if (player.y >= ground - 94) { player.y = ground - 94; player.vy = 0; player.jumps = 0; }
  player.tilt += ((player.vy / 1300) - player.tilt) * Math.min(1, dt * 10);
  const bounds = {x:player.x + 10, y:player.y + 12, w:48, h:78};
  items.forEach(item => {
    item.x -= speed * dt;
    item.phase += dt * 5;
    const box = {x:item.x, y:item.y, w:item.w, h:item.h};
    if (hit(bounds, box)) {
      if (item.kind === 'signal') {
        item.remove = true; signals += 1; score += 55 + signals * 6;
        tone([110, 146, 196, 247][signals % 4], .13, 'triangle', .04);
        statusNode.textContent = `FREQUENCY ${signals} CAPTURED — ${['kick','bass','synth','spark'][signals % 4]} layer online.`;
      } else endRun();
    }
  });
  items = items.filter(item => !item.remove && item.x + item.w > -80);
  beatIn -= dt;
  if (beatIn <= 0) { beatIn = .46; if (signals) tone(signals > 2 ? 82 : 65, .045, 'square', .018 + signals * .002); }
}

function neonText(text, x, y, size, color, align='left') {
  ctx.save(); ctx.textAlign = align; ctx.font = `700 ${size}px "DM Mono"`; ctx.fillStyle = color; ctx.shadowColor = color; ctx.shadowBlur = 17; ctx.fillText(text, x, y); ctx.restore();
}
function drawHills() {
  ctx.fillStyle = '#0e1730'; ctx.beginPath(); ctx.moveTo(0, 580); for (let x=0; x<=W; x+=55) ctx.lineTo(x, 510 + Math.sin(x*.018)*55 + Math.cos(x*.053)*30); ctx.lineTo(W, H); ctx.lineTo(0,H); ctx.fill();
  ctx.fillStyle = '#111b36'; for (let x=0; x<W; x+=44) { const h=75 + (x*13 % 150); ctx.fillRect(x, ground-h, 35, h); for(let y=ground-h+15;y<ground-10;y+=22){ if((x+y)%3) {ctx.fillStyle='#4feaff55';ctx.fillRect(x+8,y,4,6);ctx.fillStyle='#111b36';} } }
}
function drawPlayer() {
  ctx.save(); ctx.translate(player.x + 34, player.y + 46); ctx.rotate(player.tilt * .42);
  ctx.fillStyle='#06070d'; ctx.shadowColor='#ff3e9d';ctx.shadowBlur=22;ctx.beginPath();ctx.arc(0,-9,35,Math.PI,0);ctx.lineTo(34,55);ctx.lineTo(-34,55);ctx.closePath();ctx.fill();
  ctx.fillStyle='#15233b';ctx.fillRect(-25,-7,50,34);ctx.fillStyle='#4feaff';ctx.shadowColor='#4feaff';ctx.shadowBlur=18;ctx.fillRect(-18,3,14,5);ctx.fillRect(4,3,14,5);
  ctx.fillStyle='#20283a';ctx.fillRect(-28,52,18,36);ctx.fillRect(10,52,18,36);ctx.fillStyle='#edece5';ctx.fillRect(-32,84,25,8);ctx.fillRect(7,84,25,8);ctx.restore();
}
function drawItem(item) {
  ctx.save();ctx.translate(item.x + item.w/2,item.y + item.h/2);
  if(item.kind==='signal') {ctx.rotate(item.phase);ctx.strokeStyle='#d9ff36';ctx.lineWidth=3;ctx.shadowColor='#d9ff36';ctx.shadowBlur=20;ctx.beginPath();ctx.arc(0,0,17+Math.sin(item.phase)*3,0,Math.PI*2);ctx.stroke();ctx.fillStyle='#4feaff';ctx.fillRect(-5,-5,10,10);}
  else {ctx.fillStyle='#181a26';ctx.strokeStyle='#ff3e9d';ctx.lineWidth=3;ctx.shadowColor='#ff3e9d';ctx.shadowBlur=12;ctx.fillRect(-item.w/2,-item.h/2,item.w,item.h);ctx.strokeRect(-item.w/2,-item.h/2,item.w,item.h);ctx.fillStyle='#ff3e9d';ctx.fillRect(-item.w*.28,-3,item.w*.56,6);}
  ctx.restore();
}
function draw() {
  ctx.clearRect(0,0,W,H); const sky=ctx.createLinearGradient(0,0,0,H);sky.addColorStop(0,'#050813');sky.addColorStop(.55,'#10132a');sky.addColorStop(1,'#07080f');ctx.fillStyle=sky;ctx.fillRect(0,0,W,H);
  drawHills(); ctx.strokeStyle='#4feaff44';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(0,ground+2);ctx.lineTo(W,ground+2);ctx.stroke();
  ctx.fillStyle='#4feaff12';for(let x=-50;x<W+50;x+=42){ctx.fillRect(x + ((elapsed*70)%42),ground+30,2,H-ground)}
  rain.forEach(drop=>{ctx.strokeStyle='#8beeff55';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(drop.x,drop.y);ctx.lineTo(drop.x-9,drop.y+26);ctx.stroke();});
  items.forEach(drawItem); drawPlayer();
  neonText(`SIG ${String(signals).padStart(2,'0')}`, 25, 44, 18, '#d9ff36'); neonText(`SPD ${Math.floor(350 + Math.min(160,elapsed*5.5))}`, W-25, 44, 18, '#4feaff', 'right');
  scoreNode.textContent=String(Math.floor(score)).padStart(4,'0');
}
function frame(now) { const dt=Math.min(.033,(now-lastFrame)/1000);lastFrame=now;update(dt);draw();requestAnimationFrame(frame); }

startButton.addEventListener('click', startRun); restartButton.addEventListener('click', startRun);
soundButton.addEventListener('click', () => { soundOn=!soundOn;soundButton.setAttribute('aria-pressed',String(soundOn));soundButton.textContent=soundOn?'Sound on':'Sound off'; if(soundOn) tone(220,.08,'triangle',.03); });
canvas.addEventListener('pointerdown', event => { event.preventDefault(); jump(); });
addEventListener('keydown', event => { if([' ','ArrowUp','w','W'].includes(event.key)){event.preventDefault();jump();} });
requestAnimationFrame(frame);
