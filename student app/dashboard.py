from customtkinter import *
from tkinter import *
from PIL import Image
from time import strftime
import sqlite3
from tkinter import messagebox

import statisticspage
import adminpage
import studentspage
import teacherspage
from auth import session, get_role_display
from create_db import log_action


class DashboardClass():
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x690+100+5')
        self.root.title('Dashboard Page')
        self.root.config(bg='white')
        self.root.resizable(False, False)

        def date():
            date_1 = strftime('%I:%M:%S %p \t %A \t %b/%d/%Y')
            date_lbl.config(text=date_1)
            date_lbl.after(1000, date)

        # ============================== head frame ==========================
        up_frame = CTkFrame(root, width=1199, height=70, bg_color='#F6F5F5',
                            fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        up_frame.place(x=1, y=1)

        text_lbl = Label(up_frame, text='Modern School', font=('courier', 18, 'bold'),
                         bg='#F6F5F5', fg='#DA7297')
        text_lbl.place(x=30, y=5, width=200, height=60)

        date_lbl = Label(up_frame, font=('courier', 18, 'bold'), bg='#F6F5F5', fg='#DA7297')
        date_lbl.place(x=590, y=5, width=570, height=60)
        date()

        # ---- Role Badge في الهيدر ----
        rd = get_role_display(session.role)
        role_badge = Label(up_frame, text=f"  {session.admin_name}  |  {rd['label']}  ",
                           font=('arial', 11, 'bold'),
                           bg=rd['bg'], fg=rd['fg'], relief='flat')
        role_badge.place(x=240, y=20)

        # ============================== main frame ==========================
        frame = CTkFrame(root, width=1197, height=615, bg_color='white',
                         fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        frame.place(x=1, y=72)

        menu_frame = CTkFrame(frame, width=200, height=608, fg_color='#DA7297',
                              bg_color='#F6F5F5', border_color='#DA7297')
        menu_frame.place(x=3, y=3)

        # ============================== page frame ==========================
        page_frame = CTkFrame(frame, width=980, height=605,
                              bg_color='#F6F5F5', fg_color='#F6F5F5')
        page_frame.place(x=210, y=5)

        # ============================== helpers =============================
        def hide_line():
            for lb in (home_line, note_line, ser_line, state_line):
                lb.config(bg='#DA7297')

        def delete_pages():
            for w in page_frame.winfo_children():
                w.destroy()

        def line(lb, page):
            hide_line()
            lb.config(bg='white')
            delete_pages()
            page()

        # ============================== open pages ==========================
        def open_admin_page():
            if not session.require("view_admin_page"):
                return
            win = Toplevel()
            adminpage.AdminClass(win, current_admin=session.admin_username)
            root.withdraw()
            win.deiconify()

        def open_students_page():
            if not session.require("view_students"):
                return
            win = Toplevel()
            studentspage.StudentsClass(win)
            root.withdraw()
            win.deiconify()

        def open_teachers_page():
            if not session.require("view_teachers"):
                return
            win = Toplevel()
            teacherspage.TeachersClass(win)
            root.withdraw()
            win.deiconify()

        def logout():
            if messagebox.askyesno("تسجيل الخروج", "هتسجّل خروج؟"):
                log_action(session.admin_username, "LOGOUT")
                session.logout()
                root.destroy()

        # ============================== menu buttons ========================
        home_img  = CTkImage(Image.open('images/home_icon.png'),    size=(38, 38))
        note_img  = CTkImage(Image.open('images/note.png'),          size=(42, 42))
        ser_img   = CTkImage(Image.open('images/services_icon.png'), size=(38, 38))
        state_img = CTkImage(Image.open('images/ll.png'),            size=(40, 40))
        close_img = CTkImage(Image.open('images/close.png'),         size=(28, 28))

        CTkButton(menu_frame, text='HOME', width=100, height=40,
                  fg_color='#DA7297', text_color='white', bg_color='#DA7297',
                  font=('arial', 20, 'bold'), hover_color='#DA7297',
                  border_color='#DA7297', image=home_img, border_width=2,
                  border_spacing=16, corner_radius=0,
                  command=lambda: line(lb=home_line, page=home_page)).place(x=0, y=100)
        home_line = Label(menu_frame, text='', bg='white')
        home_line.place(x=3, y=120, width=5, height=40)

        CTkButton(menu_frame, text='NOTE', width=100, height=40,
                  fg_color='#DA7297', text_color='white', bg_color='#DA7297',
                  font=('arial', 20, 'bold'), hover_color='#DA7297',
                  border_color='#DA7297', image=note_img, border_width=2,
                  border_spacing=16, corner_radius=0,
                  command=lambda: line(lb=note_line, page=note_page)).place(x=0, y=180)
        note_line = Label(menu_frame, text='', bg='#DA7297')
        note_line.place(x=3, y=200, width=5, height=40)

        CTkButton(menu_frame, text='SERVICES', width=100, height=40,
                  fg_color='#DA7297', text_color='white', bg_color='#DA7297',
                  font=('arial', 20, 'bold'), hover_color='#DA7297',
                  border_color='#DA7297', image=ser_img, border_width=2,
                  border_spacing=16, corner_radius=0,
                  command=lambda: line(lb=ser_line, page=ser_page)).place(x=5, y=250)
        ser_line = Label(menu_frame, text='', bg='#DA7297')
        ser_line.place(x=3, y=270, width=5, height=40)

        CTkButton(menu_frame, text='STATISTICS', width=100, height=40,
                  fg_color='#DA7297', text_color='white', bg_color='#DA7297',
                  font=('arial', 20, 'bold'), hover_color='#DA7297',
                  border_color='#DA7297', image=state_img, border_width=2,
                  border_spacing=16, corner_radius=0,
                  command=lambda: line(lb=state_line, page=sta_page)).place(x=5, y=320)
        state_line = Label(menu_frame, text='', bg='#DA7297')
        state_line.place(x=3, y=340, width=5, height=40)

        CTkButton(menu_frame, text='LOGOUT', width=100, height=40,
                  fg_color='#DA7297', text_color='white', bg_color='#DA7297',
                  font=('arial', 16, 'bold'), hover_color='#c0506e',
                  border_color='#DA7297', image=close_img, border_width=2,
                  border_spacing=16, corner_radius=0,
                  command=logout).place(x=3, y=390)

        # ============================== HOME PAGE ===========================
        def home_page():
            home_frame = CTkFrame(page_frame, width=975, height=600,
                                  bg_color='#F6F5F5', fg_color='#F6F5F5')
            home_frame.place(x=1, y=1)

            stu_img = CTkImage(Image.open('images/stu.png'),  size=(100, 100))
            te_img  = CTkImage(Image.open('images/tech.png'), size=(100, 100))
            emp_img = CTkImage(Image.open('images/emp.png'),  size=(100, 100))

            # Students — كل الـ roles تشوفه
            student_btn = CTkButton(
                home_frame, text='Students', width=250, height=200,
                fg_color='#DA7297', text_color='white', bg_color='#F6F5F5',
                font=('arial', 30, 'bold'), border_color='#D8D2C2',
                image=stu_img, compound='top', border_spacing=20,
                hover_color='#DA7297', border_width=5, corner_radius=30,
                command=open_students_page)
            student_btn.place(x=50, y=100)

            # Teachers — كل الـ roles تشوفه
            teachers_btn = CTkButton(
                home_frame, text='Teachers', width=250, height=200,
                fg_color='#DA7297', text_color='white', bg_color='#F6F5F5',
                font=('arial', 30, 'bold'), border_color='#D8D2C2',
                image=te_img, compound='top', border_spacing=20,
                hover_color='#DA7297', border_width=5, corner_radius=30,
                command=open_teachers_page)
            teachers_btn.place(x=350, y=100)

            # Admin Page — superadmin فقط
            admin_btn = CTkButton(
                home_frame, text='Admin', width=250, height=200,
                fg_color='#DA7297' if session.can("view_admin_page") else '#aaaaaa',
                text_color='white', bg_color='#F6F5F5',
                font=('arial', 30, 'bold'), border_color='#D8D2C2',
                image=emp_img, compound='top', border_spacing=20,
                hover_color='#DA7297' if session.can("view_admin_page") else '#aaaaaa',
                border_width=5, corner_radius=30,
                command=open_admin_page)
            admin_btn.place(x=650, y=100)

            # ---- تلميح تحت الزراير المعطّلة ----
            if not session.can("view_admin_page"):
                Label(home_frame,
                      text="🔒 superadmin only",
                      bg='#F6F5F5', fg='#aaaaaa',
                      font=('arial', 10)).place(x=680, y=310)

        # ============================== NOTE PAGE ===========================
        def note_page():
            nf = CTkFrame(page_frame, width=975, height=600,
                          bg_color='#F6F5F5', fg_color='#F6F5F5')
            nf.place(x=1, y=1)
            Label(nf, text='Note Page', font=('arial', 20, 'bold'),
                  bg='#F6F5F5', fg='#DA7297').pack(pady=20)

        # ============================== SERVICES PAGE =======================
        def ser_page():
            sf = CTkFrame(page_frame, width=975, height=600,
                          bg_color='#F6F5F5', fg_color='#F6F5F5')
            sf.place(x=1, y=1)
            Label(sf, text='Services Page', font=('arial', 20, 'bold'),
                  bg='#F6F5F5', fg='#DA7297').pack(pady=20)

        # ============================== STATISTICS PAGE =====================
        def sta_page():
            if not session.require("view_statistics"):
                return
            sta_frame = CTkFrame(page_frame, width=975, height=600,
                                 bg_color='#F6F5F5', fg_color='#F6F5F5')
            sta_frame.place(x=1, y=1)

            def safe_count(conn, table_name):
                try:
                    cur = conn.cursor()
                    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                    r = cur.fetchone()
                    return r[0] if r else 0
                except Exception:
                    return 0

            def detect_table(conn, candidates):
                cur = conn.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
                existing = [r[0].lower() for r in cur.fetchall()]
                for c in candidates:
                    if c and c.lower() in existing:
                        return c
                return None

            def update_count():
                try:
                    con = sqlite3.connect('school.db')
                    students = safe_count(con, detect_table(con, ['first_student']) or 'first_student')
                    teachers = safe_count(con, detect_table(con, ['teachers'])       or 'teachers')
                    employees= safe_count(con, detect_table(con, ['employee','employees']) or '')
                    admins   = safe_count(con, detect_table(con, ['admin'])           or 'Admin')
                    accounts = safe_count(con, detect_table(con, ['account'])         or 'Account')
                    islamic  = safe_count(con, detect_table(con, ['islamic_marks'])   or 'islamic_marks')
                    arabic   = safe_count(con, detect_table(con, ['arabic_marks'])    or 'arabic_marks')
                    attendance = safe_count(con, detect_table(con, ['attendance'])    or 'attendance')
                    con.close()

                    lbl_students.config(text=f"Total Students\n[ {students} ]")
                    lbl_islamic.config(text=f"Islamic Marks\n[ {islamic} ]")
                    lbl_arabic.config(text=f"Arabic Marks\n[ {arabic} ]")
                    lbl_teachers.config(text=f"Total Teachers\n[ {teachers} ]")
                    lbl_employees.config(text=f"Total Employees\n[ {employees} ]")
                    lbl_admins.config(text=f"Total Admins\n[ {admins} ]")
                    lbl_accounts.config(text=f"Total Accounts\n[ {accounts} ]")
                    lbl_attendance.config(text=f"Attendance Records\n[ {attendance} ]")
                except Exception as ex:
                    messagebox.showerror("Error", str(ex))

            cw, ch, gx, gy, sx, sy = 295, 130, 20, 15, 30, 35
            cards = []
            for i, (var_name, default) in enumerate([
                ("lbl_students",  "Total Students\n[ 0 ]"),
                ("lbl_islamic",   "Islamic Marks\n[ 0 ]"),
                ("lbl_arabic",    "Arabic Marks\n[ 0 ]"),
                ("lbl_teachers",  "Total Teachers\n[ 0 ]"),
                ("lbl_employees", "Total Employees\n[ 0 ]"),
                ("lbl_admins",    "Total Admins\n[ 0 ]"),
                ("lbl_accounts",  "Total Accounts\n[ 0 ]"),
                ("lbl_attendance","Attendance Records\n[ 0 ]"),
            ]):
                row, col = divmod(i, 3)
                x = sx + col * (cw + gx)
                y = sy + row * (ch + gy)
                lbl = Label(sta_frame, text=default, bd=5, relief=RIDGE,
                            bg='#DA7297', fg='white',
                            font=('goudy old style', 18, 'bold'))
                lbl.place(x=x, y=y, width=cw, height=ch)
                locals()[var_name] = lbl

            # نسخ المتغيرات المحلية للـ update_count
            lbl_students   = locals()['lbl_students']
            lbl_islamic    = locals()['lbl_islamic']
            lbl_arabic     = locals()['lbl_arabic']
            lbl_teachers   = locals()['lbl_teachers']
            lbl_employees  = locals()['lbl_employees']
            lbl_admins     = locals()['lbl_admins']
            lbl_accounts   = locals()['lbl_accounts']
            lbl_attendance = locals()['lbl_attendance']

            CTkButton(sta_frame, text="REFRESH", fg_color="#DA7297", width=160, height=42,
                      text_color="white", font=("Arial", 14, "bold"),
                      command=update_count).place(x=400, y=440)
            update_count()

        # ============================== START ===============================
        home_page()


if __name__ == "__main__":
    root = Tk()
    DashboardClass(root)
    root.mainloop()
