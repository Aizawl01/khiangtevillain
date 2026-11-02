import * as THREE from './assets/three.module.js';

export function initMotion(art) {
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)');
  let enabled = !preference.matches;
  const toggle = document.createElement('button');
  toggle.className = 'motion-toggle';
  toggle.type = 'button';
  document.querySelector('.nav').append(toggle);
  const updateToggle = () => {
    toggle.textContent = enabled ? 'Motion ON' : 'Motion OFF';
    toggle.setAttribute('aria-pressed', String(enabled));
    toggle.setAttribute('aria-label', 'Enable motion effects');
    document.documentElement.classList.toggle('motion-paused', !enabled);
    if (!enabled) document.querySelectorAll('.button').forEach(button => button.style.translate='');
    document.dispatchEvent(new Event('motionchange'));
  };
  toggle.addEventListener('click', () => { enabled = !enabled; updateToggle(); });
  preference.addEventListener('change', () => { enabled = !preference.matches; updateToggle(); });

  const pulse = document.createElement('button');
  pulse.type = 'button'; pulse.className = 'signal-trigger';
  pulse.innerHTML = '<span aria-hidden="true">✳</span> Activate signal';
  pulse.setAttribute('aria-label', 'Play a ripple across the character artwork');
  art.append(pulse);
  const hint = document.createElement('span'); hint.className = 'motion-hint';
  hint.textContent = finePointer.matches ? 'MOVE / DRAG TO DISTORT' : 'TAP TO SEND A SIGNAL';
  art.append(hint);

  const ribbon = document.createElement('div'); ribbon.className = 'motion-ribbon';
  ribbon.setAttribute('aria-hidden', 'true');
  ribbon.innerHTML = '<div class="ribbon-track">'+Array(4).fill('<div class="ribbon-group"><span>AI FILMS</span><i>✳</i><span>SOUND WORLDS</span><i>✳</i><span>CREATIVE CODE</span><i>✳</i><span>FROM AIZAWL</span><i>✳</i></div>').join('')+'</div>';
  document.querySelector('.hero').after(ribbon);

  const heading = document.querySelector('.about h2');
  heading.setAttribute('aria-label', 'Imagination. With intent.');
  heading.innerHTML = '<span aria-hidden="true">IMAGINATION.</span><br><span aria-hidden="true">WITH INTENT.</span>';
  const cards = [...document.querySelectorAll('.work-grid article')];
  const media = ['assets/character.webp', 'assets/portrait.webp', 'assets/brand.webp'];
  cards.forEach((card, i) => {
    card.style.setProperty('--card-index', i);
    const content = document.createElement('div'); content.className = 'direction-copy';
    while (card.firstChild) content.append(card.firstChild);
    const picture = document.createElement('div'); picture.className = 'direction-art';
    const img = document.createElement('img'); img.src = media[i]; img.alt = ''; img.loading = 'lazy';
    picture.append(img); card.append(content, picture);
    if (i === 1) picture.insertAdjacentHTML('beforeend', '<div class="waveform" aria-hidden="true">'+Array.from({length:32},(_,n)=>'<i style="--bar:'+n+';--height:'+(15+Math.sin(n*2.1)**2*65)+'%"></i>').join('')+'</div>');
    if (i === 2) picture.insertAdjacentHTML('beforeend','<span class="code-glyph" aria-hidden="true">&lt; / &gt;</span>');
  });
  document.querySelector('.work-grid').classList.add('motion-cards');

  let queued = false;
  const paintScroll = () => {
    queued = false;
    const vh = innerHeight;
    const position = heading.getBoundingClientRect();
    const progress = Math.max(0, Math.min(1, (vh * .88 - position.top) / (vh * .65)));
    heading.style.setProperty('--reveal', enabled ? progress * 100 + '%' : '100%');
    cards.forEach((card, i) => {
      const next = cards[i + 1];
      const overlap = next ? Math.max(0, Math.min(1, (vh * .65 - next.getBoundingClientRect().top) / (vh * .55))) : 0;
      card.style.transform = enabled && innerWidth > 760 ? 'scale('+ (1 - overlap * .045) +')' : '';
      card.style.filter = enabled && innerWidth > 760 ? 'brightness('+(1 - overlap * .23)+')' : '';
    });
    const loopWidth=ribbon.querySelector('.ribbon-group').getBoundingClientRect().width;
    ribbon.querySelector('.ribbon-track').style.transform = enabled && loopWidth ? 'translateX('+(-((scrollY * .17) % loopWidth))+'px)' : '';
  };
  const schedule = () => { if (!queued) { queued = true; requestAnimationFrame(paintScroll); } };
  addEventListener('scroll', schedule, {passive:true});
  addEventListener('resize', schedule, {passive:true});
  document.addEventListener('motionchange', schedule);
  document.querySelectorAll('.button').forEach(button => {
    button.addEventListener('pointermove', event => {
      if (!enabled || !finePointer.matches) return;
      const rect = button.getBoundingClientRect();
      button.style.translate = ((event.clientX-rect.left-rect.width/2)*.12)+'px '+((event.clientY-rect.top-rect.height/2)*.12)+'px';
    });
    button.addEventListener('pointerleave', () => { button.style.translate = ''; });
  });
  const waveform = document.querySelector('.waveform');
  let waveVisible = false;
  const syncWave = () => waveform.querySelectorAll('i').forEach(bar => {
    bar.style.animationPlayState = enabled && waveVisible && !document.hidden ? 'running' : 'paused';
  });
  new IntersectionObserver(entries => {waveVisible=entries[0].isIntersecting;syncWave();}).observe(waveform);
  document.addEventListener('visibilitychange', syncWave);
  document.addEventListener('motionchange', syncWave);
  updateToggle(); paintScroll();

  // The supplied portrait is a texture, not a rigged face or expression sequence.
  // A subdivided plane supplies elastic depth; a shader supplies local refraction.
  let renderer, failed=false;
  const fallback = () => {
    failed=true;renderer?.setAnimationLoop(null);art.classList.remove('webgl-ready');
    if(renderer) renderer.domElement.hidden=true;
    pulse.hidden=true;hint.hidden=true;
  };
  try {
    renderer = new THREE.WebGLRenderer({alpha:true, antialias:false});
    renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
    renderer.domElement.setAttribute('aria-hidden', 'true');
    const scene = new THREE.Scene();
    const camera = new THREE.OrthographicCamera(-1,1,1,-1,0,2); camera.position.z = 1;
    const uniforms = {
      uImage:{value:null}, uFit:{value:new THREE.Vector2(1,1)},
      uPointer:{value:new THREE.Vector2(.5,.5)}, uPull:{value:new THREE.Vector2()},
      uStrength:{value:0}, uTime:{value:0}, uPulse:{value:9}, uAspect:{value:1}
    };
    const material = new THREE.ShaderMaterial({uniforms, transparent:true,
      vertexShader:`varying vec2 vUv; uniform vec2 uPointer; uniform vec2 uPull;
        void main(){vUv=uv; vec3 p=position; float falloff=exp(-distance(uv,uPointer)*5.0);
        p.xy+=uPull*falloff*.12; gl_Position=vec4(p.xy,0.,1.);}`,
      fragmentShader:`precision highp float;
        varying vec2 vUv; uniform sampler2D uImage; uniform vec2 uFit; uniform vec2 uPointer;
        uniform vec2 uPull; uniform float uStrength,uTime,uPulse,uAspect;
        void main(){
          vec2 delta=vUv-uPointer; vec2 metric=delta*vec2(uAspect,1.);
          float d=length(metric); float falloff=exp(-d*7.0);
          float wave=sin(d*42.-uPulse*9.)*exp(-abs(d-uPulse*.38)*13.)*exp(-uPulse*1.2);
          vec2 lens=delta*falloff*uStrength*.18;
          vec2 ripple=normalize(delta+vec2(.0001))*wave*.022;
          vec2 uv=(vUv-lens-ripple-uPull*falloff*.025-.5)*uFit+.5;
          if(uv.x<0.||uv.x>1.||uv.y<0.||uv.y>1.){gl_FragColor=vec4(.031,.035,.078,1.);return;}
          float split=falloff*uStrength*.004+abs(wave)*.003;
          vec3 color=vec3(texture2D(uImage,uv+vec2(split,0.)).r,texture2D(uImage,uv).g,texture2D(uImage,uv-vec2(split,0.)).b);
          color+=vec3(.04,.22,.25)*max(wave,0.)*.3;
          gl_FragColor=vec4(color,1.);
        }`
    });
    scene.add(new THREE.Mesh(new THREE.PlaneGeometry(2,2,48,64),material));
    const target = new THREE.Vector2(.5,.5), pull = new THREE.Vector2(), velocity = new THREE.Vector2();
    let inside=false, dragging=false, visible=true, previous=0, pulseAge=9, loaded=false;
    const resize = () => {
      renderer.setSize(art.clientWidth,art.clientHeight);
      const ratio=art.clientWidth/art.clientHeight, imageRatio=941/1672;
      uniforms.uAspect.value=ratio;
      uniforms.uFit.value.set(Math.max(1,ratio/imageRatio),Math.max(1,imageRatio/ratio));
      if (loaded) renderer.render(scene,camera);
    };
    new ResizeObserver(resize).observe(art); resize();
    new THREE.TextureLoader().load('./assets/character.webp', texture => {
      uniforms.uImage.value=texture; loaded=true;
      art.append(renderer.domElement); art.classList.add('webgl-ready'); resize();
    }, undefined, () => { fallback();renderer.dispose(); });
    const locate = event => {
      const rect=art.getBoundingClientRect();
      target.set((event.clientX-rect.left)/rect.width,1-(event.clientY-rect.top)/rect.height);
    };
    art.addEventListener('pointermove', event => {
      if (!enabled) return; locate(event); inside=true;
      if (dragging) pull.set(Math.max(-.25,Math.min(.25,(target.x-.5)*.5)),Math.max(-.25,Math.min(.25,(target.y-.5)*.5)));
    });
    art.addEventListener('pointerdown', event => {
      if (!enabled || event.target.closest('button')) return;
      locate(event); inside=true; pulseAge=0;
      if (event.pointerType==='mouse') {dragging=true; art.setPointerCapture(event.pointerId);}
    });
    const release = () => {dragging=false;pull.set(0,0);};
    art.addEventListener('pointerup', release); art.addEventListener('pointercancel', release);
    art.addEventListener('lostpointercapture', release);
    art.addEventListener('pointerleave', () => {inside=false;release();});
    pulse.addEventListener('click', () => {if(enabled){target.set(.5,.65);pulseAge=0;}});
    const frame = time => {
      if (!loaded) return;
      const dt=Math.min((time-previous)/1000||.016,.035); previous=time;
      uniforms.uTime.value=time/1000;
      uniforms.uPointer.value.lerp(target,1-Math.exp(-dt*9));
      uniforms.uStrength.value += ((inside&&enabled?1:0)-uniforms.uStrength.value)*(1-Math.exp(-dt*7));
      // Damped spring, bounded time step prevents jumps after tab suspension.
      velocity.addScaledVector(pull.clone().sub(uniforms.uPull.value),dt*65).multiplyScalar(Math.exp(-dt*9));
      uniforms.uPull.value.addScaledVector(velocity,dt);
      pulseAge+=dt; uniforms.uPulse.value=enabled?pulseAge:9;
      renderer.render(scene,camera);
    };
    const sync = () => {
      if(failed) return;
      renderer.setAnimationLoop(visible&&!document.hidden&&enabled?frame:null);
      pulse.disabled=!enabled;
      if (!enabled) {release();velocity.set(0,0);inside=false;uniforms.uStrength.value=0;uniforms.uPull.value.set(0,0);uniforms.uPulse.value=9;if(loaded)renderer.render(scene,camera);}
      previous=performance.now();
    };
    new IntersectionObserver(entries => {visible=entries[0].isIntersecting;sync();}).observe(art);
    document.addEventListener('visibilitychange',sync);
    document.addEventListener('motionchange',sync);
    renderer.domElement.addEventListener('webglcontextlost', event => {
      event.preventDefault();fallback();
    });
    sync();
  } catch(error) {
    fallback();renderer?.dispose();
    console.info('Showing the original artwork: WebGL is unavailable.', error?.message || error);
  }
}
