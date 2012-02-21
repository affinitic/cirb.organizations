var gis_url = "http://192.168.13.94:8080/"
$(document).ready(function(){
    $('#addr-widgets-municipality').focus(function(){
        searchAddress($('#addr-widgets-street').val(),$('#addr-widgets-num').val(),$('#addr-widgets-post_code').val());
    });
    

    function searchAddress(street, number, post_code) {
        var parameters = {
            language: $('html').attr('lang'),
            address: street
        }
        var my_url = gis_url+"services/urbis/Rest/Localize/getaddresses";
        $.ajax({
            type: "POST",
            url: my_url,
            data: parameters,
            dataType: "json",
            success:  function(address_data) {
                var x =Number(address_data.result[0].point.x);
                var y =Number(address_data.result[0].point.y);
                if(!(isNaN(x) || isNaN(y))) {
                    $('#orga-widgets-x').val(x);
                    $('#orga-widgets-y').val(y);
                }
            },
            error:  function(data) {
                        //alert('x,y not found for this address.');
                    }
        });

    };
});
