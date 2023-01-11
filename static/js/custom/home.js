$(document).ready(function(){
  $('.toast').toast();
});
var tempVal=$("#userID").val();
$("#change").click(
    function(){
        $("#userID").removeAttr("readonly");
        $("#change").attr("hidden", true);
        $("#save").attr("hidden", false);
    }
);
$("#save").click(
    function(){
      $("#userID").attr("readonly", true);
      $("#save").attr("hidden", true);
      $("#change").attr("hidden", false);
      var key = $("#userID").val().trim();
      if (key!="") {
        $("#userID").val(key);
        postUserid(email,key);
        $('.toast').toast('show');  
      }else{
        $("#userID").val(tempVal);
      }
    }
);

function postUserid(a,b) {
    $.post(post_userid,
      {
        email: a,
        id_user: b
      }
    );
  }