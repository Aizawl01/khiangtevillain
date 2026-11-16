(() => {
  'use strict';
  const endpoint = document.querySelector('meta[name="download-log-endpoint"]')?.content || '';
  if (!/^https:\/\/script\.google\.com\/macros\/s\/[A-Za-z0-9_-]+\/exec$/.test(endpoint)) return;
  const dialog = document.getElementById('download-dialog');
  const form = document.getElementById('download-form');
  const status = document.getElementById('download-status');
  const submit = form.querySelector('button[type="submit"]');
  const ready = document.getElementById('download-ready');
  const transport = document.getElementById('download-transport');
  const close = document.getElementById('download-close');
  let selected;
  let requestId;
  let timer;
  let pending = false;
  let opener;
  const allowedFiles = new Set(['lyric-heart.zip','lyricsvisualizer.py','krismas-lidar.zip','krismasvisualizer.py','ascii-christmas-drama.zip']);
  function source() {
    const utm = new URL(location.href).searchParams.get('utm_source')?.toLowerCase() || '';
    let ref = '';
    try { ref = new URL(document.referrer).hostname; } catch {}
    if (utm === 'instagram' || /(^|\.)instagram\.com$/.test(ref)) return 'Instagram';
    if (utm === 'youtube' || /(^|\.)(youtube\.com|youtu\.be)$/.test(ref)) return 'YouTube';
    return 'Direct / other';
  }
  function finish(message) {
    clearTimeout(timer);
    pending = false;
    submit.disabled = false;
    submit.textContent = 'Save & get the code ↓';
    status.textContent = message;
  }
  document.querySelectorAll('a[download]').forEach(link => link.addEventListener('click', event => {
    const url = new URL(link.href);
    const file = url.pathname.split('/').pop();
    if (url.origin !== location.origin || !allowedFiles.has(file)) return;
    event.preventDefault();
    selected = {file, href:url.href};
    opener = link;
    requestId = crypto.randomUUID();
    ready.hidden = true;
    ready.removeAttribute('href');
    finish('');
    form.elements.file.value = file;
    form.elements.request_id.value = requestId;
    form.elements.source.value = source();
    document.getElementById('download-project').textContent = file;
    form.action = endpoint;
    form.target = transport.name;
    dialog.showModal();
  }));
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => { clearTimeout(timer); pending=false; opener?.focus(); });
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (pending || !selected || !form.reportValidity()) return;
    pending = true;
    submit.disabled = true;
    submit.textContent = 'Saving your request…';
    status.textContent = 'Saving securely to the private download log…';
    timer = setTimeout(() => finish('The log has not confirmed your request yet. Please try again in a moment.'), 30000);
    HTMLFormElement.prototype.submit.call(form);
  });
  window.addEventListener('message', event => {
    let host;
    try { host = new URL(event.origin).hostname; } catch { return; }
    if (!(host === 'script.google.com' || /^[a-z0-9-]+-script\.googleusercontent\.com$/.test(host))) return;
    const data = event.data;
    if (!pending || !data || data.type !== 'kv-download-result' || data.requestId !== requestId) return;
    if (!data.ok || data.file !== selected.file) { finish('Could not save your request. Please check your details and try again in a minute.'); return; }
    finish('Saved. Your download is ready.');
    ready.href = selected.href;
    ready.download = selected.file;
    ready.hidden = false;
    ready.focus();
  });
  ready.addEventListener('click', () => { if (!ready.hidden) status.textContent = 'Download requested. If your browser asks, choose Save.'; });
})();
