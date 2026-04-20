from customtkinter import *
from tkinter import *
from time import strftime
from tkinter import ttk, messagebox
import sqlite3

import dashboard
from auth import session
from create_db import log_action

ALLOWED_SEARCH_COLUMNS = {"name", "subject", "phone", "national_id", "college_degree"}


class TeachersClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x690+100+5')
        self.root.title('Teachers Page')
        self.root.config(bg='white')
        self.root.resizable(False, False)

        # ✅ تحقق من صلاحية الدخول
        if not session.require("view_teachers"):
            root.after(100, root.destroy)
            return

        def date():
            date_1 = strftime('%I:%M:%S %p \t %A \t %b/%d/%Y')
            date_lbl.config(text=date_1)
            date_lbl.after(1000, date)

        up_frame = CTkFrame(root, width=1199, height=70, bg_color='#F6F5F5',
                            fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        up_frame.place(x=1, y=1)
        text_lbl = Label(up_frame, text='Teachers Page', font=('courier', 18, 'bold'),
                         bg='#F6F5F5', fg='#DA7297')
        text_lbl.place(x=150, y=5, width=200, height=60)
        date_lbl = Label(up_frame, font=('courier', 18, 'bold'), bg='#F6F5F5', fg='#DA7297')
        date_lbl.place(x=590, y=5, width=570, height=60)
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

        head_frame = CTkFrame(root, width=1197, height=615, bg_color='white',
                              fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        head_frame.place(x=1, y=72)

        var_id             = StringVar()
        var_name           = StringVar()
        var_subject        = StringVar()
        var_phone          = StringVar()
        var_national_id    = StringVar()
        var_salary         = StringVar()
        var_college_degree = StringVar()
        var_search         = StringVar()

        def get_con():
            con = sqlite3.connect('school.db')
            con.execute("PRAGMA foreign_keys = ON")
            return con

        def show():
            try:
                con = get_con(); cur = con.cursor()
                cur.execute("SELECT t_id,name,subject,phone,national_id,salary,college_degree "
                            "FROM teachers WHERE is_active=1 ORDER BY name")
                rows = cur.fetchall()
                teacher_tree.delete(*teacher_tree.get_children())
                for i, row in enumerate(rows):
                    teacher_tree.insert('', END, values=row,
                                        tags=('evenrow' if i%2==0 else 'oddrow',))
            except Exception as ex:
                messagebox.showerror("خطأ", str(ex))
            finally: con.close()

        def get_data(ev):
            row = teacher_tree.item(teacher_tree.focus())['values']
            if row:
                var_id.set(row[0]);         var_name.set(row[1])
                var_subject.set(row[2]);    var_phone.set(row[3])
                var_national_id.set(row[4]);var_salary.set(row[5])
                var_college_degree.set(row[6])

        def clear():
            for v in (var_id, var_name, var_subject, var_phone,
                      var_national_id, var_salary, var_college_degree, var_search):
                v.set("")
            cmb_search.set("Select")

        def add_teacher():
            if not session.require("add_teacher"): return
            name, subj = var_name.get().strip(), var_subject.get().strip()
            if not name or not subj:
                messagebox.showerror("خطأ", "الاسم والمادة مطلوبان."); return
            salary_val = var_salary.get().strip()
            if salary_val and not salary_val.replace('.','',1).isdigit():
                messagebox.showerror("خطأ", "الراتب لازم يكون رقم."); return
            try:
                con = get_con(); cur = con.cursor()
                cur.execute(
                    "INSERT INTO teachers(name,subject,phone,national_id,salary,college_degree) VALUES(?,?,?,?,?,?)",
                    (name, subj, var_phone.get().strip(), var_national_id.get().strip(),
                     salary_val or 0, var_college_degree.get().strip()))
                new_id = cur.lastrowid; con.commit(); con.close()
                log_action(session.admin_username, "ADD_TEACHER", "teachers",
                           new_id, f"Name:{name}")
                show(); clear()
                messagebox.showinfo("تم", "تم إضافة المدرس.")
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "الرقم القومي موجود بالفعل.")
            except Exception as ex:
                messagebox.showerror("خطأ", str(ex))

        def update():
            if not session.require("update_teacher"): return
            if not var_id.get():
                messagebox.showerror("خطأ", "اختار مدرس أولاً."); return
            salary_val = var_salary.get().strip()
            if salary_val and not salary_val.replace('.','',1).isdigit():
                messagebox.showerror("خطأ", "الراتب لازم يكون رقم."); return
            try:
                con = get_con(); cur = con.cursor()
                cur.execute(
                    "UPDATE teachers SET name=?,subject=?,phone=?,national_id=?,salary=?,college_degree=? WHERE t_id=?",
                    (var_name.get().strip(), var_subject.get().strip(), var_phone.get().strip(),
                     var_national_id.get().strip(), salary_val or 0,
                     var_college_degree.get().strip(), var_id.get()))
                con.commit(); con.close()
                log_action(session.admin_username, "UPDATE_TEACHER", "teachers",
                           int(var_id.get()), f"Name:{var_name.get()}")
                show(); clear()
                messagebox.showinfo("تم", "تم التعديل.")
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "الرقم القومي موجود لمدرس آخر.")
            except Exception as ex:
                messagebox.showerror("خطأ", str(ex))

        def delete():
            if not session.require("delete_teacher"): return
            if not var_id.get():
                messagebox.showerror("خطأ", "اختار مدرس أولاً."); return
            if not messagebox.askyesno("تأكيد", f"هتحذف: {var_name.get()}؟"): return
            try:
                con = get_con(); cur = con.cursor()
                cur.execute("UPDATE teachers SET is_active=0 WHERE t_id=?", (var_id.get(),))
                con.commit(); con.close()
                log_action(session.admin_username, "DELETE_TEACHER", "teachers",
                           int(var_id.get()), f"Name:{var_name.get()}")
                show(); clear()
                messagebox.showinfo("تم", "تم الحذف.")
            except Exception as ex:
                messagebox.showerror("خطأ", str(ex))

        def search():
            col = cmb_search.get(); val = var_search.get().strip()
            if col not in ALLOWED_SEARCH_COLUMNS:
                messagebox.showerror("خطأ", "اختار عمود بحث صحيح."); return
            if not val:
                messagebox.showerror("خطأ", "أدخل قيمة البحث."); return
            try:
                con = get_con(); cur = con.cursor()
                cur.execute(f"SELECT t_id,name,subject,phone,national_id,salary,college_degree "
                            f"FROM teachers WHERE {col} LIKE ? AND is_active=1",
                            (f'%{val}%',))
                rows = cur.fetchall()
                teacher_tree.delete(*teacher_tree.get_children())
                for row in rows:
                    teacher_tree.insert('', END, values=row)
                con.close()
                if not rows: messagebox.showinfo("بحث", "لا توجد نتائج.")
            except Exception as ex:
                messagebox.showerror("خطأ", str(ex))

        # ---- UI Fields ----
        for lbl_t, var, y in [('Name', var_name, 30),
                               ('Subject', var_subject, 80),
                               ('Phone', var_phone, 130)]:
            CTkLabel(head_frame, text=lbl_t, text_color='gray',
                     font=('arial', 14, 'bold')).place(x=30, y=y)
            CTkEntry(head_frame, textvariable=var, width=220, height=35,
                     justify=CENTER).place(x=120, y=y)

        for lbl_t, var, y in [('National ID', var_national_id, 30),
                               ('Salary', var_salary, 80),
                               ('College Degree', var_college_degree, 130)]:
            CTkLabel(head_frame, text=lbl_t, text_color='gray',
                     font=('arial', 14, 'bold')).place(x=360, y=y)
            CTkEntry(head_frame, textvariable=var, width=220, height=35,
                     justify=CENTER).place(x=500, y=y)

        # ---- Buttons — معطّلة للـ viewer ----
        for text, cmd, x, perm in [
            ('ADD',    add_teacher, 30,  'add_teacher'),
            ('UPDATE', update,     160,  'update_teacher'),
            ('DELETE', delete,     290,  'delete_teacher'),
            ('CLEAR',  clear,      420,  None),
        ]:
            state = 'normal' if (perm is None or session.can(perm)) else 'disabled'
            btn = CTkButton(head_frame, text=text, width=120, height=35,
                            fg_color='#DA7297' if state=='normal' else '#aaaaaa',
                            command=cmd, state=state)
            btn.place(x=x, y=200)

        # Viewer label
        if session.role == 'viewer':
            Label(head_frame, text="🔒 وضع عرض فقط — التعديل غير مسموح",
                  bg='#F6F5F5', fg='#888888',
                  font=('arial', 11, 'italic')).place(x=30, y=240)

        # ---- Search ----
        frame_search = CTkFrame(head_frame, width=800, height=60,
                                fg_color='#F6F5F5', bg_color='white',
                                border_color='#DA7297')
        frame_search.place(x=30, y=258)
        Label(frame_search, text='Search Teacher', font=('arial', 14, 'bold'),
              bg='white', fg='#DA7297').place(x=5, y=5, width=180, height=50)
        cmb_search = CTkComboBox(frame_search,
            values=("Select","name","subject","phone","national_id","college_degree"),
            button_color='#DA7297', button_hover_color='#DA7297',
            justify=CENTER, font=('arial', 15), width=180, height=35,
            fg_color='white', border_width=1, border_color='#DA7297',
            dropdown_fg_color='white', dropdown_text_color='#DA7297')
        cmb_search.place(x=180, y=13)
        CTkEntry(frame_search, textvariable=var_search, width=200, height=35,
                 fg_color='white', border_width=1, border_color='#DA7297',
                 justify='center').place(x=380, y=13)
        CTkButton(frame_search, text='SEARCH', width=160, height=40,
                  fg_color='#DA7297', text_color='white',
                  hover_color='#DA7297', corner_radius=10,
                  command=search).place(x=600, y=10)

        # ---- TreeView ----
        tf = Frame(head_frame, bg='gray')
        tf.place(x=30, y=335, width=1100, height=250)
        style = ttk.Style(); style.theme_use('clam')
        style.configure('Treeview', bg='#D3D3D3', font=('arial', 12),
                        fg='black', rowheight=30, fieldbackground='white')
        style.configure('Treeview.Heading', background='#DA7297',
                        foreground='white', font=('arial', 12, 'bold'))
        sc = Scrollbar(tf); sc.pack(side=RIGHT, fill=Y)
        teacher_tree = ttk.Treeview(tf,
            columns=("t_id","name","subject","phone","national_id","salary","college_degree"),
            show='headings', yscrollcommand=sc.set)
        sc.config(command=teacher_tree.yview)
        for col, hd, w in [("t_id","ID",60),("name","Name",200),("subject","Subject",150),
                            ("phone","Phone",120),("national_id","National ID",150),
                            ("salary","Salary",100),("college_degree","College Degree",200)]:
            teacher_tree.heading(col, text=hd)
            teacher_tree.column(col, width=w)
        teacher_tree.tag_configure('evenrow', background='#F6F5F5')
        teacher_tree.tag_configure('oddrow',  background='lightgray')
        teacher_tree.pack(fill=BOTH, expand=1)
        teacher_tree.bind('<ButtonRelease-1>', get_data)
        show()
