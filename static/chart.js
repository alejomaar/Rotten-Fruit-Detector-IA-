function drawChart(data){
    var ctx1 = $("fruitCanvas");
    var ctx2 = $("stateCanvas");
    var data1 = {
    labels: ["manzana", "banana", "naranja"],
    datasets: [
    {
        label: "TeamA Score",
        data: [data.apple, data.banana, data.oranges],
        backgroundColor: [
        "#b50000",
        "#c0e900",
        "#b65e00"
        ],
        borderColor: [
        "#1a2024",
        "#1a2024",
        "#1a2024"
        ],
        borderWidth: [1, 1, 1]
    }
    ]
    };

    //doughnut chart data
    var data2 = {
    labels: ["bueno","podrido"],
    datasets: [
    {
        label: "TeamB Score",
        data: [data.good,data.bad],
        backgroundColor: [
        "#0084ff",
        "#291e00"
        ],
        borderColor: [
        "#E9DAC6",
        "#CBCBCB"
        ],
        borderWidth: [1, 1]
    }
    ]
    };

    //options
    var options = {
    responsive: true,
    //maintainAspectRatio: false,
    title: {
    display: true,
    position: "top",
    text: "Doughnut Chart",
    fontSize: 10,
    fontColor: "#111"
    },
    legend: {
    display: true,
    position: "bottom",
    labels: {
        fontColor: "#333",
        fontSize: 10
    }
    }
    };

    //create Chart class object
    var chart1 = new Chart(ctx1, {
    type: "doughnut",
    data: data1,
    options: options
    });

    //create Chart class object
    var chart2 = new Chart(ctx2, {
    type: "doughnut",
    data: data2,
    options: options
        
    });
}

