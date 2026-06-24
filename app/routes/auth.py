from datetime import timedelta

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user

from ..models import User, db


auth_bp = Blueprint("auth", __name__, template_folder="../templates", url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        remember = request.form.get("remember") == "on"

        if not username or not password:
            flash("Semua field harus diisi.", "danger")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash("Username atau password tidak valid.", "danger")
            return redirect(url_for("auth.login"))

        if not user.is_active:
            flash("Akun tidak aktif.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=remember, duration=timedelta(days=7))
        flash("Login berhasil.", "success")
        return redirect(url_for("dashboard.index"))

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        role = request.form.get("role", "").strip()

        if not username or not email or not password or not confirm_password or not role:
            flash("Semua field harus diisi.", "danger")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Password dan konfirmasi password tidak cocok.", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.", "danger")
            return redirect(url_for("auth.register"))

        if role not in ["teknisi", "manajer"]:
            flash("Role tidak valid untuk registrasi.", "danger")
            return redirect(url_for("auth.register"))

        user = User(username=username, email=email, role=role, is_active=True)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registrasi berhasil. Silakan login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    flash("Anda berhasil logout.", "success")
    return redirect(url_for("auth.login"))
