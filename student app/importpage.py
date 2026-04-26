"""
importpage.py — صفحة استيراد الطلاب من CSV / Excel
====================================================
الصلاحيات المطلوبة: add_student
الاستخدام:
    import importpage
    importpage.ImportClass(Toplevel())
"""

from customtkinter import *
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from time import strftime
import sqlite3
import csv
import os

try:
    import openpyxl
    EXCEL_SUPPORTED = True
except ImportError:
    EXCEL_SUPPORTED = False

import dashboard
from auth import session
from create_db import log_action

# الأعمدة المتوقعة في الـ CSV بالترتيب
EXPECTED_COLS = [
    "student_name", "student_gender", "student_age",
    "address", "contact", "enrollment_date",
    "last_school", "repeated_years", "health_problem", "final_result"
]

# الأعمدة الاختيارية (مش لازم تكون في الـ CSV)
OPTIONAL_COLS = {"is_active", "s_ID"}

# القيم المقبولة للـ gender
VALID_GENDERS = {"Male", "Female", "ذكر", "أنثى", "male", "female"}

GENDER_MAP = {
    "ذكر":   "Male",
    "أنثى":  "Female",
    "male":  "Male",
    "female":"Female",
    "Male":  "Male",
    "Female":"Female",
}


class ImportClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x690+100+5')
        self.root.title('Import Students')
        self.root.config(bg='white')
        self.root.resizable(False, False)

        self.file_path  = None
        self.all_rows   = []    # كل الصفوف بعد القراءة
        self.valid_rows = []    # الصفوف الصحيحة فقط
        self.error_rows = []    # الصفوف فيها أخطاء

        if not session.require("add_student"):
            root.after(100, root.destroy)
            return

        # ========================= HEAD =========================
        up_frame = CTkFrame(root, width=1199, height=70, bg_color='#F6F5F5',
                            fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        up_frame.place(x=1, y=1)

        Label(up_frame, text='Import Students', font=('courier', 18, 'bold'),
              bg='#F6F5F5', fg='#DA7297').place(x=150, y=5, width=250, height=60)

        def date():
            date_lbl.config(text=strftime('%I:%M:%S %p  -  %A  -  %d/%m/%Y'))
            date_lbl.after(1000, date)
        date_lbl = Label(up_frame, font=('courier', 12, 'bold'), bg='#F6F5F5', fg='#DA7297')
        date_lbl.place(x=550, y=15, width=600, height=40)
        date()

        def back():
            win = Toplevel()
            dashboard.DashboardClass(win)
            root.withdraw()
            win.deiconify()

        CTkButton(up_frame, text='←', width=100, height=68, fg_color='#DA7297',
                  text_color='white', bg_color='#F6F5F5', font=('arial', 30, 'bold'),
                  hover_color='#DA7297', border_color='#DA7297', corner_radius=0,
                  command=back).place(x=2, y=2)

        # ========================= MAIN FRAME =========================
        main = CTkFrame(root, width=1197, height=615, bg_color='white',
                        fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        main.place(x=1, y=72)

        # ========================= TOP PANEL =========================
        top = CTkFrame(main, width=1190, height=130, fg_color='white',
                       bg_color='#F6F5F5', border_color='#DA7297', border_width=1)
        top.place(x=3, y=5)

        # ---- File picker ----
        self.file_var = StringVar(value="لم يتم اختيار ملف")
        CTkLabel(top, text='اختار الملف:', text_color='#DA7297',
                 font=('arial', 14, 'bold'), fg_color='white',
                 bg_color='white').place(x=20, y=15)

        file_lbl = CTkLabel(top, textvariable=self.file_var, text_color='gray',
                            font=('arial', 12), fg_color='white', bg_color='white',
                            anchor='w', width=600)
        file_lbl.place(x=160, y=15)

        ext = "*.csv *.xlsx *.xls" if EXCEL_SUPPORTED else "*.csv"
        ftypes = [("CSV / Excel", ext), ("All files", "*.*")]

        CTkButton(top, text='📂  Browse', width=140, height=36,
                  fg_color='#DA7297', text_color='white', font=('arial', 13, 'bold'),
                  command=lambda: self._browse(ftypes)).place(x=20, y=55)

        CTkButton(top, text='🔍  Preview', width=140, height=36,
                  fg_color='#DA7297', text_color='white', font=('arial', 13, 'bold'),
                  command=self._preview).place(x=175, y=55)

        self.import_btn = CTkButton(top, text='✅  Import Valid Rows', width=200, height=36,
                                    fg_color='#2e7d32', text_color='white',
                                    font=('arial', 13, 'bold'),
                                    command=self._import, state='disabled')
        self.import_btn.place(x=330, y=55)

        CTkButton(top, text='📥  Download Template', width=200, height=36,
                  fg_color='#888888', text_color='white', font=('arial', 13, 'bold'),
                  command=self._download_template).place(x=545, y=55)

        # ---- Stats row ----
        self.stat_total   = StringVar(value="إجمالي: 0")
        self.stat_valid   = StringVar(value="صحيح: 0")
        self.stat_errors  = StringVar(value="أخطاء: 0")
        self.stat_dupes   = StringVar(value="مكرر: 0")

        for i, (var, color) in enumerate([
            (self.stat_total,  '#555555'),
            (self.stat_valid,  '#2e7d32'),
            (self.stat_errors, '#c62828'),
            (self.stat_dupes,  '#e65100'),
        ]):
            Label(top, textvariable=var, bg='white', fg=color,
                  font=('arial', 12, 'bold')).place(x=20 + i*200, y=100)

        # ========================= TABLE TABS =========================
        tab_frame = CTkFrame(main, width=1190, height=460, fg_color='white',
                             bg_color='#F6F5F5', border_color='#DA7297', border_width=1)
        tab_frame.place(x=3, y=142)

        nb = ttk.Notebook(tab_frame)
        nb.place(x=0, y=0, width=1188, height=455)

        style = ttk.Style(); style.theme_use('clam')
        style.configure('TNotebook.Tab', font=('arial', 12, 'bold'),
                        padding=[12, 6], background='#DA7297', foreground='white')
        style.map('TNotebook.Tab', background=[('selected','#8B0000')])
        style.configure('Treeview', font=('arial', 11), rowheight=28,
                        fieldbackground='white')
        style.configure('Treeview.Heading', background='#DA7297',
                        foreground='white', font=('arial', 11, 'bold'))

        # ---- Tab 1: Valid ----
        valid_tab = Frame(nb, bg='white')
        nb.add(valid_tab, text='✅  صحيح')
        self.valid_tree = self._make_tree(valid_tab, show_status=False)

        # ---- Tab 2: Errors ----
        err_tab = Frame(nb, bg='white')
        nb.add(err_tab, text='❌  أخطاء')
        self.err_tree = self._make_tree(err_tab, show_status=True)

        # ---- Tab 3: All ----
        all_tab = Frame(nb, bg='white')
        nb.add(all_tab, text='📋  الكل')
        self.all_tree = self._make_tree(all_tab, show_status=True)

        # ========================= PROGRESS BAR =========================
        self.progress_var = DoubleVar(value=0)
        self.progress_lbl = StringVar(value="")
        Label(main, textvariable=self.progress_lbl, bg='#F6F5F5',
              fg='#DA7297', font=('arial', 11)).place(x=20, y=600)
        self.pbar = ttk.Progressbar(main, variable=self.progress_var,
                                    maximum=100, length=800, mode='determinate')
        self.pbar.place(x=300, y=600)

    # ================================================================
    #  TREE BUILDER
    # ================================================================
    def _make_tree(self, parent, show_status=False):
        cols = (["#", "status"] if show_status else ["#"]) + EXPECTED_COLS
        f = Frame(parent, bg='gray')
        f.pack(fill=BOTH, expand=1, padx=3, pady=3)

        scx = Scrollbar(f, orient=HORIZONTAL)
        scy = Scrollbar(f, orient=VERTICAL)
        scx.pack(side=BOTTOM, fill=X)
        scy.pack(side=RIGHT,  fill=Y)

        tree = ttk.Treeview(f, columns=cols, show='headings',
                            yscrollcommand=scy.set, xscrollcommand=scx.set)
        scy.config(command=tree.yview)
        scx.config(command=tree.xview)

        widths = {"#": 45, "status": 160,
                  "student_name": 140, "student_gender": 80, "student_age": 60,
                  "address": 180, "contact": 120, "enrollment_date": 110,
                  "last_school": 140, "repeated_years": 80,
                  "health_problem": 110, "final_result": 90}
        headings = {"#": "#", "status": "الحالة",
                    "student_name": "الاسم", "student_gender": "الجنس",
                    "student_age": "السن", "address": "العنوان",
                    "contact": "رقم التواصل", "enrollment_date": "تاريخ القيد",
                    "last_school": "المدرسة السابقة", "repeated_years": "سنوات رسوب",
                    "health_problem": "المشكلة الصحية", "final_result": "النتيجة"}
        for col in cols:
            tree.heading(col, text=headings.get(col, col), anchor='center')
            tree.column(col, width=widths.get(col, 100), anchor='center')

        tree.tag_configure('valid',   background='#e8f5e9')
        tree.tag_configure('error',   background='#ffebee')
        tree.tag_configure('dupe',    background='#fff3e0')
        tree.pack(fill=BOTH, expand=1)
        return tree

    # ================================================================
    #  BROWSE
    # ================================================================
    def _browse(self, ftypes):
        path = filedialog.askopenfilename(filetypes=ftypes)
        if path:
            self.file_path = path
            self.file_var.set(os.path.basename(path))
            # reset
            for tree in (self.valid_tree, self.err_tree, self.all_tree):
                tree.delete(*tree.get_children())
            self.valid_rows = []; self.error_rows = []; self.all_rows = []
            self.import_btn.configure(state='disabled')
            for v in (self.stat_total, self.stat_valid,
                      self.stat_errors, self.stat_dupes):
                v.set(v.get().split(':')[0] + ': 0')

    # ================================================================
    #  PREVIEW — قراءة + تحقق
    # ================================================================
    def _preview(self):
        if not self.file_path:
            messagebox.showerror("خطأ", "اختار ملف أولاً."); return

        try:
            raw_rows = self._read_file(self.file_path)
        except Exception as ex:
            messagebox.showerror("خطأ في القراءة", str(ex)); return

        if not raw_rows:
            messagebox.showinfo("تنبيه", "الملف فاضي."); return

        # جيب الأسماء الموجودة في DB لاكتشاف التكرار
        existing_names = self._get_existing_names()

        self.valid_rows = []; self.error_rows = []; self.all_rows = []
        dupes = 0

        for i, row in enumerate(raw_rows, start=1):
            errors, cleaned = self._validate_row(row, existing_names)
            entry = {"index": i, "raw": row, "cleaned": cleaned, "errors": errors}
            self.all_rows.append(entry)
            if errors:
                self.error_rows.append(entry)
            else:
                if cleaned['student_name'] in existing_names:
                    dupes += 1
                self.valid_rows.append(entry)

        self._populate_trees()
        self.stat_total.set(f"إجمالي: {len(raw_rows)}")
        self.stat_valid.set(f"صحيح: {len(self.valid_rows)}")
        self.stat_errors.set(f"أخطاء: {len(self.error_rows)}")
        self.stat_dupes.set(f"مكرر: {dupes}")

        if self.valid_rows:
            self.import_btn.configure(state='normal')
        else:
            messagebox.showwarning("تنبيه", "مفيش صفوف صحيحة للاستيراد.")

    # ================================================================
    #  READ FILE
    # ================================================================
    def _read_file(self, path):
        ext = os.path.splitext(path)[1].lower()
        rows = []
        if ext == '.csv':
            with open(path, encoding='utf-8-sig', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    rows.append(dict(row))
        elif ext in ('.xlsx', '.xls') and EXCEL_SUPPORTED:
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
            ws = wb.active
            headers = [str(c.value).strip() if c.value else '' for c in next(ws.iter_rows())]
            for ws_row in ws.iter_rows(min_row=2, values_only=True):
                row = {headers[j]: (str(v).strip() if v is not None else '')
                       for j, v in enumerate(ws_row)}
                rows.append(row)
            wb.close()
        else:
            raise ValueError(f"نوع الملف '{ext}' غير مدعوم.")
        return rows

    # ================================================================
    #  VALIDATE ROW
    # ================================================================
    def _validate_row(self, row, existing_names):
        errors = []
        cleaned = {}

        # --- student_name ---
        name = str(row.get('student_name', '')).strip()
        if not name:
            errors.append("الاسم فاضي")
        cleaned['student_name'] = name

        # --- student_gender ---
        gender = str(row.get('student_gender', '')).strip()
        mapped = GENDER_MAP.get(gender)
        if not mapped:
            errors.append(f"جنس غير صحيح: '{gender}'")
        cleaned['student_gender'] = mapped or gender

        # --- student_age ---
        age = str(row.get('student_age', '')).strip()
        try:
            age_int = int(float(age))
            if not (5 <= age_int <= 20):
                errors.append(f"السن خارج النطاق: {age_int}")
            cleaned['student_age'] = age_int
        except ValueError:
            errors.append(f"السن مش رقم: '{age}'")
            cleaned['student_age'] = age

        # --- address ---
        cleaned['address'] = str(row.get('address', '')).strip()

        # --- contact ---
        contact = str(row.get('contact', '')).strip()
        digits = ''.join(c for c in contact if c.isdigit())
        if len(digits) < 10:
            errors.append(f"رقم تليفون قصير: '{contact}'")
        cleaned['contact'] = contact

        # --- enrollment_date ---
        date_val = str(row.get('enrollment_date', '')).strip()
        cleaned['enrollment_date'] = date_val

        # --- last_school ---
        cleaned['last_school'] = str(row.get('last_school', '')).strip()

        # --- repeated_years ---
        rep = str(row.get('repeated_years', '0')).strip()
        try:
            rep_int = int(float(rep))
            if rep_int < 0:
                errors.append("سنوات الرسوب سالبة")
            cleaned['repeated_years'] = rep_int
        except ValueError:
            errors.append(f"سنوات الرسوب مش رقم: '{rep}'")
            cleaned['repeated_years'] = 0

        # --- health_problem ---
        cleaned['health_problem'] = str(row.get('health_problem', 'None')).strip() or 'None'

        # --- final_result ---
        result = str(row.get('final_result', '')).strip()
        cleaned['final_result'] = result or 'Pending'

        return errors, cleaned

    # ================================================================
    #  GET EXISTING NAMES FROM DB
    # ================================================================
    def _get_existing_names(self):
        try:
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            cur.execute("SELECT student_name FROM first_student")
            names = {row[0] for row in cur.fetchall()}
            con.close()
            return names
        except Exception:
            return set()

    # ================================================================
    #  POPULATE TREES
    # ================================================================
    def _populate_trees(self):
        for tree in (self.valid_tree, self.err_tree, self.all_tree):
            tree.delete(*tree.get_children())

        def row_vals(entry, show_status):
            c = entry['cleaned']
            data = [c.get(col, '') for col in EXPECTED_COLS]
            if show_status:
                status = "✅ صحيح" if not entry['errors'] else "❌ " + " | ".join(entry['errors'])
                return [entry['index'], status] + data
            return [entry['index']] + data

        for entry in self.valid_rows:
            self.valid_tree.insert('', END, values=row_vals(entry, False),
                                   tags=('valid',))

        for entry in self.error_rows:
            self.err_tree.insert('', END, values=row_vals(entry, True),
                                 tags=('error',))

        for entry in self.all_rows:
            tag = 'valid' if not entry['errors'] else 'error'
            self.all_tree.insert('', END, values=row_vals(entry, True),
                                 tags=(tag,))

    # ================================================================
    #  IMPORT — إدخال الصفوف الصحيحة في DB
    # ================================================================
    def _import(self):
        if not self.valid_rows:
            messagebox.showinfo("تنبيه", "مفيش صفوف صحيحة."); return

        confirm = messagebox.askyesno(
            "تأكيد الاستيراد",
            f"هتستورد {len(self.valid_rows)} طالب.\n"
            f"الصفوف اللي فيها أخطاء ({len(self.error_rows)}) هيتم تجاهلها.\n\nمتأكد؟"
        )
        if not confirm: return

        self.import_btn.configure(state='disabled')
        self.progress_var.set(0)
        total   = len(self.valid_rows)
        success = 0
        skipped = 0

        try:
            con = sqlite3.connect('school.db')
            con.execute("PRAGMA foreign_keys = ON")
            cur = con.cursor()

            for i, entry in enumerate(self.valid_rows, start=1):
                c = entry['cleaned']
                try:
                    cur.execute("""
                        INSERT INTO first_student
                        (student_name, student_gender, student_age, address, contact,
                         enrollment_date, last_school, repeated_years, health_problem, final_result)
                        VALUES (?,?,?,?,?,?,?,?,?,?)
                    """, (
                        c['student_name'], c['student_gender'], c['student_age'],
                        c['address'],      c['contact'],        c['enrollment_date'],
                        c['last_school'],  c['repeated_years'], c['health_problem'],
                        c['final_result']
                    ))
                    success += 1
                except sqlite3.IntegrityError:
                    skipped += 1

                # تحديث progress bar
                pct = (i / total) * 100
                self.progress_var.set(pct)
                self.progress_lbl.set(f"جارٍ الاستيراد... {i}/{total}")
                self.root.update_idletasks()

            con.commit()
            con.close()

            log_action(
                session.admin_username,
                "IMPORT_STUDENTS", "first_student",
                details=f"imported={success} skipped={skipped} file={os.path.basename(self.file_path)}"
            )

            self.progress_lbl.set(f"✅  تم استيراد {success} طالب — تم تجاهل {skipped}")
            self.progress_var.set(100)
            messagebox.showinfo(
                "تم الاستيراد",
                f"✅  تم استيراد:  {success}  طالب بنجاح\n"
                f"⏭  تم تجاهل:   {skipped}  (مكرر أو خطأ)\n\n"
                f"من الملف:  {os.path.basename(self.file_path)}"
            )
            self.import_btn.configure(state='disabled')

        except Exception as ex:
            messagebox.showerror("خطأ أثناء الاستيراد", str(ex))
            self.progress_lbl.set("❌  فشل الاستيراد")
            self.import_btn.configure(state='normal')

    # ================================================================
    #  DOWNLOAD TEMPLATE
    # ================================================================
    def _download_template(self):
        path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[("CSV", "*.csv")],
            initialfile='students_template.csv'
        )
        if not path: return
        try:
            with open(path, 'w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(EXPECTED_COLS)
                writer.writerow([
                    "محمد أحمد", "Male", "10",
                    "القاهرة، مدينة نصر", "01099887766",
                    "2024-09-01", "مدرسة المستقبل", "0", "None", "Pass"
                ])
            messagebox.showinfo("تم", f"تم حفظ القالب:\n{path}")
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))


if __name__ == "__main__":
    root = Tk()
    ImportClass(root)
    root.mainloop()
