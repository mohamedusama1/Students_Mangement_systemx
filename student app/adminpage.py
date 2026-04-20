from customtkinter import *
from tkinter import *
from PIL import Image
from time import strftime
from tkinter import ttk, messagebox
import sqlite3

import dashboard
from auth import session, ROLE_PERMISSIONS
from create_db import hash_password, log_action


class AdminClass:
    def __init__(self, root, current_admin="admin"):
        self.root = root
        self.root.geometry('1200x690+100+5')
        self.root.title('Admin Page')
        self.root.config(bg='white')
        self.root.resizable(False, False)
        self.current_admin = current_admin

        # ✅ حماية الصفحة — superadmin فقط
        if not session.require("view_admin_page"):
            root.after(100, root.destroy)
            return

        def date():
            date_1 = strftime('%I:%M:%S %p \t %A \t %b/%d/%Y')
            date_lbl.config(text=date_1)
            date_lbl.after(1000, date)

        up_frame = CTkFrame(root, width=1199, height=70, bg_color='#F6F5F5',
                            fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        up_frame.place(x=1, y=1)
        text_lbl = Label(up_frame, text='Admin Page', font=('courier', 18, 'bold'),
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

        CTkButton(up_frame, text='←', width=100, height=68,
                  fg_color='#DA7297', text_color='white', bg_color='#F6F5F5',
                  font=('arial', 30, 'bold'), hover_color='#DA7297',
                  border_color='#DA7297', corner_radius=0,
                  command=back).place(x=2, y=2)

        head_frame = CTkFrame(root, width=1197, height=615, bg_color='white',
                              fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        head_frame.place(x=1, y=72)

        Label(head_frame, text='WELCOME ADMIN\nPAGE', font=('courier', 25, 'bold'),
              bg='#F6F5F5', fg='#DA7297').place(x=20, y=50, width=300, height=100)

        logo_img = CTkImage(Image.open('images/admin.png'), size=(250, 250))
        CTkLabel(head_frame, text='', image=logo_img, fg_color='#F6F5F5').place(x=350, y=20)

        def get_con():
            con = sqlite3.connect('school.db')
            con.execute("PRAGMA foreign_keys = ON")
            return con

        # ================================================================
        #  ACCOUNT section
        # ================================================================
        acc_id   = StringVar()
        acc_name = StringVar()
        acc_user = StringVar()

        def show_accounts():
            con = get_con(); cur = con.cursor()
            try:
                cur.execute("SELECT ID, name, username FROM Account")
                acc_tree.delete(*acc_tree.get_children())
                for i, row in enumerate(cur.fetchall()):
                    acc_tree.insert('', END, values=(row[0], row[1], row[2], '••••••••'),
                                    tags=('evenrow' if i%2==0 else 'oddrow',))
            except Exception as ex:
                messagebox.showerror('خطأ', str(ex))
            finally: con.close()

        def get_acc_data(ev):
            row = acc_tree.item(acc_tree.focus())['values']
            if row:
                acc_id.set(row[0]); acc_name.set(row[1]); acc_user.set(row[2])

        def clear_acc():
            for v in (acc_id, acc_name, acc_user): v.set("")
            en_acc_pass.delete(0, END)

        def delete_account():
            if not session.require("delete_account"): return
            if not acc_id.get():
                messagebox.showerror("خطأ", "اختار حساب أولاً."); return
            if not messagebox.askyesno("تأكيد", f"هتحذف: {acc_user.get()}؟"): return
            try:
                con = get_con(); cur = con.cursor()
                cur.execute("DELETE FROM Account WHERE ID=?", (acc_id.get(),))
                con.commit(); con.close()
                log_action(self.current_admin, "DELETE_ACCOUNT", "Account",
                           int(acc_id.get()), f"Username:{acc_user.get()}")
                show_accounts(); clear_acc()
                messagebox.showinfo("تم", "تم الحذف.")
            except Exception as ex:
                messagebox.showerror("خطأ", str(ex))

        def upgrade_to_admin():
            if not session.require("upgrade_to_admin"): return
            if not acc_id.get():
                messagebox.showerror("خطأ", "اختار حساب أولاً."); return
            # اختار الـ role
            role_win = Toplevel()
            role_win.title("اختار الدور")
            role_win.geometry("300x180+450+250")
            role_win.config(bg='#F6F5F5')
            role_win.resizable(False, False)
            CTkLabel(role_win, text='اختار الدور الجديد',
                     text_color='#DA7297', font=('arial', 14, 'bold')).place(x=60, y=20)
            chosen_role = StringVar(value='admin')
            for text, val, y in [('Admin',   'admin',  60),
                                  ('Viewer',  'viewer', 95)]:
                CTkRadioButton(role_win, text=text, variable=chosen_role, value=val,
                               text_color='#DA7297', fg_color='#DA7297').place(x=80, y=y)

            def do_upgrade():
                role = chosen_role.get()
                try:
                    con = get_con(); cur = con.cursor()
                    cur.execute("SELECT * FROM Account WHERE ID=?", (acc_id.get(),))
                    data = cur.fetchone()
                    if not data:
                        messagebox.showerror("خطأ", "الحساب مش موجود."); con.close(); return
                    cur.execute("SELECT admin_ID FROM Admin WHERE admin_username=?", (data[2],))
                    if cur.fetchone():
                        messagebox.showerror("خطأ", "الـ username موجود بالفعل في Admin.")
                        con.close(); return
                    cur.execute(
                        "INSERT INTO Admin(admin_name,admin_username,admin_password,role) VALUES(?,?,?,?)",
                        (data[1], data[2], data[3], role))
                    cur.execute("DELETE FROM Account WHERE ID=?", (acc_id.get(),))
                    con.commit(); con.close()
                    log_action(self.current_admin, "UPGRADE_TO_ADMIN", "Account",
                               int(acc_id.get()), f"Username:{data[2]} role:{role}")
                    show_accounts(); show_admins(); clear_acc()
                    messagebox.showinfo("تم", f"تمت الترقية بدور: {role}")
                    role_win.destroy()
                except Exception as ex:
                    messagebox.showerror("خطأ", str(ex))

            CTkButton(role_win, text='ترقية', width=120, height=35,
                      fg_color='#DA7297', text_color='white',
                      font=('arial', 13, 'bold'),
                      command=do_upgrade).place(x=90, y=135)

            role_win.grab_set()

        # Account UI
        CTkLabel(head_frame, text='ID', text_color='gray',
                 font=('arial', 14, 'bold'), fg_color='#F6F5F5',
                 bg_color='#F6F5F5').place(x=80, y=300)
        CTkEntry(head_frame, textvariable=acc_id, justify='center', width=50, height=35,
                 font=('arial', 14, 'bold'), border_color='gray', border_width=1,
                 bg_color='#F6F5F5', fg_color='#F6F5F5',
                 state='readonly').place(x=200, y=300)
        for lbl_t, var, y in [('Account Name', acc_name, 340), ('Username', acc_user, 410)]:
            CTkLabel(head_frame, text=lbl_t, text_color='gray', font=('arial', 14, 'bold'),
                     fg_color='#F6F5F5', bg_color='#F6F5F5').place(x=20, y=y)
            CTkEntry(head_frame, textvariable=var, justify='center', width=230, height=35,
                     font=('arial', 14, 'bold'), border_color='gray', border_width=1,
                     bg_color='#F6F5F5', fg_color='#F6F5F5').place(x=20, y=y+30)
        CTkLabel(head_frame, text='New Password', text_color='gray',
                 font=('arial', 14, 'bold'), fg_color='#F6F5F5',
                 bg_color='#F6F5F5').place(x=20, y=480)
        en_acc_pass = CTkEntry(head_frame, justify='center', show='*', width=230, height=35,
                               font=('arial', 14, 'bold'), border_color='gray', border_width=1,
                               bg_color='#F6F5F5', fg_color='#F6F5F5')
        en_acc_pass.place(x=20, y=510)
        CTkButton(head_frame, text='Clear',  width=100, height=35, fg_color='#DA7297',
                  text_color='white', bg_color='white', font=('arial', 14, 'bold'),
                  corner_radius=5, command=clear_acc).place(x=20, y=560)
        CTkButton(head_frame, text='Delete', width=100, height=35, fg_color='#DA7297',
                  text_color='white', bg_color='white', font=('arial', 14, 'bold'),
                  corner_radius=5, command=delete_account).place(x=140, y=560)
        CTkButton(head_frame, text='→ Upgrade', width=110, height=35, fg_color='#8B0000',
                  text_color='white', bg_color='white', font=('arial', 13, 'bold'),
                  corner_radius=5, command=upgrade_to_admin).place(x=20, y=605)

        # Account TreeView
        acc_tf = Frame(head_frame, bg='gray')
        acc_tf.place(x=280, y=330, width=420, height=250)
        style = ttk.Style(); style.theme_use('clam')
        style.configure('Treeview', bg='#D3D3D3', font=('arial', 12),
                        fg='black', rowheight=30, fieldbackground='white')
        style.configure('Treeview.Heading', background='#DA7297',
                        foreground='white', font=('arial', 12, 'bold'))
        sc1 = Scrollbar(acc_tf); sc1.pack(side=RIGHT, fill=Y)
        acc_tree = ttk.Treeview(acc_tf,
            columns=("ID","name","username","password"), show='headings',
            yscrollcommand=sc1.set)
        sc1.config(command=acc_tree.yview)
        for col, hd, w in [("ID","ID",40),("name","Name",100),
                            ("username","Username",120),("password","Password",90)]:
            acc_tree.heading(col, text=hd, anchor='center')
            acc_tree.column(col, width=w)
        acc_tree.tag_configure('oddrow',  background='lightgray')
        acc_tree.tag_configure('evenrow', background='#F6F5F5')
        acc_tree.pack(fill=BOTH, expand=1)
        acc_tree.bind("<ButtonRelease-1>", get_acc_data)
        show_accounts()

        # ================================================================
        #  ADMIN section  (يمين)
        # ================================================================
        adm_id   = StringVar()
        adm_name = StringVar()
        adm_user = StringVar()
        adm_role = StringVar(value='admin')

        def show_admins():
            con = get_con(); cur = con.cursor()
            try:
                cur.execute("SELECT admin_ID, admin_name, admin_username, role FROM Admin")
                adm_tree.delete(*adm_tree.get_children())
                for i, row in enumerate(cur.fetchall()):
                    adm_tree.insert('', END,
                        values=(row[0], row[1], row[2], row[3], '••••••••'),
                        tags=('evenrow' if i%2==0 else 'oddrow',))
            except Exception as ex:
                messagebox.showerror('خطأ', str(ex))
            finally: con.close()

        def get_adm_data(ev):
            row = adm_tree.item(adm_tree.focus())['values']
            if row:
                adm_id.set(row[0]); adm_name.set(row[1])
                adm_user.set(row[2]); adm_role.set(row[3])

        def clear_adm():
            for v in (adm_id, adm_name, adm_user): v.set("")
            adm_role.set('admin')
            en_adm_pass.delete(0, END)

        def add_admin():
            if not session.require("add_admin"): return
            n, u, p = adm_name.get().strip(), adm_user.get().strip(), en_adm_pass.get()
            r = adm_role.get()
            if not n or not u or not p:
                messagebox.showerror("خطأ", "أدخل الاسم والـ username والباسورد."); return
            if len(p) < 6:
                messagebox.showerror("خطأ", "الباسورد أقل من 6 أحرف."); return
            # منع إضافة superadmin بواسطة admin عادي
            if r == 'superadmin' and session.role != 'superadmin':
                messagebox.showerror("خطأ", "فقط superadmin يقدر يضيف superadmin."); return
            try:
                con = get_con(); cur = con.cursor()
                cur.execute(
                    "INSERT INTO Admin(admin_name,admin_username,admin_password,role) VALUES(?,?,?,?)",
                    (n, u, hash_password(p), r))
                new_id = cur.lastrowid; con.commit(); con.close()
                log_action(self.current_admin, "ADD_ADMIN", "Admin", new_id,
                           f"Username:{u} role:{r}")
                show_admins(); clear_adm()
                messagebox.showinfo("تم", "تم إضافة الأدمن.")
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "الـ username موجود بالفعل.")
            except Exception as ex:
                messagebox.showerror("خطأ", str(ex))

        def update_admin():
            if not session.require("update_admin"): return
            if not adm_id.get():
                messagebox.showerror("خطأ", "اختار أدمن أولاً."); return
            n, u, p, r = (adm_name.get().strip(), adm_user.get().strip(),
                          en_adm_pass.get(), adm_role.get())
            if not n or not u:
                messagebox.showerror("خطأ", "الاسم والـ username مطلوبان."); return
            if r == 'superadmin' and session.role != 'superadmin':
                messagebox.showerror("خطأ", "فقط superadmin يقدر يعيّن superadmin."); return
            try:
                con = get_con(); cur = con.cursor()
                if p:
                    if len(p) < 6:
                        messagebox.showerror("خطأ", "الباسورد أقل من 6 أحرف."); con.close(); return
                    cur.execute(
                        "UPDATE Admin SET admin_name=?,admin_username=?,admin_password=?,role=? WHERE admin_ID=?",
                        (n, u, hash_password(p), r, adm_id.get()))
                else:
                    cur.execute(
                        "UPDATE Admin SET admin_name=?,admin_username=?,role=? WHERE admin_ID=?",
                        (n, u, r, adm_id.get()))
                con.commit(); con.close()
                log_action(self.current_admin, "UPDATE_ADMIN", "Admin",
                           int(adm_id.get()), f"Username:{u} role:{r}")
                show_admins(); clear_adm()
                messagebox.showinfo("تم", "تم التعديل.")
            except sqlite3.IntegrityError:
                messagebox.showerror("خطأ", "الـ username موجود لأدمن آخر.")
            except Exception as ex:
                messagebox.showerror("خطأ", str(ex))

        def delete_admin():
            if not session.require("delete_admin"): return
            if not adm_id.get():
                messagebox.showerror("خطأ", "اختار أدمن أولاً."); return
            con = get_con(); cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM Admin"); count = cur.fetchone()[0]; con.close()
            if count <= 1:
                messagebox.showerror("خطأ", "مش ممكن تحذف الأدمن الأخير."); return
            if not messagebox.askyesno("تأكيد", f"هتحذف: {adm_user.get()}؟"): return
            try:
                con = get_con(); cur = con.cursor()
                cur.execute("DELETE FROM Admin WHERE admin_ID=?", (adm_id.get(),))
                con.commit(); con.close()
                log_action(self.current_admin, "DELETE_ADMIN", "Admin",
                           int(adm_id.get()), f"Username:{adm_user.get()}")
                show_admins(); clear_adm()
                messagebox.showinfo("تم", "تم الحذف.")
            except Exception as ex:
                messagebox.showerror("خطأ", str(ex))

        # Admin UI
        CTkLabel(head_frame, text='ID', text_color='gray',
                 font=('arial', 14, 'bold'), fg_color='#F6F5F5',
                 bg_color='#F6F5F5').place(x=790, y=50)
        CTkEntry(head_frame, textvariable=adm_id, justify='center', width=50, height=35,
                 font=('arial', 14, 'bold'), border_color='gray', border_width=1,
                 bg_color='#F6F5F5', fg_color='#F6F5F5',
                 state='readonly').place(x=910, y=50)
        for lbl_t, var, y in [('Admin Name', adm_name, 90), ('Username', adm_user, 160)]:
            CTkLabel(head_frame, text=lbl_t, text_color='gray', font=('arial', 14, 'bold'),
                     fg_color='#F6F5F5', bg_color='#F6F5F5').place(x=750, y=y)
            CTkEntry(head_frame, textvariable=var, justify='center', width=230, height=35,
                     font=('arial', 14, 'bold'), border_color='gray', border_width=1,
                     bg_color='#F6F5F5', fg_color='#F6F5F5').place(x=730, y=y+30)

        # Role selector
        CTkLabel(head_frame, text='Role', text_color='gray', font=('arial', 14, 'bold'),
                 fg_color='#F6F5F5', bg_color='#F6F5F5').place(x=750, y=235)
        role_cmb = CTkComboBox(head_frame,
            values=['admin', 'viewer', 'superadmin'],
            variable=adm_role, width=230, height=35,
            button_color='#DA7297', button_hover_color='#DA7297',
            fg_color='white', border_color='#DA7297',
            dropdown_fg_color='white', dropdown_text_color='#DA7297',
            font=('arial', 13), justify='center')
        role_cmb.place(x=730, y=260)

        CTkLabel(head_frame, text='Password', text_color='gray',
                 font=('arial', 14, 'bold'), fg_color='#F6F5F5',
                 bg_color='#F6F5F5').place(x=750, y=300)
        en_adm_pass = CTkEntry(head_frame, justify='center', show='*', width=230, height=35,
                               font=('arial', 14, 'bold'), border_color='gray', border_width=1,
                               bg_color='#F6F5F5', fg_color='#F6F5F5')
        en_adm_pass.place(x=730, y=330)

        for text, cmd, y in [('Add',   add_admin,    50),
                              ('Clear', clear_adm,   100),
                              ('Update',update_admin,150),
                              ('Delete',delete_admin,200)]:
            CTkButton(head_frame, text=text, width=100, height=35, fg_color='#DA7297',
                      text_color='white', bg_color='white', font=('arial', 14, 'bold'),
                      corner_radius=5, command=cmd).place(x=1020, y=y)

        # Admin TreeView
        adm_tf = Frame(head_frame, bg='gray')
        adm_tf.place(x=730, y=380, width=430, height=210)
        sc2 = Scrollbar(adm_tf); sc2.pack(side=RIGHT, fill=Y)
        adm_tree = ttk.Treeview(adm_tf,
            columns=("admin_ID","admin_name","admin_username","role","admin_password"),
            show='headings', yscrollcommand=sc2.set)
        sc2.config(command=adm_tree.yview)
        for col, hd, w in [("admin_ID","ID",40),("admin_name","Name",100),
                            ("admin_username","Username",100),
                            ("role","Role",80),("admin_password","Pass",70)]:
            adm_tree.heading(col, text=hd, anchor='center')
            adm_tree.column(col, width=w)
        adm_tree.tag_configure('oddrow',  background='lightgray')
        adm_tree.tag_configure('evenrow', background='#F6F5F5')
        adm_tree.pack(fill=BOTH, expand=1)
        adm_tree.bind("<ButtonRelease-1>", get_adm_data)
        show_admins()


if __name__ == "__main__":
    root = Tk()
    AdminClass(root)
    root.mainloop()
