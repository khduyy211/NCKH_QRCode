// ====== SCRIPT.JS ======

// ====== XỬ LÝ MA TRẬN KỆ SÁCH ======

// Cache để lưu dữ liệu kệ đã load (tránh gọi API nhiều lần)
const shelfDataCache = {};

// Hàm lấy trạng thái dựa trên số lượng sách
function getStatusFromCount(count) {
  if (count === 0) return 'disabled';  // Không có sách
  if (count < 10) return 'empty';      // Còn ít sách
  if (count < 20) return 'warning';    // Sắp đầy
  return 'full';                       // Đầy
}

// Hàm tạo ma trận kệ sách (sử dụng dữ liệu từ API)
function createShelfMatrix(shelfId) {
  // Hiển thị loading
  const matrixContainer = document.getElementById('shelfMatrix');
  const modalTitle = document.getElementById('shelfMatrixModalLabel');
  
  matrixContainer.innerHTML = '<div class="text-center p-5"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Đang tải...</span></div><p class="mt-3">Đang tải dữ liệu kệ sách...</p></div>';
  modalTitle.innerHTML = `<i class="bi bi-grid-3x3"></i> Đang tải...`;
  
  // Kiểm tra cache trước
  if (shelfDataCache[shelfId]) {
    renderShelfMatrix(shelfDataCache[shelfId]);
    return;
  }
  
  // Gọi API để lấy dữ liệu thực
  fetch(`/api/shelf/${shelfId}/`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      // Lưu vào cache
      shelfDataCache[shelfId] = data;
      
      // Render ma trận
      renderShelfMatrix(data);
    })
    .catch(error => {
      console.error('Error loading shelf data:', error);
      matrixContainer.innerHTML = `
        <div class="alert alert-danger m-3">
          <h5>Lỗi khi tải dữ liệu</h5>
          <p>${error.message}</p>
          <p>Vui lòng thử lại sau hoặc kiểm tra kết nối mạng.</p>
        </div>
      `;
      modalTitle.innerHTML = `<i class="bi bi-exclamation-triangle"></i> Lỗi`;
    });
}

// Hàm render ma trận từ dữ liệu API
function renderShelfMatrix(data) {
  const matrixContainer = document.getElementById('shelfMatrix');
  const matrixShelfId = document.getElementById('matrixShelfId');
  const matrixRows = document.getElementById('matrixRows');
  const matrixCols = document.getElementById('matrixCols');
  const modalTitle = document.getElementById('shelfMatrixModalLabel');

  // Cập nhật thông tin kệ
  matrixShelfId.textContent = data.name;
  matrixRows.textContent = data.rows;
  matrixCols.textContent = data.cols;
  modalTitle.innerHTML = `<i class="bi bi-grid-3x3"></i> ${data.name} - ${data.description}`;

  // Xóa nội dung cũ
  matrixContainer.innerHTML = '';
  
  // Thiết lập grid
  matrixContainer.style.gridTemplateColumns = `repeat(${data.cols}, 1fr)`;
  matrixContainer.style.gridTemplateRows = `repeat(${data.rows}, 1fr)`;

  // Tạo các ô ma trận từ dữ liệu thực
  data.compartments.forEach(comp => {
    const cell = document.createElement('div');
    const status = getStatusFromCount(comp.book_count);
    
    cell.className = `matrix-cell ${status}`;
    cell.innerHTML = `
      <div class="matrix-cell-label">${comp.name}</div>
      <div class="matrix-cell-count">${comp.book_count} quyển</div>
    `;
    
    // Thêm tooltip
    cell.title = `Vị trí ${comp.name}: ${comp.book_count} quyển sách`;
    
    // Xử lý click vào ô để xem chi tiết sách
    cell.addEventListener('click', () => {
      if (status !== 'disabled') {
        showCellDetails(data.name, comp.name, comp.book_count, status);
      }
    });
    
    matrixContainer.appendChild(cell);
  });
}

// Hàm hiển thị chi tiết ô (lấy danh sách sách thật từ API)
function showCellDetails(shelfId, cellId, bookCount, status) {
  const statusText = {
    'empty': 'Còn trống',
    'warning': 'Sắp đầy', 
    'full': 'Đã đầy',
    'disabled': 'Không sử dụng'
  };
  
  // Nếu không có sách, chỉ hiển thị thông báo đơn giản
  if (bookCount === 0) {
    alert(`Vị trí ${cellId} - Kệ ${shelfId}\n\n` +
          `Trạng thái: ${statusText[status]}\n` +
          `Hiện chưa có sách trong ngăn này.`);
    return;
  }
  
  // Gọi API để lấy danh sách sách
  fetch(`/api/shelf/${shelfId}/compartment/${cellId}/`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Received compartment books:', data);
      
      // Tạo nội dung hiển thị
      let bookList = data.books.map((book, index) => 
        `${index + 1}. ${book.name} (Mã: ${book.code})\n   Loại: ${book.book_type__name}`
      ).join('\n\n');
      
      alert(`Chi tiết vị trí ${cellId} - Kệ ${shelfId}\n\n` +
            `Số lượng sách: ${bookCount} quyển\n` +
            `Trạng thái: ${statusText[status]}\n\n` +
            `Danh sách sách:\n${bookList || '(Không có dữ liệu chi tiết)'}`);
    })
    .catch(error => {
      console.error('Error loading compartment books:', error);
      alert(`Lỗi khi tải danh sách sách:\n${error.message}\n\n` +
            `Vị trí ${cellId} - Kệ ${shelfId}\n` +
            `Số lượng sách: ${bookCount} quyển`);
    });
}

// Xử lý click vào kệ sách
function initShelfClickHandlers() {
  const shelves = document.querySelectorAll('.shelf-clickable');
  
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
  
  // Xử lý đóng modal - đảm bảo modal đóng hoàn toàn và quay lại shelf-map
  if (modalElement) {
    // Lắng nghe sự kiện khi modal bị ẩn
    modalElement.addEventListener('hidden.bs.modal', function () {
      // Xóa backdrop nếu còn sót lại
      const backdrop = document.querySelector('.modal-backdrop');
      if (backdrop) {
        backdrop.remove();
      }
      // Bỏ class modal-open khỏi body để đảm bảo có thể scroll lại
      document.body.classList.remove('modal-open');
      document.body.style.overflow = '';
      document.body.style.paddingRight = '';
    });
  }
}

// Khởi tạo khi DOM đã sẵn sàng
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initShelfClickHandlers);
} else {
  initShelfClickHandlers();
}