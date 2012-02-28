var urlService = $('div.data').data('gis-service');

$(document).ready(function(){
    readonlyHidden('orga-widgets-x');
    readonlyHidden('orga-widgets-y');
    $('#addr-widgets-municipality').focus(function(){
        getaddresses($('#addr-widgets-street').val()+' '+$('#addr-widgets-num').val()+' '+$('#addr-widgets-post_code').val());
    });

    function getaddresses(addr){
        var language = $('html').attr('lang');
        var address = addr;
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
                        visible('orga-widgets-x');
                        visible('orga-widgets-y');
                    }
                },
                error:function(){
                          $('#orga-widgets-x').val('error');
                      },
            });
        });

    };
});

function readonlyHidden(inputid) {
    $('#'+inputid+'').attr('readonly', 'readonly');
    $('#formfield-'+inputid+'').attr('style', 'visibility:hidden');
}
function visible(inputid){
    $('#formfield-'+inputid+'').attr('style', 'visibility:visible');
}
