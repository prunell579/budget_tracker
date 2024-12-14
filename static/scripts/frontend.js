
let myChart=null;

function createBarChart(categories, spentAmounts, budgetedAmounts) {
    const ctx = document.getElementById('myChart').getContext('2d');

    // If a chart already exists, destroy it before creating a new one
    if (myChart !== null) {
        myChart.destroy();
    }

    myChart = new Chart(ctx, {
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

function updateCategory(selectElement) {
    const operationId = selectElement.getAttribute('data-operation-id');
    const newCategory = selectElement.value;


    // Send the updated category to the backend
    fetch('/update-category', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            operation_id: operationId,
            new_category: newCategory
        })
    })
    .then(response => {
        if (!response.ok) {
            alert('Failed to update category.');
        } else {
            response.json().then(data => {
                console.log('Update successful:', data);
                refreshChart()
                // Optionally update the chart here
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function refreshChart() {
    console.log('refreshing chart')
    fetch('/get-chart-data')
        .then(response => response.json())
        .then(data => {
            myChart.data.datasets[0].data = data.amounts; // Update chart data
            myChart.update(); // Redraw the chart
        });
}
