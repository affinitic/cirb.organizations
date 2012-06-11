$(window).bind("load", function(){
    var map = new OpenLayers.UrbisMap({div:"urbis_map", lang: $('div.data').data('lang')});
    var x = $('div.data').data('x');
    var y = $('div.data').data('y');
    var title = $('h2.name').html();
    var color = "#00f";
    points = [];
    points.push(add_point(x, y, title, color));
    map.addPoints(points);
    map.setCenter(new OpenLayers.LonLat($('div.data').data('x'), $('div.data').data('y')), 4);
});


