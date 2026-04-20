from customtkinter import * 
from tkinter import * 
from PIL import Image
from time import strftime
from tkinter import ttk,messagebox
import datetime
from tkcalendar import *
import sqlite3


import studentspage
import first_student_marks

class FirstStudentClass:
    def __init__(self,root):
        self.root = root
        self.root.geometry('1200x690+100+5')
        self.root.title('First Students Page')
        self.root.config(bg='white')
        self.root.resizable(False,False)

        def open_first_student_marks_page():
            win = Toplevel()
            first_student_marks.First_Student_Marks_Class(win)
            root.withdraw()
            win.deiconify()

        def date():
            date_1 = strftime('%I:%M:%S %p \t %A \t %b/%d/%Y')
            date_lbl.config(text=date_1)
            date_lbl.after(1000,date)

        def rec_id():
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            cur.execute("""
            WITH RECURSIVE cte AS (
            SELECT ROW_NUMBER() OVER (ORDER BY s_ID) AS new_id, s_ID
            FROM first_student

            )
            UPDATE first_student
            SET s_ID =(SELECT new_id FROM cte WHERE cte.s_ID = first_student.s_ID)
            """)

        def add():
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            if (var_name.get()=="" or var_gender.get()=="" or var_age.get()=="" or var_address.get()=="" or var_phone.get()=="" or var_date.get()=="" or var_lastschool.get()=="" or var_yearsfelid.get()=="" or var_healthproblem.get()=="" or var_finalresult.get()==""):
                messagebox.showerror("error","enter all the data")
            else:
                cur.execute("INSERT INTO first_student(student_name,student_gender,student_age,address,contact, date,last_school,years_felid,health_problem,final_result) VALUES(?,?,?,?,?,?,?,?,?,?)",(
                    var_name.get(),
                    var_gender.get(),
                    var_age.get(),
                    var_address.get(),
                    var_phone.get(),
                    var_date.get(),
                    var_lastschool.get(),
                    var_yearsfelid.get(),
                    var_healthproblem.get(),
                    var_finalresult.get(),

                )) 
                messagebox.showinfo("success","add successfully")
            con.commit()  
            rec_id()
            show()
            clear()

        def clear():
            var_name.set("")
            var_gender.set("")
            var_age.set("")
            var_address.set("")
            var_phone.set("")
            var_date.set("")
            var_lastschool.set("")
            var_yearsfelid.set("")
            var_healthproblem.set("")
            var_finalresult.set("")   

            cmb_search.set("Select") 
            var_search.set("")
            
            show()   

        def show():
            con = sqlite3.connect('school.db')   
            cur = con.cursor()
            try:
                cur.execute("select * from first_student")
                rows = cur.fetchall() 
                student_tree.delete(*student_tree.get_children())
                global count
                count = 0  
                for row in rows:
                    if count % 2 == 0:
                        student_tree.insert(parent='', index='end', iid=count, text='',values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]), tags=('evenrow',))
                    else:
                        student_tree.insert(parent='', index='end', iid=count, text='',values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10]), tags=('oddrow',))
                                  
                    count +=1
            except Exception as ex:
                messagebox.showerror("error",f"error {str(ex)}")        

        def get_data(ev):
            f = student_tree.focus()
            n = (student_tree.item(f))
            row = n['values']

            var_id.set(row[0])
            var_name.set(row[1])
            var_gender.set(row[2])
            var_age.set(row[3])
            var_address.set(row[4])
            var_phone.set(row[5])
            var_date.set(row[6])
            var_lastschool.set(row[7])
            var_yearsfelid.set(row[8])
            var_healthproblem.set(row[9])
            var_finalresult.set(row[10])

        def update():
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            cur.execute("UPDATE first_student set student_name=?, student_gender=?, student_age=?,address=?,contact=?,date=?,last_school=?,years_felid=?,health_problem=?,final_result=? where s_ID=?",(
                        var_name.get(),
                        var_gender.get(),
                        var_age.get(),
                        var_address.get(),
                        var_phone.get(),
                        var_date.get(),
                        var_lastschool.get(),
                        var_yearsfelid.get(),
                        var_healthproblem.get(),
                        var_finalresult.get(),
                        var_id.get(),

            ))
            con.commit()
            rec_id()
            messagebox.showinfo("success","update successfully")
            show()
            clear()

        def delete():
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            op = messagebox.askyesno("confirm","do you want to delete")
            op==True
            cur.execute("delete from first_student where s_ID=?",(var_id.get(),))
            con.commit()
            rec_id()
            messagebox.showinfo("success","delete successfully")
            show()
            clear()

        def search():
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            try:
                if cmb_search.get()=="Select":
                    messagebox.showerror("error","Select search by option")
                else:
                    cur.execute("select * from first_student where "+cmb_search.get()+" LIKE '%"+var_search.get()+"%'")
                    rows=cur.fetchall()  
                    if len(rows)!=0:
                        student_tree.delete(*student_tree.get_children())
                        for row in rows:
                            student_tree.insert('',END,values=row)  
                    else:
                        messagebox.showerror("error","no record found")
            except Exception as ex:
                messagebox.showerror("error",f"error {str(ex)}")                     
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
            studentspage.StudentsClass(win)
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

        #============================= search area========================
        var_search=StringVar()

        frame_search = CTkFrame(head_frame,width=880,height=60,bg_color='#F6F5F5',
                                fg_color='white',border_width=2,border_color='#DA7297')
        frame_search.place(x=30,y=10)

        lbl_text = Label(frame_search,text='Search Student',font=('arial',16,'bold'),
                         bg='white',fg='#DA7297')
        lbl_text.place(x=5,y=5,width=180,height=50)

        cmb_search = CTkComboBox(frame_search,values=("Select","student_name","contact"),
                                 button_hover_color='#DA7297',justify=CENTER,
                                 font=('arial',15),width=180,height=35,fg_color='white',
                                 border_width=1,border_color='#DA7297',button_color='#DA7297',
                                 dropdown_fg_color='white',dropdown_text_color='#DA7297')
        cmb_search.place(x=180,y=13)

        search_en = CTkEntry(frame_search,textvariable=var_search,width=250,height=35,fg_color='white',justify='center',
                             border_color='#DA7297',bg_color='white',border_width=1,
                             font=('arial',14))
        search_en.place(x=380,y=13)

        search_btn = CTkButton(frame_search,text='SEARCH',width=200,height=40,
                               fg_color='#DA7297',text_color='white',bg_color='white',
                               font=('arial',16,'bold'), hover_color='#DA7297',
                               corner_radius=10,command=search)
        search_btn.place(x=650,y=10)

        #============================= student tree ============================
        

        student_frame = Frame(head_frame,bg='gray')
        student_frame.place(x=3,y=90,width=1188,height=447)

        student_tree = ttk.Style()
        student_tree.theme_use('clam')

        student_tree.configure('Treeview',bg='#D3D3D3',font=('arial',12),fg='black',
                               rowheight=30,fieldbackground='white')
        student_tree.configure('Treeview.Heading',background='#DA7297',foreground='white',
                               font=('arial',12,'bold'),height=100)
        
        student_tree_scroll_y = Scrollbar(student_frame)
        student_tree_scroll_y.pack(side=RIGHT,fill=Y)

        student_tree_scroll_x = Scrollbar(student_frame,orient=HORIZONTAL)
        student_tree_scroll_x.pack(side=BOTTOM,fill=X)

        student_tree = ttk.Treeview(student_frame,yscrollcommand=student_tree_scroll_y.set,xscrollcommand=student_tree_scroll_x.set)
        student_tree.place(x=0,y=0,width=1171,height=430)

        student_tree_scroll_y.config(command=student_tree.yview)
        student_tree_scroll_x.config(command=student_tree.xview)

        student_tree.configure(columns=("s_ID","student_name","student_gender","student_age",
                                        "address","contact","date","last_school","years_feild",
                                        "health_problem","finall_result"))
        
        student_tree.heading("s_ID", text="ID")
        student_tree.heading("student_name", text="Student name")
        student_tree.heading("student_gender", text="Student gender")
        student_tree.heading("student_age", text="Student age")
        student_tree.heading("address", text="Address")
        student_tree.heading("contact", text="Phone number")
        student_tree.heading("date", text="Date")
        student_tree.heading("last_school", text="Last school")
        student_tree.heading("years_feild", text="Years feild")
        student_tree.heading("health_problem", text="Health problem")
        student_tree.heading("finall_result", text="Finall result")

        student_tree["show"] = "headings"

        student_tree.column("s_ID", width=50,anchor=W)
        student_tree.column("student_name", width=180,anchor=W)
        student_tree.column("student_gender", width=150,anchor=W)
        student_tree.column("student_age", width=150,anchor=W)
        student_tree.column("address", width=100,anchor=W)
        student_tree.column("contact", width=150,anchor=W)
        student_tree.column("date", width=110,anchor=W)
        student_tree.column("last_school", width=180,anchor=W)
        student_tree.column("years_feild", width=130,anchor=W)
        student_tree.column("health_problem", width=180,anchor=W)
        student_tree.column("finall_result", width=100,anchor=W)
        student_tree.bind("<ButtonRelease-1>",get_data)
        show()

        student_tree.tag_configure('oddrow', background='lightgray')
        student_tree.tag_configure('evenrow', background='#F6F5F5')

        #=================== varibale =============================
        var_id = StringVar()
        var_name =StringVar()
        var_gender = StringVar()
        var_age = StringVar()
        var_gender = StringVar()
        var_address = StringVar()
        var_phone = StringVar()
        var_date = StringVar()
        var_lastschool = StringVar()
        var_yearsfelid = StringVar()
        var_healthproblem = StringVar()
        var_finalresult = StringVar()

        #======================= entry window ======================
        #datenow = datetime.datetime.now()
        #date = datenow.strftime('%Y-%m-%d')
          
        def window_entry():
            win = Toplevel(root)
            win.geometry('1185x450+106+190')
            win.title('Add Information Students')
            win.resizable(False,False)
            win.config(bg='white')
            win.transient(root)
            #win.grab_set()
            win.focus_set()
            win.lift()

            win_en_frame = CTkFrame(win,width=1185,height=449,bg_color='#F6F5F5',fg_color='#F6F5F5',border_width=2,border_color='#DA7297')
            win_en_frame.place(x=1,y=1)

            def win_cal(event):
                global cal , date_win

                date_win = Toplevel()
                date_win.grab_set()
                date_win.geometry('250x220+200+400')
                date_win.title('choose date of brith')
                date_win.resizable(False,False)

                cal = Calendar(date_win,selectmode="day",date_pattern="mm/dd/yy")
                cal.place(x=0,y=0)

                submit_btn = Button(date_win, text='add date', bg='#DA7297',fg='white',command=date_b)
                submit_btn.place(x=80,y=190)

            def date_b():
                en_sage.delete(0,END)
                en_sage.insert(0, cal.get_date())
                date_win.destroy()

            #================== labels + entrys ============================
            
            lbl_title = CTkLabel(win_en_frame,text='Enter Students Informations',width=1120,height=60,
                                 text_color='#DA7297',font=('arial',20,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_title.place(x=20,y=5)


            lbl_sname = CTkLabel(win_en_frame,text='Student Name',width=50,height=25,
                                 text_color='#DA7297',font=('arial',16,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_sname.place(x=30,y=75)

            en_sname = CTkEntry(win_en_frame,textvariable=var_name,width=300,height=35,justify='center',fg_color='white',
                                font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            
            en_sname.place(x=30,y=100)

            lbl_sgender = CTkLabel(win_en_frame,text='Student Gender',width=50,height=25,
                                 text_color='#DA7297',font=('arial',16,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_sgender.place(x=30,y=175)

            cob_gender = CTkComboBox(win_en_frame,variable=var_gender,values=("Select","Male","Female"),
                                     button_hover_color='#DA7297',justify=CENTER,width=300,height=35,
                                     fg_color='white',border_width=1,border_color='#DA7297',button_color='#DA7297',
                                     font=('arial',15),dropdown_fg_color='white',dropdown_text_color='#DA7297')
            cob_gender.place(x=30,y=200)

            lbl_sage = CTkLabel(win_en_frame,text='Student Age',width=50,height=25,
                                 text_color='#DA7297',font=('arial',16,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_sage.place(x=30,y=275)

            en_sage = CTkEntry(win_en_frame,textvariable=var_age,width=300,height=35,justify='center',fg_color='white',
                                font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            
            en_sage.place(x=30,y=300)
            #en_sage.insert(0,"dd/mm/y")
            en_sage.bind("<1>",win_cal)
            

            lbl_address = CTkLabel(win_en_frame,text='Address',width=50,height=25,
                                 text_color='#DA7297',font=('arial',16,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_address.place(x=30,y=375)

            en_address = CTkEntry(win_en_frame,textvariable=var_address,width=300,height=35,justify='center',fg_color='white',
                                font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            
            en_address.place(x=30,y=400)


            lbl_phone = CTkLabel(win_en_frame,text='Phone number',width=50,height=25,
                                 text_color='#DA7297',font=('arial',16,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_phone.place(x=400,y=75)

            en_phone = CTkEntry(win_en_frame,textvariable=var_phone,width=300,height=35,justify='center',fg_color='white',
                                font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            
            en_phone.place(x=400,y=100)

            lbl_date = CTkLabel(win_en_frame,text='Date',width=50,height=25,
                                 text_color='#DA7297',font=('arial',16,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_date.place(x=400,y=175)

            en_date = CTkEntry(win_en_frame,textvariable=var_date,width=300,height=35,justify='center',fg_color='white',
                                font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            
            en_date.place(x=400,y=200)
            #en_date.insert('1',str(date))

            lbl_last_school = CTkLabel(win_en_frame,text='last school',width=50,height=25,
                                 text_color='#DA7297',font=('arial',16,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_last_school.place(x=400,y=275)

            en_last_school = CTkEntry(win_en_frame,textvariable=var_lastschool,width=300,height=35,justify='center',fg_color='white',
                                font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            
            en_last_school.place(x=400,y=300)

            lbl_years_field = CTkLabel(win_en_frame,text='years field',width=50,height=25,
                                 text_color='#DA7297',font=('arial',16,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_years_field.place(x=400,y=375)

            en_years_field = CTkEntry(win_en_frame,textvariable=var_yearsfelid,width=300,height=35,justify='center',fg_color='white',
                                font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            
            en_years_field.place(x=400,y=400)

            lbl_health_problem = CTkLabel(win_en_frame,text='health problem',width=50,height=25,
                                 text_color='#DA7297',font=('arial',16,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_health_problem.place(x=800,y=75)

            en_health_problem = CTkEntry(win_en_frame,textvariable=var_healthproblem,width=300,height=35,justify='center',fg_color='white',
                                font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            
            en_health_problem.place(x=800,y=100)

            lbl_final_reasult= CTkLabel(win_en_frame,text='final reasult',width=50,height=25,
                                 text_color='#DA7297',font=('arial',16,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_final_reasult.place(x=800,y=175)

            en_final_reasult = CTkEntry(win_en_frame,textvariable=var_finalresult,width=300,height=35,justify='center',fg_color='white',
                                font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            
            en_final_reasult.place(x=800,y=200)

            add_btn = CTkButton(win_en_frame,text='ADD STUDENT INFORMATION',width=300,height=40,fg_color='#DA7297',
                            text_color='white',bg_color='#F6F5F5',border_width=2,hover_color='#DA7297',
                            border_color='#F6F5F5',corner_radius=10,font=("arial",16,'bold'),command=add)
            add_btn.place(x=800,y=300)
        

        #====================== buttons ==========================
        add_btn = CTkButton(head_frame,text='ADD',width=120,height=40,fg_color='#DA7297',
                            text_color='white',bg_color='#F6F5F5',border_width=2,hover_color='#DA7297',
                            border_color='#F6F5F5',corner_radius=10,font=("arial",16,'bold'),command=window_entry)
        add_btn.place(x=100,y=565)
        

        delete_btn = CTkButton(head_frame,text='DELETE',width=120,height=40,fg_color='#DA7297',
                            text_color='white',bg_color='#F6F5F5',border_width=2,hover_color='#DA7297',
                            border_color='#F6F5F5',corner_radius=10,font=("arial",16,'bold'),command=delete)
        delete_btn.place(x=250,y=565)

        update_btn = CTkButton(head_frame,text='UPDATE',width=120,height=40,fg_color='#DA7297',
                            text_color='white',bg_color='#F6F5F5',border_width=2,hover_color='#DA7297',
                            border_color='#F6F5F5',corner_radius=10,font=("arial",16,'bold'),command=update)
        update_btn.place(x=400,y=565)

        clear_btn = CTkButton(head_frame,text='CLEAR',width=120,height=40,fg_color='#DA7297',
                            text_color='white',bg_color='#F6F5F5',border_width=2,hover_color='#DA7297',
                            border_color='#F6F5F5',corner_radius=10,font=("arial",16,'bold'),command=clear)
        clear_btn.place(x=550,y=565)

        img = CTkImage(Image.open('images/stu.png'),size=(40,40))
        marks_btn = CTkButton(head_frame,text='Student Marks',image=img,width=120,height=60,fg_color='#DA7297',
                            text_color='white',bg_color='#F6F5F5',border_width=2,hover_color='#DA7297',
                            border_color='#F6F5F5',corner_radius=10,
                            font=("arial",16,'bold'),command=open_first_student_marks_page)
        marks_btn.place(x=970,y=10)
        


if __name__=="__main__":
    root = Tk()
    FirstStudentClass(root)
    root.mainloop()        