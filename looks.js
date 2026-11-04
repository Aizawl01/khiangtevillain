(() => {
  const cards = [...document.querySelectorAll('.look-card')];
  const dialog = document.querySelector('#look-dialog');
  const closeButton = document.querySelector('.dialog-close');
  const title = document.querySelector('#look-dialog-title');
  const summary = document.querySelector('#look-dialog-summary');
  const prompt = document.querySelector('#look-dialog-prompt');
  const copy = document.querySelector('#copy-look');
  const summaries = {
    smear: 'A cinematic codec-fragment treatment that keeps the creator readable and the signal in motion.',
    flash: 'A modern Aizawl night portrait where a direct flash cuts through rain and colour.',
    crt: 'An intentional analogue-broadcast treatment with scan lines and a late-night archive feel.',
    dither: 'A graphic black-ink approach for posters, covers and bold first frames.',
    phosphor: 'A restrained cyan-and-pink glow treatment built for the KhiangteVillain world.',
    receipt: 'A collectible thermal-print layout for release announcements, track drops and event artwork.',
    datamosh: 'A real generated example built from a codec-damage brief: hard blocks, clean image area, no fake glitch overlay.'
  };
  let selected = cards[0];
  const select = (card, open = true) => {
    selected = card;
    cards.forEach(item => item.classList.toggle('active', item === card));
    const { look, number, title: cardTitle, copy: cardCopy } = card.dataset;
    title.textContent = cardTitle;
    summary.textContent = summaries[look];
    prompt.value = cardCopy;
    if (open) dialog.showModal();
  };
  cards.forEach(card => card.addEventListener('click', () => select(card)));
  closeButton.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  copy.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(prompt.value); copy.textContent = 'Copied ✓'; }
    catch { prompt.focus(); prompt.select(); document.execCommand('copy'); copy.textContent = 'Copied ✓'; }
    window.setTimeout(() => { copy.textContent = 'Copy prompt'; }, 1800);
  });
})();
