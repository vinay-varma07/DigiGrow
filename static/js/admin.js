document.addEventListener("DOMContentLoaded", () => {
    const dataElement = document.getElementById("chart-data");

    if (!dataElement || typeof Chart === "undefined") {
        return;
    }

    const chartData = JSON.parse(dataElement.textContent);

    const chartOptions = {
        responsive: true,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 5,
                ticks: {
                    stepSize: 1
                }
            }
        }
    };

    const confidenceChart = document.getElementById("confidenceChart");
    const presenceChart = document.getElementById("presenceChart");
    const platformChart = document.getElementById("platformChart");

    if (confidenceChart) {
        new Chart(confidenceChart, {
            type: "bar",
            data: {
                labels: ["Pre-training", "Post-training"],
                datasets: [{
                    label: "Confidence",
                    data: chartData.confidence,
                    borderWidth: 1
                }]
            },
            options: chartOptions
        });
    }

    if (presenceChart) {
        new Chart(presenceChart, {
            type: "bar",
            data: {
                labels: ["Pre-training", "Post-training"],
                datasets: [{
                    label: "Online Presence",
                    data: chartData.presence,
                    borderWidth: 1
                }]
            },
            options: chartOptions
        });
    }

    if (platformChart) {
        new Chart(platformChart, {
            type: "doughnut",
            data: {
                labels: chartData.platform_labels,
                datasets: [{
                    data: chartData.platform_values,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: "bottom"
                    }
                }
            }
        });
    }
});
