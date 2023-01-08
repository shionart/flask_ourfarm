var isi=[];

function post_delete_node(id_arduino){
    // let nameOfFunction = this[event.target.name];
    // console.log("target.name + "+nameOfFunction);
    // let arg1 = event.target.getAttribute('data-arg1');
    // console.log("js + "+arg1);
    $.ajax({
        url: delete_api_url,
        type: 'DELETE',
        data: {id_arduino:String(id_arduino)},
        global:false
        // success: function(result) {
        //     // Do something with the result
        // }
    });
    location.reload();
  }

function generateCard(array){
    var all="";
    for(a in array){
        var id_arduino = array[a]['id_arduino'];
        var nama = array[a]['nama'];
        var lastUpdated= array[a]['time'];
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
                            '</div>'
                            if (lastUpdated!=null ) {
                                all+='<div class="col-lg-3 col-md-12 col-sm-12 p-2">'+
                                '<a href='+page_dashboard(id_arduino)+' class="btn btn-info btn-lg col-lg-12 col-md-12 col-sm-12" role="button" aria-pressed="true">Data <i class="fas fa-chart-line"></i></a>'+
                            '</div>';
                            } else {
                                all+='<div class="col-lg-3 col-md-12 col-sm-12 p-2">'+
                                '<a class="btn btn-info.disabled btn-lg col-lg-12 col-md-12 col-sm-12" >No Data <i class="fas fa-chart-line"></i></a>'+
                            '</div>';
                            }
                            all+=
                            '<div class="col-lg-3 col-md-12 col-sm-12 p-2">'+
                                '<a href='+page_control(id_arduino)+' class="btn btn-info btn-lg col-lg-12 col-md-12 col-sm-12" role="button" aria-pressed="true">Kontrol <i class="fas fa-faucet"></i></a>'+
                            '</div>'+
                            '<div class="col-lg-1 col-md-12 col-sm-12 align-self-center">'+
                                '<div class="row justify-content-center p-2">'+
                                '<button onclick=post_delete_node("'+String(id_arduino)+'")  class="btn btn-warning btn-circle btn-sm"> <i class="fas fa-trash"></i></button></div></div>'+
                               
                        '</div>'+
                    '</div>'+
                '</div>'+
            '</div>';
    }
    return all;
}

function getControl(){
    $.get(data_control, function( data ) {
        isi = data['nodes']
        setTimeout(getControl,10000);
        if (isi==null||isi[0]==null) {
            console.log('data kosong');
            var a = 
            '<div class="col-md-12 animated--fade-in">'+
              '<h3 class="text-center mt-5">'+
               '<b>Menunggu perangkat tersambung . . . </b>'+
              '</h3>'+
              '<div class="d-flex justify-content-center">'+
                '<div class="spinner-grow text-success" role="status">'+
                  '<span class="sr-only">Loading...</span>'+
                '</div>'+
              '</div>'+
            '</div>';
            $("#listnodes").html(a);
        }
        else{
            $("#listnodes").html(generateCard(isi));
        }
    });
}

getControl();