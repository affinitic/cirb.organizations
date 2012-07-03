$(document).ready(function(){
    var map = new OpenLayers.UrbisMap({div:"urbis_map", lang: $('p.coord').data('lang')});
    var x = $('p.coord').data('x');
    var y = $('p.coord').data('y');
    var title = $('h2.name').html();
    var color = "#00f";
    points = [];
    points.push(add_one_point(x, y, title, color));
    map.addPoints(points);
    map.setCenter(new OpenLayers.LonLat(x, y), 2);
});

function add_one_point(x, y, title, color){
    return {'point': {'x': x , 'y': y }, 'title': title, 'color': color}
}

