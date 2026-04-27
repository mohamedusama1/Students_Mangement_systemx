import sqlite3
import hashlib

def hash_password(plain: str) -> str:
    salt = "school_app_salt_2024"
    return hashlib.sha256((salt + plain).encode()).hexdigest()

def create_db():
    con = sqlite3.connect('school.db')
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Account(
            ID       INTEGER PRIMARY KEY AUTOINCREMENT,
            name     TEXT NOT NULL,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )""")

    # ← role عمود جديد
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Admin(
            admin_ID       INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_name     TEXT NOT NULL,
            admin_username TEXT NOT NULL UNIQUE,
            admin_password TEXT NOT NULL,
            role           TEXT NOT NULL DEFAULT 'admin'
                           CHECK(role IN ('superadmin','admin','viewer'))
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS first_student(
            s_ID           INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name   TEXT NOT NULL,
            student_gender TEXT CHECK(student_gender IN ('Male','Female')),
            student_age    INTEGER,
            address        TEXT,
            contact        TEXT,
            enrollment_date TEXT,
            last_school    TEXT,
            repeated_years INTEGER DEFAULT 0,
            health_problem TEXT DEFAULT 'None',
            final_result   TEXT DEFAULT 'Pending',
            is_active      INTEGER DEFAULT 1
        )""")

    # islamic_marks → civic_education_marks (Civic Education / التربية الوطنية)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS civic_education_marks(
            ce_ID        INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id   INTEGER NOT NULL REFERENCES first_student(s_ID)
                         ON DELETE CASCADE ON UPDATE CASCADE,
            student_name TEXT,
            st_month     REAL DEFAULT 0, nd_month  REAL DEFAULT 0,
            chapter1     REAL DEFAULT 0, half_year REAL DEFAULT 0,
            st_month1    REAL DEFAULT 0, nd_month2 REAL DEFAULT 0,
            chapter2     REAL DEFAULT 0, chapter3  REAL DEFAULT 0,
            final_exam   REAL DEFAULT 0, final_result TEXT DEFAULT 'Pending',
            academic_year TEXT DEFAULT '2024-2025'
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS arabic_marks(
            a_ID         INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id   INTEGER NOT NULL REFERENCES first_student(s_ID)
                         ON DELETE CASCADE ON UPDATE CASCADE,
            student_name TEXT,
            st_month     REAL DEFAULT 0, nd_month  REAL DEFAULT 0,
            chapter1     REAL DEFAULT 0, half_year REAL DEFAULT 0,
            st_month1    REAL DEFAULT 0, nd_month2 REAL DEFAULT 0,
            chapter2     REAL DEFAULT 0, chapter3  REAL DEFAULT 0,
            final_exam   REAL DEFAULT 0, final_result TEXT DEFAULT 'Pending',
            academic_year TEXT DEFAULT '2024-2025'
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS teachers(
            t_id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name           TEXT NOT NULL,
            subject        TEXT NOT NULL,
            phone          TEXT,
            national_id    TEXT UNIQUE,
            salary         REAL DEFAULT 0,
            college_degree TEXT,
            hire_date      TEXT,
            is_active      INTEGER DEFAULT 1
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance(
            att_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL REFERENCES first_student(s_ID) ON DELETE CASCADE,
            att_date   TEXT NOT NULL,
            status     TEXT NOT NULL CHECK(status IN ('Present','Absent','Excused')),
            notes      TEXT,
            UNIQUE(student_id, att_date)
        )""")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS activity_log(
            log_id         INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_username TEXT NOT NULL,
            action         TEXT NOT NULL,
            target_table   TEXT,
            target_id      INTEGER,
            details        TEXT,
            log_time       TEXT DEFAULT (datetime('now','localtime'))
        )""")

    con.commit()
    con.close()
    print("✅  DB created successfully.")


def migrate_existing_db():
    con = sqlite3.connect('school.db')
    cur = con.cursor()

    def add_col(table, col, defn):
        cur.execute(f"PRAGMA table_info({table})")
        if col not in [r[1] for r in cur.fetchall()]:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {col} {defn}")
            print(f"  ✚ {table}.{col}")

    def make_table(sql, name):
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (name,))
        if not cur.fetchone():
            cur.execute(sql)
            print(f"  ✚ table {name}")

    print("🔄  Migrating...")
    add_col('Admin',         'role',           "TEXT NOT NULL DEFAULT 'admin' CHECK(role IN ('superadmin','admin','viewer'))")
    add_col('first_student', 'is_active',      'INTEGER DEFAULT 1')
    add_col('first_student', 'repeated_years', 'INTEGER DEFAULT 0')
    # rename islamic_marks → civic_education_marks لو لسه موجود
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='islamic_marks'")
    if cur.fetchone():
        cur.execute("ALTER TABLE islamic_marks RENAME TO civic_education_marks")
        print("  ✚ islamic_marks → civic_education_marks")
    add_col('civic_education_marks', 'student_id',    'INTEGER')
    add_col('civic_education_marks', 'academic_year', "TEXT DEFAULT '2024-2025'")
    add_col('arabic_marks', 'student_id',     'INTEGER')
    add_col('arabic_marks', 'academic_year',  "TEXT DEFAULT '2024-2025'")
    add_col('teachers', 'hire_date', 'TEXT')
    add_col('teachers', 'is_active', 'INTEGER DEFAULT 1')
    add_col('arabic_marks',  'student_id',     'INTEGER')
    add_col('arabic_marks',  'academic_year',  "TEXT DEFAULT '2024-2025'")
    add_col('teachers',      'hire_date',      'TEXT')
    add_col('teachers',      'is_active',      'INTEGER DEFAULT 1')

    make_table("""CREATE TABLE attendance(
        att_id INTEGER PRIMARY KEY AUTOINCREMENT, student_id INTEGER NOT NULL
        REFERENCES first_student(s_ID) ON DELETE CASCADE, att_date TEXT NOT NULL,
        status TEXT NOT NULL CHECK(status IN ('Present','Absent','Excused')),
        notes TEXT, UNIQUE(student_id,att_date))""", 'attendance')

    make_table("""CREATE TABLE activity_log(
        log_id INTEGER PRIMARY KEY AUTOINCREMENT, admin_username TEXT NOT NULL,
        action TEXT NOT NULL, target_table TEXT, target_id INTEGER, details TEXT,
        log_time TEXT DEFAULT (datetime('now','localtime')))""", 'activity_log')

    # أول أدمن يبقى superadmin
    cur.execute("UPDATE Admin SET role='superadmin' WHERE admin_ID=(SELECT MIN(admin_ID) FROM Admin)")
    if cur.rowcount:
        print("  ✚ First admin → superadmin")

    # تشفير الباسوردات القديمة
    for tbl, id_c, pw_c in [('Admin','admin_ID','admin_password'),('Account','ID','password')]:
        cur.execute(f"SELECT {id_c},{pw_c} FROM {tbl}")
        for rid, pwd in cur.fetchall():
            if len(pwd) != 64:
                cur.execute(f"UPDATE {tbl} SET {pw_c}=? WHERE {id_c}=?", (hash_password(pwd), rid))
                print(f"  🔒 {tbl} ID={rid}")

    con.commit()
    con.close()
    print("✅  Migration done.")


def log_action(admin_username, action, target_table=None, target_id=None, details=None):
    try:
        con = sqlite3.connect('school.db')
        cur = con.cursor()
        cur.execute("INSERT INTO activity_log(admin_username,action,target_table,target_id,details) VALUES(?,?,?,?,?)",
                    (admin_username, action, target_table, target_id, details))
        con.commit()
        con.close()
    except Exception:
        pass


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--migrate':
        migrate_existing_db()
    else:
        create_db()
