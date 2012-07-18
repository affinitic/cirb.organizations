$(document).ready(function(){
    var size = new OpenLayers.Size(32,32);
    var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
    var popup;
    var marker_layer;
    var map;
    var icon_marker;
    var json;
    var icon_url;
    var orga;

    icon_url = '/++resource++map_pin.png';
    icon_url = portal_url+icon_url;

    marker_layer = new OpenLayers.Layer.Markers( "Markers" );
    map = new OpenLayers.UrbisMap({div:"urbis_multi_map", lang: $('div.multidata').data('lang')});

    json_url = $('div.multidata').data('absolute_url')+"/json";
    $.getJSON(json_url, function(data){
        json = data;
        create_points();
    });
    map.setCenter(new OpenLayers.LonLat(149642, 171451), 1); 

    $('li.orga').hover(function(){
        change_marker_color(this);
    });

    //selected category
    if ($('.categorybutton-field.selected').length > 0) {
        src = $('.categorybutton-field.selected').attr('src').replace('.png', '-select.png');
        $('.categorybutton-field.selected').attr('src', src);
    }
});

function change_marker_color(elem) {
    id_current = $(elem).data('idorga');
    lat_current = $(elem).data('latorga');
    lon_current = $(elem).data('lonorga');
    for (i in json) {
        mark = json[i];
        if (mark.orga.y == lat_current && mark.orga.x == lon_current) {
            icon_blue_url = '/++resource++map_blue_pin.png';
            icon_blue_url = portal_url+icon_blue_url;
            mark.orga.icon = icon_blue_url;
        } else {
            mark.orga.icon = icon_url;
        }
    }
    create_points();
}

function create_points(){
    $.each(json, function(key, val) {
        add_maker_with_popup(val.orga);
        map.addLayer(marker_layer);
    });
}

function add_maker_with_popup(json_orga){
    lonlat = new OpenLayers.LonLat(json_orga.x, json_orga.y);
    icon_marker = new OpenLayers.Icon(json_orga.icon, size, offset);
    marker = new OpenLayers.Marker(lonlat, icon_marker.clone());
    marker.events.register('mouseover', marker, function (evt){create_popup(json_orga);OpenLayers.Event.stop(evt);});
    marker_layer.addMarker(marker);
}

function create_popup(orga){ 
    if(popup){
        popup.hide();
    }
    html = '<div class="title"><a href="'+ orga.url +'" target="_blanck"> '+ orga.name +' </a></div>';
    html += '<div class="address"><div>'+orga.street+'</div><div>'+orga.city+'</div></div>';
    popup = new OpenLayers.Popup.FramedCloud("Popup", 
                new OpenLayers.LonLat(orga.x, orga.y), 
                null,
                html, 
                null,
                true // <-- true if we want a close (X) button, false otherwise
                );
    map.addPopup(popup);
}
