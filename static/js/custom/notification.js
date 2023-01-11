
var isi=[];

/**
 * Fungsi untuk membuat card notifikasi sesuai jumlah notifikasi
 * @param {*} array dicts dari notifikasi
 * @returns html card notifikasi dan jumlah card
 */
function generateCard2(array){
    var all="";
    for(a in array){
      var id_arduino = array[a]['id_arduino'];
      var soil_moist = array[a]['soil_moist'];
      var time = array[a]['time'];
      var nama = array[a]['nama'];
      var suhu = array[a]['suhu'];
      var info = 'Kelembapan tanah berada di '+soil_moist+'%';
      if (suhu==0) {
        info ='Sensor suhu mengalami masalah!'
      } 
      all+='<form method="post" action="'+notif_dashboard(id_arduino)+'" class="inline-notif">'+
      ' <input type="hidden" id="id_arduino" name="id_arduino" value="'+id_arduino+'">'+
        '<button type="submit" class="link-button-notif dropdown-item d-flex align-items-center">'+
        '<div class="mr-3">'+
         '<div class="icon-circle bg-warning">'+
           '<i class="fas fa-exclamation-triangle text-white"></i>'+
         '</div>'+
       '</div>'+
       '<div>'+
         '<div class="small text-gray-500" id="">'+time+'</div>'+
         'Perangkat <b>'+nama+'</b>: '+info+
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
    return {alerts:all,badge:array.length};
}
/**
 * Jquery get data notifikasi dari API 
 * Json format notif[{id_arduino, soil_moist, time, nama}}]
 */
function getNotified(){
    $.get(url_notified, function( data ) {
        isi = data['notif'];
        setTimeout(getNotified,10000);
        if (isi==null || isi[0]==null) {
            console.log('tidak ada notif');
        }
        else{
          var dict = generateCard2(isi);
          $("#listnotif").html(dict['alerts']);
          if (dict['badge']!=0) {
            $("#countnotif").html(dict['badge']);  
          }
        }
    });
}

getNotified();