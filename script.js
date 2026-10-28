const prompts=[
  {category:'image',title:'Mizo Neon Rider',text:'Cinematic editorial photo of a rider on a mountain road in Mizoram, mist folding through green hills, black and red cyberpunk riding gear, wet asphalt reflections, low-angle 35mm lens, sharp subject, atmospheric film grain.'},
  {category:'image',title:'Album Cover System',text:'Square experimental album cover for [ARTIST / TRACK], one bold central symbol, ink-black negative space, acid-lime and hot-pink accents, tactile photocopy texture, modern underground electronic music identity, no text.'},
  {category:'video',title:'Cyber City Arrival',text:'A lone creator arrives in a rain-soaked future city at night. Handheld camera follows from behind, neon signs flicker through fog, slow motion rain, documentary energy, cinematic 16:9, 8 seconds, no dialogue.'},
  {category:'video',title:'Music Visual Loop',text:'Seamless 6-second loop: chrome mask slowly turns toward camera, liquid neon ripples across its surface, black void background, high contrast, hypnotic, album visualizer, centered composition.'},
  {category:'music',title:'Hill City After Dark',text:'Create a dark alternative electronic track at 92 BPM: distant choir texture, warped Mizo-inspired percussion feel, sub bass, vinyl crackle, one memorable synth motif, cinematic build, no vocals.'},
  {category:'music',title:'Trailer Pulse',text:'Instrumental cinematic trap cue, 110 BPM, sparse piano notes, distorted bass, rising impacts, tense and confident, designed for a 30-second tech-fashion reel, clean ending hit.'},
  {category:'code',title:'Creative Portfolio Brief',text:'Build a single-page portfolio for an AI filmmaker and creative technologist. Use a dark cyberpunk editorial style, accessible semantic HTML, responsive CSS, no framework, no paid APIs. Include work, prompt library, contact and copy-to-clipboard buttons.'},
  {category:'code',title:'Prompt Organizer',text:'Create a lightweight browser-only prompt library in vanilla JavaScript. Prompts need category filtering, search, copy button, share fallback, and localStorage favorites. No backend and no external credentials.'}
];

const grid=document.querySelector('#prompt-grid');
const filters=document.querySelectorAll('.filter');
const toast=document.querySelector('#toast');

function showToast(message){
  toast.textContent=message;
  toast.classList.add('show');
  setTimeout(()=>toast.classList.remove('show'),1800);
}

async function copyPrompt(text){
  try{
    await navigator.clipboard.writeText(text);
  }catch{
    const area=document.createElement('textarea');
    area.value=text;
    document.body.append(area);
    area.select();
    document.execCommand('copy');
    area.remove();
  }
  showToast('PROMPT COPIED');
}

async function sharePrompt(item){
  if(navigator.share){
    try{
      await navigator.share({title:item.title,text:item.text});
      return;
    }catch(error){
      if(error.name==='AbortError') return;
    }
  }
  await copyPrompt(item.text);
}

function render(category='all'){
  const visiblePrompts=prompts
    .map((prompt,index)=>({prompt,index}))
    .filter(({prompt})=>category==='all'||prompt.category===category);

  grid.innerHTML=visiblePrompts.map(({prompt,index},position)=>`<article class="prompt-card">
    <div class="card-meta"><span>${prompt.category}</span><span>${String(position+1).padStart(2,'0')}</span></div>
    <h3>${prompt.title}</h3>
    <p class="prompt-copy">${prompt.text}</p>
    <div class="card-actions">
      <button class="mini-button" type="button" data-copy="${index}">Copy prompt</button>
      <button class="mini-button" type="button" data-share="${index}">Share</button>
    </div>
  </article>`).join('');

  grid.querySelectorAll('[data-copy]').forEach(button=>{
    button.addEventListener('click',()=>copyPrompt(prompts[Number(button.dataset.copy)].text));
  });
  grid.querySelectorAll('[data-share]').forEach(button=>{
    button.addEventListener('click',()=>sharePrompt(prompts[Number(button.dataset.share)]));
  });
}

filters.forEach(button=>button.addEventListener('click',()=>{
  filters.forEach(filter=>filter.classList.remove('active'));
  button.classList.add('active');
  render(button.dataset.category);
}));

render();
document.querySelector('#year').textContent=new Date().getFullYear();
