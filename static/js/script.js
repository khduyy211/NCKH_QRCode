// ====== SCRIPT.JS ======

// ====== XỬ LÝ MA TRẬN KỆ SÁCH ======

// Dữ liệu mẫu cho các kệ (có thể thay thế bằng API call sau này)
const shelfData = {
  'A1-M1': { rows: 5, cols: 6, name: 'Kệ A1-M1 - Khoa học máy tính' },
  'A1-M2': { rows: 5, cols: 6, name: 'Kệ A1-M2 - Lập trình' },
  'A2-M1': { rows: 6, cols: 5, name: 'Kệ A2-M1 - Toán học' },
  'A2-M2': { rows: 6, cols: 5, name: 'Kệ A2-M2 - Vật lý' },
  'B1-M1': { rows: 5, cols: 6, name: 'Kệ B1-M1 - Văn học' },
  'B1-M2': { rows: 5, cols: 6, name: 'Kệ B1-M2 - Lịch sử' },
  'B2-M1': { rows: 6, cols: 5, name: 'Kệ B2-M1 - Địa lý' },
  'B2-M2': { rows: 6, cols: 5, name: 'Kệ B2-M2 - Sinh học' },
  'C1-M1': { rows: 5, cols: 6, name: 'Kệ C1-M1 - Hóa học' },
  'C1-M2': { rows: 5, cols: 6, name: 'Kệ C1-M2 - Kinh tế' },
  'C2-M1': { rows: 6, cols: 5, name: 'Kệ C2-M1 - Triết học' },
  'C2-M2': { rows: 6, cols: 5, name: 'Kệ C2-M2 - Tâm lý học' },
  'D1-M1': { rows: 5, cols: 6, name: 'Kệ D1-M1 - Nghệ thuật' },
  'D1-M2': { rows: 5, cols: 6, name: 'Kệ D1-M2 - Âm nhạc' },
  'D2-M1': { rows: 6, cols: 5, name: 'Kệ D2-M1 - Thể thao' },
  'D2-M2': { rows: 6, cols: 5, name: 'Kệ D2-M2 - Du lịch' },
  'E1-M1': { rows: 5, cols: 6, name: 'Kệ E1-M1 - Ngoại ngữ' },
  'E1-M2': { rows: 5, cols: 6, name: 'Kệ E1-M2 - Từ điển' },
  'E2-M1': { rows: 6, cols: 5, name: 'Kệ E2-M1 - Y học' },
  'E2-M2': { rows: 6, cols: 5, name: 'Kệ E2-M2 - Dược học' },
  'F1-M1': { rows: 5, cols: 6, name: 'Kệ F1-M1 - Nông nghiệp' },
  'F1-M2': { rows: 5, cols: 6, name: 'Kệ F1-M2 - Công nghệ' },
  'F2-M1': { rows: 6, cols: 5, name: 'Kệ F2-M1 - Kỹ thuật' },
  'F2-M2': { rows: 6, cols: 5, name: 'Kệ F2-M2 - Kiến trúc' },
  'G1-M1': { rows: 5, cols: 6, name: 'Kệ G1-M1 - Marketing' },
  'G1-M2': { rows: 5, cols: 6, name: 'Kệ G1-M2 - Quản trị' },
  'G2-M1': { rows: 6, cols: 5, name: 'Kệ G2-M1 - Luật pháp' },
  'G2-M2': { rows: 6, cols: 5, name: 'Kệ G2-M2 - Chính trị' },
  'H1-M1': { rows: 5, cols: 6, name: 'Kệ H1-M1 - Xã hội học' },
  'H1-M2': { rows: 5, cols: 6, name: 'Kệ H1-M2 - Nhân học' },
  'H2-M1': { rows: 6, cols: 5, name: 'Kệ H2-M1 - Giáo dục' },
  'H2-M2': { rows: 6, cols: 5, name: 'Kệ H2-M2 - Truyền thông' }
};

// Hàm tạo trạng thái ngẫu nhiên cho mỗi ô (để demo)
function getRandomStatus() {
  const rand = Math.random();
  if (rand < 0.4) return 'empty';      // 40% - còn trống
  if (rand < 0.7) return 'warning';    // 30% - sắp đầy
  if (rand < 0.9) return 'full';       // 20% - đã đầy
  return 'disabled';                   // 10% - không sử dụng
}

// Hàm tạo số sách ngẫu nhiên
function getRandomBookCount(status) {
  if (status === 'empty') return Math.floor(Math.random() * 30) + 1;
  if (status === 'warning') return Math.floor(Math.random() * 20) + 60;
  if (status === 'full') return Math.floor(Math.random() * 10) + 90;
  return 0;
}

// Hàm tạo ma trận kệ sách
function createShelfMatrix(shelfId) {
  const shelf = shelfData[shelfId];
  if (!shelf) return;

  const matrixContainer = document.getElementById('shelfMatrix');
  const matrixShelfId = document.getElementById('matrixShelfId');
  const matrixRows = document.getElementById('matrixRows');
  const matrixCols = document.getElementById('matrixCols');
  const modalTitle = document.getElementById('shelfMatrixModalLabel');

  // Cập nhật thông tin
  matrixShelfId.textContent = shelfId;
  matrixRows.textContent = shelf.rows;
  matrixCols.textContent = shelf.cols;
  modalTitle.innerHTML = `<i class="bi bi-grid-3x3"></i> ${shelf.name}`;

  // Xóa ma trận cũ
  matrixContainer.innerHTML = '';
  
  // Thiết lập grid
  matrixContainer.style.gridTemplateColumns = `repeat(${shelf.cols}, 1fr)`;
  matrixContainer.style.gridTemplateRows = `repeat(${shelf.rows}, 1fr)`;

  // Tạo các ô ma trận
  for (let row = 1; row <= shelf.rows; row++) {
    for (let col = 1; col <= shelf.cols; col++) {
      const cell = document.createElement('div');
      const cellId = `${String.fromCharCode(64 + row)}${col}`;
      const status = getRandomStatus();
      const bookCount = getRandomBookCount(status);
      
      cell.className = `matrix-cell ${status}`;
      cell.innerHTML = `
        <div class="matrix-cell-label">${cellId}</div>
        <div class="matrix-cell-count">${bookCount > 0 ? bookCount + ' quyển' : 'Trống'}</div>
      `;
      
      // Thêm tooltip
      cell.title = `Vị trí ${cellId}: ${bookCount} quyển sách`;
      
      // Xử lý click vào ô
      cell.addEventListener('click', () => {
        if (status !== 'disabled') {
          showCellDetails(shelfId, cellId, bookCount, status);
        }
      });
      
      matrixContainer.appendChild(cell);
    }
  }
}

// Hàm hiển thị chi tiết ô
function showCellDetails(shelfId, cellId, bookCount, status) {
  const statusText = {
    'empty': 'Còn trống',
    'warning': 'Sắp đầy', 
    'full': 'Đã đầy',
    'disabled': 'Không sử dụng'
  };
  
  alert(`Chi tiết vị trí ${cellId} - Kệ ${shelfId}\n\n` +
        `Số lượng sách: ${bookCount} quyển\n` +
        `Trạng thái: ${statusText[status]}\n\n` +
        `(Tính năng xem chi tiết sẽ được phát triển thêm)`);
}

// Xử lý click vào kệ sách
function initShelfClickHandlers() {
  console.log('Initializing shelf click handlers...');
  
  const shelves = document.querySelectorAll('.shelf-clickable');
  console.log('Found shelves:', shelves.length);
  
  if (shelves.length === 0) {
    console.warn('No shelves found with class .shelf-clickable');
    return;
  }
  
  const modalElement = document.getElementById('shelfMatrixModal');
  if (!modalElement) {
    console.error('Modal element #shelfMatrixModal not found');
    return;
  }
  
  shelves.forEach(shelf => {
    shelf.addEventListener('click', function(e) {
      e.preventDefault();
      console.log('Shelf clicked:', this.getAttribute('data-shelf-id'));
      
      const shelfId = this.getAttribute('data-shelf-id');
      if (!shelfId) {
        console.error('Shelf ID not found');
        return;
      }
      
      createShelfMatrix(shelfId);
      
      // Khởi tạo và hiển thị modal
      const matrixModal = new bootstrap.Modal(modalElement);
      matrixModal.show();
    });
    
    // Thêm style để cho biết có thể click
    shelf.style.cursor = 'pointer';
  });

  // Xử lý nút xuất báo cáo
  const exportBtn = document.getElementById('exportBtn');
  if (exportBtn) {
    exportBtn.addEventListener('click', function() {
      const shelfId = document.getElementById('matrixShelfId').textContent;
      alert(`Xuất báo cáo cho kệ ${shelfId}\n(Tính năng đang được phát triển)`);
    });
  }
  
  console.log('Shelf click handlers initialized successfully');
}

// Khởi tạo khi DOM đã sẵn sàng
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initShelfClickHandlers);
} else {
  // DOM đã sẵn sàng, chạy luôn
  initShelfClickHandlers();
}

// ====== TÌM KIẾM ======
// (Chức năng tìm kiếm có thể được thêm sau nếu cần)
