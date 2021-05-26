
var url = 'http://' + document.domain + ':' + location.port
var socket = io.connect(url);

socket.on('connect', function(msg) {
    console.log('connected to websocket on ' + url);
});

socket.on('bootstrap', function (msg) {
    $("#img").attr("src",msg.chart);
    $("#tick").html(msg.tick);


});

socket.on('chartupdate', function (msg) {
    // streamPlotly( msg.x, msg.y )
    $("#img").attr("src",msg.chart);
    $("#tick").html(msg.tick);
});