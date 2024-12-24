import random
from django.core.management.base import BaseCommand
from a_user_management.models import *  # Import your models here
from decimal import Decimal
from a_financial_management.models import Receipt
from a_institution_management.models import Branch
from a_course_management.models import Course, Section, SectionTimeSlot, SectionStudent, HomeWork

from datetime import datetime, timedelta
from django.contrib.auth.models import Group, Permission

# Predefined data lists
BOY_FIRST_NAMES = ["رضا", "علی", "طاها", "محمد", "نیما", "سینا"
                   , "یاسین", "یزدان", "آرش", "سجاد", "پویا"
                   , "حسین", "آرمین", "رامتین", "متین", "عباس"
                   , "آرشام", "احمد", "مجتبی", "عطا", "جلال"
                   , "جمشید", "حسن", "داریوش", "محسن", "مهدی"]
GIRL_FIRST_NAMES = ["سارا", "هلیا", "مریم", "پریا", "ملیکا", "منا"
                    , "ندا", "نسرین", "فاطمه", "فریما", "سارینا"
                    , "نیوشا", "نجمه", "شیرین", "شادی", "اسما"
                    , "یلدا", "نازنین", "مژده", "نسترن", "الینا"]

LAST_NAMES = [
    "محمدی", "نقاش", "حسینی", "افشانی", "سالاری", "کیانی",
    "کریمی", "صادقی", "قاسمی", "اکبری", "جوانمردی", "مرادی",
    "زارع", "احمدی", "شریفی", "رضایی", "عباسی", "یوسفی",
    "درویش", "پورمحمد", "سلطانی", "رفیعی", "ابراهیمی", "نادری",
    "افتخاری", "فیروزی", "هدایتی", "امینی", "علوی", "بهشتی"
]
CODE_MELLIS = [f"{i:010d}" for i in range(1743062499, 1743063050)]  # Example: 1111111111 to 1111111120
PHONES = [f"0912{random.randint(1000000, 9999999)}" for _ in range(550)]










class Command(BaseCommand):
    help = 'Create dummy data for the database'

    def handle(self, *args, **kwargs):
        # Example of creating dummy data
        self.stdout.write("Creating dummy data...")
        



        # A_USER_MANAGEMENT

        if not CODE_MELLIS:
            self.stdout.write(self.style.ERROR("No more unique code_melli values left to use."))
            return



        # Create instances for various models
        self.create_groups()
        self.stdout.write(f"GROUPS CREATED")


        self.create_students()
        self.stdout.write(f"STUDENTS CREATED")

        self.create_managers()
        self.stdout.write(f"MANAGER CREATED")

        self.create_employees()
        self.stdout.write(f"EMPLOYEES CREATED")

        self.create_teachers()
        self.stdout.write(f"TEACHERS CREATED")

        self.create_sample_courses()
        self.stdout.write(f"COURSES CREATED")

        self.create_sections_for_courses()
        self.stdout.write(f"SECTIONS CREATED")

        self.create_time_slots_for_sections()
        self.stdout.write(f"TIME_SLOTS CREATED")

        self.create_students_for_sections()
        self.stdout.write(f"STUDENTS_FOR_SECTIONS CREATED")

        self.create_homeworks_for_sections()
        self.stdout.write(f"HOMEWORKS CREATED")

        self.create_receipts()
        self.stdout.write(f"RECEIPTS CREATED")


    def create_students(self, count=500):
        for _ in range(count):
            gender = random.randint(0, 1)
            if gender == 0:
                first_name = random.choice(BOY_FIRST_NAMES)
            else:
                first_name = random.choice(GIRL_FIRST_NAMES)

            last_name = random.choice(LAST_NAMES)
            code_melli = CODE_MELLIS.pop()  # Ensure uniqueness
            phone = PHONES.pop()  # Ensure uniqueness
            balance = random.randint(2, 500)*100000
            balance = balance * random.randint(-1,1)
            student = Student.objects.create(
                username=f"{phone}",
                first_name=first_name,
                last_name=last_name,
                code_melli=code_melli,
                phone=phone,
                date_of_birth=timezone.now().date() - timezone.timedelta(days=random.randint(6000, 20000)),  # Random DOB
                balance=balance ,

                activity=random.choice(Student.ACTIVITY)[0],
                education=random.choice(Student.EDUCATION)[0],
                ageLevel=random.choice(Student.AGE_LEVEL)[0],
                gender=gender,
            )
        self.stdout.write(f"Created students: {count}")

    def create_managers(self, count=1):
        for _ in range(count):
            first_name = random.choice(BOY_FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            code_melli = CODE_MELLIS.pop()  # Ensure uniqueness
            phone = PHONES.pop()  # Ensure uniqueness

            manager = Manager.objects.create(
                username=f"{phone}",
                first_name=first_name,
                last_name=last_name,
                code_melli=code_melli,
                phone=phone,
                date_of_birth=timezone.now().date() - timezone.timedelta(days=random.randint(6000, 20000)),
            )
            manager.set_password("admin")
        

    def create_employees(self, count=2):
        for _ in range(count):
            first_name = random.choice(BOY_FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            code_melli = CODE_MELLIS.pop()
            phone = PHONES.pop()

            employee = Employee.objects.create(
                username=f"{phone}",
                first_name=first_name,
                last_name=last_name,
                code_melli=code_melli,
                phone=phone,
                date_of_birth=timezone.now().date() - timezone.timedelta(days=random.randint(6000, 20000)),
            )
            employee.set_password("admin")
            employee.save()


    def create_teachers(self, count=5):
        for _ in range(count):
            first_name = random.choice(BOY_FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            code_melli = CODE_MELLIS.pop()
            phone = PHONES.pop()

            teacher = Teacher.objects.create(
                username=f"{phone}",
                first_name=first_name,
                last_name=last_name,
                code_melli=code_melli,
                phone=phone,
                date_of_birth=timezone.now().date() - timezone.timedelta(days=random.randint(6000, 20000)),
            )
            teacher.set_password("admin")



        
    def create_sample_courses(self):
        course_data = [
            {
                "title": "برنامه‌نویسی پایتون",
                "description": "آموزش اصول برنامه‌نویسی با پایتون، از دستورات پایه تا ساختارهای داده پیشرفته.",
                "price": "500000",
                "courseDuration": "12 جلسه",
                "session_length": "2 ساعت",
                "course_hours": 24,
                "installment": '1'
            },
            {
                "title": "مبانی علوم داده",
                "description": "مفاهیم اولیه علوم داده شامل تحلیل و مصورسازی داده‌ها.",
                "price": "800000",
                "courseDuration": "15 جلسه",
                "session_length": "2.5 ساعت",
                "course_hours": 37,
                "installment": '1'
            },
            {
                "title": "توسعه وب با جنگو",
                "description": "ساخت برنامه‌های وب پویا با فریم‌ورک جنگو، یکی از محبوب‌ترین فریم‌ورک‌های پایتون.",
                "price": "750000",
                "courseDuration": "10 جلسه",
                "session_length": "2 ساعت",
                "course_hours": 20,
                "installment": '0'
            },
            {
                "title": "مبانی یادگیری ماشین",
                "description": "آشنایی با الگوریتم‌های یادگیری ماشین و ساخت اولین مدل‌ها.",
                "price": "1000000",
                "courseDuration": "20 جلسه",
                "session_length": "3 ساعت",
                "course_hours": 60,
                "installment": '1'
            },
            {
                "title": "مقدمه‌ای بر هوش مصنوعی",
                "description": "بررسی مفاهیم هوش مصنوعی و کاربردهای آن در دنیای واقعی.",
                "price": "1200000",
                "courseDuration": "18 جلسه",
                "session_length": "2.5 ساعت",
                "course_hours": 45,
                "installment": '0'
            },
            {
                "title": "توسعه فرانت‌اند با ری‌اکت",
                "description": "آموزش فریم‌ورک ری‌اکت و ساخت برنامه‌های وب مدرن و واکنش‌گرا.",
                "price": "600000",
                "courseDuration": "14 جلسه",
                "session_length": "2 ساعت",
                "course_hours": 28,
                "installment": '1'
            },
            {
                "title": "توسعه بک‌اند با Node.js",
                "description": "یادگیری توسعه بک‌اند با Node.js و ساخت API‌های مقیاس‌پذیر.",
                "price": "700000",
                "courseDuration": "12 جلسه",
                "session_length": "2.5 ساعت",
                "course_hours": 30,
                "installment": '0'
            },
            {
                "title": "طراحی و مدیریت پایگاه داده",
                "description": "مفاهیم پایگاه داده و یادگیری مدیریت پایگاه‌های داده SQL و NoSQL.",
                "price": "650000",
                "courseDuration": "16 جلسه",
                "session_length": "2 ساعت",
                "course_hours": 32,
                "installment": '1'
            },
            {
                "title": "توسعه اپلیکیشن موبایل با Flutter",
                "description": "ساخت اپلیکیشن‌های موبایل زیبا و کاربردی با استفاده از فلاتر.",
                "price": "900000",
                "courseDuration": "15 جلسه",
                "session_length": "2.5 ساعت",
                "course_hours": 37,
                "installment": '1'
            },
            {
                "title": "مبانی تحلیل داده",
                "description": "آشنایی با ابزارهای تحلیل داده و یادگیری کاربردی آن‌ها.",
                "price": "700000",
                "courseDuration": "10 جلسه",
                "session_length": "2 ساعت",
                "course_hours": 20,
                "installment": '0'
            },
        ]

        for data in course_data:
            Course.objects.create(
                title=data["title"],
                description=data["description"],
                price=data["price"],
                courseDuration=data["courseDuration"],
                session_length=data["session_length"],
                course_hours=data["course_hours"],
                installment=data["installment"],
            )
        

    def create_sections_for_courses(self):
        courses = Course.objects.all()
        teachers = list(Teacher.objects.all())  # Get all teachers as a list

        for course in courses:
            # Randomly decide the number of sections (2 to 4)
            num_sections = random.randint(2, 4)

            for i in range(1, num_sections + 1):
                if not teachers:  # Ensure there are teachers available
                    print("No teachers available to assign to sections.")
                    break

                # Randomly assign a teacher
                teacher = random.choice(teachers)

                # Create the section
                section = Section.objects.create(
                    name=f'گروه {i}',
                    course=course,
                    teacher=teacher,
                    online_section=random.choice([True, False]),
                    capacity=random.randint(10, 30),  # Random capacity
                    section_status=random.choice(['0', '1']),  # Random status
                    gender=random.choice(['0', '1', '2']),  # Random gender

                )


    def create_time_slots_for_sections(self):
        sections = Section.objects.all()

        for section in sections:
            # Randomly decide the number of time slots (1 or more)
            num_slots = random.randint(1, 3)

            for _ in range(num_slots):
                day = random.choice(['0', '1', '2', '3', '4', '5', '6'])  # Random day
                time_of_section = random.choice(['14 تا 16', '16 تا 18', '18 تا 20'])  # Random time
                place = random.choice(['کلاس 110', 'کلاس 120', 'کلاس 130'])  # Random place

                # Create the time slot
                time_slot = SectionTimeSlot.objects.create(
                    section=section,
                    day_of_week=day,
                    timeOfSection=time_of_section,
                    place=place,
                )


    def create_students_for_sections(self):
        sections = Section.objects.all()
        students = list(Student.objects.all())  # Get all students as a list
        
        if not sections or not students:
            print("No sections or students available to assign.")
            return

        for section in sections:
            # Determine a random number of students for this section (between 25 and 30)
            num_students = random.randint(25, 30)
            assigned_students = set()  # To enforce uniqueness of students in section

            while len(assigned_students) < num_students and students:
                student = random.choice(students)

                # Skip if this student is already in the section
                if student in assigned_students:
                    continue

                # Randomly decide whether to assign scores
                has_scores = random.choice([True, False])
                class_score = Decimal(random.uniform(0, 100)).quantize(Decimal('0.01')) if has_scores else None
                exam_score = Decimal(random.uniform(0, 100)).quantize(Decimal('0.01')) if has_scores else None

                # Determine the activity status
                if class_score is not None and exam_score is not None:
                    weighted_score = (Decimal('0.7') * class_score) + (Decimal('0.3') * exam_score)
                    if weighted_score > 70:
                        activity = '1'  # Passed
                    else:
                        activity = '2'  # Failed
                else:
                    activity = '0'  # No scores

                # Create the SectionStudent instance
                section_student = SectionStudent.objects.create(
                    section=section,
                    student=student,
                    activity=activity,
                    class_score=class_score,
                    exam_score=exam_score,
                )
                assigned_students.add(student)

            print(f"Total students assigned to section {section}: {len(assigned_students)}")


    def create_homeworks_for_sections(self):
        homework_data = [
            {
                "title": "تمرین الگوریتم مرتب‌سازی",
                "description": "الگوریتم‌های مرتب‌سازی حبابی و انتخابی را پیاده‌سازی کنید و عملکرد آن‌ها را مقایسه کنید."
            },
            {
                "title": "تمرین طراحی پایگاه داده",
                "description": "یک پایگاه داده برای مدیریت کتابخانه طراحی کنید و شامل جداول کاربران، کتاب‌ها و تراکنش‌ها باشد."
            },
            {
                "title": "تمرین برنامه‌نویسی پایتون",
                "description": "یک برنامه پایتون بنویسید که یک ماتریس را از ورودی بگیرد و دترمینان آن را محاسبه کند."
            },
            {
                "title": "تمرین تحلیل الگوریتم",
                "description": "الگوریتم جستجوی دودویی را پیاده‌سازی کنید و پیچیدگی زمانی آن را تحلیل کنید."
            },
            {
                "title": "تمرین طراحی رابط کاربری",
                "description": "یک صفحه ورود کاربر با HTML و CSS طراحی کنید که شامل اعتبارسنجی فرم باشد."
            },
            {
                "title": "تمرین برنامه‌نویسی شی‌گرا",
                "description": "یک کلاس در پایتون ایجاد کنید که مشخصات دانش‌آموزان را مدیریت کند و قابلیت اضافه کردن و حذف دانش‌آموز داشته باشد."
            },
        ]

        sections = Section.objects.all()

        if not sections:
            print("No sections available to assign homework.")
            return

        for section in sections:
            num_homeworks = random.randint(2, 5)  # Randomly decide the number of homework for each section

            for _ in range(num_homeworks):
                # Randomly select homework data from the map
                data = random.choice(homework_data)
                
                # Determine teacher and section details
                teacher = section.teacher

                # Random deadline (3 to 15 days from now)
                expire_time = datetime.now() + timedelta(days=random.randint(3, 15))

                # Create the homework instance
                homework = HomeWork.objects.create(
                    title=data["title"],
                    description=data["description"],
                    section=section,
                    teacher=teacher,
                    expire_time=expire_time,
                )

            print(f"Total homeworks created for section {section}: {num_homeworks}")


    def create_receipts(self):
        # List of titles in Persian
        titles = [
            "بابت قسط شهریه",
            "بابت شهریه",
            "بابت کلاس تقویتی",
            "بابت کمک به آموزشگاه",
            "بابت خسارت",
        ]

        # Get all students
        students = list(Student.objects.all())
        if not students:
            print("No students available to assign receipts.")
            return

        # Generate 500 receipts
        for _ in range(500):
            # Select a random title
            title = random.choice(titles)

            # Select a random student as the payer
            payer = random.choice(students)

            # Generate a random amount (e.g., between 100,000 and 5,000,000 Toman)
            amount = random.randint(2, 100) * 50000
            # Format the amount with commas
            formatted_amount = f"{amount:,}"

            # Generate a random payment method
            payment_method = random.choice(['0', '1', '2', '3', '4'])

            # Generate a random confirmed status
            confirmed = random.choice([True, False])

            # Create the receipt instance
            receipt = Receipt.objects.create(
                title=title,
                payer=payer,
                formatted_amount=formatted_amount,
                payment_method=payment_method,
                confirmed=confirmed,
            )

        print("Successfully created 500 receipts.")

    def create_groups(self):

        teacher_permissions_ids = [60, 64, 69, 70, 71, 72, 74, 76, 80, 82, 84, 88, 101, 102, 103, 104]
        owner_permissions_ids = []
        manager_permissions_ids = [58, 60, 89, 90, 91, 92, 93, 94, 95, 96, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 105, 106, 108, 97, 98, 99, 100, 101, 102, 103, 104, 41, 42, 43, 44, 49, 50, 51, 52, 53, 54, 55, 56, 4]
        employee_permissions_ids = [58, 60, 92, 96, 61, 62, 64, 72, 76, 78, 80, 81, 82, 84, 85, 86, 87, 88, 105, 108, 100, 101, 102, 103, 104, 49, 50, 52, 56]

        teacher_group = Group.objects.create(name='استاد')
        teacher_permissions = Permission.objects.filter(id__in=teacher_permissions_ids)
        teacher_group.permissions.set(teacher_permissions)

        owner_group = Group.objects.create(name='مالک')
        owner_permissions = Permission.objects.all()
        owner_group.permissions.set(owner_permissions)

        manager_group = Group.objects.create(name='مدیر')
        manager_permissions = Permission.objects.filter(id__in=manager_permissions_ids)
        manager_group.permissions.set(manager_permissions)

        employee_group = Group.objects.create(name='کارمند')
        employee_permissions = Permission.objects.filter(id__in=employee_permissions_ids)
        employee_group.permissions.set(employee_permissions)