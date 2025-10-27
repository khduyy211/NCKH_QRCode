from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Import tất cả dữ liệu: kệ sách, loại sách, và sách mẫu'

    def add_arguments(self, parser):
        parser.add_argument(
            '--books',
            type=int,
            default=100,
            help='Số lượng sách muốn tạo (mặc định: 100)'
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Xóa toàn bộ dữ liệu cũ trước khi import'
        )

    def handle(self, *args, **options):
        book_count = options['books']
        reset = options['reset']
        
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS('  IMPORT TOÀN BỘ DỮ LIỆU THƯ VIỆN'))
        self.stdout.write(self.style.SUCCESS('='*70))
        
        # Reset dữ liệu nếu được yêu cầu
        if reset:
            self.stdout.write(self.style.WARNING('\n⚠️  CẢNH BÁO: Đang xóa toàn bộ dữ liệu cũ...'))
            from demo_app.models import Book, Book_Type, Compartment, Book_Shelf
            
            Book.objects.all().delete()
            self.stdout.write(self.style.WARNING('  → Đã xóa tất cả sách'))
            
            Book_Type.objects.all().delete()
            self.stdout.write(self.style.WARNING('  → Đã xóa tất cả loại sách'))
            
            Compartment.objects.all().delete()
            self.stdout.write(self.style.WARNING('  → Đã xóa tất cả ô'))
            
            Book_Shelf.objects.all().delete()
            self.stdout.write(self.style.WARNING('  → Đã xóa tất cả kệ'))
            
            self.stdout.write(self.style.SUCCESS('✓ Đã reset database\n'))
        
        # Bước 1: Import kệ sách
        self.stdout.write(self.style.SUCCESS('\n📚 BƯỚC 1: Import kệ sách và các ô...'))
        self.stdout.write(self.style.SUCCESS('-'*70))
        call_command('import_shelves')
        
        # Bước 2: Import loại sách
        self.stdout.write(self.style.SUCCESS('\n📖 BƯỚC 2: Import loại sách...'))
        self.stdout.write(self.style.SUCCESS('-'*70))
        call_command('import_book_types')
        
        # Bước 3: Import sách mẫu
        self.stdout.write(self.style.SUCCESS(f'\n📕 BƯỚC 3: Import {book_count} sách mẫu...'))
        self.stdout.write(self.style.SUCCESS('-'*70))
        call_command('import_books', count=book_count)
        
        # Tổng kết
        from demo_app.models import Book, Book_Type, Compartment, Book_Shelf
        
        self.stdout.write(self.style.SUCCESS('\n'+'='*70))
        self.stdout.write(self.style.SUCCESS('  TỔNG KẾT'))
        self.stdout.write(self.style.SUCCESS('='*70))
        self.stdout.write(self.style.SUCCESS(f'  📚 Tổng số kệ sách: {Book_Shelf.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  📦 Tổng số ô: {Compartment.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  📖 Tổng số loại sách: {Book_Type.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  📕 Tổng số sách: {Book.objects.count()}'))
        
        # Thống kê chi tiết
        self.stdout.write(self.style.SUCCESS(f'\n  THỐNG KÊ CHI TIẾT:'))
        
        # Top 5 kệ có nhiều sách nhất
        self.stdout.write(self.style.SUCCESS(f'\n  Top 5 kệ có nhiều sách:'))
        shelves_with_books = Book_Shelf.objects.all()
        shelf_stats = [(shelf, shelf.books.count()) for shelf in shelves_with_books]
        shelf_stats.sort(key=lambda x: x[1], reverse=True)
        
        for i, (shelf, count) in enumerate(shelf_stats[:5], 1):
            self.stdout.write(self.style.SUCCESS(f'    {i}. {shelf.name} ({shelf.description}): {count} quyển'))
        
        # Top 5 loại sách phổ biến
        self.stdout.write(self.style.SUCCESS(f'\n  Top 5 loại sách phổ biến:'))
        book_types_with_books = Book_Type.objects.all()
        type_stats = [(bt, bt.books.count()) for bt in book_types_with_books]
        type_stats.sort(key=lambda x: x[1], reverse=True)
        
        for i, (book_type, count) in enumerate(type_stats[:5], 1):
            self.stdout.write(self.style.SUCCESS(f'    {i}. {book_type.name}: {count} quyển'))
        
        self.stdout.write(self.style.SUCCESS('\n'+'='*70))
        self.stdout.write(self.style.SUCCESS('  ✓ HOÀN THÀNH! Dữ liệu đã sẵn sàng sử dụng'))
        self.stdout.write(self.style.SUCCESS('='*70 + '\n'))
        
        # Hướng dẫn tiếp theo
        self.stdout.write(self.style.SUCCESS('Bạn có thể:'))
        self.stdout.write(self.style.SUCCESS('  1. Xem dữ liệu: python manage.py shell'))
        self.stdout.write(self.style.SUCCESS('  2. Chạy server: python manage.py runserver'))
        self.stdout.write(self.style.SUCCESS('  3. Vào admin: python manage.py createsuperuser (nếu chưa có)'))
        self.stdout.write(self.style.SUCCESS(''))
