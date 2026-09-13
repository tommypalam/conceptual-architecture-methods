import * as THREE from '/vendor/three/three.module.js';
import { OrbitControls } from '/vendor/three/controls/OrbitControls.js';
import { GLTFLoader } from '/vendor/three/loaders/GLTFLoader.js';

const loader = new GLTFLoader();
const assets = new Map();
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const colors = {a:0x4476c4, b:0xc98431, missing:0x8797a2};
const files = {C1:'council', C2:'boardroom', C3:'laboratory'};
const model = name => {
  if (!assets.has(name)) assets.set(name, loader.loadAsync(`/assets/${name}.glb`).catch(error => {assets.delete(name); throw error;}));
  return assets.get(name);
};
export function places(problem, count) {
  if (problem === 'C1') return Array.from({length:count},(_,i) => [Math.sin(i*Math.PI*2/count)*2.65,Math.cos(i*Math.PI*2/count)*2.65]);
  if (problem === 'C2') return [[-2.8,0],[-1.35,1.8],[1.35,1.8],[2.8,0],[1.35,-1.8],[-1.35,-1.8]];
  return [[0,2.5],[2.5,0],[0,-2.5],[-2.5,0]];
}

export class World {
  constructor(container, onSelect) {
    this.container = container;
    this.onSelect = onSelect;
    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0xdbe7e9);
    this.camera = new THREE.PerspectiveCamera(36, 1, .1, 100);
    this.renderer = new THREE.WebGLRenderer({antialias:true, alpha:false, powerPreference:'low-power'});
    this.renderer.setPixelRatio(Math.min(devicePixelRatio, 1.6));
    this.renderer.shadowMap.enabled = true;
    this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
    this.renderer.toneMappingExposure = 1.2;
    this.renderer.domElement.setAttribute('aria-label','Interactive 3D room. Use the agent buttons to inspect recorded decisions.');
    container.append(this.renderer.domElement);
    this.overlay = document.createElement('div');
    this.overlay.className = 'world-labels';
    container.append(this.overlay);
    this.leaders = document.createElementNS('http://www.w3.org/2000/svg','svg');
    this.leaders.setAttribute('aria-hidden','true');
    this.overlay.append(this.leaders);
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.target.set(0,.45,0);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = .12;
    this.controls.minDistance = 7;
    this.controls.maxDistance = 25;
    this.controls.maxPolarAngle = Math.PI*.47;
    this.controls.minPolarAngle = .12;
    this.controls.enablePan = false;
    this.controls.addEventListener('change', () => this.invalidate());
    this.scene.add(new THREE.HemisphereLight(0xf5fbff,0x78928b,2.6));
    const sun = new THREE.DirectionalLight(0xfff5e1,4.0);
    sun.position.set(-4,10,6); sun.castShadow = true;
    sun.shadow.mapSize.set(1024,1024);
    Object.assign(sun.shadow.camera,{left:-8,right:8,top:8,bottom:-8,near:1,far:30});
    sun.shadow.bias = -.0005; sun.shadow.normalBias = .025;
    this.scene.add(sun);
    const fill = new THREE.DirectionalLight(0xbadcf2,1.8); fill.position.set(8,5,-4); this.scene.add(fill);
    const floor = new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.ShadowMaterial({opacity:.12}));
    floor.rotation.x=-Math.PI/2;floor.position.y=-.68;floor.receiveShadow=true;this.scene.add(floor);
    this.actors=[];this.transients=[];this.version=0;this.request=null;this.activeUntil=0;
    this.raycaster=new THREE.Raycaster();
    let down;
    this.renderer.domElement.addEventListener('pointerdown', e => {down=[e.clientX,e.clientY];});
    this.renderer.domElement.addEventListener('pointerup', e => {
      if (!down || Math.hypot(e.clientX-down[0],e.clientY-down[1])>5) return;
      const rect=this.renderer.domElement.getBoundingClientRect();
      this.raycaster.setFromCamera(new THREE.Vector2((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1),this.camera);
      const hit=this.raycaster.intersectObjects(this.actors.map(a=>a.model),true)[0];
      if(hit){let obj=hit.object;while(obj && obj.userData.agent===undefined)obj=obj.parent;if(obj)this.onSelect(obj.userData.agent);}
    });
    this.resizeObserver=new ResizeObserver(()=>this.resize());this.resizeObserver.observe(container);
    this.visibility=()=>{if(!document.hidden)this.invalidate();};document.addEventListener('visibilitychange',this.visibility);
    this.reset();
  }
  reset(top=false) {
    this.camera.position.set(...(top?[0,17,.8]:[10.6,10.0,13.2]));
    this.controls.target.set(0,.45,0);this.controls.update();this.resize();this.invalidate();
  }
  resize() {
    const w=this.container.clientWidth,h=this.container.clientHeight;
    if(!w||!h)return;
    this.camera.aspect=w/h;
    // Keep the whole diorama in frame in narrow comparison and mobile panes.
    this.camera.fov=Math.max(30, THREE.MathUtils.radToDeg(2*Math.atan(Math.tan(THREE.MathUtils.degToRad(52)/2)/(w/h))));
    this.camera.updateProjectionMatrix();this.renderer.setSize(w,h,false);this.invalidate();
  }
  async setRun(run) {
    const version=++this.version;
    const [room,agent]=await Promise.all([model(files[run.problem]),model('agent')]);
    if(version!==this.version)return;
    if(this.room)this.scene.remove(this.room);
    for(const a of this.actors){this.scene.remove(a.model,a.ring,a.halo);a.ring.geometry.dispose();a.ring.material.dispose();a.halo.geometry.dispose();a.halo.material.dispose();}
    this.clearEffects();this.leaders.replaceChildren();this.overlay.replaceChildren(this.leaders);this.actors=[];
    this.room=room.scene.clone(true);
    this.room.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;}});
    this.scene.add(this.room);this.run=run;
    const positions=places(run.problem,run.agents.length);
    run.agents.forEach((a,i)=>{
      const [x,z]=positions[i],obj=agent.scene.clone(true);
      obj.position.set(x,0,z);obj.rotation.y=Math.atan2(-x,-z);obj.userData.agent=a.agent_id;
      obj.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;}});
      const ring=new THREE.Mesh(new THREE.RingGeometry(.40,.49,48),new THREE.MeshBasicMaterial({color:colors.missing,side:THREE.DoubleSide}));
      ring.rotation.x=-Math.PI/2;ring.position.set(x,.12,z);
      const halo=new THREE.Mesh(new THREE.RingGeometry(.55,.58,48),new THREE.MeshBasicMaterial({color:0x234354,side:THREE.DoubleSide}));
      halo.rotation.x=-Math.PI/2;halo.position.set(x,.125,z);halo.visible=false;
      const button=document.createElement('button');button.className='agent-label';button.dataset.agent=a.agent_id;
      button.addEventListener('click',()=>this.onSelect(a.agent_id));
      const leader=document.createElementNS('http://www.w3.org/2000/svg','line');
      this.leaders.append(leader);
      this.overlay.append(button);this.scene.add(obj,ring,halo);
      this.actors.push({id:a.agent_id,model:obj,ring,halo,button,leader,point:new THREE.Vector3(x,2.03,z),changed:false});
    });
    this.container.querySelector('.loading-label')?.remove();
    this.container.dataset.ready='true';this.resize();this.invalidate();
  }
  update(round, selected, animate=true) {
    if(!this.run)return;
    const n=Math.min(round,this.run.rounds.length),state=n?this.run.rounds[n-1]:null;
    this.clearEffects();
    this.actors.forEach(a=>{
      const response=state?.responses.find(r=>r.agent===a.id);
      const kind=response?.vote===this.run.labels[0]?'a':response?.vote===this.run.labels[1]?'b':'missing';
      a.ring.material.color.setHex(colors[kind]);a.halo.visible=a.id===selected;
      a.changed=!!response?.changed && animate;
      a.button.className=`agent-label ${kind} ${a.id===selected?'selected':''}`;
      const vote=response?.vote?.replaceAll('_',' ').toLowerCase() || (state?'invalid vote':'ready');
      a.button.replaceChildren();
      const name=document.createElement('strong');name.textContent=`${a.id}${a.id===this.run.ceo?' · CEO':''}`;
      const lean=document.createElement('span');lean.textContent=vote;
      a.button.append(name,lean);a.button.setAttribute('aria-label',`Inspect agent ${a.id}, ${vote}`);a.button.setAttribute('aria-pressed',a.id===selected);
    });
    if(state && this.run.problem==='C3' && animate && !reduced.matches){
      for(const a of this.actors){
        const audit=state.audit.find(x=>x.agent===a.id && x.authenticated_disclosures);
        const ids=(audit?.authenticated_disclosures||[]).filter(id=>!state.public_before.includes(id));
        if(!ids.length)continue;
        const start=a.model.position.clone().add(new THREE.Vector3(0,1.4,0));
        const end=new THREE.Vector3(0,1.28,0);
        const middle=start.clone().lerp(end,.5);middle.y=2.6;
        const curve=new THREE.QuadraticBezierCurve3(start,middle,end);
        const line=new THREE.Line(new THREE.BufferGeometry().setFromPoints(curve.getPoints(32)),new THREE.LineBasicMaterial({color:0x4b8d9d,transparent:true,opacity:.55}));
        const dot=new THREE.Mesh(new THREE.BoxGeometry(.12,.04,.17),new THREE.MeshStandardMaterial({color:0xf9faf3,emissive:0x38666c,emissiveIntensity:.35}));
        this.scene.add(line,dot);this.transients.push({line,dot,curve});
      }
    }
    this.started=performance.now();this.activeUntil=animate&&!reduced.matches?this.started+2000:0;this.invalidate();
  }
  clearEffects(){for(const t of this.transients){this.scene.remove(t.line,t.dot);t.line.geometry.dispose();t.line.material.dispose();t.dot.geometry.dispose();t.dot.material.dispose();}this.transients=[];for(const a of this.actors)a.ring.scale.setScalar(1);}
  positionLabels(){
    const w=this.container.clientWidth,h=this.container.clientHeight,placed=[];
    const entries=this.actors.map(a=>{
      const p=a.point.clone().project(this.camera);
      a.button.hidden=p.z>1||Math.abs(p.x)>1.1||Math.abs(p.y)>1.1;
      return {a,x:(p.x+1)*w/2,y:(1-p.y)*h/2,bw:a.button.offsetWidth,bh:a.button.offsetHeight};
    }).sort((a,b)=>a.y-b.y||a.x-b.x);
    for(const entry of entries){
      const {a,x,y,bw,bh}=entry;
      a.leader.style.display='none';if(a.button.hidden)continue;
      const candidates=[];
      for(const dy of [0,-1,1,-2,2,-3,3])for(const dx of [0,-1,1,-2,2]){
        const cx=Math.max(bw/2+6,Math.min(w-bw/2-6,x+dx*(bw+6)));
        const cy=Math.max(bh+42,Math.min(h-6,y+dy*(bh+6)));
        candidates.push({cx,cy,left:cx-bw/2,right:cx+bw/2,top:cy-bh,bottom:cy,cost:(cx-x)**2+(cy-y)**2});
      }
      candidates.sort((a,b)=>a.cost-b.cost);
      const chosen=candidates.find(c=>placed.every(p=>c.right+5<=p.left||c.left>=p.right+5||c.bottom+5<=p.top||c.top>=p.bottom+5))||candidates[0];
      placed.push(chosen);a.button.style.left=`${chosen.cx}px`;a.button.style.top=`${chosen.cy}px`;
      if(chosen.cost>16){
        a.leader.style.display='';
        a.leader.setAttribute('x1',chosen.cx);a.leader.setAttribute('y1',chosen.cy);
        a.leader.setAttribute('x2',x);a.leader.setAttribute('y2',y);
      }
    }
  }
  invalidate(){if(this.request===null && !document.hidden && !this.container.hidden)this.request=requestAnimationFrame(t=>this.render(t));}
  render(time){
    this.request=null;if(this.container.hidden||document.hidden)return;
    const moving=this.controls.update(),animating=time<this.activeUntil;
    const progress=Math.min(1,(time-this.started)/1800);
    for(const a of this.actors)a.ring.scale.setScalar(animating&&a.changed?1+.15*Math.sin(progress*Math.PI*4):1);
    this.positionLabels();
    for(const t of this.transients){t.dot.position.copy(t.curve.getPoint(Math.max(0,progress)));t.line.material.opacity=.5*(1-progress);t.dot.visible=progress<1;}
    this.renderer.render(this.scene,this.camera);
    if(animating||moving)this.invalidate();
  }
  dispose(){cancelAnimationFrame(this.request);this.resizeObserver.disconnect();document.removeEventListener('visibilitychange',this.visibility);this.controls.dispose();this.renderer.dispose();this.clearEffects();this.overlay.remove();this.renderer.domElement.remove();}
}
