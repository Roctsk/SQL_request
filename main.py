#pip freeze > requirements.txt

import sqlite3

contact = sqlite3.connect("university.db")
cursor = contact.cursor()

courses_data = [
    ("Математика", "Петренко"),
    ("Фізика", "Сидоренко"),
    ("Хімія", "Іваненко"),
    ("Біологія", "Коваленко"),
    ("Інформатика", "Шевченко")
]

cursor.executemany("INSERT INTO courses (course_name, instructor) VALUES (?, ?)",
               courses_data
)

student_courses_data = [
    (1, 1),
    (1, 2), 
    (2, 1),  
    (2, 4),  
    (3, 3),  
    (3, 2),  
    (4, 4),  
    (4, 5),  
    (5, 5),  
    (5, 1)   
]

cursor.executemany(
    "INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)",
    student_courses_data
)


contact.commit()


students = cursor.fetchall()
print(students)

contact.close()

DB_NAME = "university.db"

def connect_db():
    contact = sqlite3.connect(DB_NAME)
    cursor = contact.cursor()
    return contact , cursor


def add_students():
    name = input("Введіть ім'я студента: ")
    age = int(input("Введіть вік: "))
    major = input("Введіть спеціальність: ")

    contact, cursor = connect_db()
    cursor.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)",
                    (name, age, major)
    )
    contact.commit()
    contact.close()
    print("Студента додано")

def add_courses():
    course_name = input("Введіть назву курсу: ")
    instructor = input("Введіть ім'я викладача: ")

    contact, cursor = connect_db()
    cursor.execute("INSERT INTO courses (course_name, instructor) VALUES (?, ?)",
                    (course_name, instructor)
    )
    contact.commit()
    contact.close()
    print("Курс додано")


def view_students():
    contact, cursor = connect_db()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    print("Список студентів")
    for stu in students:
        print(stu)
    print()
   
def view_courses():
    contact, cursor = connect_db()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    print("Список курсів")
    for co in courses:
        print(co)
    print()


def students_in_courses():
    view_students()
    student_id = int(input("Введіть ID студента для запису: "))

    view_courses()
    course_id = int(input("Введіть ID курсу: "))

    contact, cursor = connect_db()
    cursor.execute(
        "INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)",
        (student_id, course_id)
)
    contact.commit()
    contact.close()
    print("Студента зареєстровано на курс")

def view_student_in_course():
    view_courses()
    course_id = int(input("Введіть ID курсу: "))

    contact, cursor = connect_db()
    cursor.execute("""
        SELECT students.student_id , students.name , students.age
        FROM students
        JOIN student_courses ON students.student_id = student_courses.student_id
        WHERE student_courses.course_id = ?
    """, (course_id,))

    students = cursor.fetchall()
    contact.close()

    print(f"Студенти на курсі{course_id} ")
    for s in students:
        print(s)
    print()


def main_menu():
    while True:
        print("Виберіть дію:")
        print("1. Додати студента")
        print("2. Додати курс")
        print("3. Переглянути студентів")
        print("4. Переглянути курси")
        print("5. Записати студента на курс")
        print("6. Переглянути студентів конкретного курсу")
        print("0. Вийти")

        choice = input("Введіть номер дії: ")

        print()

        if choice == "1":
            add_students()
        elif choice == "2":
            add_courses()
        elif choice == "3":
            view_students()
        elif choice == "4":
            view_courses()
        elif choice == "5":
            students_in_courses()
        elif choice == "6":
            view_student_in_course()
        elif choice == "0":
            print("Вихід ")
            break
        else:
            print("Неправильно ведена цифра ")


if __name__ == "__main__":
    main_menu()