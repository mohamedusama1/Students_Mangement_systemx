from customtkinter import *
from tkinter import *
from PIL import Image
from time import strftime

import dashboard
import firststudent
import importpage
from auth import session


class StudentsClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x690+100+5')
        self.root.title('Students Page')
        self.root.config(bg='white')
        self.root.resizable(False, False)

        def open_firststudent_page():
            window = Toplevel()
            firststudent.FirstStudentClass(window)
            root.withdraw()
            window.deiconify()

        def open_import_page():
            window = Toplevel()
            importpage.ImportClass(window)
            # مش بنعمل withdraw عشان Import صفحة مساعدة وليست رئيسية

        def date():
            date_1 = strftime('%I:%M:%S %p \t %A \t %b/%d/%Y')
            date_lbl.config(text=date_1)
            date_lbl.after(1000, date)

        # ====================== head frame ======================
        up_frame = CTkFrame(root, width=1199, height=70, bg_color='#F6F5F5',
                            fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        up_frame.place(x=1, y=1)

        Label(up_frame, text='Students Page', font=('courier', 18, 'bold'),
              bg='#F6F5F5', fg='#DA7297').place(x=150, y=5, width=200, height=60)

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

        # ====================== main frame ======================
        head_frame = CTkFrame(root, width=1197, height=615, bg_color='white',
                              fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        head_frame.place(x=1, y=72)

        img = CTkImage(Image.open('images/stu.png'), size=(150, 150))

        # ---- Grade buttons ----
        CTkButton(head_frame, text='FIRST GRADE\nMIDDLE SCHOOL', width=300, height=200,
                  fg_color='#DA7297', text_color='white', bg_color='#F6F5F5',
                  border_spacing=20, hover_color='#DA7297', border_width=5, image=img,
                  compound='top', font=('arial', 22, 'bold'), border_color='#D8D2C2',
                  corner_radius=30, command=open_firststudent_page).place(x=100, y=60)

        CTkButton(head_frame, text='SECOND GRADE\nMIDDLE SCHOOL', width=300, height=200,
                  fg_color='#DA7297', text_color='white', bg_color='#F6F5F5',
                  border_spacing=20, hover_color='#DA7297', border_width=5, image=img,
                  compound='top', font=('arial', 22, 'bold'), border_color='#D8D2C2',
                  corner_radius=30).place(x=620, y=60)

        CTkButton(head_frame, text='THIRD GRADE\nMIDDLE SCHOOL', width=300, height=200,
                  fg_color='#DA7297', text_color='white', bg_color='#F6F5F5',
                  border_spacing=20, hover_color='#DA7297', border_width=5, image=img,
                  compound='top', font=('arial', 22, 'bold'), border_color='#D8D2C2',
                  corner_radius=30).place(x=360, y=340)

        # ---- Import button — يظهر بس للي عنده صلاحية ----
        if session.can("add_student"):
            import_img = CTkImage(Image.open('images/stu.png'), size=(50, 50))
            CTkButton(head_frame,
                      text='📥  استيراد طلاب\nمن CSV / Excel',
                      width=220, height=70,
                      fg_color='#2e7d32', text_color='white', bg_color='#F6F5F5',
                      font=('arial', 14, 'bold'), border_color='#2e7d32',
                      hover_color='#1b5e20', border_width=2, corner_radius=15,
                      command=open_import_page).place(x=950, y=520)
        else:
            Label(head_frame, text="🔒 استيراد — superadmin/admin فقط",
                  bg='#F6F5F5', fg='#aaaaaa',
                  font=('arial', 10)).place(x=910, y=535)


if __name__ == "__main__":
    root = Tk()
    StudentsClass(root)
    root.mainloop()
