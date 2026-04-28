"""
curriculumpage.py — صفحة المنهج الدراسي
==========================================
- رفع ملف Word (.docx) لكل مادة
- عرض محتوى المنهج بشكل منظم
- حفظ المحتوى في DB
- دعم 8 مواد
"""

from customtkinter import *
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from time import strftime
import sqlite3
import os
import subprocess
import tempfile

import dashboard
from auth import session
from create_db import log_action

# ============================================================
#  المواد
# ============================================================
SUBJECTS = [
    ("civic_education", "Civic Education",  "#8B0000"),
    ("arabic",          "Arabic",           "#DA7297"),
    ("english",         "English",          "#c0506e"),
    ("social_studies",  "Social Studies",   "#8B0000"),
    ("mathematics",     "Mathematics",      "#DA7297"),
    ("chemistry",       "Chemistry",        "#c0506e"),
    ("physics",         "Physics",          "#8B0000"),
    ("biology",         "Biology",          "#DA7297"),
]


# ============================================================
#  DB SETUP
# ============================================================
def _ensure_curriculum_table(con):
    try:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS curriculum(
                c_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_key TEXT NOT NULL UNIQUE,
                subject_name TEXT NOT NULL,
                content     TEXT DEFAULT '',
                file_name   TEXT DEFAULT '',
                updated_by  TEXT DEFAULT '',
                updated_at  TEXT DEFAULT ''
            )
        """)
        # إدخال صفوف للمواد لو مش موجودة
        for key, name, _ in SUBJECTS:
            cur.execute("""
                INSERT OR IGNORE INTO curriculum(subject_key, subject_name)
                VALUES(?,?)
            """, (key, name))
        con.commit()
    except Exception:
        pass


def _get_db_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, 'school.db')


DB_PATH = _get_db_path()


def _extract_docx_text(path):
    """استخراج النص من ملف Word بـ python-docx أو pandoc"""
    # محاولة python-docx
    try:
        import docx as docx_lib
        doc = docx_lib.Document(path)
        lines = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if not text:
                continue
            style = para.style.name.lower()
            if 'heading 1' in style or 'عنوان 1' in style:
                lines.append(f"H1:{text}")
            elif 'heading 2' in style or 'عنوان 2' in style:
                lines.append(f"H2:{text}")
            elif 'heading 3' in style or 'عنوان 3' in style:
                lines.append(f"H3:{text}")
            elif para.runs and any(r.bold for r in para.runs if r.text.strip()):
                lines.append(f"BOLD:{text}")
            elif text.startswith(('-', '•', '*', '·')):
                lines.append(f"BULLET:{text.lstrip('-•* ·').strip()}")
            else:
                lines.append(f"TEXT:{text}")
        return "\n".join(lines)
    except ImportError:
        pass

    # محاولة pandoc
    try:
        result = subprocess.run(
            ['pandoc', path, '-t', 'plain', '--wrap=none'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            lines = []
            for line in result.stdout.splitlines():
                line = line.strip()
                if line:
                    lines.append(f"TEXT:{line}")
            return "\n".join(lines)
    except Exception:
        pass

    # قراءة نص بسيط من ZIP
    try:
        import zipfile, re
        with zipfile.ZipFile(path, 'r') as z:
            with z.open('word/document.xml') as f:
                xml = f.read().decode('utf-8', errors='ignore')
        text = re.sub(r'<[^>]+>', ' ', xml)
        text = re.sub(r'\s+', ' ', text).strip()
        lines = [f"TEXT:{t.strip()}" for t in text.split('.') if t.strip()]
        return "\n".join(lines[:200])
    except Exception as ex:
        raise Exception(f"تعذّر قراءة الملف: {ex}")


# ============================================================
#  MAIN CLASS
# ============================================================
class CurriculumClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x690+80+20')
        self.root.title('Curriculum')
        self.root.config(bg='white')
        self.root.resizable(False, False)

        # migration
        con = sqlite3.connect(DB_PATH)
        _ensure_curriculum_table(con)
        con.close()

        self._active_subject = SUBJECTS[0][0]

        # ==================== HEAD ====================
        up = CTkFrame(root, width=1199, height=70, bg_color='#F6F5F5',
                      fg_color='#F6F5F5', border_color='#DA7297', border_width=2)
        up.place(x=1, y=1)

        Label(up, text='Curriculum', font=('courier', 18, 'bold'),
              bg='#F6F5F5', fg='#DA7297').place(x=150, y=5, width=220, height=60)

        self._date_lbl = Label(up, font=('courier', 12, 'bold'),
                               bg='#F6F5F5', fg='#DA7297')
        self._date_lbl.place(x=530, y=15, width=630, height=40)
        self._tick()

        def back():
            win = Toplevel()
            dashboard.DashboardClass(win)
            root.withdraw()
            win.deiconify()

        CTkButton(up, text='←', width=100, height=68,
                  fg_color='#DA7297', text_color='white', bg_color='#F6F5F5',
                  font=('arial', 30, 'bold'), hover_color='#DA7297',
                  corner_radius=0, command=back).place(x=2, y=2)

        # ==================== SUBJECT TABS ====================
        tab_f = CTkFrame(root, width=1199, height=50,
                         fg_color='#DA7297', bg_color='white')
        tab_f.place(x=1, y=72)

        self._tab_btns = {}
        for i, (key, name, color) in enumerate(SUBJECTS):
            short = name.replace(" ", "\n") if len(name) > 9 else name
            btn = CTkButton(
                tab_f, text=short, width=148, height=48,
                fg_color='#DA7297', text_color='white', bg_color='#DA7297',
                font=('arial', 11, 'bold'), hover_color='#8B0000',
                corner_radius=0,
                command=lambda k=key, n=name: self._switch(k, n))
            btn.place(x=i * 150, y=1)
            self._tab_btns[key] = btn

        # ==================== CONTENT AREA ====================
        self._content = CTkFrame(root, width=1197, height=567,
                                 fg_color='#F6F5F5', bg_color='white',
                                 border_color='#DA7297', border_width=2)
        self._content.place(x=1, y=122)

        # افتح أول مادة
        self._switch(*SUBJECTS[0][:2])

    def _tick(self):
        self._date_lbl.config(text=strftime('%I:%M:%S %p  -  %A  -  %d/%m/%Y'))
        self.root.after(1000, self._tick)

    def _switch(self, key, name):
        for k, btn in self._tab_btns.items():
            btn.configure(fg_color='#8B0000' if k == key else '#DA7297')
        for w in self._content.winfo_children():
            w.destroy()
        self._active_subject = key
        color = next((c for k, n, c in SUBJECTS if k == key), '#DA7297')
        _CurriculumPanel(self._content, key, name, color)


# ============================================================
#  CURRICULUM PANEL
# ============================================================
class _CurriculumPanel:
    def __init__(self, parent, subject_key, subject_name, color):
        self.parent       = parent
        self.subject_key  = subject_key
        self.subject_name = subject_name
        self.color        = color

        self._build()
        self._load()

    def _con(self):
        con = sqlite3.connect(DB_PATH)
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def _build(self):
        p = self.parent

        # ---- TOP BAR ----
        top = CTkFrame(p, width=1190, height=55,
                       fg_color='white', bg_color='#F6F5F5',
                       border_color='#DA7297', border_width=1)
        top.place(x=3, y=5)

        Label(top, text=f'📚  {self.subject_name} Curriculum',
              font=('arial', 14, 'bold'),
              bg='white', fg=self.color).place(x=15, y=13)

        self.file_lbl = Label(top, text='لم يتم رفع ملف بعد',
                              font=('arial', 10), bg='white', fg='gray')
        self.file_lbl.place(x=380, y=18)

        # زرار رفع Word — للـ admin والـ superadmin فقط
        if session.can("add_marks"):
            CTkButton(top, text='📂  رفع ملف Word',
                      width=170, height=36,
                      fg_color='#DA7297', text_color='white',
                      font=('arial', 12, 'bold'), corner_radius=8,
                      command=self._upload).place(x=870, y=9)

            CTkButton(top, text='🗑  مسح المنهج',
                      width=130, height=36,
                      fg_color='#888', text_color='white',
                      font=('arial', 12, 'bold'), corner_radius=8,
                      command=self._clear_content).place(x=1050, y=9)
        else:
            Label(top, text="🔒 عرض فقط",
                  font=('arial', 10), bg='white', fg='#aaa').place(x=1050, y=18)

        # ---- CONTENT DISPLAY ----
        content_f = Frame(p, bg='white')
        content_f.place(x=3, y=68, width=1190, height=490)

        # Scrollbar
        scy = Scrollbar(content_f)
        scy.pack(side=RIGHT, fill=Y)

        self.text_widget = Text(
            content_f,
            yscrollcommand=scy.set,
            font=('arial', 12),
            bg='white', fg='#1a1a1a',
            wrap=WORD,
            padx=20, pady=15,
            relief='flat',
            state='disabled',
            cursor='arrow',
            spacing1=4, spacing3=4
        )
        self.text_widget.pack(fill=BOTH, expand=1)
        scy.config(command=self.text_widget.yview)

        # ---- تعريف الأنماط ----
        self.text_widget.tag_configure('h1',
            font=('arial', 18, 'bold'), foreground=self.color,
            spacing1=15, spacing3=8)
        self.text_widget.tag_configure('h2',
            font=('arial', 15, 'bold'), foreground='#333',
            spacing1=12, spacing3=5)
        self.text_widget.tag_configure('h3',
            font=('arial', 13, 'bold'), foreground='#555',
            spacing1=8, spacing3=4)
        self.text_widget.tag_configure('bold',
            font=('arial', 12, 'bold'), foreground='#222')
        self.text_widget.tag_configure('bullet',
            font=('arial', 12), foreground='#333',
            lmargin1=30, lmargin2=45)
        self.text_widget.tag_configure('text',
            font=('arial', 12), foreground='#444')
        self.text_widget.tag_configure('divider',
            font=('arial', 6), foreground='#DA7297')
        self.text_widget.tag_configure('empty',
            font=('arial', 20), foreground='#ccc',
            justify='center')

    def _load(self):
        """تحميل المحتوى من DB"""
        try:
            con = self._con(); cur = con.cursor()
            cur.execute(
                "SELECT content, file_name, updated_by, updated_at FROM curriculum WHERE subject_key=?",
                (self.subject_key,))
            row = cur.fetchone()
            con.close()

            if row and row[0]:
                content, fname, updated_by, updated_at = row
                self.file_lbl.config(
                    text=f'📄  {fname}   |   آخر تحديث: {updated_at}   بواسطة: {updated_by}',
                    fg='#2e7d32')
                self._render(content)
            else:
                self._show_empty()
        except Exception as ex:
            self._show_empty()

    def _show_empty(self):
        """عرض رسالة لما مفيش محتوى"""
        self.text_widget.configure(state='normal')
        self.text_widget.delete('1.0', END)
        self.text_widget.insert(END,
            "\n\n\n\n        📂  لم يتم رفع منهج لهذه المادة بعد\n\n"
            "        اضغط 'رفع ملف Word' لإضافة المنهج", 'empty')
        self.text_widget.configure(state='disabled')

    def _render(self, content):
        """عرض المحتوى المحفوظ بتنسيق"""
        self.text_widget.configure(state='normal')
        self.text_widget.delete('1.0', END)

        for line in content.splitlines():
            if not line.strip():
                self.text_widget.insert(END, '\n')
                continue

            if line.startswith('H1:'):
                self.text_widget.insert(END, line[3:] + '\n', 'h1')
                self.text_widget.insert(END, '─' * 60 + '\n', 'divider')
            elif line.startswith('H2:'):
                self.text_widget.insert(END, '\n' + line[3:] + '\n', 'h2')
            elif line.startswith('H3:'):
                self.text_widget.insert(END, line[3:] + '\n', 'h3')
            elif line.startswith('BOLD:'):
                self.text_widget.insert(END, line[5:] + '\n', 'bold')
            elif line.startswith('BULLET:'):
                self.text_widget.insert(END, '  •  ' + line[7:] + '\n', 'bullet')
            elif line.startswith('TEXT:'):
                self.text_widget.insert(END, line[5:] + '\n', 'text')
            else:
                self.text_widget.insert(END, line + '\n', 'text')

        self.text_widget.configure(state='disabled')
        self.text_widget.yview_moveto(0)

    def _upload(self):
        """رفع ملف Word واستخراج محتواه"""
        if not session.require("add_marks"):
            return

        path = filedialog.askopenfilename(
            title="اختار ملف المنهج",
            filetypes=[("Word Files", "*.docx *.doc"), ("All files", "*.*")]
        )
        if not path:
            return

        fname = os.path.basename(path)

        # مؤشر تحميل
        self.file_lbl.config(text='⏳  جارٍ قراءة الملف...', fg='#e65100')
        self.parent.update_idletasks()

        try:
            content = _extract_docx_text(path)
            if not content.strip():
                messagebox.showerror("خطأ", "الملف فاضي أو تعذّرت قراءته.")
                self.file_lbl.config(text='لم يتم رفع ملف بعد', fg='gray')
                return

            # حفظ في DB
            con = self._con(); cur = con.cursor()
            cur.execute("""
                UPDATE curriculum
                SET content=?, file_name=?, updated_by=?, updated_at=datetime('now','localtime')
                WHERE subject_key=?
            """, (content, fname, session.admin_username, self.subject_key))
            con.commit(); con.close()

            log_action(session.admin_username, "UPLOAD_CURRICULUM",
                       "curriculum", None,
                       f"subject:{self.subject_key} file:{fname}")

            self._load()
            messagebox.showinfo("تم", f"تم رفع منهج {self.subject_name} بنجاح.\n\nالملف: {fname}")

        except Exception as ex:
            messagebox.showerror("خطأ في القراءة",
                f"تعذّرت قراءة الملف.\n\nتأكد إن python-docx مثبّت:\npip install python-docx\n\nالخطأ: {ex}")
            self.file_lbl.config(text='فشل في القراءة', fg='red')

    def _clear_content(self):
        """مسح المنهج المحفوظ"""
        if not session.require("add_marks"):
            return
        if not messagebox.askyesno("تأكيد",
                f"هتمسح منهج {self.subject_name}؟\nمتأكد؟"):
            return
        try:
            con = self._con(); cur = con.cursor()
            cur.execute("""
                UPDATE curriculum SET content='', file_name='', updated_by=?, updated_at=datetime('now','localtime')
                WHERE subject_key=?
            """, (session.admin_username, self.subject_key))
            con.commit(); con.close()
            self._show_empty()
            self.file_lbl.config(text='لم يتم رفع ملف بعد', fg='gray')
            messagebox.showinfo("تم", "تم مسح المنهج.")
        except Exception as ex:
            messagebox.showerror("خطأ", str(ex))


if __name__ == "__main__":
    root = Tk()
    CurriculumClass(root)
    root.mainloop()
