
var isi=[];

function generateCard2(array){
    var all="";
    for(a in array){
      var id_arduino = array[a]['id_arduino'];
      var soil_moist = array[a]['soil_moist'];
      var time = array[a]['time'];
      // var notif = array[a]['notif'];
      var nama = array[a]['nama'];
      // var id_sensor = array[a]['id_sensor'];
      // if (notif==1) {
        
      // } else {
        all+='<form method="post" action="'+notif_dashboard(id_arduino)+'" class="inline-notif">'+
        '<button type="submit" class="link-button-notif dropdown-item d-flex align-items-center">'+
        '<div class="mr-3">'+
         '<div class="icon-circle bg-warning">'+
           '<i class="fas fa-exclamation-triangle text-white"></i>'+
         '</div>'+
       '</div>'+
       '<div>'+
         '<div class="small text-gray-500" id="">'+time+'</div>'+
         'Perangkat <b>'+nama+'</b> : Kelembapan tanah berada di '+soil_moist+'%'+
       '</div>'+
        '</button></form>';
    //     all +='<a class="dropdown-item d-flex align-items-center" href="'+notif_dashboard(id_arduino)+'">'+
    //    '<div class="mr-3">'+
    //      '<div class="icon-circle bg-warning">'+
    //        '<i class="fas fa-exclamation-triangle text-white"></i>'+
    //      '</div>'+
    //    '</div>'+
    //    '<div>'+
    //      '<div class="small text-gray-500" id="">'+time+'</div>'+
    //      'Perangkat <b>'+nama+'</b> : Kelembapan tanah berada di '+soil_moist+'%'+
    //    '</div>'+
    //  '</a>';  
      // }
      
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
            $("#listnotif").html(generateCard2(isi));
        }
    });
}

getNotified();