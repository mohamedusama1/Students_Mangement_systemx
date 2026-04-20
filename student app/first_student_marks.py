from customtkinter import * 
from tkinter import * 
from PIL import Image
from time import strftime
from tkinter import ttk,messagebox
import datetime
from tkcalendar import *
import sqlite3
import win32print
import win32ui

import firststudent


class First_Student_Marks_Class:
    def __init__(self,root):
        self.root = root
        self.root.geometry('1200x690+100+5')
        self.root.title('First Students Marks Page')
        self.root.config(bg='white')
        self.root.resizable(False,False)

        def date():
            date_1 = strftime('%I:%M:%S %p \t %A \t %b/%d/%Y')
            date_lbl.config(text=date_1)
            date_lbl.after(1000,date)


        #============================= functions student marks name ================
        def get_student_names_islamic():
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            cur.execute("SELECT student_name FROM islamic_marks")
            rows = cur.fetchall()
            con.close()
            return[row[0] for row in rows]

        def get_student_names_arabic():
            con = sqlite3.connect('school.db')
            cur = con.cursor()
            cur.execute("SELECT student_name FROM arabic_marks")
            rows = cur.fetchall()
            con.close()
            return[row[0] for row in rows]

        #============================== functions marks =====================
        def add_islamic_marks():
            #student_name = cmb_student_name_islamic.get()

            con = sqlite3.connect('school.db')
            cur = con.cursor()
            #.execute("SELECT chapter1, half_year, chapter2, chapter3, final_exam, final_result FROM islamic_marks WHERE student_name=?",(student_name,))
            result = cur.fetchone()
            con.close()

            if result:
                var_ch1, var_half_y, var_ch2, var_ch3, var_final_e,var_final_r = result
                #marks = (f"\t\t\tStudent Result\n\nSchool Name: NoOr School\n\nStudent Name: {student_name}\n\n——————————————————————————————\n\t ch one \t half year \t ch tow \t ch three \t f exam \t f result\n——————————————————————————————\nIslamic\t{var_ch1} \t {var_half_y} \t {var_ch2} \t {var_ch3} \t {var_final_e} \t {var_final_r}")
            else:
                marks = "no result"
            #text_reslut.insert(END,marks)    


        #============================== functions marks =====================
        def add_arabic_marks():
            #student_name = cmb_student_name_arabic.get()

            con = sqlite3.connect('school.db')
            cur = con.cursor()
            #cur.execute("SELECT chapter1, half_year, chapter2, chapter3, final_exam, final_result FROM arabic_marks WHERE student_name=?",(student_name,))
            result = cur.fetchone()
            con.close()

            if result:
                var_ch1, var_half_y, var_ch2, var_ch3, var_final_e,var_final_r = result
                marks = (f"\n——————————————————————————————\nArabic\t{var_ch1} \t {var_half_y} \t {var_ch2} \t {var_ch3} \t {var_final_e} \t {var_final_r}")
            else:
                marks = "no result"
            #text_reslut.insert(END,marks)    

               
        #============================== head frame ==========================
        up_frame = CTkFrame(root,width=1199,height=70,bg_color='#F6F5F5',fg_color='#F6F5F5',border_color='#DA7297',border_width=2)
        up_frame.place(x=1,y=1)

        text_lbl = Label(up_frame, text='Students Marks Page',font=('corier',18,'bold'),bg='#F6F5F5',fg='#DA7297')
        text_lbl.place(x=150,y=5,width=300,height=60)

        date_lbl = Label(up_frame,font=('corier',18,'bold'),bg='#F6F5F5',fg='#DA7297')
        date_lbl.place(x=590,y=5,width=570,height=60)
        date()

        #=================== back button ================
        def back():
            win = Toplevel()
            firststudent.FirstStudentClass(win)
            root.withdraw()
            win.deiconify()
        

        back_btn = CTkButton(up_frame,text='←', width=100,height=68,
                             fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                             font=('arial',30,'bold'),hover_color='#DA7297',border_color='#DA7297',
                             corner_radius=0,command=back)
        back_btn.place(x=2,y=2)

        #=================================================================
        #======================== islamic marks window ===================
        def window_islamic():
            win_islamic = Toplevel()
            win_islamic.geometry('1200x690+100+5')
            win_islamic.title('Add Islamic Students Marks')
            win_islamic.resizable(False,False)
            win_islamic.config(bg='#F6F5F5')

            root.withdraw()

            def date_i():
                date_1 = strftime('%I:%M:%S %p \t %A \t %b/%d/%Y')
                date_lbl.config(text=date_1)
                date_lbl.after(1000,date)

            def back():
                win_islamic.destroy()
                root.deiconify() 

            def record_id():
                con = sqlite3.connect('school.db')
                cur = con.cursor()  
                cur.execute("""
                WITH RECURSIVE cte AS(
                            SELECT ROW_NUMBER() OVER (ORDER BY i_ID) AS new_id, i_ID
                            FROM islamic_marks
                            )
                            UPDATE islamic_marks
                            SET i_ID = (SELECT new_id FROM cte WHERE cte.i_ID = islamic_marks.i_ID)
                """)








            def add_islamic_marks():
                con = sqlite3.connect('school.db')
                cur = con.cursor() 

                f_m_value = var_islamic_f_m.get()
                s_m_value = var_islamic_s_m.get()

                avreage_ch1 = (f_m_value + s_m_value) / 2

                var_islamic_ch1.set(avreage_ch1)

                f_m_value1 = var_islamic_f_m1.get()
                s_m_value2 = var_islamic_s_m2.get()

                avreage_ch2 = (f_m_value1 + s_m_value2) / 2

                var_islamic_ch2.set(avreage_ch2)

                ch1 = var_islamic_ch1.get()
                half_y = var_islamic_half_y.get()
                ch2 = var_islamic_ch2.get()

                avreage_ch3 = (ch1 + half_y + ch2) / 3

                var_islamic_ch3.set(avreage_ch3)

                ch3 = var_islamic_ch3.get()
                final_exam = var_islamic_f_exam.get()

                avreage_f = (ch3 + final_exam) / 2

                var_islamic_f_r.set(avreage_f)
                
                
                cur.execute("INSERT INTO islamic_marks(student_name,st_month,nd_month,chapter1,half_year,st_month1,nd_month2,chapter2,chapter3,final_exam,final_result) values(?,?,?,?,?,?,?,?,?,?,?)",(
                            var_s_name.get(),
                            var_islamic_f_m.get(),
                            var_islamic_s_m.get(),
                            var_islamic_ch1.get(),
                            var_islamic_half_y.get(),
                            var_islamic_f_m1.get(),
                            var_islamic_s_m2.get(),
                            var_islamic_ch2.get(),
                            var_islamic_ch3.get(),
                            var_islamic_f_exam.get(),
                            var_islamic_f_r.get(),
                ))    
                messagebox.showinfo("success","add successfully")
                con.commit()
                
                show_islamic_marks()
                clear_islamic_marks()

                

            def show_islamic_marks():
                con = sqlite3.connect('school.db')
                cur = con.cursor()
                try:
                    cur.execute("select * from islamic_marks")
                    rows = cur.fetchall()    
                    student_marks_tree_islamic.delete(*student_marks_tree_islamic.get_children())
                    global count
                    count = 0
                    for row in rows:
                        if count % 2 ==0:
                            student_marks_tree_islamic.insert(parent='',index='end',iid=count,text='',values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]),tags=('evenrow'))
                        else:
                            student_marks_tree_islamic.insert(parent='',index='end',iid=count,text='',values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]),tags=('oddrow'))
                            
                        count +=1
                except Exception as es:
                    messagebox.showerror("error",f"error: {str(es)}")  

            
            def clear_islamic_marks():
                var_s_name.set("")
                var_islamic_f_m.set("0")
                var_islamic_s_m.set("0")
                var_islamic_ch1.set("0")
                var_islamic_half_y.set("0")
                var_islamic_f_m1.set("0")
                var_islamic_s_m2.set("0")
                var_islamic_ch2.set("0")
                var_islamic_ch3.set("0")
                var_islamic_f_exam.set("0")
                var_islamic_f_r.set("0")

                var_serarch_en.set("")
                cmb_search.set("Select")

                show_islamic_marks()
            

            def get_data_islamic_marks(ev):
                n = student_marks_tree_islamic.focus()
                f = (student_marks_tree_islamic.item(n))
                row = f['values']

                var_id.set(row[0])
                var_s_name.set(row[1])
                var_islamic_f_m.set(row[2])
                var_islamic_s_m.set(row[3])
                var_islamic_ch1.set(row[4])
                var_islamic_half_y.set(row[5])
                var_islamic_f_m1.set(row[6])
                var_islamic_s_m2.set(row[7])
                var_islamic_ch2.set(row[8])
                var_islamic_ch3.set(row[9])
                var_islamic_f_exam.set(row[10])
                var_islamic_f_r.set(row[11])

            def update_islamic_marks():
                con = sqlite3.connect('school.db')
                cur = con.cursor() 

                f_m_value = var_islamic_f_m.get()
                s_m_value = var_islamic_s_m.get()

                avreage_ch1 = (f_m_value + s_m_value) / 2

                var_islamic_ch1.set(avreage_ch1)

                f_m_value1 = var_islamic_f_m1.get()
                s_m_value2 = var_islamic_s_m2.get()

                avreage_ch2 = (f_m_value1 + s_m_value2) / 2

                var_islamic_ch2.set(avreage_ch2)

                ch1 = var_islamic_ch1.get()
                half_y = var_islamic_half_y.get()
                ch2 = var_islamic_ch2.get()

                avreage_ch3 = (ch1 + half_y + ch2) / 3

                var_islamic_ch3.set(avreage_ch3)

                ch3 = var_islamic_ch3.get()
                final_exam = var_islamic_f_exam.get()

                avreage_f = (ch3 + final_exam) / 2

                var_islamic_f_r.set(avreage_f)
                
                
                cur.execute("UPDATE islamic_marks set student_name=?,st_month=?,nd_month=?,chapter1=?,half_year=?,st_month1=?,nd_month2=?,chapter2=?,chapter3=?,final_exam=?,final_result=? WHERE i_ID=?",(
                            var_s_name.get(),
                            var_islamic_f_m.get(),
                            var_islamic_s_m.get(),
                            var_islamic_ch1.get(),
                            var_islamic_half_y.get(),
                            var_islamic_f_m1.get(),
                            var_islamic_s_m2.get(),
                            var_islamic_ch2.get(),
                            var_islamic_ch3.get(),
                            var_islamic_f_exam.get(),
                            var_islamic_f_r.get(),
                            var_id.get(),
                ))    
                messagebox.showinfo("success","add successfully")
                con.commit()
                
                show_islamic_marks()
                clear_islamic_marks()




























            def delete_islamic_marks():
                con = sqlite3.connect('school.db')
                cur = con.cursor()
                op = messagebox.askyesno("confiem","do you want to delete?")
                op==True
                cur.execute("delete from islamic_marks where i_ID=?",(var_id.get(),))
                con.commit()
                record_id()
                messagebox.showinfo("success","delete successfully")
                show_islamic_marks() 
                clear_islamic_marks()     

            def search_islamic_marks():
                con = sqlite3.connect('school.db')
                cur = con.cursor()
                try:
                    if cmb_search.get()=="Select":
                        messagebox.showerror("errror","select to search")
                    elif var_serarch_en.get()=="":
                        messagebox.showerror("error","inprut to search")
                    else:
                        cur.execute("select * from islamic_marks where "+cmb_search.get()+" LIKE '%"+var_serarch_en.get()+"%'")
                        rows = cur.fetchall() 
                        if len(rows)!=0:
                            student_marks_tree_islamic.delete(*student_marks_tree_islamic.get_children())
                            for row in rows:
                                student_marks_tree_islamic.insert('',END,values=row)     
                        else:
                            messagebox.showerror("error","not found")
                except Exception as ex:
                    messagebox.showerror("error",f"error{str(ex)}")                                           
            #============================== head frame ==========================
            up_frame = CTkFrame(win_islamic,width=1199,height=70,bg_color='#F6F5F5',fg_color='#F6F5F5',border_color='#DA7297',border_width=2)
            up_frame.place(x=1,y=1)

            text_lbl = Label(win_islamic, text='Islamic Students Marks Page',font=('corier',18,'bold'),bg='#F6F5F5',fg='#DA7297')
            text_lbl.place(x=150,y=5,width=350,height=60)

            date_lbl = Label(win_islamic,font=('corier',18,'bold'),bg='#F6F5F5',fg='#DA7297')
            date_lbl.place(x=590,y=5,width=570,height=60)
            date_i()


            back_btn = CTkButton(win_islamic,text='←', width=100,height=68,
                             fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                             font=('arial',30,'bold'),hover_color='#DA7297',border_color='#DA7297',
                             corner_radius=0,command=back)
            back_btn.place(x=2,y=2)

            #============================= up frame ==========================
            head_frame_islamic = CTkFrame(win_islamic,width=1197,height=615,bg_color='white',fg_color='#F6F5F5',border_color='#DA7297',border_width=2)
            head_frame_islamic.place(x=1,y=72)

            #============================= serach area =======================
            var_serarch_en = StringVar()

            serach_frame = CTkFrame(head_frame_islamic,width=820,height=60,bg_color='#F6F5F5',fg_color='white',border_width=2,border_color='#DA7297')
            serach_frame.place(x=300,y=30)

            text_lbl = Label(serach_frame,text='Search Student',font=('arial',14,'bold'),bg='white',fg='#DA7297')
            text_lbl.place(x=5,y=5,width=180,height=50)

            cmb_search = CTkComboBox(serach_frame,values=("Select","student_name"),
                                     button_color='#DA7297',button_hover_color='#DA7297',justify=CENTER,
                                     font=('arial',15),width=180,height=35,fg_color='white',border_width=1,border_color='#DA7297',
                                     dropdown_fg_color='white',dropdown_text_color='#DA7297')
            cmb_search.place(x=180,y=13)

            search_en = CTkEntry(serach_frame,textvariable=var_serarch_en,width=200,height=35,fg_color='white',font=('arial',14),
                                 border_width=1,border_color='#DA7297',bg_color='white',justify='center')
            search_en.place(x=380,y=13)

            search_btn = CTkButton(serach_frame,text='SEARCH',width=200,height=40,
                                   fg_color='#DA7297',text_color='white',bg_color='white',
                                   font=('arial',16,'bold'),border_color='#DA7297',
                                   hover_color='#DA7297',corner_radius=10,command=search_islamic_marks)
            search_btn.place(x=600,y=10)

            #========================== logo image ========================
            img = CTkImage(Image.open('images/marks.png'),size=(300,300))
            img_lbl = CTkLabel(head_frame_islamic,text='',image=img,fg_color='#F6F5F5')
            img_lbl.place(x=1,y=20)

            #============= varibales =====================
            var_id = StringVar()
            var_s_name = StringVar()
            var_islamic_f_m = IntVar()
            var_islamic_s_m = IntVar()
            var_islamic_ch1 = IntVar()
            var_islamic_half_y = IntVar()
            var_islamic_f_m = IntVar()
            var_islamic_f_m1 = IntVar()
            var_islamic_s_m2 = IntVar()
            var_islamic_ch2 = IntVar()
            var_islamic_ch3 = IntVar()
            var_islamic_f_exam = IntVar()
            var_islamic_f_r = IntVar()

            #========================== labels + entrys ====================
            lbl_name = CTkLabel(head_frame_islamic,text='Student Name',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_name.place(x=300,y=135)

            en_name = CTkEntry(head_frame_islamic,textvariable=var_s_name,width=200,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_name.place(x=400,y=130)
            #===========================

            lbl_islamic_first = CTkLabel(head_frame_islamic,text='1st Month\nIslamic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_islamic_first.place(x=300,y=180)

            en_islamic_first = CTkEntry(head_frame_islamic,textvariable=var_islamic_f_m,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_islamic_first.place(x=400,y=180)
            #====================

            lbl_islamic_second = CTkLabel(head_frame_islamic,text='2nd Month\nIslamic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_islamic_second.place(x=460,y=180)

            en_islamic_second = CTkEntry(head_frame_islamic,textvariable=var_islamic_s_m,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_islamic_second.place(x=545,y=180)


            #====================
            lbl_islamic_chapter1 = CTkLabel(head_frame_islamic,text='Chap One\nIslamic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_islamic_chapter1.place(x=605,y=180)

            en_islamic_chapter1 = CTkEntry(head_frame_islamic,textvariable=var_islamic_ch1,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_islamic_chapter1.place(x=685,y=180)

            #====================================
            lbl_islamic_half_y = CTkLabel(head_frame_islamic,text='Half Year',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_islamic_half_y.place(x=745,y=180)

            en_islamic_half_y = CTkEntry(head_frame_islamic,textvariable=var_islamic_half_y,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_islamic_half_y.place(x=820,y=180)

            #===================================
            lbl_islamic_first1 = CTkLabel(head_frame_islamic,text='1st Month\nIslamic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_islamic_first1.place(x=875,y=180)

            en_islamic_first1 = CTkEntry(head_frame_islamic,textvariable=var_islamic_f_m1,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_islamic_first1.place(x=950,y=180)
            #====================================
            lbl_islamic_se2 = CTkLabel(head_frame_islamic,text='2nd Month\nIslamic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_islamic_se2.place(x=1010,y=180)

            en_islamic_se2 = CTkEntry(head_frame_islamic,textvariable=var_islamic_s_m2,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_islamic_se2.place(x=1100,y=180)

            #=================================
            lbl_islamic_ch2 = CTkLabel(head_frame_islamic,text='Chap Tow\nIslamic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_islamic_ch2.place(x=300,y=220)

            en_islamic_ch2 = CTkEntry(head_frame_islamic,textvariable=var_islamic_ch2,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_islamic_ch2.place(x=400,y=220)
            #==================================
            lbl_islamic_final_ch = CTkLabel(head_frame_islamic,text='Final Chap\nIslamic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_islamic_final_ch.place(x=460,y=220)

            en_islamic_final_ch = CTkEntry(head_frame_islamic,textvariable=var_islamic_ch3,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_islamic_final_ch.place(x=545,y=220)
            #===================================
            lbl_islamic_final_exam = CTkLabel(head_frame_islamic,text='Final Exam\nIslamic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_islamic_final_exam.place(x=605,y=220)

            en_islamic_final_exam = CTkEntry(head_frame_islamic,textvariable=var_islamic_f_exam,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_islamic_final_exam.place(x=685,y=220)
            #====================================
            lbl_islamic_final_y = CTkLabel(head_frame_islamic,text='Final Year\nIslamic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_islamic_final_y.place(x=745,y=220)

            en_islamic_final_y = CTkEntry(head_frame_islamic,textvariable=var_islamic_f_r,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_islamic_final_y.place(x=820,y=220)


            #=========================== buttons =============================
            add_btn = CTkButton(head_frame_islamic,text='ADD',width=120,height=40,
                                   fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                                   font=('arial',16,'bold'),border_color='#DA7297',
                                   hover_color='#DA7297',corner_radius=10,command=add_islamic_marks)
            add_btn.place(x=400,y=275)

            update_btn = CTkButton(head_frame_islamic,text='UPDARE',width=120,height=40,
                                   fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                                   font=('arial',16,'bold'),border_color='#DA7297',
                                   hover_color='#DA7297',corner_radius=10)
            update_btn.place(x=550,y=275)

            delete_btn = CTkButton(head_frame_islamic,text='DELETE',width=120,height=40,
                                   fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                                   font=('arial',16,'bold'),border_color='#DA7297',
                                   hover_color='#DA7297',corner_radius=10,command=delete_islamic_marks)
            delete_btn.place(x=700,y=275)

            clear_btn = CTkButton(head_frame_islamic,text='CLEAR',width=120,height=40,
                                   fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                                   font=('arial',16,'bold'),border_color='#DA7297',
                                   hover_color='#DA7297',corner_radius=10,command=clear_islamic_marks)
            clear_btn.place(x=850,y=275)

            #================================== student marks treeview ========================
            student_marks_tree_f = Frame(head_frame_islamic,bg='gray')
            student_marks_tree_f.place(x=2,y=340,width=1189,height=270)

            student_marks_tree = ttk.Style()
            student_marks_tree.theme_use('clam')

            student_marks_tree.configure('Treeview',bg='#D3D3D3',font=('arial',12),fg='black',
                                         rowheight=30,fieldbackground='white')
            student_marks_tree.configure('Treeview.Heading',background='#DA7297',foreground='white',font=('arial',12,'bold'),height=100)

            student_marks_scrolly = Scrollbar(student_marks_tree_f)
            student_marks_scrolly.pack(side=RIGHT,fill=Y)

            student_marks_scrollx = Scrollbar(student_marks_tree_f,orient=HORIZONTAL)
            student_marks_scrollx.pack(side=BOTTOM,fill=X)

            student_marks_tree_islamic = ttk.Treeview(student_marks_tree_f,yscrollcommand=student_marks_scrolly.selection_clear,xscrollcommand=student_marks_scrollx.set,selectmode='extended')
            student_marks_tree_islamic.place(x=0,y=0,width=1172,height=254)

            student_marks_scrolly.config(command=student_marks_tree_islamic.yview)
            student_marks_scrollx.config(command=student_marks_tree_islamic.xview)

            student_marks_tree_islamic.configure(columns=("i_ID","student_name","st_month","nd_month","chapter1",
                                                          "half_year","st_month1","nd_month2","chapter2","chapter3",
                                                          "final_exam","final_result"))
            
            student_marks_tree_islamic.heading("i_ID",text='ID')
            student_marks_tree_islamic.heading("student_name",text='Student Name')
            student_marks_tree_islamic.heading("st_month",text='1st Month')
            student_marks_tree_islamic.heading("nd_month",text='2nd month')
            student_marks_tree_islamic.heading("chapter1",text='chapter1')
            student_marks_tree_islamic.heading("half_year",text='half year')
            student_marks_tree_islamic.heading("st_month1",text='1st month')
            student_marks_tree_islamic.heading("nd_month2",text='2nd month')
            student_marks_tree_islamic.heading("chapter2",text='chapter2')
            student_marks_tree_islamic.heading("chapter3",text='chapter3')
            student_marks_tree_islamic.heading("final_exam",text='final exam')
            student_marks_tree_islamic.heading("final_result",text='final result')

            student_marks_tree_islamic["show"]="headings"

            student_marks_tree_islamic.column("i_ID",width=50,anchor=W)
            student_marks_tree_islamic.column("student_name",width=180,anchor=W)
            student_marks_tree_islamic.column("st_month",width=100,anchor=W)
            student_marks_tree_islamic.column("nd_month",width=100,anchor=W)
            student_marks_tree_islamic.column("chapter1",width=120,anchor=W)
            student_marks_tree_islamic.column("half_year",width=100,anchor=W)
            student_marks_tree_islamic.column("st_month1",width=100,anchor=W)
            student_marks_tree_islamic.column("nd_month2",width=100,anchor=W)
            student_marks_tree_islamic.column("chapter2",width=120,anchor=W)
            student_marks_tree_islamic.column("chapter3",width=100,anchor=W)
            student_marks_tree_islamic.column("final_exam",width=100,anchor=W)
            student_marks_tree_islamic.column("final_result",width=100,anchor=W)
            student_marks_tree_islamic.bind("<ButtonRelease-1>",get_data_islamic_marks)
            
            show_islamic_marks()

            student_marks_tree_islamic.tag_configure('oddrow',background='lightgray')
            student_marks_tree_islamic.tag_configure('evenrow',background='#F6F5F5')
            
            
        #=================================================================
        #==================== arabic marks window ========================
         
        def window_arabic():
            win_arabic = Toplevel()
            win_arabic.geometry('1200x690+100+5')
            win_arabic.title('Add Arabic Students Marks')
            win_arabic.resizable(False,False)
            win_arabic.config(bg='#F6F5F5')

            root.withdraw()

            def date_a():
                date_1 = strftime('%I:%M:%S %p \t %A \t %b/%d/%Y')
                date_lbl.config(text=date_1)
                date_lbl.after(1000,date)

            def back():
                win_arabic.destroy()
                root.deiconify() 

            def record_ida():
                con = sqlite3.connect('school.db')
                cur = con.cursor()  
                cur.execute("""
                WITH RECURSIVE cte AS(
                            SELECT ROW_NUMBER() OVER (ORDER BY a_ID) AS new_id, a_ID
                            FROM arabic_marks
                            )
                            UPDATE arabic_marks
                            SET a_ID = (SELECT new_id FROM cte WHERE cte.a_ID = arabic_marks.a_ID)
                """)

            def add_arabic_marks():
                con = sqlite3.connect('school.db')
                cur = con.cursor() 



                cur.execute("INSERT INTO arabic_marks(student_name,st_month,nd_month,chapter1,half_year,st_month1,nd_month2,chapter2,chapter3,final_exam,final_result) values(?,?,?,?,?,?,?,?,?,?,?)",(
                            var_s_namea.get(),
                            var_arabic_f_m.get(),
                            var_arabic_s_m.get(),
                            var_arabic_ch1.get(),
                            var_arabic_half_y.get(),
                            var_arabic_f_m1.get(),
                            var_arabic_s_m2.get(),
                            var_arabic_ch2.get(),
                            var_arabic_ch3.get(),
                            var_arabic_f_exam.get(),
                            var_arabic_f_r.get(),
                ))    
                messagebox.showinfo("success","add successfully")
                con.commit()
                record_ida()
                show_arabic_marks()
                clear_arabic_marks()

                

            def show_arabic_marks():
                con = sqlite3.connect('school.db')
                cur = con.cursor()
                try:
                    cur.execute("select * from arabic_marks")
                    rows = cur.fetchall()    
                    student_marks_tree_arabic.delete(*student_marks_tree_arabic.get_children())
                    global count
                    count = 0
                    for row in rows:
                        if count % 2 ==0:
                            student_marks_tree_arabic.insert(parent='',index='end',iid=count,text='',values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]),tags=('evenrow'))
                        else:
                            student_marks_tree_arabic.insert(parent='',index='end',iid=count,text='',values=(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]),tags=('oddrow'))
                            
                        count +=1
                except Exception as es:
                    messagebox.showerror("error",f"error: {str(es)}")  

            
            def clear_arabic_marks():
                var_s_namea.set("")
                var_arabic_f_m.set("0")
                var_arabic_s_m.set("0")
                var_arabic_ch1.set("0")
                var_arabic_half_y.set("0")
                var_arabic_f_m1.set("0")
                var_arabic_s_m2.set("0")
                var_arabic_ch2.set("0")
                var_arabic_ch3.set("0")
                var_arabic_f_exam.set("0")
                var_arabic_f_r.set("0")

                var_serarch_ena.set("")
                cmb_searcha.set("Select")

                show_arabic_marks()
            

            def get_data_arabic_marks(ev):
                n = student_marks_tree_arabic.focus()
                f = (student_marks_tree_arabic.item(n))
                row = f['values']

                var_ida.set(row[0])
                var_s_namea.set(row[1])
                var_arabic_f_m.set(row[2])
                var_arabic_s_m.set(row[3])
                var_arabic_ch1.set(row[4])
                var_arabic_half_y.set(row[5])
                var_arabic_f_m1.set(row[6])
                var_arabic_s_m2.set(row[7])
                var_arabic_ch2.set(row[8])
                var_arabic_ch3.set(row[9])
                var_arabic_f_exam.set(row[10])
                var_arabic_f_r.set(row[11])

            def update_arabic_marks():
                con = sqlite3.connect('school.db')
                cur = con.cursor() 

                f_m_value = var_arabic_f_m.get()
                s_m_value = var_arabic_s_m.get()

                f_m_value = float(f_m_value)
                s_m_value = float(s_m_value)
                
                avreage_ch1 = (f_m_value + s_m_value) / 2

                var_arabic_ch1.set(avreage_ch1)

                f_m_value1 = var_arabic_f_m1.get()
                s_m_value2 = var_arabic_s_m2.get()

                f_m_value1 = float(f_m_value1)
                s_m_value2 = float(s_m_value2)

                avreage_ch2 = (f_m_value1 + s_m_value2) / 2

                var_arabic_ch2.set(avreage_ch2)

                ch1 = float(var_arabic_ch1.get())
                half_y = float(var_arabic_half_y.get())
                ch2 = float(var_arabic_ch2.get())

                avreage_ch3 = (ch1 + half_y + ch2 ) / 3

                var_arabic_ch3.set(avreage_ch3)

                ch3 = float(var_arabic_ch3.get())
                final_exam = float(var_arabic_f_exam.get())

                avreage_f = (ch3 + final_exam) / 2

                var_arabic_f_r.set(avreage_f)
                
                cur.execute("update arabic_marks SET student_name=?,st_month=?,nd_month=?,chapter1=?,half_year=?,st_month1=?,nd_month2=?,chapter2=?,chapter3=?,final_exam=?,final_result=? WHERE a_ID=?",(
                            var_s_namea.get(),
                            var_arabic_f_m.get(),
                            var_arabic_s_m.get(),
                            var_arabic_ch1.get(),
                            var_arabic_half_y.get(),
                            var_arabic_f_m1.get(),
                            var_arabic_s_m2.get(),
                            var_arabic_ch2.get(),
                            var_arabic_ch3.get(),
                            var_arabic_f_exam.get(),
                            var_arabic_f_r.get(),
                            var_ida.get(),
                ))    
                messagebox.showinfo("success","update successfully")
                con.commit()
                record_ida()
                show_arabic_marks()
                clear_arabic_marks()  

            def delete_arabic_marks():
                con = sqlite3.connect('school.db')
                cur = con.cursor()
                op = messagebox.askyesno("confiem","do you want to delete?")
                op==True
                cur.execute("delete from arabic_marks where a_ID=?",(var_ida.get(),))
                con.commit()
                record_ida()
                messagebox.showinfo("success","delete successfully")
                show_arabic_marks() 
                clear_arabic_marks()     

            def search_arabic_marks():
                con = sqlite3.connect('school.db')
                cur = con.cursor()
                try:
                    if cmb_searcha.get()=="Select":
                        messagebox.showerror("errror","select to search")
                    elif var_serarch_ena.get()=="":
                        messagebox.showerror("error","inprut to search")
                    else:
                        cur.execute("select * from arabic_marks where "+cmb_searcha.get()+" LIKE '%"+var_serarch_ena.get()+"%'")
                        rows = cur.fetchall() 
                        if len(rows)!=0:
                            student_marks_tree_arabic.delete(*student_marks_tree_arabic.get_children())
                            for row in rows:
                                student_marks_tree_arabic.insert('',END,values=row)     
                        else:
                            messagebox.showerror("error","not found")
                except Exception as ex:
                    messagebox.showerror("error",f"error{str(ex)}")                                           
            #============================== head frame ==========================
            up_frame = CTkFrame(win_arabic,width=1199,height=70,bg_color='#F6F5F5',fg_color='#F6F5F5',border_color='#DA7297',border_width=2)
            up_frame.place(x=1,y=1)

            text_lbl = Label(win_arabic, text='Islamic Students Marks Page',font=('corier',18,'bold'),bg='#F6F5F5',fg='#DA7297')
            text_lbl.place(x=150,y=5,width=350,height=60)

            date_lbl = Label(win_arabic,font=('corier',18,'bold'),bg='#F6F5F5',fg='#DA7297')
            date_lbl.place(x=590,y=5,width=570,height=60)
            date_a()


            back_btn = CTkButton(win_arabic,text='←', width=100,height=68,
                             fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                             font=('arial',30,'bold'),hover_color='#DA7297',border_color='#DA7297',
                             corner_radius=0,command=back)
            back_btn.place(x=2,y=2)

            #============================= up frame ==========================
            head_frame_arabic = CTkFrame(win_arabic,width=1197,height=615,bg_color='white',fg_color='#F6F5F5',border_color='#DA7297',border_width=2)
            head_frame_arabic.place(x=1,y=72)

            #============================= serach area =======================
            var_serarch_ena = StringVar()

            serach_frame = CTkFrame(head_frame_arabic,width=820,height=60,bg_color='#F6F5F5',fg_color='white',border_width=2,border_color='#DA7297')
            serach_frame.place(x=300,y=30)

            text_lbl = Label(serach_frame,text='Search Student',font=('arial',14,'bold'),bg='white',fg='#DA7297')
            text_lbl.place(x=5,y=5,width=180,height=50)

            cmb_searcha = CTkComboBox(serach_frame,values=("Select","student_name"),
                                     button_color='#DA7297',button_hover_color='#DA7297',justify=CENTER,
                                     font=('arial',15),width=180,height=35,fg_color='white',border_width=1,border_color='#DA7297',
                                     dropdown_fg_color='white',dropdown_text_color='#DA7297')
            cmb_searcha.place(x=180,y=13)

            search_en = CTkEntry(serach_frame,textvariable=var_serarch_ena,width=200,height=35,fg_color='white',font=('arial',14),
                                 border_width=1,border_color='#DA7297',bg_color='white',justify='center')
            search_en.place(x=380,y=13)

            search_btn = CTkButton(serach_frame,text='SEARCH',width=200,height=40,
                                   fg_color='#DA7297',text_color='white',bg_color='white',
                                   font=('arial',16,'bold'),border_color='#DA7297',
                                   hover_color='#DA7297',corner_radius=10,command=search_arabic_marks)
            search_btn.place(x=600,y=10)

            #========================== logo image ========================
            img = CTkImage(Image.open('images/marks.png'),size=(300,300))
            img_lbl = CTkLabel(head_frame_arabic,text='',image=img,fg_color='#F6F5F5')
            img_lbl.place(x=1,y=20)

            #============= varibales =====================
            var_ida = StringVar()
            var_s_namea = StringVar()
            var_arabic_f_m = IntVar()
            var_arabic_s_m = IntVar()
            var_arabic_ch1 = IntVar()
            var_arabic_half_y = IntVar()
            var_arabic_f_m = IntVar()
            var_arabic_f_m1 = IntVar()
            var_arabic_s_m2 = IntVar()
            var_arabic_ch2 = IntVar()
            var_arabic_ch3 = IntVar()
            var_arabic_f_exam = IntVar()
            var_arabic_f_r = IntVar()

            #========================== labels + entrys ====================
            lbl_name = CTkLabel(head_frame_arabic,text='Student Name',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_name.place(x=300,y=135)

            en_name = CTkEntry(head_frame_arabic,textvariable=var_s_namea,width=200,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_name.place(x=400,y=130)
            #===========================

            lbl_arabic_first = CTkLabel(head_frame_arabic,text='1st Month\narabic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_arabic_first.place(x=300,y=180)

            en_arabic_first = CTkEntry(head_frame_arabic,textvariable=var_arabic_f_m,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_arabic_first.place(x=400,y=180)
            #====================

            lbl_arabic_second = CTkLabel(head_frame_arabic,text='2nd Month\narabic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_arabic_second.place(x=460,y=180)

            en_arabic_second = CTkEntry(head_frame_arabic,textvariable=var_arabic_s_m,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_arabic_second.place(x=545,y=180)


            #====================
            lbl_arabic_chapter1 = CTkLabel(head_frame_arabic,text='Chap One\narabic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_arabic_chapter1.place(x=605,y=180)

            en_arabic_chapter1 = CTkEntry(head_frame_arabic,textvariable=var_arabic_ch1,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_arabic_chapter1.place(x=685,y=180)

            #====================================
            lbl_arabic_half_y = CTkLabel(head_frame_arabic,text='Half Year',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_arabic_half_y.place(x=745,y=180)

            en_arabic_half_y = CTkEntry(head_frame_arabic,textvariable=var_arabic_half_y,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_arabic_half_y.place(x=820,y=180)

            #===================================
            lbl_arabic_first1 = CTkLabel(head_frame_arabic,text='1st Month\narabic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_arabic_first1.place(x=875,y=180)

            en_arabic_first1 = CTkEntry(head_frame_arabic,textvariable=var_arabic_f_m1,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_arabic_first1.place(x=950,y=180)
            #====================================
            lbl_arabic_se2 = CTkLabel(head_frame_arabic,text='2nd Month\narabic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_arabic_se2.place(x=1010,y=180)

            en_arabic_se2 = CTkEntry(head_frame_arabic,textvariable=var_arabic_s_m2,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_arabic_se2.place(x=1100,y=180)

            #=================================
            lbl_arabic_ch2 = CTkLabel(head_frame_arabic,text='Chap Tow\narabic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_arabic_ch2.place(x=300,y=220)

            en_arabic_ch2 = CTkEntry(head_frame_arabic,textvariable=var_arabic_ch2,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_arabic_ch2.place(x=400,y=220)
            #==================================
            lbl_arabic_final_ch = CTkLabel(head_frame_arabic,text='Final Chap\narabic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_arabic_final_ch.place(x=460,y=220)

            en_arabic_final_ch = CTkEntry(head_frame_arabic,textvariable=var_arabic_ch3,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_arabic_final_ch.place(x=545,y=220)
            #===================================
            lbl_arabic_final_exam = CTkLabel(head_frame_arabic,text='Final Exam\narabic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_arabic_final_exam.place(x=605,y=220)

            en_arabic_final_exam = CTkEntry(head_frame_arabic,textvariable=var_arabic_f_exam,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_arabic_final_exam.place(x=685,y=220)
            #====================================
            lbl_arabic_final_y = CTkLabel(head_frame_arabic,text='Final Year\narabic',width=50,height=25,
                                text_color='gray',font=('arial',14,'bold'),fg_color='#F6F5F5',bg_color='#F6F5F5')
            lbl_arabic_final_y.place(x=745,y=220)

            en_arabic_final_y = CTkEntry(head_frame_arabic,textvariable=var_arabic_f_r,width=50,height=35,justify=CENTER,fg_color='white',
                               font=('arial',14),border_width=1,border_color='#DA7297',bg_color='#F6F5F5')
            en_arabic_final_y.place(x=820,y=220)


            #=========================== buttons =============================
            add_btn = CTkButton(head_frame_arabic,text='ADD',width=120,height=40,
                                   fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                                   font=('arial',16,'bold'),border_color='#DA7297',
                                   hover_color='#DA7297',corner_radius=10,command=add_arabic_marks)
            add_btn.place(x=400,y=275)

            update_btn = CTkButton(head_frame_arabic,text='UPDARE',width=120,height=40,
                                   fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                                   font=('arial',16,'bold'),border_color='#DA7297',
                                   hover_color='#DA7297',corner_radius=10,command=update_arabic_marks)
            update_btn.place(x=550,y=275)

            delete_btn = CTkButton(head_frame_arabic,text='DELETE',width=120,height=40,
                                   fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                                   font=('arial',16,'bold'),border_color='#DA7297',
                                   hover_color='#DA7297',corner_radius=10,command=delete_arabic_marks)
            delete_btn.place(x=700,y=275)

            clear_btn = CTkButton(head_frame_arabic,text='CLEAR',width=120,height=40,
                                   fg_color='#DA7297',text_color='white',bg_color='#F6F5F5',
                                   font=('arial',16,'bold'),border_color='#DA7297',
                                   hover_color='#DA7297',corner_radius=10,command=clear_arabic_marks)
            clear_btn.place(x=850,y=275)

            #================================== student marks treeview ========================
            student_marks_tree_f = Frame(head_frame_arabic,bg='gray')
            student_marks_tree_f.place(x=2,y=340,width=1189,height=270)

            student_marks_tree = ttk.Style()
            student_marks_tree.theme_use('clam')

            student_marks_tree.configure('Treeview',bg='#D3D3D3',font=('arial',12),fg='black',
                                         rowheight=30,fieldbackground='white')
            student_marks_tree.configure('Treeview.Heading',background='#DA7297',foreground='white',font=('arial',12,'bold'),height=100)

            student_marks_scrolly = Scrollbar(student_marks_tree_f)
            student_marks_scrolly.pack(side=RIGHT,fill=Y)

            student_marks_scrollx = Scrollbar(student_marks_tree_f,orient=HORIZONTAL)
            student_marks_scrollx.pack(side=BOTTOM,fill=X)

            student_marks_tree_arabic = ttk.Treeview(student_marks_tree_f,yscrollcommand=student_marks_scrolly.selection_clear,xscrollcommand=student_marks_scrollx.set,selectmode='extended')
            student_marks_tree_arabic.place(x=0,y=0,width=1172,height=254)

            student_marks_scrolly.config(command=student_marks_tree_arabic.yview)
            student_marks_scrollx.config(command=student_marks_tree_arabic.xview)

            student_marks_tree_arabic.configure(columns=("i_ID","student_name","st_month","nd_month","chapter1",
                                                          "half_year","st_month1","nd_month2","chapter2","chapter3",
                                                          "final_exam","final_result"))
            
            student_marks_tree_arabic.heading("i_ID",text='ID')
            student_marks_tree_arabic.heading("student_name",text='Student Name')
            student_marks_tree_arabic.heading("st_month",text='1st Month')
            student_marks_tree_arabic.heading("nd_month",text='2nd month')
            student_marks_tree_arabic.heading("chapter1",text='chapter1')
            student_marks_tree_arabic.heading("half_year",text='half year')
            student_marks_tree_arabic.heading("st_month1",text='1st month')
            student_marks_tree_arabic.heading("nd_month2",text='2nd month')
            student_marks_tree_arabic.heading("chapter2",text='chapter2')
            student_marks_tree_arabic.heading("chapter3",text='chapter3')
            student_marks_tree_arabic.heading("final_exam",text='final exam')
            student_marks_tree_arabic.heading("final_result",text='final result')

            student_marks_tree_arabic["show"]="headings"

            student_marks_tree_arabic.column("i_ID",width=50,anchor=W)
            student_marks_tree_arabic.column("student_name",width=180,anchor=W)
            student_marks_tree_arabic.column("st_month",width=100,anchor=W)
            student_marks_tree_arabic.column("nd_month",width=100,anchor=W)
            student_marks_tree_arabic.column("chapter1",width=120,anchor=W)
            student_marks_tree_arabic.column("half_year",width=100,anchor=W)
            student_marks_tree_arabic.column("st_month1",width=100,anchor=W)
            student_marks_tree_arabic.column("nd_month2",width=100,anchor=W)
            student_marks_tree_arabic.column("chapter2",width=120,anchor=W)
            student_marks_tree_arabic.column("chapter3",width=100,anchor=W)
            student_marks_tree_arabic.column("final_exam",width=100,anchor=W)
            student_marks_tree_arabic.column("final_result",width=100,anchor=W)
            student_marks_tree_arabic.bind("<ButtonRelease-1>",get_data_arabic_marks)
            
            show_arabic_marks()

            student_marks_tree_arabic.tag_configure('oddrow',background='lightgray')
            student_marks_tree_arabic.tag_configure('evenrow',background='#F6F5F5')
            
            


        #============================= up frame ==========================
        head_frame = CTkFrame(root,width=1197,height=615,bg_color='white',fg_color='#F6F5F5',border_color='#DA7297',border_width=2)
        head_frame.place(x=1,y=72)

        #============================= buttons frame ======================
        buttons_frame = Frame(head_frame,bg='#DA7297')
        buttons_frame.place(x=3,y=3,width=1188,height=60)

        islamic_page_btn = CTkButton(buttons_frame,text='Islamic\nMarks Page',width=120,height=20,
                                     fg_color='#DA7297',text_color='white',border_color='#DA7297',
                                     border_width=2,font=('arial',16,'bold'),hover_color='#DA7297',
                                     bg_color='#DA7297',command=window_islamic)
        islamic_page_btn.place(x=5,y=1)

        arabic_page_btn = CTkButton(buttons_frame,text='Arabic\nMarks Page',width=120,height=20,
                                     fg_color='#DA7297',text_color='white',border_color='#DA7297',
                                     border_width=2,font=('arial',16,'bold'),hover_color='#DA7297',
                                     bg_color='#DA7297',command=window_arabic)
        arabic_page_btn.place(x=150,y=1)

        english_page_btn = CTkButton(buttons_frame,text='English\nMarks Page',width=120,height=20,
                                     fg_color='#DA7297',text_color='white',border_color='#DA7297',
                                     border_width=2,font=('arial',16,'bold'),hover_color='#DA7297',
                                     bg_color='#DA7297')
        english_page_btn.place(x=300,y=1)

        socialstudies_page_btn = CTkButton(buttons_frame,text='Social Studies\nMarks Page',width=120,height=20,
                                     fg_color='#DA7297',text_color='white',border_color='#DA7297',
                                     border_width=2,font=('arial',16,'bold'),hover_color='#DA7297',
                                     bg_color='#DA7297')
        socialstudies_page_btn.place(x=450,y=1)

        mathematic_page_btn = CTkButton(buttons_frame,text='Mathematic\nMarks Page',width=120,height=20,
                                     fg_color='#DA7297',text_color='white',border_color='#DA7297',
                                     border_width=2,font=('arial',16,'bold'),hover_color='#DA7297',
                                     bg_color='#DA7297')
        mathematic_page_btn.place(x=600,y=1)

        chemistry_page_btn = CTkButton(buttons_frame,text='Chemistry\nMarks Page',width=120,height=20,
                                     fg_color='#DA7297',text_color='white',border_color='#DA7297',
                                     border_width=2,font=('arial',16,'bold'),hover_color='#DA7297',
                                     bg_color='#DA7297')
        chemistry_page_btn.place(x=750,y=1)

        mathematic_page_btn = CTkButton(buttons_frame,text='Mathematic\nMarks Page',width=120,height=20,
                                     fg_color='#DA7297',text_color='white',border_color='#DA7297',
                                     border_width=2,font=('arial',16,'bold'),hover_color='#DA7297',
                                     bg_color='#DA7297')
        mathematic_page_btn.place(x=600,y=1)

        physic_page_btn = CTkButton(buttons_frame,text='Physic\nMarks Page',width=120,height=20,
                                     fg_color='#DA7297',text_color='white',border_color='#DA7297',
                                     border_width=2,font=('arial',16,'bold'),hover_color='#DA7297',
                                     bg_color='#DA7297')
        physic_page_btn.place(x=900,y=1)

        biology_page_btn = CTkButton(buttons_frame,text='Piology\nMarks Page',width=120,height=20,
                                     fg_color='#DA7297',text_color='white',border_color='#DA7297',
                                     border_width=2,font=('arial',16,'bold'),hover_color='#DA7297',
                                     bg_color='#DA7297')
        biology_page_btn.place(x=1050,y=1)
        '''
        #================================= comobox student names =========================
        lbl_select_student_name_i = Label(head_frame,text='Islamic Student Name:',font=('arial',14),
                                          bg='#F6F5F5',fg='#DA7297')
        lbl_select_student_name_i.place(x=30,y=70)

        student_name_islamic = get_student_names_islamic()
        cmb_student_name_islamic = CTkComboBox(head_frame,values=student_name_islamic,button_color='#DA7297',button_hover_color='#DA7297',
                                               justify=CENTER,font=('arial',15),width=240,height=35,
                                               fg_color='white',border_width=1,border_color='#DA7297',
                                               dropdown_fg_color='white',dropdown_text_color='#DA7297')
        cmb_student_name_islamic.place(x=30,y=100)

        lbl_select_student_name_a = Label(head_frame,text='Arabic Student Name:',font=('arial',14),
                                          bg='#F6F5F5',fg='#DA7297')
        lbl_select_student_name_a.place(x=30,y=140)

        student_name_arabic = get_student_names_arabic()
        cmb_student_name_arabic = CTkComboBox(head_frame,values=student_name_arabic,button_color='#DA7297',button_hover_color='#DA7297',
                                               justify=CENTER,font=('arial',15),width=240,height=35,
                                               fg_color='white',border_width=1,border_color='#DA7297',
                                               dropdown_fg_color='white',dropdown_text_color='#DA7297')
        cmb_student_name_arabic.place(x=30,y=170)

        #=============================== buttons marks ============================
        islamic_marks_btn = Button(head_frame,text='Add Islamic Marks', font=('arial',12,'bold'),
                                   bg='#DA7297',fg='white',cursor='hand2',command=add_islamic_marks)
        islamic_marks_btn.place(x=330,y=100,width=200)

        arabic_marks_btn = Button(head_frame,text='Add Arabic Marks', font=('arial',12,'bold'),
                                   bg='#DA7297',fg='white',cursor='hand2',command=add_arabic_marks)
        arabic_marks_btn.place(x=330,y=170,width=200)
        ''''''
        #=============================== text area ==================================
        text_reslut = Text(head_frame, width=60,height=25,font=('arial',12),bg='#D0DDD0',fg='black')
        text_reslut.place(x=600,y=100)

        #================ button text ===============
        def clear_text():
            text_reslut.delete(1.0, 'end')

        def print():
            text_result1 = text_reslut.get(1.0,'end')
            print_text(text_result1)

        def print_text(text_result1):
            printer_name = win32print.GetDefaultPrinter()
            p = win32ui.CreateDC()
            p.CreatePrinterDC(printer_name)

            p.StartDoc("result")
            p.StartPage()

            font= win32ui.CreateFont({"name": "Arial","height":12,"weight":400})

            p.SelectObject(font)

            y = 100
            for line in text_result1.splitlines():
                p.TextOut(100,y, line)
                y += 20

            p.EndPage()
            p.EndDoc()
            p.DeleteDC()
            messagebox.showinfo("success","text result print successfully")    

        clear_btn_text = Button(head_frame,text='clear',command=clear_text,font=('arial',12),fg='white',bg='#DA7297')
        clear_btn_text.place(x=600,y=570,width=100)

        print_btn_text = Button(head_frame,text='print',command=print,font=('arial',12),fg='white',bg='#DA7297')
        print_btn_text.place(x=720,y=570,width=100)
        '''





if __name__=="__main__":
    root = Tk()
    First_Student_Marks_Class(root)
    root.mainloop()                

        