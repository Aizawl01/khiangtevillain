import { cpSync, mkdirSync, rmSync } from 'node:fs';
import { resolve } from 'node:path';

const root=process.cwd();
const output=resolve(root,'_site');
const copy=(source,destination=source)=>cpSync(resolve(root,source),resolve(output,destination),{recursive:true});

rmSync(output,{recursive:true,force:true});
mkdirSync(output,{recursive:true});

for(const file of ['index.html','styles.css','script.js','brand.css','brand.js','learning.css','mizo-prompts.js','motion.js','motion.css','favicon.png'])copy(file);
for(const asset of ['character.webp','portrait.webp','brand.webp','brand-film.mp4','three.module.js','three.core.js','FLAQ-LICENSE.txt','THREE-LICENSE.txt'])copy(`assets/${asset}`);
for(const folder of ['prompt-packs','game','cloud'])copy(folder);
for(const version of ['lab','lab-v3','lab-v4','lab-v5','lab-v6','lab-v7','lab-v8','lab-v9','lab-v10','lab-v11','lab-v12','lab-v13'])copy('lab',version);

console.log(`Built ${output}`);
