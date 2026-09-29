document.addEventListener("DOMContentLoaded", function () {

    const chartCanvas = document.getElementById("marketChart");

    if (!chartCanvas) {
        return;
    }

    const years = JSON.parse(
        document.getElementById("chart-years").textContent
    );

    const values = JSON.parse(
        document.getElementById("chart-values").textContent
    );

    new Chart(chartCanvas, {
        type: "line",

        data: {
            labels: years,

            datasets: [{
                label: "Market Size",
                data: values,
                borderWidth: 2,
                tension: 0.35,
                fill: true,
                pointRadius: 3,
                pointHoverRadius: 6
            }]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false,

            plugins: {
                legend: {
                    display: false
                }
            },

            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },

                y: {
                    beginAtZero: false,
                    grid: {
                        color: "#edf0f5"
                    },

                    ticks: {
                        callback: function(value) {
                            return "$" + value + "M";
                        }
                    }
                }
            }
        }
    });

});
