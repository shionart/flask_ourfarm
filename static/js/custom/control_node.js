document.getElementById("customRadio1").onchange = function() {myFunction(id_arduino,0)};
    document.getElementById("customRadio2").onchange = function() {myFunction(id_arduino,1)};
    document.getElementById("customRadio3").onchange = function() {myFunction(id_arduino,2)};
    document.getElementById("customRadio4").onchange = function() {myFunction(id_arduino,3)};
    function ubahStatus(status) {
      if (status==1) {
          document.getElementById("status").innerHTML="Executed";
        }
        else{
          document.getElementById("status").innerHTML="Waiting";
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
        ubahStatus(data['status']);
      });  
    }
    cekStatus();
    
    
