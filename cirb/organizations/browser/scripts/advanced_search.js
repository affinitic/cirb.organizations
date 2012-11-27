$(document).ready(function(){
    if ($('body.template-orga_advanced_search').length==0){return}
    $('#form-widgets-categories-from option').sort(NASort).appendTo('select#form-widgets-categories-from');
});

function NASort(a, b) {    
    if (a.innerHTML == 'NA') {
        return 1;   
    }
    else if (b.innerHTML == 'NA') {
        return -1;   
    }       
    return (a.innerHTML > b.innerHTML) ? 1 : -1;
};
