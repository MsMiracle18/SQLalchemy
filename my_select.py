from sqlalchemy import func, distinct
from models import Student, Grade, Subject, Teacher, Group


def select_1(session):
    subquery = session.query(Grade.student_id, func.avg(Grade.grade).label('avg_grade')).group_by(Grade.student_id).subquery()
    students = session.query(Student, subquery.c.avg_grade).join(subquery, Student.id == subquery.c.student_id).order_by(subquery.c.avg_grade.desc()).limit(5).all()
    return students
#Знайти 5 студентів із найбільшим середнім балом з усіх предметів.#

def select_2(session, subject_name):
    subquery = session.query(Grade.student_id, func.avg(Grade.grade).label('avg_grade')).group_by(Grade.student_id).subquery()
    student = session.query(Student, subquery.c.avg_grade).join(subquery, Student.id == subquery.c.student_id).join(Grade, Student.id == Grade.student_id).join(Subject, Grade.subject_id == Subject.id).filter(Subject.name == subject_name).order_by(subquery.c.avg_grade.desc()).first()
    return student
#Знайти студента із найвищим середнім балом з певного предмета.#

def select_3(session, subject_name):
    avg_grades = session.query(Group.name, func.avg(Grade.grade).label('avg_grade')).join(Group.students).join(Grade, Student.id == Grade.student_id).join(Subject, Grade.subject_id == Subject.id).filter(Subject.name == subject_name).group_by(Group.name).all()
    return avg_grades
#Знайти середній бал у групах з певного предмета.#

def select_4(session):
    avg_grade = session.query(func.avg(Grade.grade).label('avg_grade')).scalar()
    return avg_grade
#Знайти середній бал на потоці (по всій таблиці оцінок).

def select_5(session, teacher_name):
    teacher = session.query(Teacher).filter(Teacher.name == teacher_name).first()
    if teacher:
        subjects = [subject.name for subject in teacher.subjects]
        return subjects
    else:
        return []
#Знайти, які курси читає певний викладач.

def select_6(session, group_name):
    students = session.query(Student).join(Group).filter(Group.name == group_name).all()
    return students
#Знайти список студентів у певній групі.

def select_7(session, group_name, subject_name):
    grades = session.query(Student, Grade).join(Group).join(Grade).join(Subject).filter(Group.name == group_name, Subject.name == subject_name).all()
    return grades
#Знайти оцінки студентів в окремій групі з певного предмета.

def select_8(session, teacher_name):
    teacher = session.query(Teacher).filter(Teacher.name == teacher_name).first()
    if teacher:
        subquery = session.query(func.avg(Grade.grade).label('avg_grade')).join(Subject).filter(Subject.teacher_id == teacher.id).subquery()
        avg_grade = session.query(subquery.c.avg_grade).scalar()
        return avg_grade
    else:
        return None
#Знайти середній бал, який ставить певний викладач зі своїх предметів.

def select_9(session, student_name):
    student = session.query(Student).filter(Student.name == student_name).first()
    if student:
        subjects = session.query(distinct(Subject.name)).join(Grade).filter(Grade.student_id == student.id).all()
        return [subject[0] for subject in subjects]
    else:
        return []
#Знайти список курсів, які відвідує студент.

def select_10(session, student_name, teacher_name):
    student = session.query(Student).filter(Student.name == student_name).first
#Список курсів, які певному студенту читає певний викладач.

