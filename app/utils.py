from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user, login_required


def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))

            current_role = getattr(current_user, "role", None)
            role_value = current_role.value if current_role is not None else None
            if role_value not in roles:
                flash("Akses ditolak. Anda tidak memiliki izin untuk melihat halaman ini.", "danger")
                return redirect(url_for("dashboard.index"))

            return view_func(*args, **kwargs)

        return wrapped
    return decorator
