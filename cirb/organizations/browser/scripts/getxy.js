var urlService;
$(window).bind("load", function(){
    urlService = $('div.data').data('gis-service');
    $("#fieldset-addr input[type='text']").focus(function(){
        address = check_address();
        if (address) {
            getaddresses(address);
        }
    });
    readonlyHiddenXY();
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

function readonlyHiddenXY() {
    xy = ['#formfield-orga-widgets-x', '#formfield-orga-widgets-y'];
    for (i=0; i < xy.length; i++) {
        $(xy[i]+' input[type=text]').attr('readonly', 'readonly');
        if ($(xy[i]+' input[type=text]').val() == '') {
            $(xy[i]).attr('style', 'visibility:hidden');
        }
    }
}
function visible(inputid){
    $('#formfield-'+inputid).attr('style', 'visibility:visible');
}
function check_address() {
    street = $('#addr-widgets-street').val();
    num = $('#addr-widgets-num').val();
    post_code = $('#addr-widgets-post_code').val();
    if (street != '' && num != '' && post_code != '') {
        return street+' '+num+' '+post_code;
    } else {
        return false;
    }
}
