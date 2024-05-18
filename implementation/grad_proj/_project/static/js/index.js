let con2=document.getElementById("con2");
const managerBTN = document.getElementById('managerBTN')
const supervisorBTN = document.getElementById('supervisorBTN')
supervisorBTN.addEventListener('click',()=>{
    con2.classList.add('active')
})
managerBTN.addEventListener('click',()=>{
    con2.classList.remove('active')
})