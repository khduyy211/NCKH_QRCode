from django.core.management.base import BaseCommand
from demo_app.models import Book_Shelf, Compartment

class Command(BaseCommand):
    help = 'Import dữ liệu kệ sách từ shelfData vào database'

    def handle(self, *args, **options):
        # Dữ liệu từ shelfData trong script.js
        # Format: 'shelf_code': {'rows': x, 'cols': y, 'description': 'text'}
        shelf_data = {
            'A1-M1': {'rows': 5, 'cols': 6, 'description': 'Khoa học máy tính'},
            'A1-M2': {'rows': 5, 'cols': 6, 'description': 'Lập trình'},
            'A2-M1': {'rows': 6, 'cols': 5, 'description': 'Toán học'},
            'A2-M2': {'rows': 6, 'cols': 5, 'description': 'Vật lý'},
            'B1-M1': {'rows': 5, 'cols': 6, 'description': 'Văn học'},
            'B1-M2': {'rows': 5, 'cols': 6, 'description': 'Lịch sử'},
            'B2-M1': {'rows': 6, 'cols': 5, 'description': 'Địa lý'},
            'B2-M2': {'rows': 6, 'cols': 5, 'description': 'Sinh học'},
            'C1-M1': {'rows': 5, 'cols': 6, 'description': 'Hóa học'},
            'C1-M2': {'rows': 5, 'cols': 6, 'description': 'Kinh tế'},
            'C2-M1': {'rows': 6, 'cols': 5, 'description': 'Triết học'},
            'C2-M2': {'rows': 6, 'cols': 5, 'description': 'Tâm lý học'},
            'D1-M1': {'rows': 5, 'cols': 6, 'description': 'Nghệ thuật'},
            'D1-M2': {'rows': 5, 'cols': 6, 'description': 'Âm nhạc'},
            'D2-M1': {'rows': 6, 'cols': 5, 'description': 'Thể thao'},
            'D2-M2': {'rows': 6, 'cols': 5, 'description': 'Du lịch'},
            'E1-M1': {'rows': 5, 'cols': 6, 'description': 'Ngoại ngữ'},
            'E1-M2': {'rows': 5, 'cols': 6, 'description': 'Từ điển'},
            'E2-M1': {'rows': 6, 'cols': 5, 'description': 'Y học'},
            'E2-M2': {'rows': 6, 'cols': 5, 'description': 'Dược học'},
            'F1-M1': {'rows': 5, 'cols': 6, 'description': 'Nông nghiệp'},
            'F1-M2': {'rows': 5, 'cols': 6, 'description': 'Công nghệ'},
            'F2-M1': {'rows': 6, 'cols': 5, 'description': 'Kỹ thuật'},
            'F2-M2': {'rows': 6, 'cols': 5, 'description': 'Kiến trúc'},
            'G1-M1': {'rows': 5, 'cols': 6, 'description': 'Marketing'},
            'G1-M2': {'rows': 5, 'cols': 6, 'description': 'Quản trị'},
            'G2-M1': {'rows': 6, 'cols': 5, 'description': 'Luật pháp'},
            'G2-M2': {'rows': 6, 'cols': 5, 'description': 'Chính trị'},
            'H1-M1': {'rows': 5, 'cols': 6, 'description': 'Xã hội học'},
            'H1-M2': {'rows': 5, 'cols': 6, 'description': 'Nhân học'},
            'H2-M1': {'rows': 6, 'cols': 5, 'description': 'Giáo dục'},
            'H2-M2': {'rows': 6, 'cols': 5, 'description': 'Truyền thông'},
        }

        self.stdout.write(self.style.SUCCESS('Bắt đầu import dữ liệu kệ sách...'))
        
        created_count = 0
        updated_count = 0

        for shelf_code, data in shelf_data.items():
            # Tạo hoặc cập nhật Book_Shelf
            shelf, created = Book_Shelf.objects.update_or_create(
                name=shelf_code,
                defaults={
                    'description': data['description']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Đã tạo kệ: {shelf_code} - {data["description"]}'))
                
                # Tạo các Compartment (ô) cho kệ này
                compartment_count = 0
                for row in range(1, data['rows'] + 1):
                    for col in range(1, data['cols'] + 1):
                        # Tạo tên ô theo format: A1, A2, B1, B2...
                        comp_name = f"{chr(64 + row)}{col}"
                        
                        Compartment.objects.get_or_create(
                            shelf=shelf,
                            name=comp_name,
                            defaults={
                                'row_number': row,
                                'column_number': col,
                                'description': f'Ô {comp_name} thuộc kệ {shelf_code}'
                            }
                        )
                        compartment_count += 1
                
                self.stdout.write(self.style.SUCCESS(f'    → Đã tạo {compartment_count} ô cho kệ {shelf_code}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'  ⟳ Đã cập nhật kệ: {shelf_code}'))

        self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
        self.stdout.write(self.style.SUCCESS(f'Hoàn thành!'))
        self.stdout.write(self.style.SUCCESS(f'  • Đã tạo mới: {created_count} kệ'))
        self.stdout.write(self.style.SUCCESS(f'  • Đã cập nhật: {updated_count} kệ'))
        self.stdout.write(self.style.SUCCESS(f'  • Tổng số kệ: {Book_Shelf.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  • Tổng số ô: {Compartment.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'{"="*60}\n'))
