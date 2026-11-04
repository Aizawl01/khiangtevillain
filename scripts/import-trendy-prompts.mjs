import { writeFile } from 'node:fs/promises';

const source = 'https://marcelgrauu.github.io/trendy-styles/';
const page = await fetch(source).then(response => {
  if (!response.ok) throw new Error(`Prompt source returned ${response.status}`);
  return response.text();
});
const start = page.indexOf('const DATA = ') + 'const DATA = '.length;
const end = page.indexOf('];', start) + 1;
if (start < 'const DATA = '.length || end <= start) throw new Error('Could not locate prompt data.');
const records = JSON.parse(page.slice(start, end)).map(({ n, name, prompt }) => ({ n, name, prompt }));
await writeFile(new URL('../assets/trendy-prompts.json', import.meta.url), `${JSON.stringify(records, null, 2)}\n`);
