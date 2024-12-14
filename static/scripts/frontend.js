
function createBarChart(categories, spentAmounts, budgetedAmounts) {
    const ctx = document.getElementById('myChart').getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'bar', // Bar chart type
        data: {
            labels: categories, // Categories on the X-axis
            datasets: [
                {
                    label: 'Amount Spent',
                    data: spentAmounts, // Amounts spent on the Y-axis
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Budgeted Amount',
                    data: budgetedAmounts, // Budgeted amounts on the Y-axis
                    backgroundColor: 'rgba(255, 159, 64, 0.2)',
                    borderColor: 'rgba(255, 159, 64, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: false, // Disable automatic resizing
            maintainAspectRatio: false, // Allow the chart to stretch
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                legend: {
                    position: 'top'
                }
            }
        }
    });
}
