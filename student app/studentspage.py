from customtkinter import * 
from tkinter import * 
from PIL import Image
from time import strftime

import dashboard
import firststudent

class StudentsClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry('1200x690+100+5')
        self.root.title('Students Page')
        self.root.config(bg='white')
        self.root.resizable(False,False)

        #=========================== import pages =========================
        def open_firststudent_page():
            window = Toplevel()
            firststudent.FirstStudentClass(window)
            root.withdraw()
            window.deiconify()

        def date():
            date_1 = strftime('%I:%M:%S %p \t %A \t %b/%d/%Y')
            date_lbl.config(text=date_1)
            date_lbl.after(1000,date)
        #============================== head frame ==========================
        up_frame = CTkFrame(root,width=1199,height=70,bg_color='#F6F5F5',fg_color='#F6F5F5',border_color='#DA7297',border_width=2)
        up_frame.place(x=1,y=1)

        text_lbl = Label(up_frame, text='Students Page',font=('corier',18,'bold'),bg='#F6F5F5',fg='#DA7297')
        text_lbl.place(x=150,y=5,width=200,height=60)

        date_lbl = Label(up_frame,font=('corier',18,'bold'),bg='#F6F5F5',fg='#DA7297')
        date_lbl.place(x=590,y=5,width=570,height=60)
        date()

        #=================== back button ================
        def back():
            win = Toplevel()
            dashboard.DashboardClass(win)
            root.withdraw()
            win.deiconify()
        

        back_btn = CTkButton(up_frame,text='←', width=100,height=68,
                             fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                             font=('arial',30,'bold'),hover_color='#DA7297',border_color='#DA7297',
                             corner_radius=0,command=back)
        back_btn.place(x=2,y=2)

        #============================= up frame ==========================
        head_frame = CTkFrame(root,width=1197,height=615,bg_color='white',fg_color='#F6F5F5',border_color='#DA7297',border_width=2)
        head_frame.place(x=1,y=72)

        #============================= buttons ===========================
        img = CTkImage(Image.open('images/stu.png'),size=(150,150))

        first_btn = CTkButton(head_frame,text='FIRST GRADE MIDDLE SCHOOL',width=300,height=200,
                              fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                              border_spacing=20,hover_color='#DA7297',border_width=5,image=img,
                              compound='top',font=('arial',25,'bold'),border_color='#D8D2C2',
                              corner_radius=30,command=open_firststudent_page)
        first_btn.place(x=100,y=60)

        second_btn = CTkButton(head_frame,text='SECOND GRADE MIDDLE SCHOOL',width=300,height=200,
                              fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                              border_spacing=20,hover_color='#DA7297',border_width=5,image=img,
                              compound='top',font=('arial',25,'bold'),border_color='#D8D2C2',
                              corner_radius=30)
        second_btn.place(x=620,y=60)

        third_btn = CTkButton(head_frame,text='THIRD GRADE MIDDLE SCHOOL',width=300,height=200,
                              fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                              border_spacing=20,hover_color='#DA7297',border_width=5,image=img,
                              compound='top',font=('arial',25,'bold'),border_color='#D8D2C2',
                              corner_radius=30)
        third_btn.place(x=360,y=340)

        


if __name__=="__main__":
    root = Tk()
    StudentsClass(root)
    root.mainloop()        