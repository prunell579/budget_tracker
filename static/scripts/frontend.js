
let myChart=null;
let supportedCategories = fetchSupportedCategories();

// Global variables to track the currently displayed month and year
let currentMonth = new Date().getMonth() + 1; // Months are 0-indexed, so +1
let currentYear = new Date().getFullYear();

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    loadOperations(currentYear, currentMonth); // Fetch and display operations

    // Add event listeners to the navigation buttons
    document.getElementById('prevMonth').addEventListener('click', () => {
        changeMonth(-1); // Go to the previous month
    });
    document.getElementById('nextMonth').addEventListener('click', () => {
        changeMonth(1); // Go to the next month
    });
});

// Update the current month and fetch the operations
function changeMonth(delta) {
    currentMonth += delta;

    if (currentMonth < 1) {
        currentMonth = 12;
        currentYear -= 1;
    } else if (currentMonth > 12) {
        currentMonth = 1;
        currentYear += 1;
    }

    loadOperations(currentYear, currentMonth);
    refreshChart(currentYear, currentMonth);
}

// Call the function to fetch categories
async function fetchSupportedCategories() {
    try {
        const response = await fetch('/get-supported-categories');
        if (!response.ok) {
            throw new Error('Failed to fetch supported categories');
        }
        const categories = await response.json();
        return categories;
        // Use the categories as needed in your frontend logic
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}


function loadOperations(year, month) {
    fetch(`/get-operations?year=${year}&month=${month}`)
        .then(response => response.json())
        .then(async data => {
            const operations = data.operations;
            const tbody = document.querySelector('#operations-table tbody');
            tbody.innerHTML = ''; // Clear existing rows

            for (const operation_item of Object.entries(operations)) {
                const row = document.createElement('tr');

                // this is ugly and i dont know why data has this shape
                const operation = operation_item[1];
    
                // Date column
                const dateCell = document.createElement('td');
                dateCell.innerText = operation.date;
                row.appendChild(dateCell);

                // Amount column
                const amountCell = document.createElement('td');
                amountCell.innerText = parseFloat(operation.amount).toFixed(2);
                row.appendChild(amountCell);

                // Description column
                const descCell = document.createElement('td');
                descCell.innerText = operation.description;
                row.appendChild(descCell);

                // Account label column
                const accountCell = document.createElement('td');
                accountCell.innerText = operation.account_label;
                row.appendChild(accountCell);

                // Category dropdown column
                const categoryCell = document.createElement('td');
                const select = document.createElement('select');
                select.className = 'category-select';
                select.setAttribute('data-operation-id', operation.id);
                select.onchange = () => updateCategory(select); // Attach event handler

                const resolved_supported_categories = await supportedCategories;
                for (const [key, cat_string] of Object.entries(resolved_supported_categories)) {
                    const option = document.createElement('option');
                    option.value = cat_string;
                    option.innerText = cat_string;
                    if (cat_string === operation.category) {
                        option.selected = true;
                    }
                    select.appendChild(option);
                };

                categoryCell.appendChild(select);
                row.appendChild(categoryCell);

                // Add the row to the table body
                tbody.appendChild(row);
            }
        })
        .catch(error => {
            console.error('Error loading operations:', error);
            alert('Failed to load operations.');
        });
}


function createBarChart(spentAmounts, budgetedAmounts) {
    const ctx = document.getElementById('myChart').getContext('2d');

    categories = Object.keys(spentAmounts)

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
                refreshChart(currentYear, currentMonth)
                // Optionally update the chart here
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function refreshChart(year, month) {
    console.log('refreshing chart')
    fetch(`/get-chart-data?year=${year}&month=${month}`)
        .then(response => response.json())
        .then(data => {
            myChart.data.datasets[0].data = data.amounts; // Update chart data
            myChart.update(); // Redraw the chart
        });
}
