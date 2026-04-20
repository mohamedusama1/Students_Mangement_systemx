# statisticspage.py
from customtkinter import *
from tkinter import *
from tkinter import messagebox
from time import strftime
import sqlite3
import dashboard

class StatisticsClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('900x520+150+80')
        self.root.title('Statistics')
        self.root.config(bg='white')
        self.root.resizable(False, False)

        def date():
            date_1 = strftime('%I:%M:%S %p  -  %A  -  %d/%m/%Y')
            date_lbl.config(text=date_1)
            date_lbl.after(1000, date)

        # header
        head = CTkFrame(root, width=898, height=70, fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        head.place(x=1, y=1)
        title = Label(head, text='Statistics', font=('Corier', 20, 'bold'), bg='#F6F5F5', fg='#DA7297')
        title.place(x=20, y=10)
        date_lbl = Label(head, font=('corier', 12, 'bold'), bg='#F6F5F5', fg='#DA7297')
        date_lbl.place(x=480, y=10, width=380, height=50)
        date()

        # back button
        def back():
            win = Toplevel()
            dashboard.DashboardClass(win)
            root.withdraw()
            win.deiconify()

        back_btn = CTkButton(head, text='←', width=70, height=64, fg_color='#DA7297',
                             text_color='white', font=('arial', 20, 'bold'),
                             corner_radius=0, command=back)
        back_btn.place(x=2, y=3)

        # main frame
        frame = CTkFrame(root, width=896, height=430, fg_color='white', border_color='#DA7297', border_width=2)
        frame.place(x=1, y=72)

        # vars to display counts
        self.total_students = StringVar()
        self.total_teachers = StringVar()
        self.total_admins = StringVar()
        self.total_physics_marks = StringVar()
        self.total_english_marks = StringVar()
        self.total_accounts = StringVar()

        # helper: safe count query (returns int)
        def safe_count(conn, table_name):
            try:
                cur = conn.cursor()
                cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                return cur.fetchone()[0] or 0
            except Exception:
                return 0

        # detect possible marks table names
        def detect_table_names(conn):
            cur = conn.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            rows = [r[0].lower() for r in cur.fetchall()]
            # return detected names or defaults
            physics = None
            english = None
            if 'physics_marks' in rows:
                physics = 'physics_marks'
            elif 'islamic_marks' in rows:
                # user earlier used islamic; treat as physics per request mapping
                physics = 'islamic_marks'

            if 'english_marks' in rows:
                english = 'english_marks'
            elif 'arabic_marks' in rows:
                # user earlier used arabic; treat as english per mapping
                english = 'arabic_marks'

            return physics, english

        def refresh_stats():
            try:
                con = sqlite3.connect('school.db')
                cur = con.cursor()

                # Students
                # possible table name: first_student or firststudent
                student_tables = ['first_student', 'firststudent', 'students']
                students_count = 0
                for t in student_tables:
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND LOWER(name)=?", (t.lower(),))
                    if cur.fetchone():
                        students_count = safe_count(con, t)
                        break

                # Teachers
                teacher_tables = ['teachers', 'teacher']
                teachers_count = 0
                for t in teacher_tables:
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND LOWER(name)=?", (t.lower(),))
                    if cur.fetchone():
                        teachers_count = safe_count(con, t)
                        break

                # Admins
                admin_tables = ['admin', 'admins', 'adminpage', 'admin_table']
                admins_count = 0
                for t in admin_tables:
                    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND LOWER(name)=?", (t.lower(),))
                    if cur.fetchone():
                        admins_count = safe_count(con, t)
                        break

                # Accounts
                accounts_count = 0
                cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND LOWER(name)='account'")
                if cur.fetchone():
                    accounts_count = safe_count(con, 'Account') if safe_count(con, 'Account') else safe_count(con, 'account')

                # Marks (physics / english) detection
                physics_table, english_table = detect_table_names(con)
                physics_count = safe_count(con, physics_table) if physics_table else 0
                english_count = safe_count(con, english_table) if english_table else 0

                # update vars
                self.total_students.set(str(students_count))
                self.total_teachers.set(str(teachers_count))
                self.total_admins.set(str(admins_count))
                self.total_accounts.set(str(accounts_count))
                self.total_physics_marks.set(str(physics_count))
                self.total_english_marks.set(str(english_count))

                con.close()
            except Exception as ex:
                messagebox.showerror("Error", f"Failed to load statistics:\n{str(ex)}")

        # layout cards
        card_w = 260
        card_h = 110
        pad_x = 40
        pad_y = 28

        def make_card(x, y, title, var, color='#DA7297'):
            c = CTkFrame(frame, width=card_w, height=card_h, fg_color=color, corner_radius=8)
            c.place(x=x, y=y)
            lbl_title = Label(c, text=title, bg=color, fg='white', font=('arial', 12, 'bold'))
            lbl_title.place(x=10, y=8)
            lbl_value = Label(c, textvariable=var, bg=color, fg='white', font=('arial', 30, 'bold'))
            lbl_value.place(x=10, y=35)
            return c

        # top row
        make_card(pad_x, pad_y, 'Total Students', self.total_students)
        make_card(pad_x + card_w + 20, pad_y, 'Total Teachers', self.total_teachers)
        make_card(pad_x + 2*(card_w + 20), pad_y, 'Total Admins', self.total_admins)

        # second row
        make_card(pad_x, pad_y + card_h + 20, 'Physics Marks Records', self.total_physics_marks)
        make_card(pad_x + card_w + 20, pad_y + card_h + 20, 'English Marks Records', self.total_english_marks)
        make_card(pad_x + 2*(card_w + 20), pad_y + card_h + 20, 'Total Accounts', self.total_accounts)

        # refresh button
        refresh_btn = CTkButton(frame, text='REFRESH', width=140, height=36, fg_color='#DA7297', command=refresh_stats)
        refresh_btn.place(x=frame.winfo_reqwidth() - 180, y=frame.winfo_reqheight() - 60)

        # initial load
        refresh_stats()
