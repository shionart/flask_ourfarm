// var data_control=[];
var isi=[];
function get_data_control(){
    for (a in isi){
        for(b in a){
            return b;
        }
    }
}

var cardv2 = '<div class="card border-left-primary shadow h-100 py-2">'+
                '<div class="card-body">'+
                    '<div class="row no-gutters align-items-center">'+
                        '<div class="col mr-2">'+
                            '<div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Earnings (Monthly)</div>'+
                            '<div class="h5 mb-0 font-weight-bold text-gray-800">$40,000</div>'+
                        '</div>'+
                        '<div class="col-auto">'+
                            '<i class="fas fa-calendar fa-2x text-gray-300"></i>'+
                        '</div>'+
                    '</div>'+
                '</div>'+
            '</div>';
// var card = $('#test').html();
// var pathArray = window.location.pathname.split('/');
// var url_control = window.location.origin;
// url_control += "/get_control";

function generateCard(array){
    var all="";
    for(a in array){
       var id_arduino = array[a]['id_arduino'];
    //    var perintah= array[a]['perintah'];
    //    var status= array[a]['status'];
       var nama="nama perangkat";
       all +=   '<div class="card border-left-success shadow py-2 ">'+
                    '<div class="card-body">'+
                        '<div class="row no-gutters align-items-center">'+
                            '<div class="col-7">'+
                                '<div class="text-xs font-weight-bold text-success text-uppercase mb-1">'+id_arduino+
                                    '<div class="h5 mb-0 font-weight-bold text-gray-800">'+nama+'</div>'+
                                '</div>'+
                            '</div>'+
                            '<div class="col-3">'+
                                '<a href='+page_dashboard(id_arduino)+' class="btn btn-info btn-lg active" role="button" aria-pressed="true">Dashboard</a>'+
                            '</div>'+
                            '<div class="col-2">'+
                                '<a href='+page_control(id_arduino)+' class="btn btn-info btn-lg active" role="button" aria-pressed="true">Control</a>'+
                            '</div>'+
                        '</div>'+
                    '</div>'+
                '</div>'+
                '<br>';
    }
    return all;
}

function getControl(){
    $.get(data_control, function( data ) {
        isi = data['nodes']
        setTimeout(getControl,10000);
        if (isi==null) {
            console.log('data kosong');
        }
        else{
            // for (a in isi) {
            //     console.log(isi[a]['id_arduino']);    
            // }
            // console.log(isi);
            
            $("#listnodes").html(generateCard(isi));

        }
        // alert( "Load was performed." );
    });
}

getControl();