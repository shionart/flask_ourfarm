var data_control=[];
var isi=[];
function get_data_control(){
    return card;
}

var cardv2 = {"<div></div>"}
var card = $('#test').html();
var pathArray = window.location.pathname.split('/');
var url_control = window.location.origin;
url_control += "/get_control";

// function generateCard(array){
//     for(a in array){
//         id_arduino = a.['id_arduino'];
//         a.['perintah'];
//         a.['status'];
//     }
// }

function getControl(){
    $.get(url_control, function( data ) {
        isi = data['nodes']
        setTimeout(getControl,10000);
        if (isi==null) {
            console.log('data kosong');
        }else{
            console.log('ada data');
            // generateCard(isi);
            $("#listnodes").html("mikum");
            data_control=data;

        }
        // alert( "Load was performed." );
    });
}

getControl();