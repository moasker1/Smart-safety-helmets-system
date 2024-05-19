const sideBTN = document.querySelectorAll('#sideBTN');
const menuBar = document.querySelector('.menuBar')
const menuControls = document.getElementById('menuControls')
window.onload = function () {
    for(let i=0 ; i<sideBTN.length;i++){
        sideBTN[0].style.background = 'linear-gradient(90deg,#02CBF2,#0286A0)';
        sideBTN[0].style.color = '#FEFEFC';
        
    }
}
sideBTN.forEach(item => {
    item.addEventListener('click', () => {
        // Remove any existing black background from other list items
        sideBTN.forEach(otherItem =>{
            otherItem.style.background = '';
            otherItem.style.color = '#989897';
        });

        // Set the background color of the clicked item to black
        item.style.background = 'linear-gradient(90deg,#02CBF2,#0286A0)';
        item.style.color = '#FEFEFC';
    });
});
menuControls.addEventListener('click',()=>{
    menuBar.classList.toggle( "active" );
})
let tablebody = document.getElementById('table2body')
let searchbar = document.getElementById('searchbar2')
let filterSelect = document.getElementById('filterSelect')
let mode = 'name'
if(mode == 'name'){
    searchbar.onkeyup=()=>{
        let filter = searchbar.value.toUpperCase();
        let tr= tablebody.getElementsByTagName('tr');
                    for(var i=0; i<tr.length; i++){
                        let td = tr[i].getElementsByTagName('td')[1];
                        if(td){
                            let txtvalue = td.textContent;
                            if(txtvalue.toLocaleUpperCase().indexOf(filter)>-1){
                                tr[i].style.display='';
                                
                            }else{   
                                tr[i].style.display='none';
                            }
                        }
                    }
    }
}
filterSelect.addEventListener('change',()=>{
    searchbar.focus();
    const filterValue = filterSelect.value
    mode=filterValue;
    if(mode == 'phone'){
        searchbar.onkeyup=()=>{
            let filter = searchbar.value.toUpperCase();
            let tr= tablebody.getElementsByTagName('tr');
                        for(var i=0; i<tr.length; i++){
                            let td = tr[i].getElementsByTagName('td')[2];
                            if(td){
                                let txtvalue = td.textContent;
                                if(txtvalue.toLocaleUpperCase().indexOf(filter)>-1){
                                    tr[i].style.display='';
                                    
                                }else{   
                                    tr[i].style.display='none';
                                }
                            }
                        }
        }
    }
    if(mode == 'username'){
        searchbar.onkeyup=()=>{
            let filter = searchbar.value.toUpperCase();
            let tr= tablebody.getElementsByTagName('tr');
                        for(var i=0; i<tr.length; i++){
                            let td = tr[i].getElementsByTagName('td')[3];
                            if(td){
                                let txtvalue = td.textContent;
                                if(txtvalue.toLocaleUpperCase().indexOf(filter)>-1){
                                    tr[i].style.display='';
                                    
                                }else{   
                                    tr[i].style.display='none';
                                }
                            }
                        }
        }
    }
    if(mode == 'name'){
        searchbar.onkeyup=()=>{
            let filter = searchbar.value.toUpperCase();
            let tr= tablebody.getElementsByTagName('tr');
                        for(var i=0; i<tr.length; i++){
                            let td = tr[i].getElementsByTagName('td')[1];
                            if(td){
                                let txtvalue = td.textContent;
                                if(txtvalue.toLocaleUpperCase().indexOf(filter)>-1){
                                    tr[i].style.display='';
                                    
                                }else{   
                                    tr[i].style.display='none';
                                }
                            }
                        }
        }
    }
})