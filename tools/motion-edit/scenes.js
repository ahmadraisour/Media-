// مكتبة المشاهد. كل نوع إله:
//   TPL[type](s)        -> HTML المشهد (s = إعدادات المشهد من project.json، والصور بـs.img/s.bg/s.fg...)
//   UPD[type](el,t,T,s) -> الحركة لكل فريم (t نسبي من بداية المشهد، T مطلق، s.len = طول المشهد)
// الأوقات المطلقة للضربات (hits) بتنكتب بـproject.json، مو هون.
// ktTop: مكان الكتابة المتحركة الافتراضي لكل نوع (بينكتب فوقه بـs.kt).

var seed=5;function rnd(){seed=(seed*16807)%2147483647;return seed/2147483647}
var DOTS=[];for(var i=0;i<46;i++)DOTS.push({x:rnd()*1080,y:rnd()*1920,r:1.5+rnd()*4,s:10+rnd()*30,a:.15+rnd()*.45,ph:rnd()*6});
var STARS=[];for(var i=0;i<160;i++)STARS.push({a:rnd()*6.283,d:rnd(),s:.5+rnd()*1.5});
var BILLS=[];for(var i=0;i<10;i++)BILLS.push({side:i%2?1:-1,t0:0.75+(i%5)*0.09+(i%2?0.45:0),y:500+rnd()*900,r:rnd()*360,vr:(rnd()-.5)*700,sz:110+rnd()*90,vy:(rnd()-.5)*500});

function v(x,d){return x===undefined?d:x}
var XMARK='<line x1="-20" y1="-20" x2="20" y2="20" stroke="#fff" stroke-width="15" stroke-linecap="round"/><line x1="20" y1="-20" x2="-20" y2="20" stroke="#fff" stroke-width="15" stroke-linecap="round"/><line x1="-20" y1="-20" x2="20" y2="20" stroke="#e5484d" stroke-width="9" stroke-linecap="round"/><line x1="20" y1="-20" x2="-20" y2="20" stroke="#e5484d" stroke-width="9" stroke-linecap="round"/>';
var RL='fill="none" stroke="#e5484d" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" style="filter:drop-shadow(0 0 10px rgba(229,72,77,.9)) drop-shadow(0 3px 4px rgba(0,0,0,.6))"';
var BAR='stroke="#ff5a5f" stroke-width="16" stroke-linecap="round" opacity="0" style="filter:drop-shadow(0 0 14px #ff3b40) drop-shadow(0 0 30px rgba(255,59,64,.8))"';

var KT_TOP={mars:250,wall:250,mg:250};

var TPL={
 // ===== مشاهد المتاهة (v11) =====
 // ولد بيرسم خط بالقلم والإيد بتلحقه، بيعلق بالحيط مع ✕
 kid:function(s){return '<div class="cam"><div class="lay bgw"><img class="lay" src="'+v(s.bg,'L/kid_bg.jpg')+'" style="filter:blur(1.6px)"><svg class="sp" width="1080" height="1920"><path class="ln" d="M578 1063 L652 1087 L637 1152 L722 1177 L737 1127" fill="none" stroke="#2a2a33" stroke-width="13" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/><g class="x" opacity="0" transform="translate(737 1127) scale(1.5)"><line x1="-18" y1="-18" x2="18" y2="18" stroke="#e5484d" stroke-width="9" stroke-linecap="round"/><line x1="18" y1="-18" x2="-18" y2="18" stroke="#e5484d" stroke-width="9" stroke-linecap="round"/></g></svg></div><img class="lay hand" src="'+v(s.hand,'L/hand.png')+'"></div><canvas class="pc" width="1080" height="1920"></canvas><div class="leak"></div><div class="shade"></div>'},
 // متاهة من فوق، 3 خطوط حمرا بتعلق بالحيط (s.hits = 3 أزواج [بداية الخط، لحظة الضربة])
 wall:function(s){var R=[['M548 1005 L548 1436','485','1446','570','1446','548 1395'],['M554 926 L556 862 L708 862','717','826','717','898','668 862'],['M540 995 L540 1042 L360 1042 L360 1246','325','1256','395','1256','360 1205']],h='';
   R.forEach(function(r,i){h+='<g class="rt" data-i="'+i+'"><path class="rl" d="'+r[0]+'" '+RL+'/><line class="bar" x1="'+r[1]+'" y1="'+r[2]+'" x2="'+r[3]+'" y2="'+r[4]+'" '+BAR+'/><g class="x" opacity="0" transform="translate('+r[5]+')">'+XMARK+'</g></g>'});
   return '<div class="cam"><img class="lay bg" src="'+v(s.bg,'L/aerial.png')+'"><svg class="sp" width="1080" height="1920" style="overflow:visible">'+h+'</svg></div><div class="vig"></div><div class="tsh"></div>'},
 // كوكب بيكبر وشخص مقصوص بيطلع من تحت مع غبار
 mars:function(s){return '<div class="mg"></div><img class="sp planet" src="'+v(s.planet,'L/mars.png')+'" style="width:700px;height:700px;left:190px;top:520px;filter:drop-shadow(0 0 60px rgba(255,110,40,.45))"><img class="cut astro" src="'+v(s.fg,'img/mars_cut.png')+'" style="height:1760px;bottom:-200px"><canvas class="pc" width="1080" height="1920"></canvas><div class="dust"></div>'},
 // عمق 2.5D مع جزيئات ذهبية و"دفشة" على كلمة (s.punch)
 joy:function(s){return '<div class="cam"><div class="lay bgw"><img class="lay" src="'+v(s.bg,'L/kidjoy_bg.jpg')+'" style="filter:blur(2px)"></div><img class="lay fg" src="'+v(s.fg,'L/kidjoy_cut.png')+'"></div><canvas class="pc" width="1080" height="1920"></canvas><div class="shade"></div>'},
 // عمق 2.5D، زوم قوي مع ميلان خفيف، هزة وتسكير أطراف على s.hit
 maze:function(s){return '<div class="cam"><img class="lay bg" src="'+v(s.bg,'L/manmaze_bg.jpg')+'"><img class="lay fg" src="'+v(s.fg,'L/manmaze_cut.png')+'"></div><div class="vig"></div><div class="shade"></div>'},
 // عمق 2.5D، بان جانبي، هزة + رمادي على s.hits
 shop:function(s){return '<div class="cam"><img class="lay bg" src="'+v(s.bg,'L/shop_bg.jpg')+'"><img class="lay fg" src="'+v(s.fg,'L/shop_cut.png')+'"></div><div class="shade"></div>'},
 // صورة مع مصاري بتطير يمين ويسار، دفشة على s.hits
 money:function(s){return '<div class="cam"><img class="lay bg" src="'+v(s.bg,'img/money.png')+'"></div><div class="bills"></div><div class="shade"></div>'},

 // ===== مشاهد عامة للفيديوهات الجاية =====
 // depth: خلفية + شخص مقصوص (عمق 2.5D). s.bg, s.fg, s.zoom [من,لـ], s.pan [x من, x لـ], s.fgPan, s.rot [من,لـ]
 //        s.hits: [{t, shake, gray, vig, punch, blur}] بأوقات مطلقة
 depth:function(s){return '<div class="cam"><img class="lay bg" src="'+s.bg+'"'+(s.bgBlur?' style="filter:blur('+s.bgBlur+'px)"':'')+'>'+(s.fg?'<img class="lay fg" src="'+s.fg+'">':'')+'</div><div class="vig"></div><div class="shade"></div>'},
 // photo: صورة وحدة بملء الشاشة بحركة كاميرا (نفس إعدادات depth بلا fg)
 photo:function(s){return TPL.depth({bg:s.img||s.bg,bgBlur:s.bgBlur})},
 // mg: موشن غرافيك: خلفية كحلية، عنصر بيعبّر عن الفكرة (s.el) بيكبر، وشخص مقصوص (s.fg) بيطلع من تحت
 mg:function(s){var e=s.el?'<img class="sp mgel" src="'+s.el+'" style="width:'+v(s.elSize,700)+'px;height:'+v(s.elSize,700)+'px;left:'+(540-v(s.elSize,700)/2)+'px;top:'+v(s.elTop,520)+'px;filter:drop-shadow(0 0 60px '+v(s.glow,'rgba(245,197,66,.4)')+')">':'';
   return '<div class="mg"></div>'+e+(s.fg?'<img class="cut mgfg" src="'+s.fg+'" style="height:'+v(s.fgH,1760)+'px;bottom:'+v(s.fgBottom,-200)+'px">':'')+'<canvas class="pc" width="1080" height="1920"></canvas><div class="dust"></div>'}
};

function hitsFx(s,T){ // تأثيرات الضربات العامة
  var o={x:0,y:0,punch:0,gray:0,vig:0,blur:0};(s.hits||[]).forEach(function(h){
    if(h.shake){var sh=shake(T,h.t,0.3,h.shake===true?12:h.shake,90);o.x+=sh[0];o.y+=sh[1]}
    if(h.punch&&T>=h.t)o.punch+=(h.punch===true?0.05:h.punch)*Math.max(0,1-(T-h.t)/0.3);
    if(h.gray)o.gray+=Math.max(0,1-Math.abs(T-h.t-0.15)/0.45);
    if(h.vig)o.vig=Math.max(o.vig,(h.vig===true?0.85:h.vig)*eo((T-h.t)/0.4));
    if(h.blur&&T>=h.t)o.blur=Math.max(o.blur,8*Math.max(0,1-(T-h.t)/0.4));
  });return o}

var UPD={
 kid:function(el,t,T,s){var p=eio(t/s.len),L=el.querySelector('.ln');if(!L._L){L._L=L.getTotalLength();L.style.strokeDasharray=L._L}
   var d=eio((t-0.25)/1.75),len=L._L*d;L.style.strokeDashoffset=L._L-len;var q=L.getPointAtLength(len);var lift=eo((t-2.15)/0.5);
   el.querySelector('.hand').style.transform='translate('+(q.x-578-30*lift)+'px,'+(q.y-1063-55*lift)+'px) scale('+(1+0.025*lift)+')';
   el.querySelector('.x').setAttribute('opacity',eo((t-2.0)/0.12));var sh=shake(t,2.0,0.3,14,95);
   el.querySelector('.cam').style.transform='translate('+(-20+40*p+sh[0])+'px,'+(30-70*p+sh[1])+'px) rotate('+(-1.4+2.2*p)+'deg) scale('+(1.06+0.14*p)+')';
   el.querySelector('.cam').style.transformOrigin='540px 1000px';el.querySelector('.bgw').style.transform='scale('+(1-0.03*p)+')';
   var c=el.querySelector('canvas').getContext('2d');c.clearRect(0,0,1080,1920);DOTS.forEach(function(o){var y=(o.y-o.s*t*2+1920)%1920,x=o.x+12*Math.sin(t*1.3+o.ph);c.beginPath();c.arc(x,y,o.r,0,7);c.fillStyle='rgba(255,220,150,'+(o.a*(0.6+0.4*Math.sin(t*3+o.ph)))+')';c.fill()});
   el.querySelector('.leak').style.background='radial-gradient(ellipse 60% 40% at '+(-40+140*p)+'% 18%,rgba(255,170,60,.5),rgba(255,170,60,0) 70%)';},
 wall:function(el,t,T,s){var p=eio(t/s.len),HIT=s.hits,sx=0,sy=0;
   el.querySelectorAll('.rt').forEach(function(g,i){var L=g.querySelector('.rl');if(!L._L){L._L=L.getTotalLength();L.style.strokeDasharray=L._L}
     var h=HIT[i],d=eio((T-h[0])/(h[1]-h[0]));L.style.strokeDashoffset=L._L*(1-d);L.style.opacity=(T<h[0])?0:1;
     var k=T-h[1];var bo=k<0?0:(k<0.08?k/0.08:0.75+0.25*Math.max(0,1-(k-0.08)/0.3));g.querySelector('.bar').setAttribute('opacity',bo);
     var xe=k<0?0:eo(k/0.12),xg=g.querySelector('.x');xg.setAttribute('opacity',xe);var tr=xg.getAttribute('transform').split(')')[0]+')';xg.setAttribute('transform',tr+' scale('+(1+0.6*(1-xe))+')');
     var dim=(i<2&&T>HIT[i+1][0])?0.55:1;g.style.opacity=dim;
     var sh=shake(T,h[1],0.3,12,95);sx+=sh[0];sy+=sh[1];});
   var c=el.querySelector('.cam');c.style.transformOrigin='552px 1060px';c.style.transform='translate('+sx+'px,'+(sy-20*p)+'px) scale('+(1.06+0.14*p)+')';
   var vv=0;HIT.forEach(function(h){var k=T-h[1];if(k>=0&&k<0.45)vv=Math.max(vv,k<0.06?k/0.06:1-(k-0.06)/0.39)});el.querySelector('.vig').style.opacity=0.45*vv;},
 mars:function(el,t){var pe=eo(t/1.0),pl=el.querySelector('.planet');pl.style.transform='scale('+(0.35+0.9*pe+0.06*cl((t-1.0)/0.75))+') rotate('+(t*5)+'deg)';
   var ae=eo((t-0.15)/0.75),ct=el.querySelector('.astro');ct.style.transform='translateX(-50%) translateY('+(900*(1-ae))+'px)';
   dust(el.querySelector('canvas').getContext('2d'),t,0.15,'196,110,60');},
 joy:function(el,t,T,s){var p=eio(t/s.len);
   var pu=(T>=s.punch)?1+0.06*Math.max(0,1-(T-s.punch)/0.35):1;
   el.querySelector('.fg').style.transform='scale('+(1+0.07*p)+')';el.querySelector('.fg').style.transformOrigin='540px 1500px';el.querySelector('.bgw').style.transform='scale('+(1.07-0.05*p)+')';
   el.querySelector('.cam').style.transform='scale('+pu+')';var c=el.querySelector('canvas').getContext('2d');c.clearRect(0,0,1080,1920);
   for(var i=0;i<26;i++){var a=i*2.4+t*0.8,r=(i*37%300)+t*60;var x=540+Math.cos(a)*r*1.6,y=1300+Math.sin(a)*r;var al=(Math.sin(t*6+i)+1)/2;c.beginPath();c.arc(x,y,2+i%3,0,7);c.fillStyle='rgba(255,230,140,'+(0.5*al)+')';c.fill()}},
 maze:function(el,t,T,s){var p=eio(t/s.len);var cam=el.querySelector('.cam');cam.style.transformOrigin='540px 980px';var sh=shake(t,s.hit-s.a,0.3,10,80);
   cam.style.transform='translate('+sh[0]+'px,'+sh[1]+'px) rotate('+(-2+4*p)+'deg) scale('+(1.0+0.32*p)+')';el.querySelector('.fg').style.transform='scale('+(1+0.05*p)+')';el.querySelector('.fg').style.transformOrigin='540px 1000px';
   el.querySelector('.vig').style.opacity=0.85*eo((T-s.hit)/0.4);},
 shop:function(el,t,T,s){var p=eio(t/s.len),H=s.hits;el.querySelector('.fg').style.transform='translate('+(10-20*p)+'px,0) scale('+(1+0.03*p)+')';el.querySelector('.fg').style.transformOrigin='540px 1900px';
   var sh=shake(T,H[0],0.3,12,90),sh2=shake(T,H[1],0.3,12,90);var g=Math.max(0,1-Math.abs(T-H[0]-0.15)/0.45)+Math.max(0,1-Math.abs(T-H[1]-0.15)/0.45);
   el.querySelector('.bg').style.filter='grayscale('+Math.min(.8,g)+')';el.querySelector('.cam').style.transform='translate('+(sh[0]+sh2[0]-25+50*p)+'px,'+(sh[1]+sh2[1])+'px) scale('+(1.1-0.04*p)+')';},
 money:function(el,t,T,s){var p=eio(t/s.len),H=s.hits;var pu=(T>=H[0])?0.05*Math.max(0,1-(T-H[0])/0.3):0;var pu2=(T>=H[1])?0.05*Math.max(0,1-(T-H[1])/0.3):0;var sh=shake(T,H[0],0.25,10,90);
   el.querySelector('.cam').style.transform='translate('+sh[0]+'px,'+sh[1]+'px) scale('+(1.04+0.08*p+pu+pu2)+')';var h='';
   BILLS.forEach(function(b){var lt=t-b.t0;if(lt<0||lt>1.2)return;var x=540+b.side*lt*1100,y=b.y+b.vy*lt+260*lt*lt;var o=Math.min(1,lt/0.08)*Math.min(1,(1.2-lt)/0.2);
     h+='<img src="'+v(s.bill,'L/bill.png')+'" style="position:absolute;left:'+(x-b.sz/2)+'px;top:'+(y-b.sz/2)+'px;width:'+b.sz+'px;opacity:'+o+';transform:rotate('+(b.r+b.vr*lt)+'deg);filter:blur('+(lt*3).toFixed(1)+'px) drop-shadow(0 8px 12px rgba(0,0,0,.5))">'});
   el.querySelector('.bills').innerHTML=h;},

 depth:function(el,t,T,s){var p=eio(t/s.len),z=v(s.zoom,[1.04,1.16]),px=v(s.pan,[0,0]),py=v(s.panY,[0,0]),r=v(s.rot,[0,0]),fp=v(s.fgPan,[0,0]),fz=v(s.fgZoom,[1,1.04]);
   var f=hitsFx(s,T),cam=el.querySelector('.cam');cam.style.transformOrigin=v(s.origin,'540px 1000px');
   cam.style.transform='translate('+(px[0]+(px[1]-px[0])*p+f.x)+'px,'+(py[0]+(py[1]-py[0])*p+f.y)+'px) rotate('+(r[0]+(r[1]-r[0])*p)+'deg) scale('+(z[0]+(z[1]-z[0])*p+f.punch)+')';
   var fg=el.querySelector('.fg');if(fg){fg.style.transformOrigin='540px 1900px';fg.style.transform='translate('+(fp[0]+(fp[1]-fp[0])*p)+'px,0) scale('+(fz[0]+(fz[1]-fz[0])*p)+')'}
   var bg=el.querySelector('.bg'),fl=(s.bgBlur?'blur('+s.bgBlur+'px) ':'')+'grayscale('+Math.min(.8,f.gray)+')'+(f.blur?' blur('+f.blur.toFixed(1)+'px)':'');bg.style.filter=fl;
   el.querySelector('.vig').style.opacity=f.vig;},
 photo:function(el,t,T,s){UPD.depth(el,t,T,s)},
 mg:function(el,t,T,s){var e=el.querySelector('.mgel');if(e){var pe=eo(t/1.0);e.style.transform='scale('+(0.35+0.9*pe+0.06*cl((t-1.0)/0.75))+') rotate('+(t*v(s.spin,0))+'deg)'}
   var f=el.querySelector('.mgfg');if(f){var ae=eo((t-0.15)/0.75);f.style.transform='translateX(-50%) translateY('+(900*(1-ae))+'px)'}
   if(s.dust!==false)dust(el.querySelector('canvas').getContext('2d'),t,0.15,v(s.dustRGB,'196,110,60'));}
};

function dust(c,t,start,rgb){c.clearRect(0,0,1080,1920);
  for(var i=0;i<70;i++){var t0=start+(i%14)*0.04,lt=t-t0;if(lt<0)continue;var ang=-Math.PI/2+((i*53)%100/100-0.5)*2.4,sp=180+(i*37)%260;
    var x=540+Math.cos(ang)*sp*lt*1.6+((i*29)%300-150),y=1900+Math.sin(ang)*sp*lt*1.2+90*lt*lt;var al=Math.max(0,0.8-lt*0.5);if(al<=0)continue;
    var r=18+(i%5)*10+lt*40;var g=c.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,'rgba('+rgb+','+al+')');g.addColorStop(1,'rgba('+rgb+',0)');c.fillStyle=g;c.beginPath();c.arc(x,y,r,0,7);c.fill()}}
