from django.core.management.base import BaseCommand
from demo_app.models import Book, Book_Shelf, Compartment, Book_Type
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Import dữ liệu sách mẫu vào database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=100,
            help='Số lượng sách muốn tạo (mặc định: 100)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Kiểm tra dữ liệu cần thiết đã có chưa
        if not Book_Shelf.objects.exists():
            self.stdout.write(self.style.ERROR('Lỗi: Chưa có dữ liệu kệ sách!'))
            self.stdout.write(self.style.WARNING('Vui lòng chạy: python manage.py import_shelves'))
            return
        
        if not Book_Type.objects.exists():
            self.stdout.write(self.style.ERROR('Lỗi: Chưa có dữ liệu loại sách!'))
            self.stdout.write(self.style.WARNING('Vui lòng chạy: python manage.py import_book_types'))
            return

        # Dữ liệu mẫu cho sách
        sample_books = {
            'Khoa học máy tính': [
                ('Trí tuệ nhân tạo hiện đại', 'Stuart Russell'),
                ('Học sâu', 'Ian Goodfellow'),
                ('Cấu trúc dữ liệu và giải thuật', 'Thomas Cormen'),
                ('Hệ điều hành', 'Abraham Silberschatz'),
                ('Mạng máy tính', 'Andrew Tanenbaum'),
            ],
            'Lập trình': [
                ('Python cho người mới bắt đầu', 'Mark Lutz'),
                ('Clean Code', 'Robert Martin'),
                ('Design Patterns', 'Gang of Four'),
                ('JavaScript: The Good Parts', 'Douglas Crockford'),
                ('Effective Java', 'Joshua Bloch'),
            ],
            'Toán học': [
                ('Giải tích 1', 'Nguyễn Đình Trí'),
                ('Đại số tuyến tính', 'Gilbert Strang'),
                ('Xác suất thống kê', 'Hoàng Trọng'),
                ('Toán rời rạc', 'Kenneth Rosen'),
                ('Giải tích số', 'Richard Burden'),
            ],
            'Văn học': [
                ('Số đỏ', 'Vũ Trọng Phụng'),
                ('Tôi thấy hoa vàng trên cỏ xanh', 'Nguyễn Nhật Ánh'),
                ('Nhà giả kim', 'Paulo Coelho'),
                ('Đắc nhân tâm', 'Dale Carnegie'),
                ('Sapiens', 'Yuval Noah Harari'),
            ],
            'Kinh tế': [
                ('Kinh tế học vi mô', 'Gregory Mankiw'),
                ('Tư bản luận', 'Karl Marx'),
                ('Freakonomics', 'Steven Levitt'),
                ('Thinking Fast and Slow', 'Daniel Kahneman'),
                ('The Wealth of Nations', 'Adam Smith'),
            ],
        }

        self.stdout.write(self.style.SUCCESS(f'Bắt đầu tạo {count} sách mẫu...'))
        
        created_count = 0
        skipped_count = 0
        
        # Lấy danh sách tất cả kệ, ô và loại sách
        shelves = list(Book_Shelf.objects.all())
        compartments = list(Compartment.objects.all())
        book_types = list(Book_Type.objects.all())

        if not compartments:
            self.stdout.write(self.style.ERROR('Lỗi: Không có ô nào trong kệ!'))
            return

        # Tạo sách
        for i in range(count):
            # Chọn ngẫu nhiên loại sách
            book_type = random.choice(book_types)
            
            # Lấy sách mẫu từ loại đó (nếu có)
            if book_type.name in sample_books:
                book_name, author = random.choice(sample_books[book_type.name])
            else:
                book_name = f'Sách về {book_type.name} - Tập {i+1}'
                author = f'Tác giả {random.randint(1, 100)}'
            
            # Chọn ngẫu nhiên kệ và ô
            shelf = random.choice(shelves)
            compartment = random.choice(shelf.compartments.all())
            
            # Tạo ngày xuất bản ngẫu nhiên (trong 10 năm qua)
            days_ago = random.randint(0, 3650)
            published_date = datetime.now().date() - timedelta(days=days_ago)
            
            # Kiểm tra xem sách đã tồn tại chưa
            if Book.objects.filter(name=book_name, author=author, shelf=shelf).exists():
                skipped_count += 1
                continue
            
            # Tạo sách
            book = Book.objects.create(
                shelf=shelf,
                compartment=compartment,
                book_type=book_type,
                name=book_name,
                author=author,
                description=f'Sách thuộc thể loại {book_type.name}. {book_type.description}',
                published_date=published_date
            )
            
            created_count += 1
            
            if created_count % 10 == 0:
                self.stdout.write(self.style.SUCCESS(f'  → Đã tạo {created_count} sách...'))

        self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
        self.stdout.write(self.style.SUCCESS(f'Hoàn thành!'))
        self.stdout.write(self.style.SUCCESS(f'  • Đã tạo mới: {created_count} sách'))
        self.stdout.write(self.style.SUCCESS(f'  • Đã bỏ qua: {skipped_count} sách (trùng lặp)'))
        self.stdout.write(self.style.SUCCESS(f'  • Tổng số sách: {Book.objects.count()}'))
        
        # Thống kê theo kệ
        self.stdout.write(self.style.SUCCESS(f'\nThống kê theo kệ (5 kệ đầu):'))
        for shelf in shelves[:5]:
            book_count = shelf.books.count()
            self.stdout.write(self.style.SUCCESS(f'  • {shelf.name}: {book_count} sách'))
        
        self.stdout.write(self.style.SUCCESS(f'{"="*60}\n'))
