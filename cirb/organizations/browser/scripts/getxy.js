var urlService;
var map;
var marker;

$(document).ready(function(){
    map = new OpenLayers.UrbisMap({div:"urbis_map_form", lang: $('html').attr('lang')});
    urlService = $('div.data').data('gis-service');
    $("#fieldset-addr input[type='text']").focus(function(){
        updatexy();
    });

    $("#localize").click(function(){
        updatexy();
    });
    readonlyHiddenXY();
    updatemap();
});

function updatemap(){
    x = $('#orga-widgets-x').val();
    y = $('#orga-widgets-y').val();
    title = $('#orga-widgets-name').val();
    if (x && y){
        if (marker) {marker.destroy();}
        var portal_url = $('div.data').data('portal_url');
        var icon_url = '/++resource++map_pin.png';
        icon_url = portal_url+icon_url;
        var size = new OpenLayers.Size(32,32);
        var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
        var icon_marker = new OpenLayers.Icon(icon_url, size, offset);
        var marker_layer = new OpenLayers.Layer.Markers( "Markers" );

        lonlat = new OpenLayers.LonLat(x, y);
        marker = new OpenLayers.Marker(lonlat, icon_marker);

        marker_layer.addMarker(marker);
        map.addLayer(marker_layer);

        map.setCenter(new OpenLayers.LonLat(x, y), 2);
    }
}

function updatexy(){
    var address = check_address();
    if (!address) {
        return
    }
    var language = $('html').attr('lang');
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
                    updatemap();
                    //visible('orga-widgets-x');
                    //visible('orga-widgets-y');
                }
            },
            error:function(){
                $('#orga-widgets-x').val('error');
            },
        });
    });

}

function readonlyHiddenXY() {
    xy = ['#formfield-orga-widgets-x', '#formfield-orga-widgets-y'];
    for (i=0; i < xy.length; i++) {
        $(xy[i]+' input[type=text]').attr('readonly', 'readonly');
    }
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
