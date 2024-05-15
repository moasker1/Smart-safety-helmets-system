let manager=document.getElementById("manager");
let supervisor=document.getElementById("supervisor");
let con1=document.getElementById("con1");
let con2=document.getElementById("con2");
manager.onclick=function(){
    con1.style.display="none";
    con2.style.display="flex";
}
supervisor.onclick=function(){
    con1.style.display="none";
    con2.style.display="flex";
}
const container=document.querySelector(".con");

// for(var i=0;i<90;i++){
//     const blocks=document.createElement("div");
//     blocks.classList.add("block");
//     container.appendChild(blocks)
// };

// function AnimateBlocks(){
//     anime({
//         targets:".block",
//         translateX: function(){
//             return anime.random(-700,700);
//         },
//         translateY: function(){
//             return anime.random(-500,500);
//         },
//         scale: function(){
//             return anime.random(1,7);
//         },
//         easing:"linear",
//         duration:3000,
//         delay:anime.stagger(10),
//         complete:AnimateBlocks,
//     })
// };

AnimateBlocks();
const managerBTN = document.getElementById('managerBTN')
const supervisorBTN = document.getElementById('supervisorBTN')
supervisorBTN.addEventListener('click',()=>{
    con2.classList.add('active')
})
managerBTN.addEventListener('click',()=>{
    con2.classList.remove('active')
})