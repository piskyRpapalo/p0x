// Ojo-Vivo · Agentes y Procesos. Hardware = solo ubicación.
var MOCK={hud:{salud:"19/20",tareas:"4 Activas",firmas:"12",tests:"540/540",vram:"8.5GB"},
agents:{
 instalador:{room:"agora",tribe:"p",state:"s-sano",tarea:"Esperando nuevo usuario"},
 enlace:{room:"agora",tribe:"e",state:"s-sano",tarea:"Sincronizando Tablón"},
 curador:{room:"memoria",tribe:"p",state:"s-busy",tarea:"Indexando FTS5"},
 privacidad:{room:"frontera",tribe:"p",state:"s-sano",tarea:"Filtro listo"},
 afinador:{room:"inferencia",tribe:"h",state:"s-sano",tarea:"LoRA v7 cargado"},
 analista:{room:"inferencia",tribe:"p",state:"s-sano",tarea:"Leyendo contexto"},
 coder:{room:"forja",tribe:"p",state:"s-busy",tarea:"Generando dataset v8"},
 guardian:{room:"auditoria",tribe:"h",state:"s-sano",tarea:"Auditando 77 ficheros"},
 cowork:{room:"firmas",tribe:"o",state:"s-stale",tarea:"Esperando firma Soberano"}}};
function render(d){
 var hud=document.getElementById("hud");
 hud.innerHTML="<span>SALUD <b>"+d.hud.salud+"</b></span><span>TAREAS <b>"+d.hud.tareas+"</b></span><span>FIRMAS <b>"+d.hud.firmas+"</b></span><span>VRAM <b>"+d.hud.vram+"</b></span><span>TESTS <b>"+d.hud.tests+"</b></span>";
 Object.keys(d.agents).forEach(function(id){var a=d.agents[id];
  var slot=document.querySelector('.agent-slot[data-room="'+a.room+'"]');if(!slot)return;
  var el=document.createElement("div");el.className="agent "+a.tribe+" "+a.state;
  el.title=id+" · "+a.tarea;el.innerHTML="<i></i>";
  el.onclick=function(){openActa(id,a)};slot.appendChild(el);});}
function openActa(id,a){var box=document.getElementById("acta");box.hidden=false;
 document.getElementById("acta-body").textContent=
  "[acta] "+id+"\nestado: "+a.state+"\ntarea: "+a.tarea+"\n(fuente: mock · cablear estado.json)";}
document.getElementById("acta-close").onclick=function(){document.getElementById("acta").hidden=true};
render(MOCK);
