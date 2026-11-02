// Motion is optional. The brand, film, services and contact are present in HTML.
import {initMotion} from './motion.js';
try { initMotion(document.querySelector('.hero-art')); }
catch { console.info('The portfolio remains available without motion.'); }

