from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import current_user
from sqlalchemy import delete

from ..models import User, Troubleshoot, ClusterHistory, db
from ..utils import role_required

admin_bp = Blueprint("admin", __name__, template_folder="../templates", url_prefix="/admin")


@admin_bp.route("/users")
@role_required(["admin"])
def users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)


@admin_bp.route("/users/tambah", methods=["GET", "POST"])
@role_required(["admin"])
def tambah_user():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        role = request.form.get("role", "").strip()
        is_active = request.form.get("is_active") == "on"
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if not username or not email or not role or not password or not confirm_password:
            flash("Semua field harus diisi.", "danger")
            return redirect(url_for("admin.tambah_user"))

        if password != confirm_password:
            flash("Password dan konfirmasi password tidak cocok.", "danger")
            return redirect(url_for("admin.tambah_user"))

        if User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.", "danger")
            return redirect(url_for("admin.tambah_user"))

        if User.query.filter_by(email=email).first():
            flash("Email sudah digunakan.", "danger")
            return redirect(url_for("admin.tambah_user"))

        if role not in ["admin", "teknisi", "manajer"]:
            flash("Role tidak valid.", "danger")
            return redirect(url_for("admin.tambah_user"))

        user = User(username=username, email=email, role=role, is_active=is_active)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("User berhasil ditambahkan.", "success")
        return redirect(url_for("admin.users"))

    return render_template("admin/tambah_user.html")


@admin_bp.route("/users/edit/<int:id>", methods=["GET", "POST"])
@role_required(["admin"])
def edit_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        own_account = True
    else:
        own_account = False

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        role = request.form.get("role", "").strip()
        is_active = request.form.get("is_active") == "on"

        if not username or not email or not role:
            flash("Semua field harus diisi.", "danger")
            return redirect(url_for("admin.edit_user", id=id))

        if user.username != username and User.query.filter_by(username=username).first():
            flash("Username sudah digunakan.", "danger")
            return redirect(url_for("admin.edit_user", id=id))

        if user.email != email and User.query.filter_by(email=email).first():
            flash("Email sudah digunakan.", "danger")
            return redirect(url_for("admin.edit_user", id=id))

        if role not in ["admin", "teknisi", "manajer"]:
            flash("Role tidak valid.", "danger")
            return redirect(url_for("admin.edit_user", id=id))

        user.username = username
        user.email = email
        if not own_account:
            user.role = role
        user.is_active = is_active
        db.session.commit()

        flash("User berhasil diperbarui.", "success")
        return redirect(url_for("admin.users"))

    return render_template("admin/edit_user.html", user=user, own_account=own_account)


@admin_bp.route("/users/toggle-active/<int:id>", methods=["POST"])
@role_required(["admin"])
def toggle_active_user(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        return jsonify(success=False, message="Admin tidak bisa menonaktifkan dirinya sendiri."), 400

    user.is_active = not user.is_active
    db.session.commit()
    status = "Aktif" if user.is_active else "Nonaktif"
    return jsonify(success=True, message=f"User berhasil di{ 'aktifkan' if user.is_active else 'nonaktifkan' }.", status=status)


@admin_bp.route("/users/reset-password/<int:id>", methods=["POST"])
@role_required(["admin"])
def reset_password(id):
    user = User.query.get_or_404(id)
    user.set_password("password123")
    db.session.commit()
    flash("Password berhasil di-reset ke password123.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/delete-all-data", methods=["POST"])
@role_required(["admin"])
def delete_all_data():
    try:
        db.session.execute(delete(Troubleshoot))
        db.session.execute(delete(ClusterHistory))
        db.session.commit()
        flash("Semua data troubleshoot dan riwayat clustering berhasil dihapus.", "success")
    except Exception:
        db.session.rollback()
        flash("Gagal menghapus semua data.", "danger")
    return redirect(url_for("dashboard.index"))
