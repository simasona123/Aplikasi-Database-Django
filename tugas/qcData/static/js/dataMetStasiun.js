var ctx = document.getElementById('myChart').getContext('2d');
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels1,
        datasets: [{
            label: 'Jumlah Data',
            data: data1,
            backgroundColor: [
                'rgba(1, 8, 124, 0.7)',
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255, 99, 132, 1)',
                'rgba(153, 102, 255, 0.2)',
            ],
            borderWidth: 1,
            fill: true,
        }]
    },
    options: {
        title : {
            display : true,
            text : "Jumlah Data Dari Waktu ke Waktu"
        },
        layout :{
            padding : {
                left: 25,
                right: 25,
                top: 20,
                bottom: 0
            }
        },
        scales: {
            xAxes: [{
                type: 'time',
                distribution : 'series',
                bounds : 'data',
                time: {
                    unit :'month',
                    displayFormats: {

                    },
                },
            }],
        },
    }
    });
