// ====== ADMIN.JS ======
// Biểu đồ thống kê mượn sách theo tháng
const borrowCtx = document.getElementById("borrowChart").getContext("2d");
new Chart(borrowCtx, {
    type: "line",
    data: {
        labels: ["Th1", "Th2", "Th3", "Th4", "Th5", "Th6", "Th7", "Th8", "Th9", "Th10"],
        datasets: [{
            label: "Lượt mượn",
            data: [150, 200, 180, 250, 300, 270, 320, 310, 290, 330],
            borderColor: "#007bff",
            tension: 0.3,
            fill: true,
            backgroundColor: "rgba(0,123,255,0.1)"
        }]
    },
    options: {
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true } }
    }
});

// Biểu đồ thể loại sách
const categoryCtx = document.getElementById("categoryChart").getContext("2d");
new Chart(categoryCtx, {
    type: "doughnut",
    data: {
        labels: ["Công nghệ", "Kinh tế", "Khoa học", "Văn học"],
        datasets: [{
            data: [35, 25, 20, 20],
            backgroundColor: ["#0d6efd", "#198754", "#ffc107", "#dc3545"],
            hoverOffset: 10
        }]
    },
    options: {
        plugins: {
            legend: { position: "bottom" }
        }
    }
});
