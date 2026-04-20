from customtkinter import *
from tkinter import *
from PIL import Image
from tkinter import messagebox
import sqlite3

import dashboard
from auth import session, get_role_display
from create_db import hash_password, log_action


class LoginClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1100x600+100+50')
        self.root.title('Login Page')
        self.root.config(bg='#F6F5F5')
        self.root.resizable(False, False)

        def open_dashboard():
            window = Toplevel()
            dashboard.DashboardClass(window)
            root.withdraw()
            window.deiconify()

        def login():
            username = var_username.get().strip()
            password = var_password.get()
            if not username or not password:
                messagebox.showerror("خطأ", "أدخل اسم المستخدم وكلمة المرور.")
                return
            hashed = hash_password(password)
            try:
                con = sqlite3.connect('school.db')
                cur = con.cursor()
                cur.execute(
                    "SELECT admin_ID, admin_name, admin_username, role "
                    "FROM Admin WHERE admin_username=? AND admin_password=?",
                    (username, hashed)
                )
                row = cur.fetchone()
                con.close()
                if row:
                    admin_id, admin_name, admin_username, role = row
                    session.login(admin_id, admin_name, admin_username, role)
                    log_action(username, "LOGIN_SUCCESS", details=f"role={role}")
                    rd = get_role_display(role)
                    messagebox.showinfo("تم تسجيل الدخول",
                        f"أهلاً {admin_name}!\nالدور: {rd['label']}\n\nاضغط OK للمتابعة.")
                    open_dashboard()
                else:
                    log_action(username, "LOGIN_FAILED")
                    messagebox.showerror("خطأ", "اسم المستخدم أو كلمة المرور غلط.")
            except Exception as e:
                messagebox.showerror("خطأ", str(e))

        login_frame   = CTkFrame(root, width=1080, height=550, fg_color='#F6F5F5', bg_color='#F6F5F5')
        sign_up_frame = CTkFrame(root, width=1080, height=550, fg_color='#F6F5F5', bg_color='#F6F5F5')
        for f in (login_frame, sign_up_frame):
            f.place(x=10, y=20)

        def show_frame(f): f.tkraise()
        show_frame(login_frame)

        img = CTkImage(Image.open('images/login.png'), size=(490, 400))
        CTkLabel(login_frame, text='', image=img, fg_color='#F6F5F5').place(x=10, y=70)

        var_username = StringVar()
        var_password = StringVar()

        fr = CTkFrame(login_frame, width=520, height=500, fg_color='#F6F5F5',
                      bg_color='#F6F5F5', border_width=2, corner_radius=30,
                      border_color='#DA7297')
        fr.place(x=520, y=20)

        CTkLabel(fr, text='Login Page', corner_radius=10, fg_color='#DA7297',
                 width=200, height=30, text_color='white',
                 font=('arial', 20, 'bold')).place(x=160, y=50)
        CTkLabel(fr, text='Login To Continue', width=200, height=25,
                 text_color='#DA7297', font=('arial', 18, 'bold')).place(x=30, y=110)
        CTkLabel(fr, text='Not A Member?', width=150, height=25,
                 text_color='#DA7297', font=('arial', 14, 'bold')).place(x=30, y=150)
        CTkButton(fr, text='Sign Up Page', width=100, height=20, fg_color='transparent',
                  text_color='gray', font=('arial', 14, 'bold'), bg_color='transparent',
                  hover_color='#F6F5F5',
                  command=lambda: show_frame(sign_up_frame)).place(x=160, y=150)
        CTkLabel(fr, text='Enter Your Username.', width=200, height=25,
                 text_color='gray', font=('arial', 14)).place(x=25, y=200)
        CTkEntry(fr, textvariable=var_username, width=350, height=35,
                 font=('courier', 14), border_width=1, border_color='#DA7297',
                 justify='center').place(x=50, y=230)
        CTkLabel(fr, text='Enter Your Password.', width=200, height=25,
                 text_color='gray', font=('arial', 14)).place(x=25, y=280)
        CTkEntry(fr, textvariable=var_password, width=350, height=35,
                 font=('courier', 14), border_width=1, border_color='#DA7297',
                 justify='center', show='*').place(x=50, y=310)
        CTkButton(fr, text='Forgot Password', width=150, height=20, fg_color='transparent',
                  text_color='#DA7297', font=('arial', 16, 'bold'), bg_color='transparent',
                  hover_color='#F6F5F5',
                  command=lambda: forgot_password()).place(x=150, y=360)
        CTkButton(fr, text='Login', width=150, height=20, border_spacing=20,
                  fg_color='#DA7297', text_color='white', bg_color='#F6F5F5',
                  font=('arial', 16, 'bold'), border_color='#DA7297',
                  hover_color='#DA7297', border_width=2, corner_radius=20,
                  command=login).place(x=155, y=400)

        def forgot_password():
            win = Toplevel()
            win.geometry('400x300+680+150')
            win.title('Forgot Password')
            win.config(bg='#F6F5F5')
            win.resizable(False, False)
            CTkLabel(win, text='Update Your Password', text_color='#DA7297',
                     font=('arial', 16, 'bold')).place(x=50, y=30)
            CTkLabel(win, text='Username', text_color='gray',
                     font=('arial', 14)).place(x=50, y=80)
            en_u = CTkEntry(win, width=300, height=35, font=('arial', 14),
                            border_width=1, border_color='#DA7297')
            en_u.place(x=50, y=110)
            CTkLabel(win, text='New Password', text_color='gray',
                     font=('arial', 14)).place(x=50, y=155)
            en_p = CTkEntry(win, width=300, height=35, font=('arial', 14),
                            border_width=1, border_color='#DA7297', show='*')
            en_p.place(x=50, y=185)

            def do_update():
                u, p = en_u.get().strip(), en_p.get()
                if not u or not p:
                    messagebox.showerror("خطأ", "أدخل الـ username والباسورد الجديد."); return
                if len(p) < 6:
                    messagebox.showerror("خطأ", "الباسورد أقل من 6 أحرف."); return
                try:
                    con = sqlite3.connect('school.db')
                    cur = con.cursor()
                    cur.execute("UPDATE Admin SET admin_password=? WHERE admin_username=?",
                                (hash_password(p), u))
                    if cur.rowcount == 0:
                        messagebox.showerror("خطأ", "الـ username مش موجود.")
                    else:
                        con.commit()
                        messagebox.showinfo("تم", "تم تحديث كلمة المرور.")
                        win.destroy()
                    con.close()
                except Exception as e:
                    messagebox.showerror("خطأ", str(e))

            CTkButton(win, text='Update Password', width=180, border_spacing=12,
                      fg_color='#DA7297', text_color='white', bg_color='#F6F5F5',
                      font=('arial', 14, 'bold'), corner_radius=20,
                      command=do_update).place(x=60, y=240)

        # ---- Sign Up ----
        s_name = StringVar(); s_user = StringVar()
        s_pass = StringVar(); s_conf = StringVar()

        img2 = CTkImage(Image.open('images/login.png'), size=(490, 400))
        CTkLabel(sign_up_frame, text='', image=img2, fg_color='#F6F5F5').place(x=10, y=70)
        sfr = CTkFrame(sign_up_frame, width=520, height=500, fg_color='#F6F5F5',
                       bg_color='#F6F5F5', border_width=2, corner_radius=30,
                       border_color='#DA7297')
        sfr.place(x=520, y=20)
        CTkLabel(sfr, text='Sign Up Page', corner_radius=10, fg_color='#DA7297',
                 width=200, height=25, text_color='white',
                 font=('arial', 20, 'bold')).place(x=150, y=20)
        CTkLabel(sfr, text='Already a Member?', text_color='#DA7297',
                 font=('arial', 14, 'bold')).place(x=70, y=90)
        CTkButton(sfr, text='Login Page', width=100, height=20, fg_color='transparent',
                  text_color='gray', font=('arial', 14, 'bold'), bg_color='transparent',
                  hover_color='#F6F5F5',
                  command=lambda: show_frame(login_frame)).place(x=210, y=90)

        for lbl_t, var, y_l, y_e, mask in [
            ('Name',     s_name, 120, 150, False),
            ('Username', s_user, 190, 220, False),
            ('Password', s_pass, 260, 290, True),
            ('Confirm',  s_conf, 330, 360, True),
        ]:
            CTkLabel(sfr, text=lbl_t, height=25, text_color='gray',
                     font=('arial', 14)).place(x=75, y=y_l)
            kw = dict(textvariable=var, width=350, height=35, font=('courier', 14),
                      border_width=1, border_color='#DA7297', justify='center')
            if mask: kw['show'] = '*'
            CTkEntry(sfr, **kw).place(x=75, y=y_e)

        def sign_up():
            n, u, p, cp = s_name.get().strip(), s_user.get().strip(), s_pass.get(), s_conf.get()
            if not all([n, u, p, cp]):
                messagebox.showerror('خطأ', 'أدخل كل البيانات.'); return
            if p != cp:
                messagebox.showerror('خطأ', 'الباسورد والتأكيد مش متطابقين.'); return
            if len(p) < 6:
                messagebox.showerror('خطأ', 'الباسورد أقل من 6 أحرف.'); return
            try:
                con = sqlite3.connect('school.db')
                cur = con.cursor()
                cur.execute("INSERT INTO Account(name,username,password) VALUES(?,?,?)",
                            (n, u, hash_password(p)))
                con.commit(); con.close()
                messagebox.showinfo('تم', 'تم إنشاء الحساب.')
                for v in (s_name, s_user, s_pass, s_conf): v.set("")
            except sqlite3.IntegrityError:
                messagebox.showerror('خطأ', 'الـ username موجود بالفعل.')
            except Exception as e:
                messagebox.showerror('خطأ', str(e))

        CTkButton(sfr, text='Sign Up', width=150, height=20, border_spacing=20,
                  fg_color='#DA7297', text_color='white', bg_color='#F6F5F5',
                  font=('arial', 16, 'bold'), border_color='#DA7297',
                  hover_color='#DA7297', border_width=2, corner_radius=20,
                  command=sign_up).place(x=155, y=410)


if __name__ == "__main__":
    root = Tk()
    LoginClass(root)
    root.mainloop()
