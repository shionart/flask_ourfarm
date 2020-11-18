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
function myFunction(a,b) {
  $.post(post_url,
    {
      id_arduino: a,
      perintah: b
    }
  );
}
function cekStatus() {
  $.get(get_url, function (data) {
    setTimeout(cekStatus,1000);
    // let isi = data['status'];
    // console.log(isi);
    ubahFooter(data['perintah'],data['status']);
  });  
}
ubahPerintah(perintah);
$("#customRadio1").change(function() {myFunction(id_arduino,0)});
$("#customRadio2").change(function() {myFunction(id_arduino,1)});
$("#customRadio3").change(function() {myFunction(id_arduino,2)});
$("#customRadio4").change(function() {myFunction(id_arduino,3)});
cekStatus();
    
    
