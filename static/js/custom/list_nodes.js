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
                                '<div class="text-xs font-weight-bold text-success text-uppercase mb-1">'+id_arduino+
                                    '<div class="h5 mb-0 font-weight-bold text-gray-800">'+nama+'<i class="fas fa-leaf"></i>'+
                                    '</div>'+
                                '</div>'+
                                '<div id="'+id_arduino+'" class=" mb-0 text-gray-500">Update Terakhir : '+lastUpdated+
                                '</div>'+
                            '</div>'+
                            '<div class="col-lg-1"></div>'+
                            '<div class="col-lg-3 col-md-12 col-sm-12 p-2">'+
<<<<<<< HEAD
<<<<<<< HEAD
                                '<a href='+page_dashboard(id_arduino)+' class="btn btn-info btn-lg active col-lg-12 col-md-12 col-sm-12" role="button" aria-pressed="true">Dashboard</a>'+
                            '</div>'+
                            '<div class="col-lg-3 col-md-12 col-sm-12 p-2">'+
                                '<a href='+page_control(id_arduino)+' class="btn btn-info btn-lg active col-lg-12 col-md-12 col-sm-12" role="button" aria-pressed="true">Control</a>'+
=======
                                '<a href='+page_dashboard(id_arduino)+' class="btn btn-info btn-lg active col-lg-12 col-md-12 col-sm-12" role="button" aria-pressed="true">Dasbor</a>'+
                            '</div>'+
                            '<div class="col-lg-3 col-md-12 col-sm-12 p-2">'+
                                '<a href='+page_control(id_arduino)+' class="btn btn-info btn-lg active col-lg-12 col-md-12 col-sm-12" role="button" aria-pressed="true">Kontrol</a>'+
>>>>>>> 19b48acd42595c7b5ab03967e7c6e61061f822d1
=======
                                '<a href='+page_dashboard(id_arduino)+' class="btn btn-info btn-lg active col-lg-12 col-md-12 col-sm-12" role="button" aria-pressed="true">Dashboard</a>'+
                            '</div>'+
                            '<div class="col-lg-3 col-md-12 col-sm-12 p-2">'+
                                '<a href='+page_control(id_arduino)+' class="btn btn-info btn-lg active col-lg-12 col-md-12 col-sm-12" role="button" aria-pressed="true">Control</a>'+
>>>>>>> parent of 19b48ac (update tampilan dikit)
                            '</div>'+
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
        if (isi==null) {
            console.log('data kosong');
        }
        else{
            $("#listnodes").html(generateCard(isi));
        }
    });
}

getControl();