// Call the dataTables jQuery plugin
var pathArray = window.location.pathname.split('/');
var url_baru = window.location.origin;

url_baru += "/get/";
url_baru += pathArray[2];
function cek() {
  return url_baru;
}
$(document).ready(function() {
  var table = $('#sensorTable').DataTable({
    destroy:true,
    // order:false,
    "ajax": {
              url: url_baru,
              dataSrc: 'sensor'
            },
    "columns": [
        { "data": "tanggal" },
        { "data": "jam" },
        { "data": "lembap" },
        { "data": "suhu" },
        { "data": "sm" },
        { "data": "relay" }
    ]
    ,"order" : [[0,"desc"]]
  });
  setInterval( function () {
    table.ajax.reload();
  }, 10000 );
 
});
