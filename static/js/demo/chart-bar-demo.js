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

var data_suhu = [];
var data_lembap = [];
var data_sm = [];
function re_suhu(){
  return data_suhu;
}
function re_sm(){
  return data_sm;
}
// Bar Chart Data persen
// function chartLembap(){
  // await getData();
  var ctx1 = document.getElementById("myBarLembapUdara");
  var myBarLembapUdara = new Chart(ctx1, {
    type: 'bar',
    data: {
      labels:["","","","","","","","","",""], //["January", "February", "March", "April", "May", "June"],
      datasets: [{
        label: "Kelembapan",
        backgroundColor: "#4e73df",
        hoverBackgroundColor: "#2e59d9",
        borderColor: "#4e73df",
        data: data_lembap,
      }],
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        
        padding: {
          left: 0,
          right: 0,
          top: 0,
          bottom: 0
        }
      },
      scales: {
        xAxes: [{
          time: {
            unit: 'month'
          },
          gridLines: {
            display: false,
            drawBorder: false
          },
          ticks: {
            maxTicksLimit: 6
          },
          maxBarThickness: 25,
        }],
        yAxes: [{
          ticks: {
            min: 0,
            max: 100,
            maxTicksLimit: 6,
            padding: 5,
            // Include a dollar sign in the ticks sumbu Y
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
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
        callbacks: {
          label: function(tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': ' + number_format(tooltipItem.yLabel) + '%';
          }
        }
      },
    }
  });
//   return myBarLembapUdara;
// }
// function chartSuhu(){
  var ctx2 = document.getElementById("myBarSuhu");
  var myBarSuhu = new Chart(ctx2, {
    type: 'bar',
    data: {
      labels:["","","","","","","","","",""], //["January", "February", "March", "April", "May", "June"],
      datasets: [{
        label: "Suhu Udara",
        backgroundColor: "#4e73df",
        hoverBackgroundColor: "#2e59d9",
        borderColor: "#4e73df",
        data: data_suhu,
      }],
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        
        padding: {
          left: 0,
          right: 0,
          top: 0,
          bottom: 0
        }
      },
      scales: {
        xAxes: [{
          time: {
            unit: 'month'
          },
          gridLines: {
            display: false,
            drawBorder: false
          },
          ticks: {
            maxTicksLimit: 6
          },
          maxBarThickness: 25,
        }],
        yAxes: [{
          ticks: {
            min: 0,
            max: 50,
            maxTicksLimit: 6,
            padding: 5,
            // Include a dollar sign in the ticks sumbu Y
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
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
        callbacks: {
          label: function(tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': ' + number_format(tooltipItem.yLabel,2) + '%';
          }
        }
      },
    }
  });
// }
// function chartSm(){
  var ctx3 = document.getElementById("myBarLembapTanah");
  var myBarLembapTanah = new Chart(ctx3, {
    type: 'bar',
    data: {
      labels:["","","","","","","","","",""], //["January", "February", "March", "April", "May", "June"],
      datasets: [{
        label: "Kelembapan",
        backgroundColor: "#4e73df",
        hoverBackgroundColor: "#2e59d9",
        borderColor: "#4e73df",
        data: data_sm,
      }],
    },
    options: {
      maintainAspectRatio: false,
      layout: {
        
        padding: {
          left: 0,
          right: 0,
          top: 0,
          bottom: 0
        }
      },
      scales: {
        xAxes: [{
          time: {
            unit: 'month'
          },
          gridLines: {
            display: false,
            drawBorder: false
          },
          ticks: {
            maxTicksLimit: 6
          },
          maxBarThickness: 25,
        }],
        yAxes: [{
          ticks: {
            // min: 0,
            // max: 100,
            maxTicksLimit: 6,
            padding: 5,
            // Include a dollar sign in the ticks sumbu Y
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
        titleMarginBottom: 10,
        titleFontColor: '#6e707e',
        titleFontSize: 14,
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
        callbacks: {
          label: function(tooltipItem, chart) {
            var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
            return datasetLabel + ': ' + number_format(tooltipItem.yLabel) + '%';
          }
        }
      },
    }
  });
// }
//bar chart pake class
function updateChart() {
  myBarLembapUdara.data.datasets[0].data = data_lembap;
  myBarSuhu.data.datasets[0].data = data_suhu;
  myBarLembapTanah.data.datasets[0].data = data_sm;
  myBarLembapUdara.update();
  myBarSuhu.update();
  myBarLembapTanah.update();
}
// chartSuhu();
// chartLembap();
// chartSm();

function getData(){
  $.get("http://127.0.0.1:5000/get", function(data){
    setTimeout(getData,1000*10);
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
    data_suhu=data['bar_data']['suhu'];
    data_lembap=data['bar_data']['lembap'];
    data_sm=data['bar_data']['sm'];
    updateChart();
  });
}

getData();

//contoh
var ctx = document.getElementById("myBarChart");
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ["January", "February", "March", "April", "May", "June"],
    datasets: [{
      label: "Revenue",
      backgroundColor: "#4e73df",
      hoverBackgroundColor: "#2e59d9",
      borderColor: "#4e73df",
      data: [4215, 5312, 6251, 7841, 9821, 14984],
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
          unit: 'month'
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 6
        },
        maxBarThickness: 25,
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 15000,
          maxTicksLimit: 5,
          padding: 10,
          // Include a dollar sign in the ticks
          callback: function(value, index, values) {
            return '$' + number_format(value);
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
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': $' + number_format(tooltipItem.yLabel);
        }
      }
    },
  }
});
