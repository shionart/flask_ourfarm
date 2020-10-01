// Call the dataTables jQuery plugin
$(document).ready(function() {
  var table = $('#sensorTable').DataTable({
    destroy:true,
    // order:false,
    "ajax": {
              url: 'http://127.0.0.1:5000/get',
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
