// 새싹 소녀 컷아웃 뼈대 리그 (스파인 방식) — 파츠 이미지를 관절로 돌려서 그림
window.SPROUT_RIG={style:/walk=smooth/.test(location.search)?'smooth':'maple'};
(function(){
const NAMES=['head','torso','armF','armB','staff','skirt','legF','legB','bag'];
const R={img:{},ready:false};
let left=NAMES.length;
NAMES.forEach(n=>{const im=new Image();im.onload=()=>{if(--left===0)R.ready=true};im.src='img/rig/'+n+'.webp';R.img[n]=im});
const S=0.5; // 파츠는 시트의 2배 크기로 저장됨 → 시트 단위로 환산
function part(n){return R.img[n]}
// 이미지의 (ax,ay) 비율 지점을 피벗으로 회전해 그림
function drawPart(ctx,n,ax,ay,sx,sy,sh,syTop){const im=part(n);if(!im||!im.naturalWidth)return;
 const w=im.naturalWidth*S*(sx||1),h=im.naturalHeight*S*(sy||1);ctx.drawImage(im,-w*ax,-h*ay,w,h)}
// 다리: 무릎에서 둘로 나눠 그림 (위 46% 허벅지, 아래 54% 종아리+부츠)
function drawLeg(ctx,n,thigh,knee,len){const im=part(n);if(!im||!im.naturalWidth)return;
 const W=im.naturalWidth,H=im.naturalHeight,cut=Math.round(H*.46);const w=W*S,h=H*S*len,hk=cut*S*len,hs=(H-cut)*S*len;
 ctx.save();ctx.rotate(thigh);
 ctx.drawImage(im,0,0,W,cut+2,-w/2,-4,w,hk+3);
 ctx.translate(0,hk-6);ctx.rotate(knee);
 ctx.drawImage(im,0,cut-2,W,H-cut+2,-w/2,-2,w,hs+2);
 ctx.restore()}
const D=Math.PI/180;
function footLen(){const im=part('legF');const H=(im&&im.naturalHeight)||404;const cut=Math.round(H*.46);return {hk:cut*S*1.03,hs:(H-cut)*S*1.03}}
// pose 계산: phase(0~1 한 사이클), mode
function pose(m,ph,t,sp,k){k=k||0;const ez=x=>{x=Math.max(0,Math.min(1,x));if(x<.22)return -.14*Math.sin(x/.22*Math.PI/2);if(x<.6){const u=(x-.22)/.38;return -.14+1.22*u*u*(3-2*u)}return 1.08-.08*((x-.6)/.4)};const lunge=(P,a)=>{a=Math.max(0,a);P.thF=-42*a*D;P.knF=34*a*D;P.thB=32*a*D;P.knB=8*a*D};
 const P={dy:0,lean:0,thF:0,knF:0,thB:0,knB:0,arF:0,arB:0,head:0,skirt:0,skY:1,stf:0};
 if(m==='run'&&window.SPROUT_RIG.style!=='smooth'){ // 메이플식: 직립, 8포즈로 또렷하게 끊기
  const q=8,f=ph*q,i=Math.floor(f),fr=f-i,e=fr<.62?0:(fr-.62)/.38;ph=(i+e*e*(3-2*e))/q;
  const s=Math.sin(2*Math.PI*ph);
  const leg=(p)=>{const sn=Math.sin(2*Math.PI*p);const sw=Math.max(0,Math.cos(2*Math.PI*(p-.03)));return [(-27*sn+2)*D,(6+52*sw*sw)*D]};
  const a=leg(ph),b=leg(ph+.5);P.thF=a[0];P.knF=a[1];P.thB=b[0];P.knB=b[1];
  P.dy=-3*Math.pow(Math.max(0,Math.cos(4*Math.PI*(ph-.13))),2)*sp;P.lean=3*D*sp;
  P.arF=(9*s-12)*D*sp;P.arB=-30*s*D*sp+4*D;P.head=0;P.skirt=(-2+2.5*Math.sin(4*Math.PI*(ph-.1)))*D*sp;P.skY=1;P.stf=-P.arF-P.lean+30*D;
 }else if(m==='run'){const s=Math.sin(2*Math.PI*ph),c=Math.cos(2*Math.PI*ph);
  const leg=(p)=>{const sn=Math.sin(2*Math.PI*p),cs=Math.cos(2*Math.PI*p);
   const th=-46*sn+4;                       // 허벅지 앞뒤 스윙
   const swing=Math.max(0,Math.cos(2*Math.PI*(p-.03))); // 앞으로 넘어오는 구간
   const kn=(10+95*swing*swing);         // 무릎 접힘 (뒤로)
   return [th*D,kn*D]};
  const a=leg(ph),b=leg(ph+.5);P.thF=a[0];P.knF=a[1];P.thB=b[0];P.knB=b[1];
  P.dy=-11*Math.pow(Math.max(0,Math.cos(4*Math.PI*(ph-.13))),2)*sp;
  P.lean=(15+2.5*Math.cos(4*Math.PI*(ph-.08)))*D*sp;
  P.arF=(16*s-22)*D*sp;P.arB=-55*s*D*sp+8*D;
  P.head=(-7+2.5*Math.cos(4*Math.PI*(ph-.14)))*D*sp;
  P.skirt=(-9+5*Math.sin(4*Math.PI*(ph-.12)))*D*sp;P.skY=1+.04*Math.cos(4*Math.PI*(ph-.1))*sp;
  P.stf=-P.arF-P.lean+30*D;
 }else if(m==='idle'){const b=Math.sin(t*3.2);P.dy=b*1.6;P.head=Math.sin(t*1.6)*1.2*D;P.arF=(4+b*1.5)*D;P.arB=(-3-b*1.5)*D;P.skirt=Math.sin(t*1.6+1)*1.2*D;P.thF=3*D;P.thB=-3*D;P.knF=2*D;P.knB=2*D;P.stf=-P.arF+12*D}
 else if(m==='rise'){P.air=1;P.lean=4*D;P.thF=-58*D;P.knF=75*D;P.thB=18*D;P.knB=28*D;P.arF=-35*D;P.arB=-120*D;P.head=-4*D;P.skirt=6*D;P.skY=.96;P.stf=-P.arF+20*D}
 else if(m==='fall'){P.air=1;const w=Math.sin(t*14)*3;P.lean=-3*D;P.thF=-22*D;P.knF=38*D;P.thB=-6*D;P.knB=30*D;P.arF=-40*D;P.arB=(95+w)*D;P.head=3*D;P.skirt=(-4+w*.6)*D;P.skY=.88;P.skX=1.12;P.stf=-P.arF+35*D}
 else if(m==='crouch'){P.thF=-38*D;P.knF=70*D;P.thB=-30*D;P.knB=66*D;P.lean=14*D;P.arF=10*D;P.arB=30*D;P.head=4*D;P.skY=.9;P.stf=-P.arF+20*D}
 else if(m==='a1'){const e=ez(k/.7);P.arF=(150+150*e)*D;P.stf=180*D;P.stfA=.82;P.lean=(-6+18*e)*D;lunge(P,.7*e+.2);P.arB=(20-50*e)*D;P.head=(2-4*e)*D;P.skirt=-6*e*D}
 else if(m==='a2'){const e=ez(k/.7);P.arF=(-35-95*e)*D;P.stf=180*D;P.stfA=.82;P.lean=(14-20*e)*D;lunge(P,.9-.3*e);P.arB=(-30+60*e)*D;P.head=-3*e*D;P.skirt=5*e*D}
 else if(m==='wind3'){P.arF=165*D;P.stf=180*D;P.stfA=.82;P.lean=-14*D;P.thF=10*D;P.knF=10*D;P.thB=-8*D;P.knB=24*D;P.arB=-40*D;P.head=4*D}
 else if(m==='a3'){const e=ez(k/.6);P.arF=(165+135*e)*D;P.stf=180*D;P.stfA=.82;P.lean=(-14+38*e)*D;lunge(P,1.05*e);P.arB=(-40+90*e)*D;P.head=-6*e*D;P.skirt=-10*e*D;P.skY=1-.06*e}
 else if(m==='up'){const e=ez(k/.65);P.arF=(-30-160*e)*D;P.stf=180*D;P.stfA=.82;P.lean=(10-18*e)*D;lunge(P,.5*(1-e));P.arB=(30-10*e)*D;P.head=5*e*D;P.air=k>.25?1:0;if(P.air){P.thF=-30*D;P.knF=50*D;P.thB=12*D;P.knB=30*D}}
 else if(m==='air'){const e=ez(k/.7);P.air=1;P.arF=(150+160*e)*D;P.stf=180*D;P.stfA=.82;P.lean=(-4+20*e)*D;P.thF=-40*D;P.knF=70*D;P.thB=10*D;P.knB=50*D;P.arB=(-60+80*e)*D;P.skY=.92;P.skX=1.08}
 else if(m==='hurt'){P.lean=-20*D;P.thF=-14*D;P.knF=22*D;P.thB=-26*D;P.knB=30*D;P.arF=-70*D;P.arB=80*D;P.head=-8*D;P.skirt=10*D;P.stf=-P.arF+40*D}
 else if(m==='cast'){const b=Math.sin(t*18)*2;P.lean=-5*D;P.arF=(-158+b)*D;P.stf=180*D;P.stfA=.82;P.arB=(-60-b)*D;P.thF=4*D;P.thB=-6*D;P.knF=4*D;P.knB=6*D;P.head=6*D;P.skY=.95;P.skX=1.06;P.dy=-3}
 else if(m==='dash'){P.lean=30*D;P.thF=-62*D;P.knF=30*D;P.thB=48*D;P.knB=40*D;P.arF=30*D;P.arB=70*D;P.head=-12*D;P.skirt=-14*D;P.stf=-P.arF-P.lean+60*D;P.dy=6}
 else if(m==='brake'){P.lean=-12*D;P.thF=-30*D;P.knF=8*D;P.thB=-6*D;P.knB=40*D;P.arF=-45*D;P.arB=40*D;P.head=5*D;P.skirt=-10*D;P.stf=-P.arF+25*D}
 else if(m==='climb'){const w=Math.sin(ph*6.283);P.air=1;P.arF=(-165+12*w)*D;P.arB=(-165-12*w)*D;P.thF=(-20+18*w)*D;P.knF=40*D;P.thB=(-20-18*w)*D;P.knB=40*D;P.stf=-P.arF+10*D}
 {const bt=(t+((t/7|0)%2?0:.0))%3.6;P.blink=(bt<.13||(bt>.26&&bt<.37&&((t/3.6|0)%3===0)))?1:0;if(m==='hurt')P.blink=1}
 return P}
// 캐릭터 그리기: (x,y)=발바닥 중앙, h=목표 키(px), face=1 오른쪽
function draw(ctx,x,y,h,face,P,opt){if(!R.ready)return false;opt=opt||{};
 const k=h/575;ctx.save();ctx.translate(x,y);ctx.scale(k*face,k);
 const L=footLen();const fy=(th,kn)=>Math.cos(th)*(L.hk-6)+Math.cos(th+kn)*L.hs;const low=Math.max(fy(P.thF,P.knF),fy(P.thB,P.knB))-6;
 const hipY=-(P.air?(L.hk-6+L.hs-18):low)+P.dy;ctx.translate(0,hipY);
 // 뒤쪽 다리, 뒤팔
 ctx.save();ctx.translate(-10,-6);ctx.filter&&0;drawLeg(ctx,'legB',P.thB,P.knB,1.03);ctx.restore();
 ctx.save();ctx.rotate(P.lean);ctx.translate(-26,-126);ctx.rotate(P.arB);ctx.scale(.82,.82);drawPart(ctx,'armB',.5,.06);ctx.restore();
 ctx.save();ctx.translate(12,-6);drawLeg(ctx,'legF',P.thF,P.knF,1.03);ctx.restore();
 // 몸통 + 치마 + 가방
 ctx.save();ctx.rotate(P.lean);
  ctx.save();ctx.translate(2,-8);ctx.rotate(P.skirt);ctx.scale(P.skX||1,P.skY);drawPart(ctx,'skirt',.5,.05,.92,.80);ctx.restore();
  ctx.save();ctx.translate(0,4);drawPart(ctx,'torso',.5,1);ctx.restore();
  ctx.save();ctx.translate(-30,-10);ctx.rotate(P.skirt*1.5);ctx.scale(.62,.62);drawPart(ctx,'bag',.5,.2);ctx.restore();
  const head=()=>{ctx.save();ctx.translate(6,-132);ctx.rotate(P.head);drawPart(ctx,'head',.5,.93,.98,.98);
   if(P.blink>0){const w=564*S*.98,h=470*S*.98,ox=-w*.5,oy=-h*.93,q=w/564;for(const [ex,ey] of [[252,322],[389,316]]){const X=ox+ex*q,Y=oy+ey*q;ctx.fillStyle='#fdebe0';ctx.beginPath();ctx.ellipse(X,Y-2*q,27*q,36*q*P.blink,0,0,7);ctx.fill();ctx.strokeStyle='#5b4a55';ctx.lineWidth=5*q;ctx.lineCap='round';ctx.beginPath();ctx.arc(X,Y-14*q+34*q*P.blink,24*q,.18*Math.PI,.82*Math.PI);ctx.stroke()}}
   ctx.restore()};
  const arm=()=>{ctx.save();ctx.translate(22,-124);ctx.rotate(P.arF);ctx.scale(.82,.82);
   ctx.save();ctx.translate(2,160);ctx.rotate(P.stf+(opt.stfRot||0));ctx.scale(.75,.75);drawPart(ctx,'staff',.55,P.stfA||.62);ctx.restore();
   drawPart(ctx,'armF',.5,.06);ctx.restore()};
  if(Math.cos(P.arF)<-.15&&-Math.sin(P.arF)<.45){arm();head()}else{head();arm()}
 ctx.restore();
 ctx.restore();return true}
window.SPROUT_RIG.R=R;window.SPROUT_RIG.pose=pose;window.SPROUT_RIG.draw=draw;
})();
