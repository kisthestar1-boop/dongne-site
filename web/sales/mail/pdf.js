const {chromium}=require('playwright');const fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage();
const D=__dirname;const fs2=fs.readdirSync(D).filter(f=>/^(letter_.*|flyer|promo_a4)\.html$/.test(f));
for(const f of fs2){await p.goto('file://'+D+'/'+f);await p.waitForTimeout(300);const a5=f==='flyer.html';await p.pdf({path:D+'/'+f.replace('.html','.pdf'),format:a5?'A5':'A4',printBackground:true});}
await p.goto('file://'+D+'/promo_a4.html');await p.setViewportSize({width:794,height:1123});await p.screenshot({path:'/tmp/claude-0/-home-claude/243f3630-8159-5960-8ba0-474ea1a500c0/scratchpad/promo_prev.png'});
await p.goto('file://'+D+'/flyer.html');await p.setViewportSize({width:560,height:794});await p.screenshot({path:'/tmp/claude-0/-home-claude/243f3630-8159-5960-8ba0-474ea1a500c0/scratchpad/flyer_prev.png'});
console.log(fs2.length);await b.close()})();
