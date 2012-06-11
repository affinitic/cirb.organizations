function add_point(x, y, title, color){
    return {'point': {'x': x , 'y': y }, 'title': title, 'color': color}
}

$(window).bind("load", function(){
    if ($('div.multidata').data('lang')) {
        var map = new OpenLayers.UrbisMap({div:"urbis_map", lang: $('div.multidata').data('lang')});
        //map.addControls([new OpenLayers.Control.UrbisPanel({controls:["address","switch"]})]);

        json_url = $('div.multidata').data('absolute_url')+"/json";
        $.getJSON(json_url, function(data){
            var items = [];
            $.each(data, function(key, val) {
                items.push(add_point(val.orga.x, val.orga.y, val.orga.name , '#00f'));
            });
            map.addPoints(items);
        });
        map.setCenter(new OpenLayers.LonLat(149642,171451), 1); 
    }
});
