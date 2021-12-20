// var data_control=[];
var isi=[];
// function get_data_control(){
//     for (a in isi){
//         for(b in a){
//             return b;
//         }
//     }
// }

// var card = $('#test').html();
// var pathArray = window.location.pathname.split('/');
// var url_control = window.location.origin;
// url_control += "/get_control";

function generateCard(array){
    var all="";
    for(a in array){
        var id_arduino = array[a]['id_arduino'];
        var nama = array[a]['nama'];
        var lastUpdated= array[a]['time'];
        // getLastUpdated(id_arduino);
        if (nama==null) {
            nama="nama perangkat";
        }
        all +=  
            '<div class="col-xl-6 col-md-6 col-sm-12 mb-4">'+
                '<div class="card border-left-success shadow py-2">'+
                    '<div class="card-body">'+
                        '<div class="row no-gutters align-items-center">'+
                            '<div class="col-lg-5 col-md-12">'+
                                '<div class="text-xs font-weight-bold text-gray-500 text-uppercase mb-1">'+id_arduino+
                                    '<div class="h5 mb-0 font-weight-bold text-success">'+nama+' <i class="fas fa-seedling"></i>'+
                                    '</div>'+
                                '</div>'+
                                '<div id="'+id_arduino+'" class=" mb-0 text-gray-500">Update Terakhir : '+lastUpdated+
                                '</div>'+
                            '</div>'+
                            '<div class="col-lg-3 col-md-12 col-sm-12 p-2">'+
                                '<a href='+page_dashboard(id_arduino)+' class="btn btn-info btn-lg col-lg-12 col-md-12 col-sm-12" role="button" aria-pressed="true">Data <i class="fas fa-chart-line"></i></a>'+
                            '</div>'+
                            '<div class="col-lg-3 col-md-12 col-sm-12 p-2">'+
                                '<a href='+page_control(id_arduino)+' class="btn btn-info btn-lg col-lg-12 col-md-12 col-sm-12" role="button" aria-pressed="true">Kontrol <i class="fas fa-faucet"></i></a>'+
                            '</div>'+
                            '<div class="col-lg-1 col-md-12 col-sm-12 align-self-center">'+
                                '<div class="row justify-content-center p-2">'+
                                '<form action="'+post_delete_node()+'" method="post">'+
                                '<input name="id_arduino" id="id_arduino" value="'+id_arduino+'" hidden="true"></input>'+
                                '<button class="btn btn-warning btn-circle" type="submit"> <i class="fas fa-trash"></i></button></div></div>'+
                        '</div>'+
                    '</div>'+
                '</div>'+
            '</div>';
    }
    return all;
}
/*function getLastUpdated(id_arduino){
    // console.log(url_last_updated(id_arduino));
    $.get(url_last_updated(id_arduino),function String( data ) {
        console.log(data['time']);
        $("#"+id_arduino).html("Update Terakhir : "+data['time'])
     });

    // return a['time'];
}*/
function getControl(){
    $.get(data_control, function( data ) {
        isi = data['nodes']
        setTimeout(getControl,10000);
        if (isi==null||isi[0]==null) {
            console.log('data kosong');
        }
        else{
            $("#listnodes").html(generateCard(isi));
        }
    });
}

getControl();