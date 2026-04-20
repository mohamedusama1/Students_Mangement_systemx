import sqlite3
import hashlib
from datetime import date, timedelta
import random
from create_db import hash_password


def fill_dummy_data():
    con = sqlite3.connect('school.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    print("🔄  إدخال البيانات التجريبية...")

    # Admin — مع roles مختلفة
    cur.executemany("""
        INSERT OR IGNORE INTO Admin(admin_name,admin_username,admin_password,role) VALUES(?,?,?,?)
    """, [
        ('Manager',    'admin',  hash_password('12345'),    'superadmin'),
        ('Supervisor', 'super',  hash_password('admin123'), 'admin'),
        ('Observer',   'viewer', hash_password('view123'),  'viewer'),
    ])
    print("  ✅ Admin (3 roles)")

    cur.executemany("""
        INSERT OR IGNORE INTO Account(name,username,password) VALUES(?,?,?)
    """, [
        ('Ahmed Ali',  'ahmed2024', hash_password('pass123')),
        ('Sarah Taha', 'sarah_t',   hash_password('567890')),
    ])
    print("  ✅ Account")

    cur.executemany("""
        INSERT OR IGNORE INTO teachers(name,subject,phone,national_id,salary,college_degree,hire_date) VALUES(?,?,?,?,?,?,?)
    """, [
        ('Mr. Ibrahim', 'Arabic',  '01012345678', '29001011234567', 5000, 'Bachelor of Education', '2018-09-01'),
        ('Ms. Huda',    'Islamic', '01123456789', '29505051234567', 4500, 'Bachelor of Arts',      '2019-09-01'),
        ('Mr. John',    'Math',    '01234567890', '28810101234567', 6000, 'B.Sc Mathematics',      '2017-09-01'),
        ('Ms. Nadia',   'Science', '01098765432', '30001011234568', 5500, 'B.Sc Science',          '2020-09-01'),
        ('Mr. Kamal',   'English', '01187654321', '29709091234567', 5200, 'Bachelor of Arts',      '2021-09-01'),
    ])
    print("  ✅ Teachers")

    students = [
        ('Mohamed Ahmed','Male',  10,'Cairo, Nasr City',  '01099887766','2023-09-12','Future School', 0,'None',  'Pass'),
        ('Fatima Hassan','Female',11,'Giza, Dokki',        '01122334455','2023-09-15','Sunrise School',0,'Asthma','Pass'),
        ('Omar Khaled',  'Male',  10,'Alexandria',         '01233445566','2023-09-10','Nile School',   1,'None',  'Fail'),
        ('Nour Salem',   'Female',10,'Cairo, Heliopolis',  '01011223344','2023-09-12','Stars School',  0,'None',  'Pass'),
        ('Youssef Adel', 'Male',  11,'Giza, Haram',        '01277889900','2023-09-11','Palm School',   0,'None',  'Pass'),
        ('Aya Mostafa',  'Female',10,'Cairo, Maadi',       '01566778899','2023-09-13','Lotus School',  0,'None',  'Pass'),
        ('Hassan Fathy', 'Male',  12,'Alexandria, Smouha', '01655443322','2023-09-14','Ocean School',  2,'None',  'Fail'),
        ('Mariam Samir', 'Female',10,'Cairo, 6th October', '01744332211','2023-09-12','Green School',  0,'None',  'Pass'),
    ]
    cur.executemany("""
        INSERT OR IGNORE INTO first_student
        (student_name,student_gender,student_age,address,contact,
         enrollment_date,last_school,repeated_years,health_problem,final_result)
        VALUES(?,?,?,?,?,?,?,?,?,?)
    """, students)
    print("  ✅ Students")

    cur.execute("SELECT s_ID, student_name FROM first_student")
    smap = {name: sid for sid, name in cur.fetchall()}

    islamic_data = [
        ('Mohamed Ahmed','10','9', '18','45','10','10','19','20','95','Excellent'),
        ('Fatima Hassan','9', '9', '17','40','9', '8', '18','19','88','Very Good'),
        ('Nour Salem',   '10','10','19','46','10','10','20','20','97','Excellent'),
        ('Youssef Adel', '8', '9', '16','38','8', '9', '17','18','83','Good'),
        ('Aya Mostafa',  '9', '10','18','43','9', '10','19','19','90','Excellent'),
        ('Mariam Samir', '10','9', '18','44','10','9', '18','20','92','Excellent'),
    ]
    for row in islamic_data:
        sid = smap.get(row[0])
        if sid:
            cur.execute("""INSERT OR IGNORE INTO islamic_marks
                (student_id,student_name,st_month,nd_month,chapter1,half_year,
                 st_month1,nd_month2,chapter2,chapter3,final_exam,final_result)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""", (sid, row[0]) + row[1:])
    print("  ✅ Islamic Marks")

    arabic_data = [
        ('Mohamed Ahmed','10','10','20','48','10','10','20','20','98','Excellent'),
        ('Fatima Hassan','8', '9', '15','38','9', '9', '16','18','85','Very Good'),
        ('Nour Salem',   '10','10','19','47','10','10','20','19','96','Excellent'),
        ('Youssef Adel', '7', '8', '14','35','8', '8', '15','17','80','Good'),
        ('Aya Mostafa',  '9', '10','18','44','9', '10','18','19','91','Excellent'),
        ('Mariam Samir', '10','9', '19','45','10','9', '19','20','93','Excellent'),
    ]
    for row in arabic_data:
        sid = smap.get(row[0])
        if sid:
            cur.execute("""INSERT OR IGNORE INTO arabic_marks
                (student_id,student_name,st_month,nd_month,chapter1,half_year,
                 st_month1,nd_month2,chapter2,chapter3,final_exam,final_result)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""", (sid, row[0]) + row[1:])
    print("  ✅ Arabic Marks")

    school_days = []
    d = date.today()
    while len(school_days) < 5:
        if d.weekday() < 5: school_days.append(d.strftime('%Y-%m-%d'))
        d -= timedelta(days=1)

    statuses = ['Present','Present','Present','Present','Absent']
    att_rows = [(sid, dd, random.choice(statuses), None)
                for sid in smap.values() for dd in school_days]
    cur.executemany("""INSERT OR IGNORE INTO attendance(student_id,att_date,status,notes)
        VALUES(?,?,?,?)""", att_rows)
    print(f"  ✅ Attendance ({len(att_rows)} records)")

    cur.execute("""INSERT INTO activity_log(admin_username,action,target_table,details)
        VALUES('admin','FILL_DUMMY_DATA','ALL','Initial data by fill_data.py')""")

    con.commit(); con.close()
    print("\n✅  كل البيانات اتدخلت بنجاح!")
    print("\n📋  بيانات الدخول:")
    print("   superadmin → username: admin    | password: 12345")
    print("   admin      → username: super    | password: admin123")
    print("   viewer     → username: viewer   | password: view123")


if __name__ == "__main__":
    fill_dummy_data()
