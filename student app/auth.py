"""
auth.py  —  نظام الصلاحيات الكامل
=====================================================
الـ Roles:
    superadmin  →  كل الصلاحيات بدون قيود
    admin       →  Students, Teachers, Statistics  (بدون Admin Page)
    viewer      →  عرض فقط — مفيش add/update/delete

الاستخدام في أي صفحة:
    from auth import session, require_permission, ROLE_PERMISSIONS

    # 1. تحقق من صلاحية فتح الصفحة
    if not session.can("view_teachers"):
        messagebox.showerror("رفض", "مش عندك صلاحية.")
        return

    # 2. تعطيل زرار حسب الصلاحية
    if not session.can("add_teacher"):
        add_btn.configure(state="disabled")
"""

from tkinter import messagebox

# ============================================================
#  PERMISSIONS — كل الأذونات الممكنة في النظام
# ============================================================

PERMISSIONS = {
    # ---- Admin Page ----
    "view_admin_page",
    "add_admin",
    "update_admin",
    "delete_admin",
    "upgrade_to_admin",
    "view_accounts",
    "delete_account",

    # ---- Teachers Page ----
    "view_teachers",
    "add_teacher",
    "update_teacher",
    "delete_teacher",

    # ---- Students Page ----
    "view_students",
    "add_student",
    "update_student",
    "delete_student",

    # ---- Marks ----
    "view_marks",
    "add_marks",
    "update_marks",
    "delete_marks",

    # ---- Attendance ----
    "view_attendance",
    "add_attendance",
    "update_attendance",

    # ---- Statistics ----
    "view_statistics",

    # ---- Settings ----
    "view_settings",
    "change_own_password",
}

# ============================================================
#  ROLE → PERMISSIONS MAP
# ============================================================

ROLE_PERMISSIONS: dict[str, set] = {

    "superadmin": PERMISSIONS.copy(),   # كل شيء

    "admin": {
        # Teachers
        "view_teachers", "add_teacher", "update_teacher", "delete_teacher",
        # Students
        "view_students", "add_student", "update_student", "delete_student",
        # Marks
        "view_marks", "add_marks", "update_marks", "delete_marks",
        # Attendance
        "view_attendance", "add_attendance", "update_attendance",
        # Statistics
        "view_statistics",
        # حساب الأدمن نفسه
        "change_own_password",
    },

    "viewer": {
        # عرض فقط — مفيش أي تعديل
        "view_teachers",
        "view_students",
        "view_marks",
        "view_attendance",
        "view_statistics",
        "change_own_password",
    },
}

# ============================================================
#  SESSION — بيانات الأدمن المسجّل دخوله (Singleton)
# ============================================================

class Session:
    """
    session واحدة طول فترة تشغيل البرنامج.
    بتتملى في login.py بعد نجاح الدخول.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._reset()
        return cls._instance

    def _reset(self):
        self.admin_id       = None
        self.admin_name     = ""
        self.admin_username = ""
        self.role           = ""
        self._permissions   = set()
        self.logged_in      = False

    def login(self, admin_id: int, admin_name: str,
              admin_username: str, role: str):
        self.admin_id       = admin_id
        self.admin_name     = admin_name
        self.admin_username = admin_username
        self.role           = role.lower()
        self._permissions   = ROLE_PERMISSIONS.get(self.role, set()).copy()
        self.logged_in      = True

    def logout(self):
        self._reset()

    def can(self, permission: str) -> bool:
        """True لو الأدمن عنده الصلاحية دي"""
        return permission in self._permissions

    def require(self, permission: str, parent=None) -> bool:
        """
        لو مش عنده الصلاحية — بيعرض رسالة ويرجع False.
        استخدامها:
            if not session.require("delete_teacher"):
                return
        """
        if self.can(permission):
            return True
        role_ar = {"superadmin": "Super Admin",
                   "admin":      "Admin",
                   "viewer":     "Viewer"}.get(self.role, self.role)
        messagebox.showerror(
            "صلاحية مرفوضة",
            f"مش عندك صلاحية لعمل هذا.\n\n"
            f"الدور الحالي: {role_ar}\n"
            f"الصلاحية المطلوبة: {permission}",
            parent=parent
        )
        return False

    def apply_widget(self, widget, permission: str,
                     allowed_state="normal", denied_state="disabled"):
        """
        تطبيق الصلاحية على ويدجت تلقائياً:
            session.apply_widget(delete_btn, "delete_teacher")
        """
        state = allowed_state if self.can(permission) else denied_state
        try:
            widget.configure(state=state)
        except Exception:
            pass

    def apply_widgets(self, widgets_perms: list[tuple]):
        """
        تطبيق صلاحيات على ويدجتس متعددة دفعة واحدة:
            session.apply_widgets([
                (add_btn,    "add_teacher"),
                (update_btn, "update_teacher"),
                (delete_btn, "delete_teacher"),
            ])
        """
        for widget, perm in widgets_perms:
            self.apply_widget(widget, perm)

    def __repr__(self):
        return (f"<Session user='{self.admin_username}' "
                f"role='{self.role}' logged_in={self.logged_in}>")


# Singleton instance — استوردها في كل الملفات
session = Session()


# ============================================================
#  ROLE BADGE — لعرض الدور بشكل واضح في الـ UI
# ============================================================

ROLE_COLORS = {
    "superadmin": {"bg": "#8B0000", "fg": "white",  "label": "Super Admin"},
    "admin":      {"bg": "#DA7297", "fg": "white",  "label": "Admin"},
    "viewer":     {"bg": "#888888", "fg": "white",  "label": "Viewer"},
}

def get_role_display(role: str) -> dict:
    """يرجع dict فيه bg, fg, label للـ role"""
    return ROLE_COLORS.get(role.lower(),
                           {"bg": "#555", "fg": "white", "label": role})
