// 새싹 소녀 컷아웃 뼈대 리그 (스파인 방식) — 파츠 이미지를 관절로 돌려서 그림
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
function pose(m,ph,t,sp){
 const P={dy:0,lean:0,thF:0,knF:0,thB:0,knB:0,arF:0,arB:0,head:0,skirt:0,skY:1,stf:0};
 if(m==='run'){const s=Math.sin(2*Math.PI*ph),c=Math.cos(2*Math.PI*ph);
  const leg=(p)=>{const sn=Math.sin(2*Math.PI*p),cs=Math.cos(2*Math.PI*p);
   const th=-40*sn;                       // 허벅지 앞뒤 스윙
   const swing=Math.max(0,Math.cos(2*Math.PI*(p-.03))); // 앞으로 넘어오는 구간
   const kn=(12+80*swing*swing);         // 무릎 접힘 (뒤로)
   return [th*D,kn*D]};
  const a=leg(ph),b=leg(ph+.5);P.thF=a[0];P.knF=a[1];P.thB=b[0];P.knB=b[1];
  P.dy=-1.5*Math.cos(4*Math.PI*ph)*sp;
  P.lean=(11+2.2*Math.cos(4*Math.PI*(ph-.08)))*D*sp;
  P.arF=(14*s-18)*D*sp;P.arB=-44*s*D*sp+6*D;
  P.head=(-3+2.5*Math.cos(4*Math.PI*(ph-.14)))*D*sp;
  P.skirt=(-5+4*Math.sin(4*Math.PI*(ph-.12)))*D*sp;P.skY=1+.04*Math.cos(4*Math.PI*(ph-.1))*sp;
  P.stf=-P.arF-P.lean+30*D;
 }else if(m==='idle'){const b=Math.sin(t*3.2);P.dy=b*1.6;P.head=Math.sin(t*1.6)*1.2*D;P.arF=(4+b*1.5)*D;P.arB=(-3-b*1.5)*D;P.skirt=Math.sin(t*1.6+1)*1.2*D;P.thF=3*D;P.thB=-3*D;P.knF=2*D;P.knB=2*D;P.stf=-P.arF+12*D}
 return P}
// 캐릭터 그리기: (x,y)=발바닥 중앙, h=목표 키(px), face=1 오른쪽
function draw(ctx,x,y,h,face,P,opt){if(!R.ready)return false;opt=opt||{};
 const k=h/575;ctx.save();ctx.translate(x,y);ctx.scale(k*face,k);
 const L=footLen();const fy=(th,kn)=>Math.cos(th)*(L.hk-6)+Math.cos(th+kn)*L.hs;const low=Math.max(fy(P.thF,P.knF),fy(P.thB,P.knB))-6;
 const hipY=-low+P.dy;ctx.translate(0,hipY);
 // 뒤쪽 다리, 뒤팔
 ctx.save();ctx.translate(-10,-6);ctx.filter&&0;drawLeg(ctx,'legB',P.thB,P.knB,1.03);ctx.restore();
 ctx.save();ctx.rotate(P.lean);ctx.translate(-26,-126);ctx.rotate(P.arB);ctx.scale(.82,.82);drawPart(ctx,'armB',.5,.06);ctx.restore();
 ctx.save();ctx.translate(12,-6);drawLeg(ctx,'legF',P.thF,P.knF,1.03);ctx.restore();
 // 몸통 + 치마 + 가방
 ctx.save();ctx.rotate(P.lean);
  ctx.save();ctx.translate(2,-8);ctx.rotate(P.skirt);ctx.scale(1,P.skY);drawPart(ctx,'skirt',.5,.05,.92,.80);ctx.restore();
  ctx.save();ctx.translate(0,4);drawPart(ctx,'torso',.5,1);ctx.restore();
  ctx.save();ctx.translate(-30,-10);ctx.rotate(P.skirt*1.5);ctx.scale(.62,.62);drawPart(ctx,'bag',.5,.2);ctx.restore();
  // 머리
  ctx.save();ctx.translate(6,-132);ctx.rotate(P.head);drawPart(ctx,'head',.5,.93,.98,.98);ctx.restore();
  // 앞팔 + 지팡이
  ctx.save();ctx.translate(22,-124);ctx.rotate(P.arF);ctx.scale(.82,.82);
   ctx.save();ctx.translate(2,160);ctx.rotate(P.stf+(opt.stfRot||0));ctx.scale(.75,.75);drawPart(ctx,'staff',.55,.62);ctx.restore();
   drawPart(ctx,'armF',.5,.06);ctx.restore();
 ctx.restore();
 ctx.restore();return true}
window.SPROUT_RIG={R,pose,draw};
})();
