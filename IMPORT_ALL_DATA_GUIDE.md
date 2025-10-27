# 📚 Hướng dẫn Import Dữ liệu Thư viện

## 🎯 Tổng quan

Dự án có **4 lệnh management commands** để import dữ liệu:

| Lệnh | Chức năng | Số lượng |
|------|-----------|----------|
| `import_shelves` | Import kệ sách và các ô | 32 kệ, ~960 ô |
| `import_book_types` | Import loại sách | 32 loại |
| `import_books` | Import sách mẫu | Tùy chỉnh (mặc định: 100) |
| `import_all` | Import tất cả một lượt | Tất cả |

---

## 🚀 Cách sử dụng nhanh

### Phương án 1: Import tất cả cùng lúc (Khuyến nghị)

```bash
# Import với 200 sách mẫu
python manage.py import_all --books 200

# Hoặc reset và import lại từ đầu
python manage.py import_all --books 200 --reset
```

### Phương án 2: Import từng bước

```bash
# Bước 1: Import kệ sách
python manage.py import_shelves

# Bước 2: Import loại sách
python manage.py import_book_types

# Bước 3: Import sách (số lượng tùy chỉnh)
python manage.py import_books --count 200
```

---

## 📋 Chi tiết các lệnh

### 1. `import_shelves`
Import 32 kệ sách từ shelfData (JavaScript)

**Dữ liệu import:**
- **Book_Shelf**: 32 kệ (A1-M1 đến H2-M2)
- **Compartment**: ~960 ô (mỗi kệ 5x6 hoặc 6x5)

**Ví dụ:**
```bash
python manage.py import_shelves
```

**Kết quả:**
```
✓ Đã tạo kệ: A1-M1 - Khoa học máy tính
  → Đã tạo 30 ô cho kệ A1-M1
✓ Đã tạo kệ: A1-M2 - Lập trình
  → Đã tạo 30 ô cho kệ A1-M2
...
```

---

### 2. `import_book_types`
Import 32 loại sách

**Danh sách loại:**
- Khoa học máy tính, Lập trình, Toán học, Vật lý
- Văn học, Lịch sử, Địa lý, Sinh học, Hóa học
- Kinh tế, Triết học, Tâm lý học
- Nghệ thuật, Âm nhạc, Thể thao, Du lịch
- Ngoại ngữ, Từ điển, Y học, Dược học
- Nông nghiệp, Công nghệ, Kỹ thuật, Kiến trúc
- Marketing, Quản trị, Luật pháp, Chính trị
- Xã hội học, Nhân học, Giáo dục, Truyền thông

**Ví dụ:**
```bash
python manage.py import_book_types
```

---

### 3. `import_books`
Import sách mẫu với số lượng tùy chỉnh

**Tham số:**
- `--count`: Số lượng sách (mặc định: 100)

**Ví dụ:**
```bash
# Import 100 sách
python manage.py import_books

# Import 500 sách
python manage.py import_books --count 500
```

**Dữ liệu sách:**
- Tên sách và tác giả được chọn từ danh sách mẫu
- Phân bổ ngẫu nhiên vào các kệ và ô
- Ngày xuất bản ngẫu nhiên (trong 10 năm qua)
- Mỗi sách có: name, author, description, published_date

**Sách mẫu bao gồm:**
- *Khoa học máy tính*: "Trí tuệ nhân tạo hiện đại", "Học sâu", "Cấu trúc dữ liệu"...
- *Lập trình*: "Python cho người mới", "Clean Code", "Design Patterns"...
- *Toán học*: "Giải tích 1", "Đại số tuyến tính", "Xác suất thống kê"...
- *Văn học*: "Số đỏ", "Tôi thấy hoa vàng", "Nhà giả kim", "Đắc nhân tâm"...
- *Kinh tế*: "Kinh tế học vi mô", "Tư bản luận", "Freakonomics"...

---

### 4. `import_all` (Lệnh tổng hợp)
Import tất cả dữ liệu một lượt

**Tham số:**
- `--books`: Số lượng sách (mặc định: 100)
- `--reset`: Xóa toàn bộ dữ liệu cũ trước khi import

**Ví dụ:**
```bash
# Import lần đầu
python manage.py import_all --books 200

# Reset và import lại
python manage.py import_all --books 300 --reset
```

**Quy trình:**
1. Xóa dữ liệu cũ (nếu có --reset)
2. Import kệ sách và ô
3. Import loại sách
4. Import sách mẫu
5. Hiển thị thống kê tổng hợp

---

## 📊 Thống kê sau khi import

```bash
python manage.py import_all --books 200
```

**Kết quả:**
```
============================================================
  TỔNG KẾT
============================================================
  📚 Tổng số kệ sách: 32
  📦 Tổng số ô: 960
  📖 Tổng số loại sách: 32
  📕 Tổng số sách: 200

  THỐNG KÊ CHI TIẾT:

  Top 5 kệ có nhiều sách:
    1. A1-M1 (Khoa học máy tính): 15 quyển
    2. B1-M1 (Văn học): 12 quyển
    3. C1-M2 (Kinh tế): 10 quyển
    ...

  Top 5 loại sách phổ biến:
    1. Khoa học máy tính: 18 quyển
    2. Lập trình: 15 quyển
    3. Văn học: 13 quyển
    ...
============================================================
```

---

## 🔍 Kiểm tra dữ liệu

### Sử dụng Django Shell

```bash
python manage.py shell
```

```python
from demo_app.models import Book_Shelf, Compartment, Book_Type, Book

# 1. Xem tất cả kệ
Book_Shelf.objects.all()

# 2. Xem chi tiết kệ A1-M1
shelf = Book_Shelf.objects.get(name='A1-M1')
print(f"Kệ: {shelf.name}")
print(f"Mô tả: {shelf.description}")
print(f"Số ô: {shelf.compartments.count()}")
print(f"Số sách: {shelf.books.count()}")

# 3. Xem các ô trong kệ
for comp in shelf.compartments.all()[:5]:
    print(f"  Ô {comp.name}: Hàng {comp.row_number}, Cột {comp.column_number}")
    print(f"    → Số sách: {comp.books.count()}")

# 4. Xem tất cả loại sách
for bt in Book_Type.objects.all():
    print(f"{bt.name}: {bt.books.count()} quyển")

# 5. Xem sách trong kệ A1-M1
books = Book.objects.filter(shelf__name='A1-M1')
for book in books:
    print(f"  - {book.name} by {book.author}")

# 6. Tìm sách theo loại
python_books = Book.objects.filter(book_type__name='Lập trình')
print(f"Có {python_books.count()} sách về Lập trình")

# 7. Tìm sách theo tác giả
books = Book.objects.filter(author__icontains='Nguyễn')
print(f"Có {books.count()} sách của tác giả có tên Nguyễn")
```

---

## 🗑️ Reset dữ liệu

### Cách 1: Sử dụng --reset flag
```bash
python manage.py import_all --books 200 --reset
```

### Cách 2: Xóa thủ công trong shell
```bash
python manage.py shell
```

```python
from demo_app.models import Book, Book_Type, Compartment, Book_Shelf

# Xóa từng bảng (theo thứ tự phụ thuộc)
Book.objects.all().delete()
Book_Type.objects.all().delete()
Compartment.objects.all().delete()
Book_Shelf.objects.all().delete()

print("Đã xóa toàn bộ dữ liệu!")
```

---

## 🎨 Tích hợp với Django Admin

### 1. Đăng ký models trong admin.py

```python
from django.contrib import admin
from .models import Book_Shelf, Compartment, Book_Type, Book

@admin.register(Book_Shelf)
class BookShelfAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'compartment_count', 'book_count')
    search_fields = ('name', 'description')
    
    def compartment_count(self, obj):
        return obj.compartments.count()
    compartment_count.short_description = 'Số ô'
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Số sách'

@admin.register(Compartment)
class CompartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'shelf', 'row_number', 'column_number', 'book_count')
    list_filter = ('shelf',)
    search_fields = ('name', 'shelf__name')
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Số sách'

@admin.register(Book_Type)
class BookTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'book_count')
    search_fields = ('name',)
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Số sách'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'book_type', 'shelf', 'compartment', 'published_date')
    list_filter = ('book_type', 'shelf', 'published_date')
    search_fields = ('name', 'author', 'description')
    date_hierarchy = 'published_date'
```

### 2. Tạo superuser và truy cập admin

```bash
# Tạo superuser (nếu chưa có)
python manage.py createsuperuser

# Chạy server
python manage.py runserver

# Truy cập: http://127.0.0.1:8000/admin/
```

---

## 🐛 Troubleshooting

### Lỗi: "No such table"
```bash
python manage.py makemigrations
python manage.py migrate
```

### Lỗi: "Chưa có dữ liệu kệ sách"
```bash
# Phải import theo thứ tự
python manage.py import_shelves
python manage.py import_book_types
python manage.py import_books
```

### Lỗi: "Unknown command"
- Kiểm tra file `__init__.py` trong thư mục `management/` và `commands/`
- Restart terminal hoặc Django server

---

## ✅ Checklist

- [ ] Đã chạy migrations
- [ ] Đã import kệ sách (`import_shelves`)
- [ ] Đã import loại sách (`import_book_types`)
- [ ] Đã import sách mẫu (`import_books`)
- [ ] Đã kiểm tra dữ liệu trong shell hoặc admin
- [ ] Đã tạo superuser để truy cập admin

---

## 📝 Ghi chú

- Tất cả các lệnh đều sử dụng `update_or_create()` nên an toàn khi chạy nhiều lần
- Dữ liệu sách được tạo ngẫu nhiên nên mỗi lần chạy sẽ khác nhau
- Có thể tùy chỉnh số lượng sách bằng tham số `--count`
- Sử dụng `--reset` để xóa và import lại từ đầu
