from customtkinter import *
from tkinter import *
from tkinter import messagebox
from time import strftime
import sqlite3
import dashboard


class StatisticsClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('980x570+100+60')
        self.root.title('Statistics')
        self.root.config(bg='white')
        self.root.resizable(False, False)

        def date():
            date_lbl.config(text=strftime('%I:%M:%S %p  -  %A  -  %d/%m/%Y'))
            date_lbl.after(1000, date)

        # ---- head ----
        head = CTkFrame(root, width=978, height=70, fg_color='#F6F5F5',
                        border_color='#DA7297', border_width=2)
        head.place(x=1, y=1)

        Label(head, text='Statistics', font=('courier', 20, 'bold'),
              bg='#F6F5F5', fg='#DA7297').place(x=20, y=10)

        date_lbl = Label(head, font=('courier', 12, 'bold'),
                         bg='#F6F5F5', fg='#DA7297')
        date_lbl.place(x=370, y=10, width=580, height=50)
        date()

        def back():
            win = Toplevel()
            dashboard.DashboardClass(win)
            root.withdraw()
            win.deiconify()

        CTkButton(head, text='←', width=70, height=64, fg_color='#DA7297',
                  text_color='white', font=('arial', 20, 'bold'),
                  corner_radius=0, command=back).place(x=2, y=3)

        # ---- main frame ----
        frame = CTkFrame(root, width=976, height=488, fg_color='white',
                         border_color='#DA7297', border_width=2)
        frame.place(x=1, y=72)

        # ---- counters ----
        self.vars = {k: StringVar() for k in [
            'students', 'teachers', 'admins', 'accounts',
            'civic', 'arabic', 'english', 'social',
            'math', 'chemistry', 'physics', 'biology',
            'attendance',
        ]}

        def safe_count(conn, table):
            try:
                cur = conn.cursor()
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                r = cur.fetchone()
                return r[0] if r else 0
            except Exception:
                return 0

        def table_exists(cur, name):
            cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND LOWER(name)=?",
                (name.lower(),))
            return bool(cur.fetchone())

        def refresh():
            try:
                con = sqlite3.connect('school.db')
                cur = con.cursor()

                self.vars['students'].set(
                    str(safe_count(con, 'first_student') if table_exists(cur, 'first_student') else 0))
                self.vars['teachers'].set(
                    str(safe_count(con, 'teachers') if table_exists(cur, 'teachers') else 0))
                self.vars['admins'].set(
                    str(safe_count(con, 'Admin') if table_exists(cur, 'Admin') else 0))
                self.vars['accounts'].set(
                    str(safe_count(con, 'Account') if table_exists(cur, 'Account') else 0))
                self.vars['attendance'].set(
                    str(safe_count(con, 'attendance') if table_exists(cur, 'attendance') else 0))

                # جداول الدرجات — civic بدل islamic
                marks_map = {
                    'civic':     'civic_education_marks',
                    'arabic':    'arabic_marks',
                    'english':   'english_marks',
                    'social':    'social_marks',
                    'math':      'math_marks',
                    'chemistry': 'chemistry_marks',
                    'physics':   'physics_marks',
                    'biology':   'biology_marks',
                }
                for key, tbl in marks_map.items():
                    cnt = safe_count(con, tbl) if table_exists(cur, tbl) else 0
                    self.vars[key].set(str(cnt))

                con.close()
            except Exception as ex:
                messagebox.showerror("Error", str(ex))

        # ---- cards layout ----
        cw, ch = 210, 95
        gx, gy = 15, 12

        cards = [
            # row 1 — people
            ('students',   'Total Students',      '#DA7297', 0, 0),
            ('teachers',   'Total Teachers',      '#DA7297', 1, 0),
            ('admins',     'Total Admins',        '#DA7297', 2, 0),
            ('accounts',   'Total Accounts',      '#DA7297', 3, 0),
            # row 2 — marks group 1
            ('civic',      'Civic Education',     '#8B0000', 0, 1),
            ('arabic',     'Arabic Marks',        '#8B0000', 1, 1),
            ('english',    'English Marks',       '#8B0000', 2, 1),
            ('social',     'Social Studies',      '#8B0000', 3, 1),
            # row 3 — marks group 2
            ('math',       'Mathematics',         '#c0506e', 0, 2),
            ('chemistry',  'Chemistry',           '#c0506e', 1, 2),
            ('physics',    'Physics',             '#c0506e', 2, 2),
            ('biology',    'Biology',             '#c0506e', 3, 2),
            # row 4 — attendance (wide)
            ('attendance', 'Attendance Records',  '#555555', 0, 3),
        ]

        sx, sy = 18, 12
        for key, title, color, col, row in cards:
            x = sx + col * (cw + gx)
            y = sy + row * (ch + gy)
            # attendance card wider
            w = cw * 2 + gx if key == 'attendance' else cw

            card = Frame(frame, bg=color, bd=0, relief='flat')
            card.place(x=x, y=y, width=w, height=ch)

            Label(card, text=title, bg=color, fg='white',
                  font=('arial', 11, 'bold')).place(x=8, y=6)
            Label(card, textvariable=self.vars[key], bg=color, fg='white',
                  font=('arial', 28, 'bold')).place(x=8, y=32)

        # ---- refresh button ----
        CTkButton(frame, text='🔄  REFRESH', width=160, height=40,
                  fg_color='#DA7297', text_color='white',
                  font=('arial', 14, 'bold'),
                  command=refresh).place(x=780, y=430)

        refresh()
