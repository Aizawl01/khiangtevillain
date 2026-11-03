import * as THREE from '../assets/three.module.js';

const stage = document.querySelector('#stage');
const host = document.querySelector('#webgl');
const fallback = document.querySelector('#fallback');
const input = document.querySelector('#image-input');
const pointCount = document.querySelector('#point-count');
const status = document.querySelector('#status');
const controls = {depth:document.querySelector('#depth'), spread:document.querySelector('#spread'), density:document.querySelector('#density')};
const outputs = {depth:document.querySelector('#depth-out'), spread:document.querySelector('#spread-out'), density:document.querySelector('#density-out')};
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');

let renderer, scene, camera, cloud, material, basePositions, targetDepth = 58, targetScatter = .18;
let yaw = .18, pitch = -.08, zoom = 1, burst = 3, pointerDown = false, lastPoint, raf;
const densityNames = ['LOW','HIGH','MAX'];

function updateReadouts() { outputs.depth.value = controls.depth.value; outputs.spread.value = controls.spread.value; outputs.density.value = densityNames[controls.density.value]; targetDepth = Number(controls.depth.value); targetScatter = Number(controls.spread.value) / 100; }
function fire() { burst = 0; status.textContent = 'SIGNAL SENT // PARTICLES LIVE'; }
function resetView() { yaw=.18; pitch=-.08; zoom=1; targetScatter=.18; controls.spread.value=18; updateReadouts(); status.textContent='VIEW RESET // SIGNAL STABLE'; }

function setup() {
  try {
    renderer = new THREE.WebGLRenderer({alpha:true,antialias:false,powerPreference:'high-performance'});
    renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
    renderer.setSize(stage.clientWidth, stage.clientHeight); host.append(renderer.domElement);
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(34, stage.clientWidth / stage.clientHeight, .1, 20);
    camera.position.z = 4.05;
    scene.add(new THREE.AmbientLight(0xffffff,.1));
    addEventListener('resize', resize, {passive:true});
    new ResizeObserver(resize).observe(stage);
    stage.addEventListener('pointerdown', startDrag);
    stage.addEventListener('pointermove', drag);
    stage.addEventListener('pointerup', stopDrag);
    stage.addEventListener('pointercancel', stopDrag);
    stage.addEventListener('wheel', event => { event.preventDefault(); zoom = Math.max(.65,Math.min(1.55,zoom - event.deltaY*.0007)); }, {passive:false});
    stage.addEventListener('click', event => { if (!event.target.closest('button,input,label')) fire(); });
    requestAnimationFrame(render);
    loadImage('../assets/character.webp', 'OFFICIAL SIGNAL LOADED');
  } catch { fallback.hidden=false; status.textContent='3D MODE UNAVAILABLE'; }
}
function resize() { if (!renderer) return; const w=stage.clientWidth,h=stage.clientHeight; renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix(); }
function startDrag(event) { if(event.target.closest('button,input,label')) return; pointerDown=true;lastPoint={x:event.clientX,y:event.clientY};stage.setPointerCapture?.(event.pointerId); }
function drag(event) { if(!pointerDown) return; yaw+=(event.clientX-lastPoint.x)*.006; pitch=Math.max(-.8,Math.min(.8,pitch+(event.clientY-lastPoint.y)*.006));lastPoint={x:event.clientX,y:event.clientY}; }
function stopDrag(){pointerDown=false;}
function loadImage(src, message) { const image=new Image(); image.onload=()=>{buildCloud(image);status.textContent=message;}; image.onerror=()=>{fallback.hidden=false;status.textContent='IMAGE COULD NOT LOAD';}; image.src=src; }
function buildCloud(image) {
  if (!renderer) return;
  const density = Number(controls.density.value);
  const maxWidth = [82,120,158][density];
  const ratio = image.naturalHeight / image.naturalWidth;
  const canvas=document.createElement('canvas'); canvas.width=maxWidth;canvas.height=Math.max(74,Math.min(190,Math.round(maxWidth*ratio)));
  const ctx=canvas.getContext('2d',{willReadFrequently:true});ctx.drawImage(image,0,0,canvas.width,canvas.height);
  const pixels=ctx.getImageData(0,0,canvas.width,canvas.height).data;
  const positions=[],colors=[],seeds=[]; const cut=Math.max(1,density===2?1:2);
  for(let y=0;y<canvas.height;y+=cut){for(let x=0;x<canvas.width;x+=cut){const i=(y*canvas.width+x)*4;const a=pixels[i+3];if(a<100)continue;const r=pixels[i]/255,g=pixels[i+1]/255,b=pixels[i+2]/255;const l=(r+g+b)/3;if(l<.055&&Math.random()>.12)continue;const nx=(x/canvas.width-.5)*2.35,ny=-(y/canvas.height-.5)*2.85;const z=(l-.5)*.72+Math.sin(x*.19)*.025;positions.push(nx,ny,z);const cyan=Math.max(g,b),pink=Math.max(r,b*.6);colors.push(Math.min(1,r*.35+pink*.55),Math.min(1,g*.35+cyan*.5),Math.min(1,b*.55+cyan*.35));seeds.push(Math.random());}}
  if (cloud) { scene.remove(cloud); cloud.geometry.dispose(); }
  material?.dispose();
  const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));geometry.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));geometry.setAttribute('aSeed',new THREE.Float32BufferAttribute(seeds,1));
  material=new THREE.ShaderMaterial({transparent:true,depthWrite:false,vertexColors:true,uniforms:{uTime:{value:0},uScatter:{value:targetScatter},uDepth:{value:targetDepth/100},uBurst:{value:3},uPixel:{value:Math.min(devicePixelRatio,1.5)}},vertexShader:`attribute float aSeed; attribute vec3 color; varying vec3 vColor; uniform float uTime,uScatter,uDepth,uBurst,uPixel; void main(){vColor=color;vec3 p=position;p.z*=1.+uDepth*2.2;float wave=sin(aSeed*48.+uTime*1.2);vec3 dir=normalize(vec3(sin(aSeed*87.),cos(aSeed*43.),sin(aSeed*157.)));p+=dir*(uScatter*.9+sin(uTime+aSeed*30.)*.016);p+=dir*exp(-uBurst*2.)*sin(uBurst*18.+aSeed*22.)*.55;vec4 mv=modelViewMatrix*vec4(p,1.);gl_PointSize=(1.2+uDepth*2.8)*uPixel*(3.7/-mv.z);gl_Position=projectionMatrix*mv;}`,fragmentShader:`varying vec3 vColor;void main(){float d=length(gl_PointCoord-.5);if(d>.5)discard;float a=smoothstep(.5,.05,d);gl_FragColor=vec4(vColor,a*.92);}`});
  cloud=new THREE.Points(geometry,material);scene.add(cloud);basePositions=positions;pointCount.textContent=`${positions.length.toLocaleString()} POINTS`;
}
function render(time) { raf=requestAnimationFrame(render); if(!renderer||!cloud)return; material.uniforms.uTime.value=time*.001;material.uniforms.uScatter.value+=(targetScatter-material.uniforms.uScatter.value)*.08;material.uniforms.uDepth.value+=(targetDepth/100-material.uniforms.uDepth.value)*.08;burst+=.028;material.uniforms.uBurst.value=burst;cloud.rotation.y+=(yaw-cloud.rotation.y)*.08;cloud.rotation.x+=(pitch-cloud.rotation.x)*.08;camera.position.z+=(4.05/zoom-camera.position.z)*.08;renderer.render(scene,camera); }

Object.values(controls).forEach(control=>control.addEventListener('input',updateReadouts));
document.querySelector('#burst').addEventListener('click',fire);document.querySelector('#reset').addEventListener('click',resetView);document.querySelector('#official').addEventListener('click',()=>loadImage('../assets/character.webp','OFFICIAL SIGNAL LOADED'));
input.addEventListener('change',event=>{const file=event.target.files?.[0];if(!file)return;if(file.size>10*1024*1024){status.textContent='IMAGE TOO LARGE // 10 MB MAX';input.value='';return;}const url=URL.createObjectURL(file);loadImage(url,'YOUR SIGNAL LOADED // LOCAL ONLY');setTimeout(()=>URL.revokeObjectURL(url),3000);});
updateReadouts();if(reduceMotion.matches){fallback.hidden=false;status.textContent='REDUCED MOTION MODE';}else setup();
