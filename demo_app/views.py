from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Book_Shelf, Compartment, Book, Book_Type

# Create your views here.
def index(req):
    return render(req,"index.html")

def bookshelf(req):
    """Trang hiển thị sơ đồ kệ sách với thông tin thực tế từ database"""
    shelves = Book_Shelf.objects.all().order_by('name')
    
    # Tạo dictionary với thông tin chi tiết của từng kệ
    shelves_data = {}
    for shelf in shelves:
        book_count = shelf.books.count()
        compartment_count = shelf.compartments.count()
        
        # Tính phần trăm đầy
        if compartment_count > 0:
            # Giả sử mỗi ô có thể chứa tối đa 30 quyển
            max_capacity = compartment_count * 30
            fill_percentage = (book_count / max_capacity * 100) if max_capacity > 0 else 0
        else:
            fill_percentage = 0
        
        # Xác định trạng thái
        if book_count == 0:
            status = 'empty'
        elif fill_percentage < 30:
            status = 'low'
        elif fill_percentage < 70:
            status = 'medium'
        else:
            status = 'high'
        
        shelves_data[shelf.name] = {
            'name': shelf.name,
            'description': shelf.description,
            'book_count': book_count,
            'compartment_count': compartment_count,
            'fill_percentage': round(fill_percentage, 1),
            'status': status
        }
    
    # Thêm shelves_data vào context dưới dạng JSON để JavaScript có thể sử dụng
    import json
    context = {
        'shelves': shelves,
        'shelves_data': shelves_data,
        'shelves_data_json': json.dumps(shelves_data),
        'total_shelves': shelves.count(),
    }
    return render(req, "bookshelf.html", context=context)

def admin(req):
    dic = {
        "title":"admin-1"
    }
    return render(req,"admin.html",context=dic)

# ===== API ENDPOINTS =====

def api_get_shelf_data(request, shelf_name):
    """
    API trả về dữ liệu chi tiết của 1 kệ sách
    URL: /api/shelf/<shelf_name>/
    Response: JSON với thông tin kệ, các ô và số sách
    """
    try:
        shelf = Book_Shelf.objects.get(name=shelf_name)
        compartments = shelf.compartments.all().order_by('row_number', 'column_number')
        
        # Tính số hàng và cột
        rows = compartments.values('row_number').distinct().count()
        cols = compartments.values('column_number').distinct().count()
        
        # Tạo dữ liệu các ô
        compartments_data = []
        for comp in compartments:
            book_count = comp.books.count()
            compartments_data.append({
                'name': comp.name,
                'row': comp.row_number,
                'col': comp.column_number,
                'book_count': book_count,
                'description': comp.description or ''
            })
        
        data = {
            'name': shelf.name,
            'description': shelf.description or '',
            'rows': rows,
            'cols': cols,
            'total_books': shelf.books.count(),
            'compartments': compartments_data
        }
        
        return JsonResponse(data)
    
    except Book_Shelf.DoesNotExist:
        return JsonResponse({
            'error': 'Shelf not found',
            'message': f'Không tìm thấy kệ sách với mã {shelf_name}'
        }, status=404)

def api_get_all_shelves(request):
    """
    API trả về danh sách tất cả kệ sách
    URL: /api/shelves/
    Response: JSON với danh sách kệ
    """
    shelves = Book_Shelf.objects.all().order_by('name')
    
    shelves_data = []
    for shelf in shelves:
        compartments = shelf.compartments.all()
        rows = compartments.values('row_number').distinct().count()
        cols = compartments.values('column_number').distinct().count()
        
        shelves_data.append({
            'name': shelf.name,
            'description': shelf.description or '',
            'rows': rows,
            'cols': cols,
            'book_count': shelf.books.count(),
            'compartment_count': compartments.count()
        })
    
    return JsonResponse({
        'shelves': shelves_data,
        'total': len(shelves_data)
    })

def api_get_compartment_books(request, shelf_name, compartment_name):
    """
    API trả về danh sách sách trong 1 ô cụ thể
    URL: /api/shelf/<shelf_name>/compartment/<compartment_name>/
    Response: JSON với danh sách sách
    """
    try:
        shelf = Book_Shelf.objects.get(name=shelf_name)
        compartment = Compartment.objects.get(shelf=shelf, name=compartment_name)
        
        books = compartment.books.all()
        books_data = []
        
        for book in books:
            books_data.append({
                'code': book.code,
                'name': book.name,
                'author': book.author,
                'book_type__name': book.book_type.name,
                'description': book.description or '',
                'published_date': book.published_date.strftime('%Y-%m-%d') if book.published_date else None
            })
        
        data = {
            'compartment': compartment.name,
            'shelf': shelf.name,
            'books': books_data,
            'total_books': len(books_data)
        }
        
        return JsonResponse(data)
    
    except (Book_Shelf.DoesNotExist, Compartment.DoesNotExist):
        return JsonResponse({
            'error': 'Not found',
            'message': 'Không tìm thấy kệ hoặc ô'
        }, status=404)