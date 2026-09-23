const menu=document.getElementById("menu");const nav=document.getElementById("nav");
if(menu)menu.addEventListener("click",()=>nav.classList.toggle("open"));
document.querySelectorAll(".nav a").forEach(a=>a.addEventListener("click",()=>nav.classList.remove("open")));
