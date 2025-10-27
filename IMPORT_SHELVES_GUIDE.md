# Hướng dẫn Import Dữ liệu Kệ Sách

## 📋 Tổng quan
Script này sẽ import dữ liệu từ `shelfData` (JavaScript) vào database Django.

## 🚀 Cách sử dụng

### Bước 1: Tạo migrations (nếu chưa có)
```bash
python manage.py makemigrations
python manage.py migrate
```

### Bước 2: Chạy lệnh import
```bash
python manage.py import_shelves
```

### Bước 3: Kiểm tra kết quả
```bash
python manage.py shell
```

Trong shell:
```python
from demo_app.models import Book_Shelf, Compartment

# Xem tất cả kệ
shelves = Book_Shelf.objects.all()
for shelf in shelves:
    print(f"{shelf.name} - {shelf.description} ({shelf.location})")

# Xem chi tiết 1 kệ
shelf = Book_Shelf.objects.get(name='A1-M1')
print(f"Kệ: {shelf.name}")
print(f"Mô tả: {shelf.description}")
print(f"Số ô: {shelf.compartments.count()}")

# Xem các ô trong kệ
for comp in shelf.compartments.all()[:5]:  # Chỉ xem 5 ô đầu
    print(f"  - Ô {comp.name}: Hàng {comp.row_number}, Cột {comp.column_number}")
```

## 📊 Dữ liệu sẽ được import

### Book_Shelf (32 kệ)
| Mã kệ | Description | Location | Số hàng x cột |
|-------|-------------|----------|---------------|
| A1-M1 | Khoa học máy tính | Tầng 1, Cột trái | 5 x 6 (30 ô) |
| A1-M2 | Lập trình | Tầng 1, Cột trái | 5 x 6 (30 ô) |
| A2-M1 | Toán học | Tầng 1, Cột trái | 6 x 5 (30 ô) |
| ... | ... | ... | ... |

### Compartment (ô trong kệ)
Mỗi kệ sẽ có nhiều ô, ví dụ kệ A1-M1 (5x6) sẽ có:
- A1, A2, A3, A4, A5, A6 (hàng 1)
- B1, B2, B3, B4, B5, B6 (hàng 2)
- C1, C2, C3, C4, C5, C6 (hàng 3)
- D1, D2, D3, D4, D5, D6 (hàng 4)
- E1, E2, E3, E4, E5, E6 (hàng 5)

**Tổng cộng**: 32 kệ x ~30 ô/kệ = ~960 ô

## 🔄 Update lại dữ liệu

Nếu bạn muốn update lại:
```bash
# Lệnh sẽ tự động update nếu kệ đã tồn tại
python manage.py import_shelves
```

## 🗑️ Xóa dữ liệu cũ (nếu muốn reset)

```bash
python manage.py shell
```

```python
from demo_app.models import Book_Shelf, Compartment

# Xóa tất cả (cẩn thận!)
Compartment.objects.all().delete()
Book_Shelf.objects.all().delete()
```

Sau đó chạy lại:
```bash
python manage.py import_shelves
```

## 🎯 Ví dụ sử dụng trong View

### views.py
```python
from django.shortcuts import render
from django.http import JsonResponse
from demo_app.models import Book_Shelf, Compartment

def get_shelf_data(request, shelf_name):
    """API trả về dữ liệu kệ cho JavaScript"""
    try:
        shelf = Book_Shelf.objects.get(name=shelf_name)
        compartments = shelf.compartments.all()
        
        data = {
            'name': shelf.name,
            'description': shelf.description,
            'location': shelf.location,
            'rows': compartments.values('row_number').distinct().count(),
            'cols': compartments.values('column_number').distinct().count(),
            'compartments': [
                {
                    'name': c.name,
                    'row': c.row_number,
                    'col': c.column_number,
                    'book_count': c.books.count()
                }
                for c in compartments
            ]
        }
        
        return JsonResponse(data)
    except Book_Shelf.DoesNotExist:
        return JsonResponse({'error': 'Shelf not found'}, status=404)

def bookshelf(request):
    """Trang hiển thị sơ đồ kệ"""
    shelves = Book_Shelf.objects.all().order_by('name')
    context = {
        'shelves': shelves,
        'total_shelves': shelves.count()
    }
    return render(request, 'bookshelf.html', context)
```

### urls.py
```python
from django.urls import path
from demo_app import views

urlpatterns = [
    path('shelf-map/', views.bookshelf, name='shelf-map'),
    path('api/shelf/<str:shelf_name>/', views.get_shelf_data, name='get-shelf-data'),
]
```

### JavaScript cập nhật
```javascript
// Thay vì dùng shelfData hardcode, gọi API
function createShelfMatrix(shelfId) {
  // Gọi API Django
  fetch(`/api/shelf/${shelfId}/`)
    .then(response => response.json())
    .then(data => {
      console.log('Dữ liệu từ database:', data);
      
      // Cập nhật modal
      document.getElementById('matrixShelfId').textContent = data.name;
      document.getElementById('matrixRows').textContent = data.rows;
      document.getElementById('matrixCols').textContent = data.cols;
      
      // Render ma trận
      const matrixContainer = document.getElementById('shelfMatrix');
      matrixContainer.innerHTML = '';
      matrixContainer.style.gridTemplateColumns = `repeat(${data.cols}, 1fr)`;
      
      // Tạo các ô từ dữ liệu thực
      data.compartments.forEach(comp => {
        const cell = document.createElement('div');
        cell.className = `matrix-cell ${getStatusFromCount(comp.book_count)}`;
        cell.innerHTML = `
          <div class="matrix-cell-label">${comp.name}</div>
          <div class="matrix-cell-count">${comp.book_count} quyển</div>
        `;
        matrixContainer.appendChild(cell);
      });
      
      // Hiển thị modal
      const modal = new bootstrap.Modal(document.getElementById('shelfMatrixModal'));
      modal.show();
    })
    .catch(error => {
      console.error('Lỗi khi lấy dữ liệu:', error);
      alert('Không thể tải dữ liệu kệ sách!');
    });
}

function getStatusFromCount(count) {
  if (count === 0) return 'disabled';
  if (count < 30) return 'empty';
  if (count < 70) return 'warning';
  return 'full';
}
```

## ✅ Checklist

- [ ] Đã chạy migrations
- [ ] Đã chạy `python manage.py import_shelves`
- [ ] Kiểm tra dữ liệu trong Django admin hoặc shell
- [ ] Cập nhật views.py để tạo API endpoint
- [ ] Cập nhật urls.py để map URL
- [ ] Cập nhật JavaScript để gọi API thay vì dùng hardcode data

## 🐛 Troubleshooting

### Lỗi: "No such table: demo_app_book_shelf"
```bash
python manage.py migrate
```

### Lỗi: "No module named 'demo_app.management'"
- Đảm bảo có file `__init__.py` trong thư mục `management/` và `management/commands/`

### Lỗi: "Unknown command: 'import_shelves'"
- Restart server Django
- Kiểm tra tên app trong INSTALLED_APPS

## 📝 Ghi chú

- Script sử dụng `update_or_create()` nên an toàn khi chạy nhiều lần
- Compartments chỉ được tạo khi kệ được tạo mới (không duplicate)
- Có thể mở rộng để import thêm Book_Type và Book sau này
