const board = document.querySelector('#signal-board');
const count = document.querySelector('#signal-count');
const status = document.querySelector('#game-status');
const restart = document.querySelector('#restart-game');
const transmission = document.querySelector('#transmission-link');
const consolePanel = document.querySelector('.hunt-console');
const beacons = [...document.querySelectorAll('.beacon')];
const storageKey = 'kv-signal-hunt';

function readProgress() {
  try { return new Set(JSON.parse(localStorage.getItem(storageKey) || '[]')); }
  catch { return new Set(); }
}
function writeProgress(found) {
  try { localStorage.setItem(storageKey, JSON.stringify([...found])); }
  catch { /* The game still works if storage is unavailable. */ }
}
let found = readProgress();

function render() {
  const complete = found.size === beacons.length;
  count.textContent = String(found.size);
  beacons.forEach(beacon => {
    const active = found.has(beacon.dataset.signal);
    beacon.classList.toggle('is-found', active);
    beacon.setAttribute('aria-pressed', String(active));
    beacon.disabled = active;
  });
  consolePanel.classList.toggle('is-unlocked', complete);
  transmission.hidden = !complete;
  if (complete) status.textContent = 'All signals stabilised. The Villain transmission is unlocked.';
  else status.textContent = `${beacons.length - found.size} signal${beacons.length - found.size === 1 ? '' : 's'} still hiding in the grid. Tap every beacon.`;
}

beacons.forEach(beacon => beacon.addEventListener('click', () => {
  found.add(beacon.dataset.signal);
  writeProgress(found);
  render();
}));

restart.addEventListener('click', () => {
  found = new Set();
  writeProgress(found);
  render();
  board.focus?.();
});

render();
