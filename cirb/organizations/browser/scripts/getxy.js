var urlService = "http://service.gis.irisnetlab.be/urbis/";

$(document).ready(function(){
    $('#addr-widgets-municipality').focus(function(){
        getaddresses($('#addr-widgets-street').val()+' '+$('#addr-widgets-num').val()+' '+$('#addr-widgets-post_code').val());
    });

    function getaddresses(addr){
    var language = '';//document.getElementById("l1").value;
    var address = addr;
    //var div = document.getElementById("responseGetAddresses");
    //div.className = "responseWait";
    //div.innerHTML = "";
    $(function() {
        $.ajax({
            dataType:'jsonp',
            url: urlService+'Rest/Localize/getaddresses',
            data: { language:language,address:address },
            success:function(address_data) {
                var x =Number(address_data.result[0].point.x);
                var y =Number(address_data.result[0].point.y);
                if(!(isNaN(x) || isNaN(y))) {
                    $('#orga-widgets-x').val(x);
                    $('#orga-widgets-y').val(y);
                }
            },
            error:function(){
                $('#orga-widgets-x').val('error');
            },
        });
    });

    };
});
