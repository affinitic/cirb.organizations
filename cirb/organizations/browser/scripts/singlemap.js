$(document).ready(function(){
    
    var map = new OpenLayers.UrbisMap({div:"urbis_map", lang: $('p.coord').data('lang')});
    
    var portal_url = $('p.coord').data('portal_url');
    var icon_url = '/++resource++map_pin.png';
    icon_url = portal_url+icon_url;
    var size = new OpenLayers.Size(32,32);
    var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
    var icon_marker = new OpenLayers.Icon(icon_url, size, offset);
    var marker_layer = new OpenLayers.Layer.Markers( "Markers" );

    
    var x = $('p.coord').data('x');
    var y = $('p.coord').data('y');

    lonlat = new OpenLayers.LonLat(x, y);
    marker = new OpenLayers.Marker(lonlat, icon_marker);

    marker_layer.addMarker(marker);
    map.addLayer(marker_layer);

    map.setCenter(new OpenLayers.LonLat(x, y), 2);
});

function add_one_point(x, y, title, color){
    return {'point': {'x': x , 'y': y }, 'title': title, 'color': color}
}

