from django.core.management.base import BaseCommand
from demo_app.models import Book_Type

class Command(BaseCommand):
    help = 'Import dữ liệu loại sách (Book Types) vào database'

    def handle(self, *args, **options):
        # Dữ liệu các loại sách dựa trên shelfData
        book_types_data = [
            {'name': 'Khoa học máy tính', 'description': 'Sách về máy tính, công nghệ thông tin, AI, Machine Learning'},
            {'name': 'Lập trình', 'description': 'Sách về các ngôn ngữ lập trình: Python, Java, C++, JavaScript'},
            {'name': 'Toán học', 'description': 'Sách về đại số, giải tích, hình học, thống kê'},
            {'name': 'Vật lý', 'description': 'Sách về cơ học, nhiệt học, điện từ, quang học'},
            {'name': 'Văn học', 'description': 'Tiểu thuyết, thơ ca, truyện ngắn, văn học Việt Nam và thế giới'},
            {'name': 'Lịch sử', 'description': 'Lịch sử Việt Nam, lịch sử thế giới, lịch sử văn minh'},
            {'name': 'Địa lý', 'description': 'Địa lý tự nhiên, địa lý kinh tế, bản đồ'},
            {'name': 'Sinh học', 'description': 'Sinh học tế bào, di truyền học, sinh thái học'},
            {'name': 'Hóa học', 'description': 'Hóa vô cơ, hóa hữu cơ, hóa phân tích'},
            {'name': 'Kinh tế', 'description': 'Kinh tế học, tài chính, ngân hàng, kinh doanh'},
            {'name': 'Triết học', 'description': 'Triết học phương Đông, phương Tây, đạo đức học'},
            {'name': 'Tâm lý học', 'description': 'Tâm lý học hành vi, nhận thức, phát triển'},
            {'name': 'Nghệ thuật', 'description': 'Hội họa, điêu khắc, kiến trúc, thiết kế'},
            {'name': 'Âm nhạc', 'description': 'Lý thuyết âm nhạc, nhạc cụ, nhạc sĩ nổi tiếng'},
            {'name': 'Thể thao', 'description': 'Các môn thể thao, huấn luyện, dinh dưỡng thể thao'},
            {'name': 'Du lịch', 'description': 'Cẩm nang du lịch, văn hóa các nước'},
            {'name': 'Ngoại ngữ', 'description': 'Tiếng Anh, tiếng Trung, tiếng Nhật, tiếng Hàn'},
            {'name': 'Từ điển', 'description': 'Từ điển các ngôn ngữ, từ điển chuyên ngành'},
            {'name': 'Y học', 'description': 'Y học lâm sàng, giải phẫu, sinh lý bệnh'},
            {'name': 'Dược học', 'description': 'Dược lý, hóa dược, dược liệu'},
            {'name': 'Nông nghiệp', 'description': 'Trồng trọt, chăn nuôi, công nghệ sau thu hoạch'},
            {'name': 'Công nghệ', 'description': 'Công nghệ mới, IoT, Blockchain, Cloud Computing'},
            {'name': 'Kỹ thuật', 'description': 'Kỹ thuật cơ khí, điện, điện tử viễn thông'},
            {'name': 'Kiến trúc', 'description': 'Thiết kế kiến trúc, quy hoạch đô thị'},
            {'name': 'Marketing', 'description': 'Marketing chiến lược, Digital Marketing, SEO'},
            {'name': 'Quản trị', 'description': 'Quản trị doanh nghiệp, lãnh đạo, quản lý nhân sự'},
            {'name': 'Luật pháp', 'description': 'Luật dân sự, hình sự, thương mại'},
            {'name': 'Chính trị', 'description': 'Chính trị học, quan hệ quốc tế'},
            {'name': 'Xã hội học', 'description': 'Nghiên cứu xã hội, văn hóa, cộng đồng'},
            {'name': 'Nhân học', 'description': 'Nhân chủng học, dân tộc học'},
            {'name': 'Giáo dục', 'description': 'Phương pháp giảng dạy, tâm lý học giáo dục'},
            {'name': 'Truyền thông', 'description': 'Báo chí, PR, truyền thông đa phương tiện'},
        ]

        self.stdout.write(self.style.SUCCESS('Bắt đầu import dữ liệu loại sách...'))
        
        created_count = 0
        updated_count = 0

        for data in book_types_data:
            book_type, created = Book_Type.objects.update_or_create(
                name=data['name'],
                defaults={
                    'description': data['description']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Đã tạo loại: {data["name"]}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'  ⟳ Đã cập nhật loại: {data["name"]}'))

        self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
        self.stdout.write(self.style.SUCCESS(f'Hoàn thành!'))
        self.stdout.write(self.style.SUCCESS(f'  • Đã tạo mới: {created_count} loại sách'))
        self.stdout.write(self.style.SUCCESS(f'  • Đã cập nhật: {updated_count} loại sách'))
        self.stdout.write(self.style.SUCCESS(f'  • Tổng số loại: {Book_Type.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'{"="*60}\n'))
