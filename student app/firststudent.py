"""
firststudent.py
===============
Flow:
  1. FirstStudentClass  → جدول كل الطلاب + بحث + CRUD للطالب
  2. لما تضغط "View Marks" على طالب → فتح صفحة الدرجات الـ 8 مواد
"""

from customtkinter import *
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image
from time import strftime
import sqlite3

import dashboard
from auth import session
from create_db import log_action

# ============================================================
#  SUBJECTS & COLUMNS
# ============================================================
SUBJECTS = [
    ("civic_education_marks", "Civic Education"),
    ("arabic_marks",          "Arabic"),
    ("english_marks",         "English"),
    ("social_marks",          "Social Studies"),
    ("math_marks",            "Mathematics"),
    ("chemistry_marks",       "Chemistry"),
    ("physics_marks",         "Physics"),
    ("biology_marks",         "Biology"),
]

MARKS_COLS = [
    "student_id", "student_name",
    "st_month", "nd_month", "chapter1", "half_year",
    "st_month1", "nd_month2", "chapter2", "chapter3",
    "final_exam", "final_result"
]

MARKS_HEADINGS = {
    "student_id": "ID", "student_name": "Student Name",
    "st_month": "1st Month", "nd_month": "2nd Month",
    "chapter1": "Chapter 1", "half_year": "Half Year",
    "st_month1": "1st Month", "nd_month2": "2nd Month",
    "chapter2": "Chapter 2", "chapter3": "Chapter 3",
    "final_exam": "Final Exam", "final_result": "Final Result",
}

MARKS_WIDTHS = {
    "student_id": 55, "student_name": 160,
    "st_month": 72, "nd_month": 72, "chapter1": 72, "half_year": 78,
    "st_month1": 72, "nd_month2": 72, "chapter2": 72, "chapter3": 72,
    "final_exam": 78, "final_result": 100,
}

STU_COLS = ["s_ID", "student_name", "student_gender", "student_age",
            "address", "contact", "final_result"]
STU_HEADINGS = {
    "s_ID": "ID", "student_name": "Student Name",
    "student_gender": "Gender", "student_age": "Age",
    "address": "Address", "contact": "Contact",
    "final_result": "Result",
}
STU_WIDTHS = {
    "s_ID": 50, "student_name": 180, "student_gender": 70,
    "student_age": 50, "address": 200, "contact": 120, "final_result": 80,
}


# ============================================================
#  MIGRATION — run on startup
# ============================================================
import os as _os

def _get_db_path():
    """يجيب مسار school.db من نفس فولدر الـ script"""
    here = _os.path.dirname(_os.path.abspath(__file__))
    return _os.path.join(here, 'school.db')

DB_PATH = _get_db_path()


def _ensure_tables(con):
    """migration آمن — بيتجاهل أي خطأ write permission"""
    try:
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys = ON")

        # rename islamic → civic أولاً
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='islamic_marks'")
        if cur.fetchone():
            try:
                cur.execute("ALTER TABLE islamic_marks RENAME TO civic_education_marks")
            except Exception:
                pass

        for table, _ in SUBJECTS:
            try:
                cur.execute(f"""
                    CREATE TABLE IF NOT EXISTS {table}(
                        m_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER REFERENCES first_student(s_ID)
                                   ON DELETE CASCADE ON UPDATE CASCADE,
                        student_name TEXT,
                        st_month REAL DEFAULT 0, nd_month REAL DEFAULT 0,
                        chapter1 REAL DEFAULT 0, half_year REAL DEFAULT 0,
                        st_month1 REAL DEFAULT 0, nd_month2 REAL DEFAULT 0,
                        chapter2 REAL DEFAULT 0, chapter3 REAL DEFAULT 0,
                        final_exam REAL DEFAULT 0, final_result TEXT DEFAULT 'Pending'
                    )""")
                cur.execute(f"PRAGMA table_info({table})")
                if "student_id" not in [r[1] for r in cur.fetchall()]:
                    cur.execute(f"ALTER TABLE {table} ADD COLUMN student_id INTEGER")
            except Exception:
                pass

        # أضف is_active لو مش موجود
        try:
            cur.execute("PRAGMA table_info(first_student)")
            fs_cols = [r[1] for r in cur.fetchall()]
            if "is_active" not in fs_cols:
                cur.execute("ALTER TABLE first_student ADD COLUMN is_active INTEGER DEFAULT 1")
                cur.execute("UPDATE first_student SET is_active=1")
            if "repeated_years" not in fs_cols:
                cur.execute("ALTER TABLE first_student ADD COLUMN repeated_years INTEGER DEFAULT 0")
        except Exception:
            pass

        con.commit()
    except Exception:
        pass  # readonly DB — الصفحة هتشتغل بدون migration


# ============================================================
#  SCREEN 1 — قائمة الطلاب
# ============================================================
class FirstStudentClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x690+80+20')
        self.root.title('First Grade — Students')
        self.root.config(bg='white')
        self.root.resizable(False, False)

        # migration
        con = sqlite3.connect(DB_PATH)
        _ensure_tables(con)
        con.close()

        # ==================== HEAD ====================
        up_frame = CTkFrame(root, width=1199, height=70, bg_color='#F6F5F5',
                            fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        up_frame.place(x=1, y=1)

        Label(up_frame, text='First Grade — Students',
              font=('courier', 18, 'bold'),
              bg='#F6F5F5', fg='#DA7297').place(x=150, y=5, width=320, height=60)

        self._date_lbl = Label(up_frame, font=('courier', 13, 'bold'),
                               bg='#F6F5F5', fg='#DA7297')
        self._date_lbl.place(x=580, y=5, width=580, height=60)
        self._tick()

        def back():
            import studentspage
            win = Toplevel()
            studentspage.StudentsClass(win)
            root.withdraw()
            win.deiconify()

        CTkButton(up_frame, text='←', width=100, height=68,
                  fg_color='#DA7297', text_color='white', bg_color='#F6F5F5',
                  font=('arial', 30, 'bold'), hover_color='#DA7297',
                  corner_radius=0, command=back).place(x=2, y=2)

        # ==================== MAIN ====================
        main = CTkFrame(root, width=1197, height=615, bg_color='white',
                        fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        main.place(x=1, y=72)

        # ---- Variables ----
        self.var_id     = StringVar()
        self.var_name   = StringVar()
        self.var_gender = StringVar()
        self.var_age    = StringVar()
        self.var_addr   = StringVar()
        self.var_cont   = StringVar()
        self.var_result = StringVar()
        self.var_search = StringVar()

        # ==================== ENTRY FIELDS ====================
        fields = [
            ("Name",   self.var_name,   30,  10),
            ("Gender", self.var_gender, 200, 10),
            ("Age",    self.var_age,    330, 10),
            ("Contact",self.var_cont,   430, 10),
            ("Address",self.var_addr,   620, 10),
            ("Result", self.var_result, 870, 10),
        ]
        for lbl_t, var, x, y in fields:
            Label(main, text=lbl_t, font=('arial', 11, 'bold'),
                  bg='#F6F5F5', fg='gray').place(x=x, y=y)
            w = 140 if lbl_t in ("Address",) else 90 if lbl_t == "Name" else \
                80 if lbl_t == "Contact" else 60
            # name wider
            if lbl_t == "Name": w = 150
            if lbl_t == "Address": w = 220
            if lbl_t == "Contact": w = 130
            CTkEntry(main, textvariable=var, width=w, height=30,
                     font=('arial', 11), border_color='#DA7297',
                     justify='center').place(x=x, y=y + 22)

        # ID (readonly)
        Label(main, text='ID', font=('arial', 11, 'bold'),
              bg='#F6F5F5', fg='gray').place(x=5, y=10)
        CTkEntry(main, textvariable=self.var_id, width=45, height=30,
                 font=('arial', 11), border_color='gray',
                 state='readonly', justify='center').place(x=5, y=32)

        # ==================== CRUD BUTTONS ====================
        for text, cmd, x, perm in [
            ("ADD",    self._add,    30,  "add_student"),
            ("UPDATE", self._update, 160, "update_student"),
            ("DELETE", self._delete, 290, "delete_student"),
            ("CLEAR",  self._clear,  420, None),
        ]:
            state = 'normal' if (perm is None or session.can(perm)) else 'disabled'
            CTkButton(main, text=text, width=120, height=35,
                      fg_color='#DA7297' if state == 'normal' else '#aaa',
                      text_color='white', font=('arial', 12, 'bold'),
                      corner_radius=8, state=state,
                      command=cmd).place(x=x, y=68)

        # ==================== SEARCH ====================
        sf = CTkFrame(main, width=750, height=44, fg_color='white',
                      bg_color='#F6F5F5', border_color='#DA7297', border_width=1)
        sf.place(x=560, y=62)

        Label(sf, text='Search:', font=('arial', 12, 'bold'),
              bg='white', fg='#DA7297').place(x=8, y=10)

        self.cmb_search = CTkComboBox(
            sf,
            values=["student_name", "student_gender", "final_result", "contact"],
            button_color='#DA7297', button_hover_color='#DA7297',
            justify=CENTER, font=('arial', 12), width=160, height=32,
            fg_color='white', border_color='#DA7297',
            dropdown_fg_color='white', dropdown_text_color='#DA7297')
        self.cmb_search.set("Select")
        self.cmb_search.place(x=75, y=6)

        CTkEntry(sf, textvariable=self.var_search, width=180, height=32,
                 fg_color='white', border_color='#DA7297',
                 justify='center').place(x=248, y=6)

        CTkButton(sf, text='SEARCH', width=120, height=34,
                  fg_color='#DA7297', text_color='white',
                  font=('arial', 12, 'bold'), corner_radius=6,
                  command=self._search).place(x=440, y=5)

        CTkButton(sf, text='SHOW ALL', width=110, height=34,
                  fg_color='#555', text_color='white',
                  font=('arial', 12, 'bold'), corner_radius=6,
                  command=self._show).place(x=574, y=5)

        # ==================== TREEVIEW ====================
        tree_f = Frame(main, bg='gray')
        tree_f.place(x=3, y=115, width=1188, height=490)

        style = ttk.Style(); style.theme_use('clam')
        style.configure('Treeview', font=('arial', 11), rowheight=30,
                        fieldbackground='white')
        style.configure('Treeview.Heading', background='#DA7297',
                        foreground='white', font=('arial', 11, 'bold'))

        # extra column للزرار
        all_cols = STU_COLS + ["marks_btn"]
        scy = Scrollbar(tree_f); scy.pack(side=RIGHT, fill=Y)
        scx = Scrollbar(tree_f, orient=HORIZONTAL); scx.pack(side=BOTTOM, fill=X)

        self.tree = ttk.Treeview(tree_f, columns=all_cols, show='headings',
                                 yscrollcommand=scy.set, xscrollcommand=scx.set)
        scy.config(command=self.tree.yview)
        scx.config(command=self.tree.xview)

        for col in STU_COLS:
            self.tree.heading(col, text=STU_HEADINGS[col], anchor='center')
            self.tree.column(col, width=STU_WIDTHS[col], anchor='center')

        self.tree.heading("marks_btn", text="📊 Marks", anchor='center')
        self.tree.column("marks_btn", width=100, anchor='center')

        self.tree.tag_configure('evenrow', background='#F6F5F5')
        self.tree.tag_configure('oddrow',  background='#ffe0eb')
        self.tree.pack(fill=BOTH, expand=1)

        self.tree.bind('<ButtonRelease-1>', self._on_click)

        self._show()

    # ---- tick ----
    def _tick(self):
        self._date_lbl.config(text=strftime('%I:%M:%S %p      %A      %b/%d/%Y'))
        self.root.after(1000, self._tick)

    # ---- DB ----
    def _con(self):
        con = sqlite3.connect(DB_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        return con

    # ---- Show ----
    def _show(self):
        con = self._con(); cur = con.cursor()
        try:
            cur.execute("""
                SELECT s_ID, student_name, student_gender, student_age,
                       address, contact, final_result
                FROM first_student WHERE COALESCE(is_active,1)=1
                ORDER BY s_ID
            """)
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for i, row in enumerate(rows):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                # أضف عمود الزرار
                self.tree.insert('', END, values=list(row) + ["📊 View Marks"],
                                 tags=(tag,))
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))
        finally:
            con.close()

    # ---- Click handler ----
    def _on_click(self, ev):
        item = self.tree.focus()
        row  = self.tree.item(item)['values']
        if not row: return

        col_id = self.tree.identify_column(ev.x)
        col_idx = int(col_id.replace('#', '')) - 1

        # عمود "View Marks" هو آخر عمود
        if col_idx == len(STU_COLS):
            self._open_marks_page(row)
        else:
            # ملء الـ fields للتعديل
            self.var_id.set(str(row[0]))
            self.var_name.set(str(row[1]))
            self.var_gender.set(str(row[2]))
            self.var_age.set(str(row[3]))
            self.var_addr.set(str(row[4]))
            self.var_cont.set(str(row[5]))
            self.var_result.set(str(row[6]))

    # ---- Open marks page ----
    def _open_marks_page(self, row):
        sid  = row[0]
        name = row[1]
        win  = Toplevel()
        win.grab_set()
        MarksPageClass(win, sid, name, self.root)

    # ==================== CRUD ====================
    def _add(self):
        if not session.require("add_student"): return
        name = self.var_name.get().strip()
        if not name:
            messagebox.showerror("خطأ", "اسم الطالب مطلوب."); return
        try:
            con = self._con(); cur = con.cursor()
            cur.execute("""
                INSERT INTO first_student
                (student_name, student_gender, student_age,
                 address, contact, final_result, is_active)
                VALUES(?,?,?,?,?,?,1)
            """, (name, self.var_gender.get(), self.var_age.get() or 0,
                  self.var_addr.get(), self.var_cont.get(),
                  self.var_result.get() or 'Pending'))
            new_id = cur.lastrowid
            con.commit(); con.close()
            log_action(session.admin_username, "ADD_STUDENT",
                       "first_student", new_id, f"Name:{name}")
            self._show(); self._clear()
            messagebox.showinfo("تم", "تمت إضافة الطالب.")
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))

    def _update(self):
        if not session.require("update_student"): return
        if not self.var_id.get():
            messagebox.showerror("خطأ", "اختار طالب من الجدول."); return
        try:
            con = self._con(); cur = con.cursor()
            cur.execute("""
                UPDATE first_student
                SET student_name=?, student_gender=?, student_age=?,
                    address=?, contact=?, final_result=?
                WHERE s_ID=?
            """, (self.var_name.get(), self.var_gender.get(),
                  self.var_age.get() or 0, self.var_addr.get(),
                  self.var_cont.get(), self.var_result.get() or 'Pending',
                  self.var_id.get()))
            con.commit(); con.close()
            log_action(session.admin_username, "UPDATE_STUDENT",
                       "first_student", int(self.var_id.get()),
                       f"Name:{self.var_name.get()}")
            self._show(); self._clear()
            messagebox.showinfo("تم", "تم التعديل.")
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))

    def _delete(self):
        if not session.require("delete_student"): return
        if not self.var_id.get():
            messagebox.showerror("خطأ", "اختار طالب من الجدول."); return
        if not messagebox.askyesno("تأكيد",
                f"هتحذف الطالب: {self.var_name.get()}؟"):
            return
        try:
            con = self._con(); cur = con.cursor()
            cur.execute("UPDATE first_student SET is_active=0 WHERE s_ID=?",
                        (self.var_id.get(),))
            con.commit(); con.close()
            log_action(session.admin_username, "DELETE_STUDENT",
                       "first_student", int(self.var_id.get()),
                       f"Name:{self.var_name.get()}")
            self._show(); self._clear()
            messagebox.showinfo("تم", "تم الحذف.")
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))

    def _clear(self):
        for v in (self.var_id, self.var_name, self.var_gender,
                  self.var_age, self.var_addr, self.var_cont,
                  self.var_result, self.var_search):
            v.set("")
        self.cmb_search.set("Select")

    def _search(self):
        col = self.cmb_search.get()
        val = self.var_search.get().strip()
        ALLOWED = {"student_name", "student_gender", "final_result", "contact"}
        if col not in ALLOWED:
            messagebox.showerror("خطأ", "اختار عمود بحث."); return
        if not val:
            messagebox.showerror("خطأ", "أدخل قيمة البحث."); return
        try:
            con = self._con(); cur = con.cursor()
            cur.execute(f"""
                SELECT s_ID, student_name, student_gender, student_age,
                       address, contact, final_result
                FROM first_student
                WHERE {col} LIKE ? AND COALESCE(is_active,1)=1
            """, (f'%{val}%',))
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for i, row in enumerate(rows):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert('', END,
                                 values=list(row) + ["📊 View Marks"],
                                 tags=(tag,))
            con.close()
            if not rows:
                messagebox.showinfo("بحث", "لا توجد نتائج.")
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))


# ============================================================
#  SCREEN 2 — درجات طالب واحد (8 مواد)
# ============================================================
class MarksPageClass:
    def __init__(self, root, student_id, student_name, parent_root):
        self.root         = root
        self.student_id   = student_id
        self.student_name = student_name
        self.parent_root  = parent_root

        root.geometry('1300x700+60+20')
        root.title(f'Marks — {student_name}')
        root.config(bg='white')
        root.resizable(False, False)

        # HEAD
        up = CTkFrame(root, width=1299, height=70, bg_color='#F6F5F5',
                      fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        up.place(x=1, y=1)

        Label(up, text=f'Marks:  {student_name}  (ID: {student_id})',
              font=('courier', 16, 'bold'),
              bg='#F6F5F5', fg='#DA7297').place(x=150, y=5, width=700, height=60)

        self._date_lbl = Label(up, font=('courier', 12, 'bold'),
                               bg='#F6F5F5', fg='#DA7297')
        self._date_lbl.place(x=870, y=10, width=390, height=50)
        self._tick()

        def back():
            root.destroy()

        CTkButton(up, text='←', width=100, height=68,
                  fg_color='#DA7297', text_color='white', bg_color='#F6F5F5',
                  font=('arial', 30, 'bold'), hover_color='#DA7297',
                  corner_radius=0, command=back).place(x=2, y=2)

        # SUBJECT BUTTONS
        btn_f = CTkFrame(root, width=1299, height=55,
                         fg_color='#DA7297', bg_color='white')
        btn_f.place(x=1, y=72)

        self._subject_btns = {}
        for i, (table, label) in enumerate(SUBJECTS):
            text = label.replace(" ", "\n") if len(label) > 10 else label
            btn = CTkButton(
                btn_f, text=text, width=148, height=53,
                fg_color='#DA7297', text_color='white', bg_color='#DA7297',
                font=('arial', 11, 'bold'), hover_color='#8B0000',
                corner_radius=0,
                command=lambda t=table, lbl=label: self._switch(t, lbl))
            btn.place(x=i * 150, y=1)
            self._subject_btns[table] = btn

        # CONTENT
        self._content = CTkFrame(root, width=1297, height=570,
                                 fg_color='#F6F5F5', bg_color='white',
                                 border_color='#DA7297', border_width=2)
        self._content.place(x=1, y=128)

        # افتح أول مادة
        self._switch(*SUBJECTS[0])

    def _tick(self):
        self._date_lbl.config(text=strftime('%I:%M:%S %p  %b/%d/%Y'))
        self.root.after(1000, self._tick)

    def _switch(self, table, label):
        for t, btn in self._subject_btns.items():
            btn.configure(fg_color='#8B0000' if t == table else '#DA7297')
        for w in self._content.winfo_children():
            w.destroy()
        _MarksPanel(self._content, table, label, self.student_id, self.student_name)


# ============================================================
#  MARKS PANEL — CRUD درجات مادة واحدة لطالب واحد
# ============================================================
class _MarksPanel:
    def __init__(self, parent, table, subject, student_id, student_name):
        self.parent       = parent
        self.table        = table
        self.subject      = subject
        self.student_id   = student_id
        self.student_name = student_name

        self.var_st     = StringVar()
        self.var_nd     = StringVar()
        self.var_ch1    = StringVar()
        self.var_half   = StringVar()
        self.var_st1    = StringVar()
        self.var_nd2    = StringVar()
        self.var_ch2    = StringVar()
        self.var_ch3    = StringVar()
        self.var_exam   = StringVar()
        self.var_result = StringVar()

        self._build()
        self._load()

    def _con(self):
        con = sqlite3.connect(DB_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def _build(self):
        p = self.parent

        # صورة
        try:
            img = CTkImage(Image.open('images/marks.png'), size=(170, 170))
            CTkLabel(p, text='', image=img, fg_color='#F6F5F5').place(x=10, y=10)
        except Exception:
            pass

        # معلومات الطالب
        info_frame = CTkFrame(p, width=900, height=55,
                              fg_color='white', bg_color='#F6F5F5',
                              border_color='#DA7297', border_width=1)
        info_frame.place(x=195, y=10)

        Label(info_frame,
              text=f'Student:  {self.student_name}    (ID: {self.student_id})    Subject:  {self.subject}',
              font=('arial', 13, 'bold'), bg='white', fg='#DA7297').place(x=15, y=14)

        # Grade fields
        fields = [
            ("1st Month",    self.var_st,    195, 85),
            ("2nd Month",    self.var_nd,    310, 85),
            ("Chapter 1",    self.var_ch1,   430, 85),
            ("Half Year",    self.var_half,  555, 85),
            ("1st Month",    self.var_st1,   680, 85),
            ("2nd Month",    self.var_nd2,   800, 85),
            ("Chapter 2",    self.var_ch2,   920, 85),
            ("Chapter 3",    self.var_ch3,   195, 155),
            ("Final Exam",   self.var_exam,  320, 155),
            ("Final Result", self.var_result,455, 155),
        ]
        for lbl_t, var, x, y in fields:
            Label(p, text=lbl_t, font=('arial', 11, 'bold'),
                  bg='#F6F5F5', fg='gray').place(x=x, y=y)
            w = 130 if lbl_t == "Final Result" else 90
            CTkEntry(p, textvariable=var, width=w, height=30,
                     font=('arial', 11), border_color='#DA7297',
                     justify='center').place(x=x, y=y + 22)

        # Buttons
        for text, cmd, x, perm in [
            ("SAVE",   self._save,   195, "add_marks"),
            ("UPDATE", self._update, 325, "update_marks"),
            ("DELETE", self._delete, 455, "delete_marks"),
            ("CLEAR",  self._clear,  585, None),
        ]:
            state = 'normal' if (perm is None or session.can(perm)) else 'disabled'
            CTkButton(p, text=text, width=120, height=36,
                      fg_color='#DA7297' if state == 'normal' else '#aaa',
                      text_color='white', font=('arial', 12, 'bold'),
                      corner_radius=8, state=state,
                      command=cmd).place(x=x, y=218)

        # Status label
        self.status_lbl = Label(p, text='', font=('arial', 11),
                                bg='#F6F5F5', fg='#2e7d32')
        self.status_lbl.place(x=730, y=225)

        # TreeView — كل الطلاب في هذه المادة
        Label(p, text=f'All Students — {self.subject}',
              font=('arial', 12, 'bold'),
              bg='#F6F5F5', fg='#DA7297').place(x=5, y=265)

        tree_f = Frame(p, bg='gray')
        tree_f.place(x=3, y=288, width=1288, height=270)

        style = ttk.Style(); style.theme_use('clam')
        style.configure('Treeview', font=('arial', 11), rowheight=27,
                        fieldbackground='white')
        style.configure('Treeview.Heading', background='#DA7297',
                        foreground='white', font=('arial', 11, 'bold'))

        scx = Scrollbar(tree_f, orient=HORIZONTAL)
        scy = Scrollbar(tree_f)
        scx.pack(side=BOTTOM, fill=X)
        scy.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(tree_f, columns=MARKS_COLS, show='headings',
                                 yscrollcommand=scy.set, xscrollcommand=scx.set)
        scy.config(command=self.tree.yview)
        scx.config(command=self.tree.xview)

        for col in MARKS_COLS:
            self.tree.heading(col, text=MARKS_HEADINGS[col], anchor='center')
            self.tree.column(col, width=MARKS_WIDTHS[col], anchor='center')

        self.tree.tag_configure('current', background='#ffe0eb')
        self.tree.tag_configure('evenrow', background='#F6F5F5')
        self.tree.tag_configure('oddrow',  background='lightgray')
        self.tree.pack(fill=BOTH, expand=1)
        self.tree.bind('<ButtonRelease-1>', self._tree_click)

    def _load(self):
        """يجيب درجات الطالب الحالي ويملا الـ fields، وبيعرض كل الطلاب في الجدول"""
        con = self._con(); cur = con.cursor()
        try:
            # درجات الطالب الحالي
            cur.execute(f"""
                SELECT st_month, nd_month, chapter1, half_year,
                       st_month1, nd_month2, chapter2, chapter3,
                       final_exam, final_result
                FROM {self.table} WHERE student_id=?
            """, (self.student_id,))
            row = cur.fetchone()
            if row:
                for var, val in zip([self.var_st, self.var_nd, self.var_ch1,
                                     self.var_half, self.var_st1, self.var_nd2,
                                     self.var_ch2, self.var_ch3,
                                     self.var_exam, self.var_result], row):
                    var.set(str(val))
                self.status_lbl.config(text='✅ درجات موجودة — اضغط UPDATE للتعديل',
                                       fg='#2e7d32')
            else:
                self.status_lbl.config(text='➕ لا توجد درجات — اضغط SAVE للإضافة',
                                       fg='#e65100')

            # كل الطلاب في المادة
            cur.execute(f"""
                SELECT student_id, student_name,
                       st_month, nd_month, chapter1, half_year,
                       st_month1, nd_month2, chapter2, chapter3,
                       final_exam, final_result
                FROM {self.table} ORDER BY student_id
            """)
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for i, r in enumerate(rows):
                tag = 'current' if r[0] == self.student_id else \
                      ('evenrow' if i % 2 == 0 else 'oddrow')
                self.tree.insert('', END, values=r, tags=(tag,))

        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))
        finally:
            con.close()

    def _tree_click(self, ev):
        row = self.tree.item(self.tree.focus())['values']
        if not row: return
        for var, val in zip([self.var_st, self.var_nd, self.var_ch1,
                             self.var_half, self.var_st1, self.var_nd2,
                             self.var_ch2, self.var_ch3,
                             self.var_exam, self.var_result], row[2:]):
            var.set(str(val))

    def _grades(self):
        def n(v, lbl):
            try: return float(v.get())
            except ValueError: raise ValueError(f"'{lbl}' لازم يكون رقم.")
        return (n(self.var_st,'1st'), n(self.var_nd,'2nd'),
                n(self.var_ch1,'Ch1'), n(self.var_half,'Half'),
                n(self.var_st1,'1st2'), n(self.var_nd2,'2nd2'),
                n(self.var_ch2,'Ch2'), n(self.var_ch3,'Ch3'),
                n(self.var_exam,'Exam'), self.var_result.get() or 'Pending')

    def _save(self):
        if not session.require("add_marks"): return
        try: g = self._grades()
        except ValueError as ex:
            messagebox.showerror("خطأ", str(ex)); return

        # تحقق مش موجود
        con = self._con(); cur = con.cursor()
        cur.execute(f"SELECT m_ID FROM {self.table} WHERE student_id=?",
                    (self.student_id,))
        if cur.fetchone():
            con.close()
            messagebox.showwarning("تنبيه",
                "الطالب ده عنده درجات بالفعل.\nاستخدم UPDATE للتعديل.")
            return
        try:
            cur.execute(f"""
                INSERT INTO {self.table}
                (student_id, student_name, st_month, nd_month, chapter1,
                 half_year, st_month1, nd_month2, chapter2, chapter3,
                 final_exam, final_result)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """, (self.student_id, self.student_name) + g)
            con.commit()
            log_action(session.admin_username, "ADD_MARKS", self.table,
                       self.student_id, f"student:{self.student_name}")
            messagebox.showinfo("تم", "تمت إضافة الدرجات.")
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))
        finally:
            con.close()
        self._load()

    def _update(self):
        if not session.require("update_marks"): return
        try: g = self._grades()
        except ValueError as ex:
            messagebox.showerror("خطأ", str(ex)); return

        con = self._con(); cur = con.cursor()
        try:
            cur.execute(f"""
                UPDATE {self.table}
                SET st_month=?, nd_month=?, chapter1=?, half_year=?,
                    st_month1=?, nd_month2=?, chapter2=?, chapter3=?,
                    final_exam=?, final_result=?
                WHERE student_id=?
            """, g + (self.student_id,))
            if cur.rowcount == 0:
                messagebox.showwarning("تنبيه",
                    "مفيش درجات للطالب ده — اضغط SAVE أولاً.")
            else:
                con.commit()
                log_action(session.admin_username, "UPDATE_MARKS", self.table,
                           self.student_id, f"student:{self.student_name}")
                messagebox.showinfo("تم", "تم تعديل الدرجات.")
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))
        finally:
            con.close()
        self._load()

    def _delete(self):
        if not session.require("delete_marks"): return
        if not messagebox.askyesno("تأكيد",
                f"هتحذف درجات {self.student_name} في {self.subject}؟"):
            return
        con = self._con(); cur = con.cursor()
        try:
            cur.execute(f"DELETE FROM {self.table} WHERE student_id=?",
                        (self.student_id,))
            con.commit()
            log_action(session.admin_username, "DELETE_MARKS", self.table,
                       self.student_id, f"student:{self.student_name}")
            self._clear()
            messagebox.showinfo("تم", "تم الحذف.")
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))
        finally:
            con.close()
        self._load()

    def _clear(self):
        for v in (self.var_st, self.var_nd, self.var_ch1, self.var_half,
                  self.var_st1, self.var_nd2, self.var_ch2, self.var_ch3,
                  self.var_exam, self.var_result):
            v.set("")


if __name__ == "__main__":
    root = Tk()
    FirstStudentClass(root)
    root.mainloop()
