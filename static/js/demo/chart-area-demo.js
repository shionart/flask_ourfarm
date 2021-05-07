// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}



var data_suhu2 = [];
var data_lembap2 = [];
var data_sm2 = [];
// Area Chart Example
  var ctx = document.getElementById("myBarLembapUdara");
  var myBarLembapUdara = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
      datasets: [{
        label: "Lembap Udara",
        lineTension: 0.3,
        backgroundColor: "rgba(78, 115, 223, 0.00)",
        borderColor: "#36b9cc",
        pointRadius: 3,
        pointBackgroundColor: "rgba(78, 115, 223, 1)",
        pointBorderColor: "#36b9cc",
        pointHoverRadius: 3,
        pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
        pointHoverBorderColor: "rgba(78, 115, 223, 1)",
        pointHitRadius: 10,
        pointBorderWidth: 2,
        data: data_lembap2,
      }],
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 25,
          bottom: 0
        }
      },
      scales: {
        xAxes: [{
          time: {
            unit: 'date'
          },
          gridLines: {
            display: false,
            drawBorder: false
          },
          ticks: {
            maxTicksLimit: 7
          }
        }],
        yAxes: [{
          ticks: {
            maxTicksLimit: 5,
            padding: 10,
            // Include a dollar sign in the ticks
            callback: function(value, index, values) {
              return number_format(value) + '%';
            }
          },
          gridLines: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
            borderDash: [2],
            zeroLineBorderDash: [2]
          }
        }],
      },
      legend: {
        display: false
      },
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        intersect: false,
        mode: 'index',
        caretPadding: 10,
        callbacks: {
          label: function(tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': ' + number_format(tooltipItem.yLabel) +'%';
          }
        }
      }
    }
  });

  var ctx = document.getElementById("myBarSuhu");
  var myBarSuhu = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
      datasets: [{
        label: "Suhu",
        lineTension: 0.3,
        backgroundColor: "rgba(78, 115, 223, 0.00)",
        borderColor: "#e74a3b",
        pointRadius: 3,
        pointBackgroundColor: "rgba(78, 115, 223, 1)",
        pointBorderColor: "#e74a3b",
        pointHoverRadius: 3,
        pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
        pointHoverBorderColor: "rgba(78, 115, 223, 1)",
        pointHitRadius: 10,
        pointBorderWidth: 2,
        data: data_suhu2,
      }],
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 25,
          bottom: 0
        }
      },
      scales: {
        xAxes: [{
          time: {
            unit: 'date'
          },
          gridLines: {
            display: false,
            drawBorder: false
          },
          ticks: {
            maxTicksLimit: 7
          }
        }],
        yAxes: [{
          ticks: {
            maxTicksLimit: 5,
            padding: 10,
            // Include a dollar sign in the ticks
            callback: function(value, index, values) {
              return number_format(value,2) + '°C';
            }
          },
          gridLines: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
            borderDash: [2],
            zeroLineBorderDash: [2]
          }
        }],
      },
      legend: {
        display: false
      },
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        intersect: false,
        mode: 'index',
        caretPadding: 10,
        callbacks: {
          label: function(tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': ' + number_format(tooltipItem.yLabel,2)+'°C';
          }
        }
      }
    }
  });

  var ctx = document.getElementById("myBarLembapTanah");
  var myBarLembapTanah = new Chart(ctx, {
    type: 'line',
    data: {
      labels: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
      datasets: [{
        label: "Lembap Tanah",
        lineTension: 0.3,
        backgroundColor: "rgba(78, 115, 223, 0.00)",
        borderColor: "#1cc88a",
        pointRadius: 3,
        pointBackgroundColor: "rgba(78, 115, 223, 1)",
        pointBorderColor: "#1cc88a",
        pointHoverRadius: 3,
        pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
        pointHoverBorderColor: "rgba(78, 115, 223, 1)",
        pointHitRadius: 10,
        pointBorderWidth: 2,
        data: data_sm2,
      }],
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        padding: {
          left: 10,
          right: 25,
          top: 25,
          bottom: 0
        }
      },
      scales: {
        xAxes: [{
          time: {
            unit: 'date'
          },
          gridLines: {
            display: false,
            drawBorder: false
          },
          ticks: {
            maxTicksLimit: 7
          }
        }],
        yAxes: [{
          ticks: {
            maxTicksLimit: 5,
            padding: 10,
            // Include a dollar sign in the ticks
            callback: function(value, index, values) {
              return number_format(value)+'%';
            }
          },
          gridLines: {
            color: "rgb(234, 236, 244)",
            zeroLineColor: "rgb(234, 236, 244)",
            drawBorder: false,
            borderDash: [2],
            zeroLineBorderDash: [2]
          }
        }],
      },
      legend: {
        display: false
      },
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        intersect: false,
        mode: 'index',
        caretPadding: 10,
        callbacks: {
          label: function(tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': ' + number_format(tooltipItem.yLabel)+'%';
          }
        }
      }
    }
  });

function updateChart2() {
  myBarLembapUdara.data.datasets[0].data = data_lembap2;
  myBarSuhu.data.datasets[0].data = data_suhu2;
  myBarLembapTanah.data.datasets[0].data=data_sm2;
  myBarLembapUdara.update();
  myBarSuhu.update();
  myBarLembapTanah.update();
}
// var pathArray = window.location.pathname.split('/');
// var url_baru2 = window.location.origin;
// url_baru2 += "/get/";
// url_baru2 += pathArray[2];
function ubahYesterday(a, b, c){
  // console.log(a['nilai']+b['nilai']+c['nilai']);
  if (a['sign']>0) {
    $('#yesterdayudara').html("<i class='fas fa fa-angle-double-up'></i>"+a['nilai']);
  }else{
    $('#yesterdayudara').html("<i class='fas fa fa-angle-double-down'></i>"+a['nilai']*-1);
  }
  if (b['sign']>0) {
    $('#yesterdaysuhu').html("<i class='fas fa fa-angle-double-up'></i>"+b['nilai']);
  }else{
    $('#yesterdaysuhu').html("<i class='fas fa fa-angle-double-down'></i>"+b['nilai']*-1);
  }
  if (c['sign']>0) {
    $('#yesterdaysm').html("<i class='fas fa fa-angle-double-up'></i>"+c['nilai']);
  }else{
    $('#yesterdaysm').html("<i class='fas fa fa-angle-double-down'></i>"+c['nilai']*-1);
  }
}

function getData2(){
  $.get(data_id, function(data){
    setTimeout(getData2,1000);
    console.log(data['bar_data']);
    $('#curr_lembap_udara').html(data['curr_data']['lembap']);
    $('#curr_suhu').html(data['curr_data']['suhu']);
    $('#curr_lembap_tanah').html(data['curr_data']['sm']);
    $('#prog_lembap_udara').css("width",data['curr_data']['lembap']+"%");
    $('#prog_lembap_udara').attr("aria-valuenow",data['curr_data']['lembap']+"");
    $('#prog_suhu').css("width",data['curr_data']['suhu']+"%");
    $('#prog_suhu').attr("aria-valuenow",data['curr_data']['suhu']+"");
    $('#prog_lembap_tanah').css("width",data['curr_data']['sm']+"%");
    $('#prog_lembap_tanah').attr("aria-valuenow",data['curr_data']['sm']+"");
    ubahYesterday(data['yesterday']['lembap'], data['yesterday']['suhu'], data['yesterday']['sm']);
    data_suhu2=data['bar_data']['suhu'];
    data_lembap2=data['bar_data']['lembap'];
    data_sm2=data['bar_data']['sm'];
    updateChart2();
   
  });
}
getData2();