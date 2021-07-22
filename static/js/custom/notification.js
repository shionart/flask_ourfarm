
var isi=[];

function generateCard(array){
    var all="";
    for(a in array){
        var id_arduino = array[a]['id_arduino'];
        var soil_moist = array[a]['soil_moist'];
        var time = array[a]['time'];
        // getLastUpdated(id_arduino);
    //    if (nama==null) {
    //     nama="nama perangkat";
    //    }
       all +=   '<a class="dropdown-item d-flex align-items-center" href="#">'+
       '<div class="mr-3">'+
         '<div class="icon-circle bg-warning">'+
           '<i class="fas fa-exclamation-triangle text-white"></i>'+
         '</div>'+
       '</div>'+
       '<div>'+
         '<div class="small text-gray-500" id="">'+time+'</div>'+
         '!Arduino '+id_arduino+' : Kelembapan tanah berada di '+soil_moist+'% !'+
       '</div>'+
     '</a>';
    }
    return all;
}

function getNotified(){
    $.get(url_notified, function( data ) {
        isi = data['notif'];
        setTimeout(getNotified,10000);
        if (isi==null) {
            console.log('tidak ada notif');
        }
        else{
            $("#listnotif").html(generateCard(isi));
        }
    });
}

getNotified();