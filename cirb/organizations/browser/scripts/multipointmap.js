var size = new OpenLayers.Size(32,32);
var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
var popup;
var portal_url;
var marker_layer;
var map;
var icon_marker;
var json;
var icon_url;

$(document).ready(function(){
    portal_url = $('div.multidata').data('portal_url');
    icon_url = '/++resource++map_pin.png';
    icon_url = portal_url+icon_url;

    marker_layer = new OpenLayers.Layer.Markers( "Markers" );
    map = new OpenLayers.UrbisMap({div:"urbis_multi_map", lang: $('div.multidata').data('lang')});

    json_url = $('div.multidata').data('absolute_url')+"/json";
    $.getJSON(json_url, function(data){
        json = data;
        create_points();
    });
    map.setCenter(new OpenLayers.LonLat(149642,171451), 1); 

    $('li.orga').hover(function(){
        id_current = $(this).data('idorga');
        lat_current = $(this).data('latorga');
        lon_current = $(this).data('lonorga');
        for (i in json) {
            mark = json[i];
            if (mark.orga.y == lat_current && mark.orga.x == lon_current) {
                icon_blue_url = '/++resource++map_blue_pin.png';
                icon_blue_url = portal_url+icon_blue_url;
                mark.orga.icon = icon_blue_url;
                create_points();
            } else {
                mark.orga.icon = icon_url;
            }
        }
    });
});

function create_points(){
    $.each(json, function(key, val) {

        add_maker_with_popup(val.orga.icon, val.orga.x, val.orga.y, val.orga.url, val.orga.name);
        map.addLayer(marker_layer);

    });
}

function add_maker_with_popup(icon_url, x, y, orga_url, orga_name){
    lonlat = new OpenLayers.LonLat(x, y);
    icon_marker = new OpenLayers.Icon(icon_url, size, offset);
    marker = new OpenLayers.Marker(lonlat, icon_marker.clone());
    marker.events.register('mouseover', marker, function(evt) { 
        if(popup){
            popup.hide();
        }
        html = '<div><a href="'+ orga_url+'"> '+orga_name +' </a></div>';
        popup = new OpenLayers.Popup.FramedCloud("Popup", 
            new OpenLayers.LonLat(x, y), 
            null,
            html, 
            null,
            true // <-- true if we want a close (X) button, false otherwise
            );
        map.addPopup(popup);
    });

    marker_layer.addMarker(marker);

}
