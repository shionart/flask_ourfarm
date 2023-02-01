function ubahFooter(perintah,status) {
  if (status==1) {
      $("#status").html("Executed");
    }
    else{
      $("#status").html("Waiting");
    }
  switch (perintah) {
    case 0:
      $("#perintah").html("Default (Otomatis)");
      break;
    case 1:
      $("#perintah").html("Interval");
      break;
    case 2:
      $("#perintah").html("Stay On");
      break;
    case 3:
      $("#perintah").html("Stay Off");
      break;
    default:
      break;
  }
}
function ubahPerintah(perintah) {
  switch (perintah) {
    case 0:
      document.getElementById("perintah1").checked = true;
      break;
    case 1:
        document.getElementById("perintah2").checked = true;
        break;
    case 2:
        document.getElementById("perintah3").checked = true;
        break;
    case 3:
      document.getElementById("perintah4").checked = true;
      break;
    default:
      break;
  }
}
function ubahjeda(jeda) {
  switch (jeda) {
    case 2:
      $('select option[value="2"]').attr("selected",true);
      break;
    case 4:
      $('select option[value="4"]').attr("selected",true);
      break;
    case 6:
      $('select option[value="6"]').attr("selected",true);
      break;
    case 8:
      $('select option[value="8"]').attr("selected",true);
      break;
    case 12:
      $('select option[value="12"]').attr("selected",true);
      break;
    case 24:
      $('select option[value="24"]').attr("selected",true);
      break;
    default:
      break;
  }
}

function ubahDeskripsi(perintah_i) {
  switch (perintah_i) {
    case 0:
      $("#form_default").attr("hidden", false);
      // $("#batas_atas").removeAttr('disabled');
      // $("#batas_bawah").removeAttr('disabled');
      $("#form_jeda").attr("hidden", true);
      // $("#select_jeda").attr('disabled','disabled');
      break;
    case 1:
      $("#form_default").attr("hidden", true);
      // $("#batas_atas").attr('disabled','disabled');
      // $("#batas_bawah").attr('disabled','disabled');
      $("#form_jeda").attr("hidden", false);
      // $("#select_jeda").removeAttr('disabled');
      break;
    default:
        $("#form_default").attr("hidden", true);
        // $("#batas_atas").attr('disabled','disabled');
        // $("#batas_bawah").attr('disabled','disabled');
        $("#form_jeda").attr("hidden", true);
        // $("#select_jeda").attr('disabled','disabled');
    break;
  };
}
/**
 * Fungsi yg triggered ketika melakukan perubahan perintah
 * Setiap melakukan perubahan perintah dilakukan :
 * POST data ke API local (update data Control),
 * GET data ke API web pusat (update data control):
 * jika failed data masuk ke queue table
 * @param {*} perintah 
 */
function myFunction(perintah_i) {
  ubahDeskripsi(perintah_i);
  $.post(api_control_url,
    {
      perintah: perintah_i,
      status:"0",
      nama:"",
      id_user:""
    }
  );
  try {//post perintah ke api bayu
    $.get(sync_control_get, {nilai:perintah_i}).fail(function() {
      post_failure(perintah_i);
      console.log("post failure");
    });
    console.log("fetching from website pusat")
  } catch (error) {
    console.log("Error :"+error);
  }
    /**
     $.get(api_queue_url, function (data) {
       for (let index = 0; index < data.length; index++) {
         const element = data[index];
         // console.log(element["perintah"]);
         $.get(sync_control_get,
           {
             nilai:element["perintah"]
           }
         ); //Di sini tiap dia ubah malah hapus data
       }
     });//.done(delete_queue(element["idqueue_control"]))di sini connect ga konnect tetep aja ngapus karena yg diek request api_queue_url nya bukan sync_control_get
     //post to web pusat perintah yg diubah
     * 
     */
}

function delete_queue(idqueue) {
  $.ajax({
    url: api_queue_url,
    type: 'DELETE',
    data : {idqueue_control: idqueue},
    success: function() {
        console.log("Queue Terhapus");
    }
});
}

function post_failure(perintah_i){
  $.post(api_queue_url,
    {
      id_arduino:id_arduino,
      id_user:id_user,
      perintah:perintah_i
    }
  );
}
function cekStatus() {
  
  $.get(api_control_url, function (data) {
    setTimeout(cekStatus,1000);
    // let isi = data['status'];
    // console.log(isi);
    ubahFooter(data['perintah'],data['status']);
  });  
}
$("#perintah1").change(function() {ubahDeskripsi(0)});
$("#perintah2").change(function() {ubahDeskripsi(1)});
$("#perintah3").change(function() {ubahDeskripsi(2)});
$("#perintah4").change(function() {ubahDeskripsi(3)});
ubahPerintah(perintah);
ubahjeda(jeda);
ubahDeskripsi(perintah);
cekStatus();
    
    
