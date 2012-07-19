var urlService;
var simplemap;
var simplemarker;
var size;
var offset;
var icon_marker;
var simplemarker_layer;
var icon_url = portal_url+'/++resource++map_pin.png';

$(document).ready(function(){

    simplemarker_layer = new OpenLayers.Layer.Markers( "Markers" );
    simplemap = new OpenLayers.UrbisMap({div:"urbis_map_form", lang: $('html').attr('lang')});
    size = new OpenLayers.Size(32,32);
    offset = new OpenLayers.Pixel(-(size.w/2), -size.h);

    urlService = $('div.data').data('gis-service');
    $("#fieldset-addr input[type='text']").focus(function(){
        updatexy();
    });

    $("#localize").click(function(){
        updatexy();
    });
    if ($("#localize")) {
        readonlyHiddenXY();
        updatexy();
    }
});

function updatemap(){
    x = $('#orga-widgets-x').val();
    y = $('#orga-widgets-y').val();
    title = $('#orga-widgets-name').val();
    if (x && y){
        if (simplemarker) {simplemarker.destroy();}
        simplemarker_layer.clearMarkers();
        icon_marker = new OpenLayers.Icon(icon_url, size, offset);

        simplemarker = new OpenLayers.Marker(new OpenLayers.LonLat(x, y), icon_marker.clone());

        simplemarker_layer.addMarker(simplemarker);
        simplemap.addLayer(simplemarker_layer);

        simplemap.setCenter(new OpenLayers.LonLat(x, y), 2);
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
                if (address_data.result.length != 0 ){
                    var x =Number(address_data.result[0].point.x);
                    var y =Number(address_data.result[0].point.y);
                    if(!(isNaN(x) || isNaN(y))) {
                        $('#orga-widgets-x').val(x);
                        $('#orga-widgets-y').val(y);
                        updatemap();
                        //visible('orga-widgets-x');
                        //visible('orga-widgets-y');
                    }
                }else {
                    $('#orga-widgets-x').val('xxx');
                    $('#orga-widgets-y').val('yyy');
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
