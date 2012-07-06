function add_single_point(x, y, title, color, url){
    return {'point': {'x': x , 'y': y }, 'title': title, 'color': color, 'url': url}
}

$(document).ready(function(){
    var portal_url = $('div.multidata').data('portal_url');
    var icon_url = '/++resource++map_pin.png';
    icon_url = portal_url+icon_url;
    var size = new OpenLayers.Size(32,32);
    var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
    var icon_marker = new OpenLayers.Icon(icon_url, size, offset);
    var marker_layer = new OpenLayers.Layer.Markers( "Markers" );
    var popup;

    if ($('div.multidata').data('lang')) {
        var map = new OpenLayers.UrbisMap({div:"urbis_map", lang: $('div.multidata').data('lang')});

        json_url = $('div.multidata').data('absolute_url')+"/json";
        $.getJSON(json_url, function(data){
            $.each(data, function(key, val) {
                lonlat = new OpenLayers.LonLat(val.orga.x, val.orga.y);
                marker = new OpenLayers.Marker(lonlat, icon_marker.clone());
                marker.events.register('mouseover', marker, function(evt) { 
                    if(popup){
                        popup.hide();
                    }
                    html = '<div><a href="'+ val.orga.url+'"> '+val.orga.name +' </a></div>';
                    popup = new OpenLayers.Popup.FramedCloud("Popup", 
                                new OpenLayers.LonLat(val.orga.x, val.orga.y), 
                                null,
                                html, 
                                null,
                                true // <-- true if we want a close (X) button, false otherwise
                                );
                    map.addPopup(popup);
                });
                    
                marker_layer.addMarker(marker);
                map.addLayer(marker_layer);
            });
        });
        map.setCenter(new OpenLayers.LonLat(149642,171451), 1); 
    }
});
