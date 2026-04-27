"""
firststudent.py — صفحة درجات الصف الأول الإعدادي
===================================================
المواد: Civic Education / Arabic / English / Social Studies
        Math / Chemistry / Physics / Biology
التغييرات:
  - Islamic Marks → Civic Education Marks
  - إضافة student_id في كل جداول الدرجات
  - الجدول بيعرض student_id كأول عمود
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
#  إعداد جداول الدرجات — اسم الجدول + اسم العرض
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

# الأعمدة المشتركة في كل جداول الدرجات
MARKS_COLS = [
    "student_id", "student_name",
    "st_month", "nd_month", "chapter1", "half_year",
    "st_month1", "nd_month2", "chapter2", "chapter3",
    "final_exam", "final_result"
]

TREE_HEADINGS = {
    "student_id":   "ID",
    "student_name": "Student Name",
    "st_month":     "1st Month",
    "nd_month":     "2nd Month",
    "chapter1":     "Chapter 1",
    "half_year":    "Half Year",
    "st_month1":    "1st Month",
    "nd_month2":    "2nd Month",
    "chapter2":     "Chapter 2",
    "chapter3":     "Chapter 3",
    "final_exam":   "Final Exam",
    "final_result": "Final Result",
}

TREE_WIDTHS = {
    "student_id": 50, "student_name": 170,
    "st_month": 75, "nd_month": 75, "chapter1": 75, "half_year": 80,
    "st_month1": 75, "nd_month2": 75, "chapter2": 75, "chapter3": 75,
    "final_exam": 80, "final_result": 100,
}


def _ensure_tables(con):
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    # الخطوة 1: rename الأول قبل CREATE
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='islamic_marks'")
    if cur.fetchone():
        cur.execute("ALTER TABLE islamic_marks RENAME TO civic_education_marks")
    # الخطوة 2: CREATE IF NOT EXISTS
    for table, _ in SUBJECTS:
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table}(
                m_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER REFERENCES first_student(s_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                student_name TEXT, st_month REAL DEFAULT 0, nd_month REAL DEFAULT 0,
                chapter1 REAL DEFAULT 0, half_year REAL DEFAULT 0,
                st_month1 REAL DEFAULT 0, nd_month2 REAL DEFAULT 0,
                chapter2 REAL DEFAULT 0, chapter3 REAL DEFAULT 0,
                final_exam REAL DEFAULT 0, final_result TEXT DEFAULT 'Pending'
            )""")
        # الخطوة 3: أضف student_id لو ناقص
        cur.execute(f"PRAGMA table_info({table})")
        if "student_id" not in [r[1] for r in cur.fetchall()]:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN student_id INTEGER")
    con.commit()


# ============================================================
#  MAIN CLASS
# ============================================================
class FirstStudentClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1300x700+80+20')
        self.root.title('First Students Marks Page')
        self.root.config(bg='white')
        self.root.resizable(False, False)

        # ==================== HEAD ====================
        up_frame = CTkFrame(root, width=1299, height=70, bg_color='#F6F5F5',
                            fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        up_frame.place(x=1, y=1)

        Label(up_frame, text='Students Marks Page', font=('courier', 18, 'bold'),
              bg='#F6F5F5', fg='#DA7297').place(x=150, y=5, width=300, height=60)

        self._date_lbl = Label(up_frame, font=('courier', 14, 'bold'),
                               bg='#F6F5F5', fg='#DA7297')
        self._date_lbl.place(x=560, y=5, width=700, height=60)
        self._tick()

        def back():
            import studentspage
            win = Toplevel()
            studentspage.StudentsClass(win)
            root.withdraw()
            win.deiconify()

        CTkButton(up_frame, text='←', width=100, height=68, fg_color='#DA7297',
                  text_color='white', bg_color='#F6F5F5', font=('arial', 30, 'bold'),
                  hover_color='#DA7297', corner_radius=0, command=back).place(x=2, y=2)

        # ==================== SUBJECT BUTTONS ====================
        btn_frame = CTkFrame(root, width=1299, height=55, fg_color='#DA7297',
                             bg_color='white')
        btn_frame.place(x=1, y=72)

        self._active_table = None
        self._subject_btns = {}

        for i, (table, label) in enumerate(SUBJECTS):
            btn = CTkButton(
                btn_frame,
                text=label.replace(" ", "\n") if len(label) > 10 else label,
                width=148, height=53,
                fg_color='#DA7297', text_color='white', bg_color='#DA7297',
                font=('arial', 11, 'bold'), hover_color='#8B0000',
                corner_radius=0,
                command=lambda t=table, lbl=label: self._open_marks(t, lbl)
            )
            btn.place(x=i * 150, y=1)
            self._subject_btns[table] = btn

        # ==================== CONTENT AREA ====================
        self._content = CTkFrame(root, width=1297, height=570, fg_color='#F6F5F5',
                                 bg_color='white', border_color='#DA7297', border_width=2)
        self._content.place(x=1, y=128)

        # فتح أول مادة تلقائياً
        con = sqlite3.connect('school.db')
        _ensure_tables(con)
        con.close()
        self._open_marks(*SUBJECTS[0])

    def _tick(self):
        self._date_lbl.config(text=strftime('%I:%M:%S %p      %A      %b/%d/%Y'))
        self.root.after(1000, self._tick)

    # ============================================================
    #  OPEN MARKS PAGE FOR SUBJECT
    # ============================================================
    def _open_marks(self, table, subject_label):
        # تغيير لون الزرار النشط
        for t, btn in self._subject_btns.items():
            btn.configure(fg_color='#8B0000' if t == table else '#DA7297',
                          hover_color='#8B0000')

        # مسح المحتوى القديم
        for w in self._content.winfo_children():
            w.destroy()

        self._active_table = table
        _MarksPanel(self._content, table, subject_label)


# ============================================================
#  MARKS PANEL — CRUD لكل مادة
# ============================================================
class _MarksPanel:
    def __init__(self, parent, table, subject_label):
        self.parent  = parent
        self.table   = table
        self.subject = subject_label

        # variables
        self.var_id      = StringVar()
        self.var_sid     = StringVar()   # student_id
        self.var_name    = StringVar()
        self.var_st      = StringVar()
        self.var_nd      = StringVar()
        self.var_ch1     = StringVar()
        self.var_half    = StringVar()
        self.var_st1     = StringVar()
        self.var_nd2     = StringVar()
        self.var_ch2     = StringVar()
        self.var_ch3     = StringVar()
        self.var_exam    = StringVar()
        self.var_result  = StringVar()
        self.var_search  = StringVar()

        self._build()
        self._show()

    # ---- DB ----
    def _con(self):
        con = sqlite3.connect('school.db')
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def _get_students(self):
        """قائمة الطلاب للـ ComboBox"""
        con = self._con(); cur = con.cursor()
        cur.execute("SELECT s_ID, student_name FROM first_student WHERE is_active=1 ORDER BY student_name")
        rows = cur.fetchall(); con.close()
        return rows  # [(id, name), ...]

    # ---- BUILD UI ----
    def _build(self):
        p = self.parent

        # --- صورة ---
        try:
            img = CTkImage(Image.open('images/marks.png'), size=(180, 180))
            CTkLabel(p, text='', image=img, fg_color='#F6F5F5').place(x=10, y=10)
        except Exception:
            pass

        # --- Search ---
        search_frame = CTkFrame(p, width=800, height=50, fg_color='white',
                                bg_color='#F6F5F5', border_color='#DA7297', border_width=1)
        search_frame.place(x=200, y=10)

        Label(search_frame, text='Search Student', font=('arial', 13, 'bold'),
              bg='white', fg='#DA7297').place(x=10, y=10)

        self.cmb_search = CTkComboBox(
            search_frame,
            values=["student_id", "student_name", "final_result"],
            button_color='#DA7297', button_hover_color='#DA7297',
            justify=CENTER, font=('arial', 13), width=160, height=35,
            fg_color='white', border_color='#DA7297',
            dropdown_fg_color='white', dropdown_text_color='#DA7297')
        self.cmb_search.set("Select")
        self.cmb_search.place(x=180, y=8)

        CTkEntry(search_frame, textvariable=self.var_search,
                 width=200, height=35, fg_color='white',
                 border_color='#DA7297', justify='center').place(x=360, y=8)

        CTkButton(search_frame, text='SEARCH', width=160, height=38,
                  fg_color='#DA7297', text_color='white', font=('arial', 13, 'bold'),
                  corner_radius=8, command=self._search).place(x=580, y=6)

        # --- Student picker ---
        Label(p, text='Student Name', font=('arial', 12, 'bold'),
              bg='#F6F5F5', fg='gray').place(x=200, y=75)

        students = self._get_students()
        stu_names = [f"{sid} — {name}" for sid, name in students]
        self._stu_map = {f"{sid} — {name}": (sid, name) for sid, name in students}

        self.cmb_student = CTkComboBox(
            p, values=stu_names if stu_names else ["— لا يوجد طلاب —"],
            width=320, height=35, font=('arial', 12),
            button_color='#DA7297', button_hover_color='#DA7297',
            fg_color='white', border_color='#DA7297',
            dropdown_fg_color='white', dropdown_text_color='#DA7297',
            command=self._on_student_select)
        self.cmb_student.set("اختار الطالب")
        self.cmb_student.place(x=340, y=73)

        CTkLabel(p, text='student_id:', text_color='gray',
                 font=('arial', 11), fg_color='#F6F5F5',
                 bg_color='#F6F5F5').place(x=680, y=75)
        CTkEntry(p, textvariable=self.var_sid, width=70, height=35,
                 font=('arial', 12), border_color='#DA7297',
                 state='readonly', justify='center').place(x=760, y=73)

        # --- Grade fields ---
        fields = [
            ("1st Month",   self.var_st,   200, 125),
            ("2nd Month",   self.var_nd,   340, 125),
            ("Chapter 1",   self.var_ch1,  480, 125),
            ("Half Year",   self.var_half, 620, 125),
            ("1st Month",   self.var_st1,  760, 125),
            ("2nd Month",   self.var_nd2,  900, 125),
            ("Chapter 2",   self.var_ch2,  200, 185),
            ("Chapter 3",   self.var_ch3,  340, 185),
            ("Final Exam",  self.var_exam, 480, 185),
            ("Final Result",self.var_result,620, 185),
        ]
        for lbl_t, var, x, y in fields:
            Label(p, text=lbl_t, font=('arial', 11, 'bold'),
                  bg='#F6F5F5', fg='gray').place(x=x, y=y)
            w = 120 if lbl_t == "Final Result" else 80
            CTkEntry(p, textvariable=var, width=w, height=30,
                     font=('arial', 11), border_color='#DA7297',
                     justify='center').place(x=x, y=y + 22)

        # --- Buttons ---
        btn_y = 255
        ALLOWED_SEARCH_COLS = {"student_id", "student_name", "final_result"}
        for text, cmd, x, perm in [
            ("ADD",    self._add,    200, "add_marks"),
            ("UPDATE", self._update, 330, "update_marks"),
            ("DELETE", self._delete, 460, "delete_marks"),
            ("CLEAR",  self._clear,  590, None),
        ]:
            state = 'normal' if (perm is None or session.can(perm)) else 'disabled'
            CTkButton(p, text=text, width=120, height=38,
                      fg_color='#DA7297' if state == 'normal' else '#aaaaaa',
                      text_color='white', font=('arial', 13, 'bold'),
                      corner_radius=8, state=state,
                      command=cmd).place(x=x, y=btn_y)

        if session.role == 'viewer':
            Label(p, text="🔒 وضع عرض فقط", bg='#F6F5F5', fg='#888',
                  font=('arial', 10, 'italic')).place(x=730, y=265)

        # --- TreeView ---
        tree_frame = Frame(p, bg='gray')
        tree_frame.place(x=5, y=305, width=1285, height=255)

        style = ttk.Style(); style.theme_use('clam')
        style.configure('Treeview', font=('arial', 11), rowheight=28,
                        fieldbackground='white')
        style.configure('Treeview.Heading', background='#DA7297',
                        foreground='white', font=('arial', 11, 'bold'))

        scx = Scrollbar(tree_frame, orient=HORIZONTAL)
        scy = Scrollbar(tree_frame, orient=VERTICAL)
        scx.pack(side=BOTTOM, fill=X)
        scy.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=MARKS_COLS,
            show='headings',
            yscrollcommand=scy.set,
            xscrollcommand=scx.set
        )
        scy.config(command=self.tree.yview)
        scx.config(command=self.tree.xview)

        for col in MARKS_COLS:
            self.tree.heading(col, text=TREE_HEADINGS[col], anchor='center')
            self.tree.column(col, width=TREE_WIDTHS[col], anchor='center')

        self.tree.tag_configure('evenrow', background='#F6F5F5')
        self.tree.tag_configure('oddrow',  background='lightgray')
        self.tree.pack(fill=BOTH, expand=1)
        self.tree.bind('<ButtonRelease-1>', self._get_data)

    # ---- Student select ----
    def _on_student_select(self, choice):
        info = self._stu_map.get(choice)
        if info:
            sid, name = info
            self.var_sid.set(str(sid))
            self.var_name.set(name)

    # ---- Show all ----
    def _show(self):
        con = self._con(); cur = con.cursor()
        try:
            cur.execute(f"""
                SELECT student_id, student_name,
                       st_month, nd_month, chapter1, half_year,
                       st_month1, nd_month2, chapter2, chapter3,
                       final_exam, final_result
                FROM {self.table}
                ORDER BY student_id
            """)
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for i, row in enumerate(rows):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                self.tree.insert('', END, values=row, tags=(tag,))
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))
        finally:
            con.close()

    # ---- Get data on click ----
    def _get_data(self, ev):
        item = self.tree.focus()
        row  = self.tree.item(item)['values']
        if not row: return
        # row = (student_id, student_name, st_month, nd_month, chapter1, half_year,
        #         st_month1, nd_month2, chapter2, chapter3, final_exam, final_result)
        sid  = row[0]
        name = row[1]
        self.var_sid.set(str(sid))
        self.var_name.set(str(name))
        self.var_st.set(str(row[2]));   self.var_nd.set(str(row[3]))
        self.var_ch1.set(str(row[4]));  self.var_half.set(str(row[5]))
        self.var_st1.set(str(row[6]));  self.var_nd2.set(str(row[7]))
        self.var_ch2.set(str(row[8]));  self.var_ch3.set(str(row[9]))
        self.var_exam.set(str(row[10])); self.var_result.set(str(row[11]))

        # اختار الطالب في الـ ComboBox
        key = f"{sid} — {name}"
        if key in self._stu_map:
            self.cmb_student.set(key)

    # ---- Validate grades ----
    def _get_grade_vals(self):
        """يرجع dict بقيم الدرجات أو يرفع ValueError"""
        def num(v, label):
            try: return float(v.get())
            except ValueError: raise ValueError(f"'{label}' لازم يكون رقم.")

        return {
            "student_id":   self.var_sid.get(),
            "student_name": self.var_name.get(),
            "st_month":     num(self.var_st,   "1st Month"),
            "nd_month":     num(self.var_nd,   "2nd Month"),
            "chapter1":     num(self.var_ch1,  "Chapter 1"),
            "half_year":    num(self.var_half, "Half Year"),
            "st_month1":    num(self.var_st1,  "1st Month (2)"),
            "nd_month2":    num(self.var_nd2,  "2nd Month (2)"),
            "chapter2":     num(self.var_ch2,  "Chapter 2"),
            "chapter3":     num(self.var_ch3,  "Chapter 3"),
            "final_exam":   num(self.var_exam, "Final Exam"),
            "final_result": self.var_result.get() or "Pending",
        }

    # ---- ADD ----
    def _add(self):
        if not session.require("add_marks"): return
        sid = self.var_sid.get()
        if not sid:
            messagebox.showerror("خطأ", "اختار الطالب أولاً."); return
        try:
            g = self._get_grade_vals()
        except ValueError as ex:
            messagebox.showerror("خطأ", str(ex)); return

        try:
            con = self._con(); cur = con.cursor()
            cur.execute(f"""
                INSERT INTO {self.table}
                (student_id, student_name, st_month, nd_month, chapter1, half_year,
                 st_month1, nd_month2, chapter2, chapter3, final_exam, final_result)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """, (g['student_id'], g['student_name'],
                  g['st_month'],   g['nd_month'],   g['chapter1'], g['half_year'],
                  g['st_month1'],  g['nd_month2'],  g['chapter2'], g['chapter3'],
                  g['final_exam'], g['final_result']))
            new_id = cur.lastrowid
            con.commit(); con.close()
            log_action(session.admin_username, "ADD_MARKS", self.table,
                       new_id, f"student:{g['student_name']} subject:{self.subject}")
            self._show(); self._clear()
            messagebox.showinfo("تم", "تمت إضافة الدرجات.")
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))

    # ---- UPDATE (بـ student_id) ----
    def _update(self):
        if not session.require("update_marks"): return
        sid = self.var_sid.get()
        if not sid:
            messagebox.showerror("خطأ", "اختار طالب من الجدول أولاً."); return
        try:
            g = self._get_grade_vals()
        except ValueError as ex:
            messagebox.showerror("خطأ", str(ex)); return

        try:
            con = self._con(); cur = con.cursor()
            cur.execute(f"""
                UPDATE {self.table}
                SET student_name=?, st_month=?, nd_month=?, chapter1=?, half_year=?,
                    st_month1=?, nd_month2=?, chapter2=?, chapter3=?,
                    final_exam=?, final_result=?
                WHERE student_id=?
            """, (g['student_name'], g['st_month'],  g['nd_month'],  g['chapter1'],
                  g['half_year'],    g['st_month1'], g['nd_month2'], g['chapter2'],
                  g['chapter3'],     g['final_exam'],g['final_result'],
                  sid))
            if cur.rowcount == 0:
                messagebox.showwarning("تنبيه", "الطالب ده مش عنده درجات — اضغط ADD.")
            else:
                con.commit()
                log_action(session.admin_username, "UPDATE_MARKS", self.table,
                           None, f"student_id:{sid} subject:{self.subject}")
                messagebox.showinfo("تم", "تم تعديل الدرجات.")
            con.close()
            self._show(); self._clear()
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))

    # ---- DELETE ----
    def _delete(self):
        if not session.require("delete_marks"): return
        sid = self.var_sid.get()
        if not sid:
            messagebox.showerror("خطأ", "اختار طالب من الجدول."); return
        if not messagebox.askyesno("تأكيد",
                f"هتحذف درجات {self.var_name.get()} في {self.subject}؟"):
            return
        try:
            con = self._con(); cur = con.cursor()
            cur.execute(f"DELETE FROM {self.table} WHERE student_id=?", (sid,))
            con.commit(); con.close()
            log_action(session.admin_username, "DELETE_MARKS", self.table,
                       None, f"student_id:{sid}")
            self._show(); self._clear()
            messagebox.showinfo("تم", "تم الحذف.")
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))

    # ---- CLEAR ----
    def _clear(self):
        for v in (self.var_id, self.var_sid, self.var_name,
                  self.var_st, self.var_nd, self.var_ch1, self.var_half,
                  self.var_st1, self.var_nd2, self.var_ch2, self.var_ch3,
                  self.var_exam, self.var_result, self.var_search):
            v.set("")
        self.cmb_student.set("اختار الطالب")
        self.cmb_search.set("Select")

    # ---- SEARCH ----
    def _search(self):
        col = self.cmb_search.get()
        val = self.var_search.get().strip()
        ALLOWED = {"student_id", "student_name", "final_result"}
        if col not in ALLOWED:
            messagebox.showerror("خطأ", "اختار عمود بحث صحيح."); return
        if not val:
            messagebox.showerror("خطأ", "أدخل قيمة البحث."); return
        try:
            con = self._con(); cur = con.cursor()
            cur.execute(f"""
                SELECT student_id, student_name,
                       st_month, nd_month, chapter1, half_year,
                       st_month1, nd_month2, chapter2, chapter3,
                       final_exam, final_result
                FROM {self.table} WHERE {col} LIKE ?
            """, (f'%{val}%',))
            rows = cur.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert('', END, values=row)
            con.close()
            if not rows:
                messagebox.showinfo("بحث", "لا توجد نتائج.")
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))


if __name__ == "__main__":
    root = Tk()
    FirstStudentClass(root)
    root.mainloop()
