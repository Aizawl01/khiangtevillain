(() => {
  const cards = [...document.querySelectorAll('.look-card')];
  const dialog = document.querySelector('#look-dialog');
  const closeButton = document.querySelector('.dialog-close');
  const title = document.querySelector('#look-dialog-title');
  const summary = document.querySelector('#look-dialog-summary');
  const prompt = document.querySelector('#look-dialog-prompt');
  const copy = document.querySelector('#copy-look');
  const summaries = {
    datamosh: 'Real generated result: a Mizo creator on a rain-wet Aizawl lane, broken by hard codec blocks.',
    blob: 'Real generated result: a Mizo portrait with imperfect computer-vision detections over the photograph.',
    flash: 'Real generated result: direct flash, monsoon rain and an Aizawl rooftop café.',
    receipt: 'Real generated result: a fictional thermal-paper artifact from an Aizawl shared-taxi night.',
    crt: 'Real generated result: one contemporary Mizo subject inside an analogue broadcast frame.',
    dither: 'Real generated result: a rain-day Aizawl street reduced to one-bit ink and paper.',
    phosphor: 'Real generated result: one Mizo night scene drawn in overdriven magenta phosphor.'
  };
  let sourcePrompts = {};
  const promptsReady = fetch('assets/trendy-prompts.json')
    .then(response => response.ok ? response.json() : [])
    .then(items => { sourcePrompts = Object.fromEntries(items.map(item => [item.n, item.prompt])); })
    .catch(() => {});
  let selected = cards[0];
  const select = (card, open = true) => {
    selected = card;
    cards.forEach(item => item.classList.toggle('active', item === card));
    const { look, title: cardTitle, copy: cardCopy, promptId } = card.dataset;
    title.textContent = cardTitle;
    summary.textContent = summaries[look];
    prompt.value = sourcePrompts[promptId] || cardCopy || 'Prompt loading…';
    if (open) dialog.showModal();
  };
  cards.forEach(card => card.addEventListener('click', async () => { await promptsReady; select(card); }));
  closeButton.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  copy.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(prompt.value); copy.textContent = 'Copied ✓'; }
    catch { prompt.focus(); prompt.select(); document.execCommand('copy'); copy.textContent = 'Copied ✓'; }
    window.setTimeout(() => { copy.textContent = 'Copy prompt'; }, 1800);
  });
})();
