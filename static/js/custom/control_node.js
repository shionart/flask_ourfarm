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
      $("#perintah").html("Scheduled");
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
      document.getElementById("customRadio1").checked = true;
      break;
    case 1:
        document.getElementById("customRadio2").checked = true;
        break;
    case 2:
        document.getElementById("customRadio3").checked = true;
        break;
    case 3:
      document.getElementById("customRadio4").checked = true;
      break;
    default:
      break;
  }
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
  $.post(api_control_url,
    {
      perintah: perintah_i,
      status:"0",
      nama:""
    }
  );
  try {//sync ke api bayu
    $.get(sync_control_get, {nilai:perintah_i}).fail(function() {
      post_failure(perintah_i);
      console.log("post failure");
    });
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
ubahPerintah(perintah);
$("#customRadio1").change(function() {myFunction(0)});
$("#customRadio2").change(function() {myFunction(1)});
$("#customRadio3").change(function() {myFunction(2)});
$("#customRadio4").change(function() {myFunction(3)});
cekStatus();
    
    
