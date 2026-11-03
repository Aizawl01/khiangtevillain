// Motion is optional. The brand, film, services and contact are present in HTML.
import {initMotion} from './motion.js';

const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
const boot = document.querySelector('#signal-boot');
const skipBoot = document.querySelector('#skip-boot');

function initSignalBoot() {
  if (!boot || reduceMotion.matches) return;

  let finished = false;
  const onKeydown = event => { if (event.key === 'Escape') finish(); };
  const finish = () => {
    if (finished) return;
    finished = true;
    removeEventListener('keydown', onKeydown);
    boot.classList.add('is-leaving');
    boot.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('booting');
    setTimeout(() => boot.remove(), 720);
  };

  document.body.classList.add('booting');
  boot.classList.add('is-active');
  boot.setAttribute('aria-hidden', 'false');
  skipBoot?.focus({preventScroll:true});
  skipBoot?.addEventListener('click', finish);
  addEventListener('keydown', onKeydown);
  setTimeout(finish, 1850);
}

function initPageSignal() {
  const field = document.createElement('div');
  field.className = 'page-signal-field';
  field.setAttribute('aria-hidden', 'true');
  document.body.append(field);

  const addSignal = event => {
    if (reduceMotion.matches || document.documentElement.classList.contains('motion-paused')) return;
    if (event.target.closest('a, button, input, video, summary, .hero-art, .prompt-card')) return;
    const ripple = document.createElement('span');
    ripple.className = 'page-signal-ripple';
    ripple.style.setProperty('--x', `${event.clientX}px`);
    ripple.style.setProperty('--y', `${event.clientY}px`);
    ripple.style.setProperty('--rotation', `${Math.round(Math.random() * 360)}deg`);
    field.append(ripple);
    ripple.addEventListener('animationend', () => ripple.remove(), {once:true});
  };

  addEventListener('pointerdown', addSignal, {passive:true});
}

function initScrollGlitch() {
  let quietTimer;
  const root = document.documentElement;
  const stop = () => root.classList.remove('is-scrolling');
  const flash = () => {
    if (reduceMotion.matches || root.classList.contains('motion-paused')) return;
    root.classList.add('is-scrolling');
    clearTimeout(quietTimer);
    quietTimer = setTimeout(stop, 130);
  };
  addEventListener('scroll', flash, {passive:true});
  document.addEventListener('motionchange', () => {
    if (root.classList.contains('motion-paused')) stop();
  });
}

initSignalBoot();
initPageSignal();
initScrollGlitch();
try { initMotion(document.querySelector('.hero-art')); }
catch { console.info('The portfolio remains available without motion.'); }

