from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade
import random

fake = Faker()

# Підключення до бази даних
DATABASE_URL = "postgresql://your_username:your_password@localhost:5432/your_database_name"
engine = create_engine(DATABASE_URL)

# Створення сесії
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Генерація груп
groups = [Group(name=fake.unique.random_element(elements=("A", "B", "C"))) for _ in range(3)]
session.add_all(groups)
session.commit()

# Генерація викладачів
teachers = [Teacher(name=fake.unique.first_name()) for _ in range(random.randint(3, 5))]
session.add_all(teachers)
session.commit()

# Генерація предметів та призначення викладачів
subjects = [Subject(name=fake.unique.word(), teacher_id=random.choice(teachers).id) for _ in range(random.randint(5, 8))]
session.add_all(subjects)
session.commit()

# Генерація студентів
students = [Student(name=fake.unique.first_name() + " " + fake.unique.last_name(), group_id=random.choice(groups).id) for _ in range(random.randint(30, 50))]
session.add_all(students)
session.commit()

# Генерація оцінок для студентів
for student in students:
    for subject in subjects:
        for _ in range(random.randint(0, 20)):
            grade = random.randint(1, 5)
            date = fake.date_of_birth(minimum_age=18, maximum_age=25).strftime('%d.%m.%Y')
            session.add(Grade(student_id=student.id, subject_id=subject.id, grade=grade, date=date))

session.commit()

# Закриття сесії
session.close()
