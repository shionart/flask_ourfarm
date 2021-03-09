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
        postUserid(email,$("#userID").val());
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