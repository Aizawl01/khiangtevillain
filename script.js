const prompts=[
  {category:'image',title:'Mizo Neon Rider',text:'Cinematic editorial photo of a rider on a mountain road in Mizoram, mist folding through green hills, black and red cyberpunk riding gear, wet asphalt reflections, low-angle 35mm lens, sharp subject, atmospheric film grain.'},
  {category:'image',title:'Album Cover System',text:'Square experimental album cover for [ARTIST / TRACK], one bold central symbol, ink-black negative space, acid-lime and hot-pink accents, tactile photocopy texture, modern underground electronic music identity, no text.'},
  {category:'video',title:'Cyber City Arrival',text:'A lone creator arrives in a rain-soaked future city at night. Handheld camera follows from behind, neon signs flicker through fog, slow motion rain, documentary energy, cinematic 16:9, 8 seconds, no dialogue.'},
  {category:'video',title:'Music Visual Loop',text:'Seamless 6-second loop: chrome mask slowly turns toward camera, liquid neon ripples across its surface, black void background, high contrast, hypnotic, album visualizer, centered composition.'},
  {category:'music',title:'Hill City After Dark',text:'Create a dark alternative electronic track at 92 BPM: distant choir texture, warped Mizo-inspired percussion feel, sub bass, vinyl crackle, one memorable synth motif, cinematic build, no vocals.'},
  {category:'music',title:'Trailer Pulse',text:'Instrumental cinematic trap cue, 110 BPM, sparse piano notes, distorted bass, rising impacts, tense and confident, designed for a 30-second tech-fashion reel, clean ending hit.'},
  {category:'code',title:'Creative Portfolio Brief',text:'Build a single-page portfolio for an AI filmmaker and creative technologist. Use a dark cyberpunk editorial style, accessible semantic HTML, responsive CSS, no framework, no paid APIs. Include work, prompt library, contact and copy-to-clipboard buttons.'},
  {category:'code',title:'Prompt Organizer',text:'Create a lightweight browser-only prompt library in vanilla JavaScript. Prompts need category filtering, search, copy button, share fallback, and localStorage favorites. No backend and no external credentials.'},
  {category:'image',title:'Aizawl Night Shift',text:'Contemporary editorial street portrait in Aizawl after rain: a young creative in a clean technical jacket stands beside a glowing storefront on a steep hill road, wet concrete, electric-blue reflections, misty city lights behind, 35mm documentary photography, confident and understated, vertical 4:5 composition.'},
  {category:'image',title:'Hill City Product Drop',text:'Premium sneaker campaign photographed on a modern Aizawl rooftop at blue hour, low concrete wall, distant layered hills and soft fog, chrome speaker, acid-lime product accent, crisp studio-grade detail mixed with real street texture, wide-angle 24mm, square 1:1 composition.'},
  {category:'video',title:'Aizawl Rain Reel',text:'Vertical 9:16 fashion reel, one continuous 8-second scene. A creator walks uphill through a rain-wet Aizawl street at night; passing headlights slide across the pavement, light fog moves through the frame, the camera tracks backward smoothly at walking pace, energetic modern music-video mood.'},
  {category:'video',title:'Cloudline Transition',text:'Vertical short video, 6 seconds. Start on a close-up of a hand closing a laptop in a minimal hill-city cafe; the camera whip-pans upward into low clouds moving over the Aizawl skyline, then settles on neon window light. Natural motion blur, soft dawn light, polished social reel pacing.'},
  {category:'video',title:'Night Ride Teaser',text:'Cinematic 16:9 teaser, 8 seconds. A black motorcycle moves slowly along a clean mountain road outside Aizawl at blue hour; the camera follows from a low rear angle, tail light reflects on wet asphalt, clouds drift across dark green hills, restrained premium ad energy.'},
  {category:'music',title:'Cloudline Club Edit',text:'Create a modern alternative-electronic track at 108 BPM for a hill-city night reel: tight kick, elastic sub bass, clipped percussion, airy vocal texture without lyrics, one bright synth hook, brief halftime switch, clean four-bar ending for seamless looping.'},
  {category:'music',title:'Monsoon Creator Intro',text:'Produce a 12-second cinematic creator intro: distant thunder ambience, a single plucked electric guitar note, warm sub bass swelling into precise electronic drums, modern and spacious, no vocals, end with a sharp logo sting and one second of clean tail.'},
  {category:'code',title:'Viral Reel Blueprint',text:'Act as a short-form creative director. Build a 7-day vertical-video plan for a modern AI creator in Aizawl. For each reel provide: a 2-second visual hook, one clear shot list, on-screen text under 8 words, edit rhythm, caption, and a call to action. Keep it specific, energetic, and contemporary; avoid traditional-costume clichés.'},
  {category:'trending',title:'Creator Blind Spot',text:'Based on this creator profile: [PASTE YOUR NICHE, AUDIENCE, AND LAST 5 POSTS], identify the one question I should be asking but am not. Then give me: the hidden opportunity, why it matters now, three reel ideas, and the first action to take today. Be direct, specific, and constructive.'},
  {category:'trending',title:'Aizawl Carousel Director',text:'Act as an elite social art director. Turn this idea into a 7-slide Instagram carousel for a modern Aizawl creator: [IDEA]. Give each slide a bold 6-word-or-less headline, the visual composition, the exact on-image text, and a final save-worthy call to action. Style: clean editorial, hill-city energy, no generic AI language.'},
  {category:'trending',title:'Scroll-Stop Image Concept',text:'Create a high-fashion editorial image for a vertical social post: a young creative on an Aizawl rooftop after a storm, reflective wet concrete, minimal technical clothing, one acid-lime object, cloud-covered hills in the distance, direct flash photography, sharp texture, art-magazine composition, 4:5.'},
  {category:'trending',title:'10-Second Hook Lab',text:'You are a viral short-video strategist. For this topic: [TOPIC], write five 10-second reel concepts. Each must include: a first-frame visual hook, spoken or on-screen line, three-shot sequence, sound-design cue, caption, and one reason a viewer would save or share it. Make every concept feel visual, fast, and original.'}
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
