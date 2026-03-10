const ctxStatus = document.getElementById('statusChart').getContext('2d');
const statusChart = new Chart(ctxStatus, {
    type: 'pie',
    data: {
        labels: ['Completed', 'In Progress', 'Pending'],
        datasets: [{
            label: 'Task Status',
            data: [18, 3, 4],
            backgroundColor: ['#10B981', '#F59E0B', '#EF4444']
        }]
    }
});

const ctxEmployee = document.getElementById('employeeChart').getContext('2d');
const employeeChart = new Chart(ctxEmployee, {
    type: 'bar',
    data: {
        labels: ['Paul', 'James', 'Mary'],
        datasets: [{
            label: 'Tasks Completed',
            data: [10, 8, 7],
            backgroundColor: '#3B82F6'
        }]
    },
    options:{
        scales:{
            y:{beginAtZero:true}
        }
    }
});