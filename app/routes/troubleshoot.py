import os
from datetime import datetime
from io import BytesIO

import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_file
from flask_login import login_required, current_user
from sqlalchemy import or_
from werkzeug.utils import secure_filename

from ..models import Troubleshoot, User, Pelanggan, Perangkat, db
from ..forms import TroubleshootForm, UploadForm, AssignTroubleForm, UpdateStatusForm
from ..models.troubleshoot import (
    JenisTroubleEnum,
    PerangkatEnum,
    ServiceEnum,
    KategoriClusterEnum,
    StatusTroubleEnum,
)

troubleshoot_bp = Blueprint("troubleshoot", __name__, template_folder="../templates", url_prefix="/troubleshoot")


def allowed_file(filename):
    return filename.lower().endswith(".xlsx")


def parse_duration(value):
    if not value:
        return None
    if isinstance(value, str):
        parts = value.split()
        for part in parts:
            if part.isdigit():
                return int(part)
    if isinstance(value, (int, float)):
        return int(value)
    return None


def get_kategori_filter_enum(value):
    if not value:
        return None
    try:
        return KategoriClusterEnum(value)
    except ValueError:
        return None


def can_modify(entry):
    if current_user.role.value == "admin":
        return True
    if current_user.role.value == "teknisi" and entry.created_by == current_user.id:
        return True
    return False


@troubleshoot_bp.route("/")
@login_required
def index():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str).strip()
    kategori_filter = request.args.get("kategori", "", type=str)

    query = Troubleshoot.query

    # Technician only sees their assigned tasks
    if current_user.role.value == "teknisi":
        query = query.filter_by(assigned_to=current_user.id)

    if search:
        query = query.filter(
            or_(
                Troubleshoot.nama_pelanggan.ilike(f"%{search}%"),
                Troubleshoot.jenis_trouble.ilike(f"%{search}%"),
                Troubleshoot.perangkat.ilike(f"%{search}%"),
            )
        )

    if kategori_filter:
        kategori_enum = get_kategori_filter_enum(kategori_filter)
        if kategori_enum is not None:
            query = query.filter_by(kategori_cluster=kategori_enum)

    pagination = query.order_by(Troubleshoot.created_at.desc()).paginate(page=page, per_page=15)

    return render_template(
        "troubleshoot/index.html",
        pagination=pagination,
        search=search,
        kategori_filter=kategori_filter,
    )


@troubleshoot_bp.route("/tambah", methods=["GET", "POST"])
@login_required
def tambah():
    if current_user.role.value == "manajer":
        flash("Manajer tidak dapat menambah data.", "danger")
        return redirect(url_for("troubleshoot.index"))

    form = TroubleshootForm()
    
    # Populate dropdown choices from database
    form.pelanggan_id.choices = [(p.id, f"{p.nama} ({p.kontak})") for p in Pelanggan.query.all()]
    form.perangkat_id.choices = [(p.id, f"{p.nama} - {p.tipe}") for p in Perangkat.query.all()]
    
    if form.validate_on_submit():
        if form.selesai_pengerjaan.data and form.selesai_pengerjaan.data < form.tanggal_komplain.data:
            flash("Tanggal selesai tidak boleh sebelum tanggal komplain.", "danger")
            return render_template("troubleshoot/tambah.html", form=form)

        if Troubleshoot.query.filter_by(no_spk=form.no_spk.data).first():
            flash("No SPK sudah ada.", "danger")
            return render_template("troubleshoot/tambah.html", form=form)

        try:
            # Get pelanggan and perangkat from form
            pelanggan = Pelanggan.query.get(form.pelanggan_id.data)
            perangkat = Perangkat.query.get(form.perangkat_id.data)
            
            if not pelanggan or not perangkat:
                flash("Pelanggan atau Perangkat tidak ditemukan.", "danger")
                return render_template("troubleshoot/tambah.html", form=form)
            
            entry = Troubleshoot(
                no_spk=form.no_spk.data,
                nama_pelanggan=pelanggan.nama,
                informasi_trouble=form.informasi_trouble.data,
                jenis_trouble=JenisTroubleEnum[form.jenis_trouble.data.replace(" ", "_")],
                perangkat=PerangkatEnum[form.perangkat_tipe.data],
                service=ServiceEnum[form.service.data],
                tanggal_komplain=form.tanggal_komplain.data,
                selesai_pengerjaan=form.selesai_pengerjaan.data,
                durasi_pengerjaan=form.durasi_pengerjaan.data,
                keterangan_action=form.keterangan_action.data,
                kategori_cluster=None,
                created_by=current_user.id,
                pelanggan_id=pelanggan.id,
                perangkat_id=perangkat.id,
            )
            db.session.add(entry)
            db.session.commit()
            flash("Data troubleshoot berhasil ditambahkan.", "success")
            return redirect(url_for("troubleshoot.index"))
        except Exception as e:
            db.session.rollback()
            flash(f"Terjadi kesalahan saat menyimpan data: {str(e)}", "danger")

    return render_template("troubleshoot/tambah.html", form=form)


@troubleshoot_bp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    entry = Troubleshoot.query.get_or_404(id)
    if not can_modify(entry):
        flash("Anda tidak memiliki izin untuk mengedit data ini.", "danger")
        return redirect(url_for("troubleshoot.index"))

    form = TroubleshootForm(obj=entry)
    
    # Populate dropdown choices
    form.pelanggan_id.choices = [(p.id, f"{p.nama} ({p.kontak})") for p in Pelanggan.query.all()]
    form.perangkat_id.choices = [(p.id, f"{p.nama} - {p.tipe}") for p in Perangkat.query.all()]
    
    if form.validate_on_submit():
        if form.selesai_pengerjaan.data and form.selesai_pengerjaan.data < form.tanggal_komplain.data:
            flash("Tanggal selesai tidak boleh sebelum tanggal komplain.", "danger")
            return render_template("troubleshoot/edit.html", form=form, entry=entry)

        existing = Troubleshoot.query.filter_by(no_spk=form.no_spk.data).first()
        if existing and existing.id != entry.id:
            flash("No SPK sudah digunakan oleh data lain.", "danger")
            return render_template("troubleshoot/edit.html", form=form, entry=entry)

        try:
            # Get pelanggan and perangkat from form
            pelanggan = Pelanggan.query.get(form.pelanggan_id.data)
            perangkat = Perangkat.query.get(form.perangkat_id.data)
            
            if not pelanggan or not perangkat:
                flash("Pelanggan atau Perangkat tidak ditemukan.", "danger")
                return render_template("troubleshoot/edit.html", form=form, entry=entry)
            
            entry.no_spk = form.no_spk.data
            entry.nama_pelanggan = pelanggan.nama
            entry.informasi_trouble = form.informasi_trouble.data
            entry.jenis_trouble = JenisTroubleEnum[form.jenis_trouble.data.replace(" ", "_")]
            entry.perangkat = PerangkatEnum[form.perangkat_tipe.data]
            entry.service = ServiceEnum[form.service.data]
            entry.tanggal_komplain = form.tanggal_komplain.data
            entry.selesai_pengerjaan = form.selesai_pengerjaan.data
            entry.durasi_pengerjaan = form.durasi_pengerjaan.data
            entry.keterangan_action = form.keterangan_action.data
            entry.pelanggan_id = pelanggan.id
            entry.perangkat_id = perangkat.id
            db.session.commit()
            flash("Data troubleshoot berhasil diperbarui.", "success")
            return redirect(url_for("troubleshoot.index"))
        except Exception as e:
            db.session.rollback()
            flash(f"Terjadi kesalahan saat memperbarui data: {str(e)}", "danger")

    if request.method == "GET":
        form.jenis_trouble.data = entry.jenis_trouble.value
        form.perangkat_tipe.data = entry.perangkat.value
        form.service.data = entry.service.value
        form.pelanggan_id.data = entry.pelanggan_id
        form.perangkat_id.data = entry.perangkat_id

    return render_template("troubleshoot/edit.html", form=form, entry=entry)


@troubleshoot_bp.route("/hapus/<int:id>", methods=["POST"])
@login_required
def hapus(id):
    entry = Troubleshoot.query.get_or_404(id)
    if not can_modify(entry):
        flash("Anda tidak memiliki izin untuk menghapus data ini.", "danger")
        return redirect(url_for("troubleshoot.index"))

    try:
        db.session.delete(entry)
        db.session.commit()
        flash("Data troubleshoot berhasil dihapus.", "success")
    except Exception:
        db.session.rollback()
        flash("Terjadi kesalahan saat menghapus data.", "danger")

    return redirect(url_for("troubleshoot.index"))


@troubleshoot_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if current_user.role.value == "manajer":
        flash("Manajer tidak dapat mengunggah data.", "danger")
        return redirect(url_for("troubleshoot.index"))

    form = UploadForm()
    summary = None

    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        if not allowed_file(filename):
            flash("Hanya file .xlsx yang diperbolehkan.", "danger")
            return redirect(url_for("troubleshoot.upload"))

        os.makedirs(current_app.config["UPLOAD_FOLDER"], exist_ok=True)
        upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(upload_path)

        imported = 0
        skipped = 0
        try:
            df = pd.read_excel(upload_path, dtype=str)
            # normalize column names
            df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns]

            expected_required = {
                "No_SPK",
                "Nama_Pelanggan",
                "Informasi_Trouble",
                "Jenis_Trouble",
                "Perangkat",
                "Service",
            }
            # Accept either spelling for tanggal complaint column
            date_candidates = {"Tanggal_Compliment_Pelanggan", "Tanggal_Complaint_Pelanggan", "Tanggal_Complain_Pelanggan"}
            optional_columns = {"Selesai_Pengerjaan", "Durasi_Pengerjaan", "Keterangan_Action"}

            present = set(df.columns)
            missing = expected_required - present
            if not (present & date_candidates):
                missing.add("Tanggal_Complaint (kolom harus salah satu dari: " + ", ".join(sorted(date_candidates)) + ")")

            if missing:
                flash(f"File Excel tidak memiliki kolom yang diperlukan: {', '.join(sorted(missing))}", "danger")
                return redirect(url_for("troubleshoot.upload"))

            for _, row in df.iterrows():
                no_spk = str(row.get("No_SPK", "")).strip()
                if not no_spk:
                    continue
                if Troubleshoot.query.filter_by(no_spk=no_spk).first():
                    skipped += 1
                    continue

                # determine tanggal_komplain column
                tanggal_col = None
                for c in date_candidates:
                    if c in row.index:
                        tanggal_col = c
                        break

                entry = Troubleshoot(
                    no_spk=no_spk,
                    nama_pelanggan=str(row.get("Nama_Pelanggan", "")).strip(),
                    informasi_trouble=str(row.get("Informasi_Trouble", "")).strip(),
                    jenis_trouble=JenisTroubleEnum[str(row.get("Jenis_Trouble", "")).replace(" ", "_")],
                    perangkat=PerangkatEnum[str(row.get("Perangkat", "")).strip()],
                    service=ServiceEnum[str(row.get("Service", "")).strip()],
                    tanggal_komplain=pd.to_datetime(row.get(tanggal_col, ""), errors="coerce").date() if tanggal_col else None,
                    selesai_pengerjaan=pd.to_datetime(row.get("Selesai_Pengerjaan", ""), errors="coerce").date(),
                    durasi_pengerjaan=parse_duration(row.get("Durasi_Pengerjaan", "")),
                    keterangan_action=str(row.get("Keterangan_Action", "")).strip(),
                    created_by=current_user.id,
                )
                db.session.add(entry)
                imported += 1

            db.session.commit()
            summary = f"Berhasil import {imported} baris, skip {skipped} duplikat."
            flash(summary, "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.exception("Gagal memproses file Excel saat upload")
            flash(f"Terjadi kesalahan saat memproses file Excel: {str(e)}", "danger")
        finally:
            try:
                os.remove(upload_path)
            except OSError:
                pass

    return render_template("troubleshoot/upload.html", form=form, summary=summary)


@troubleshoot_bp.route("/export")
@login_required
def export():
    query = Troubleshoot.query.order_by(Troubleshoot.created_at.desc()).all()
    rows = []
    for item in query:
        rows.append({
            "No_SPK": item.no_spk,
            "Nama_Pelanggan": item.nama_pelanggan,
            "Informasi_Trouble": item.informasi_trouble,
            "Jenis_Trouble": item.jenis_trouble.value,
            "Perangkat": item.perangkat.value,
            "Service": item.service.value,
            "Tanggal_Compliment_Pelanggan": item.tanggal_komplain.strftime("%Y-%m-%d") if item.tanggal_komplain else "",
            "Selesai_Pengerjaan": item.selesai_pengerjaan.strftime("%Y-%m-%d") if item.selesai_pengerjaan else "",
            "Durasi_Pengerjaan": f"{item.durasi_pengerjaan} Hari" if item.durasi_pengerjaan is not None else "",
            "Keterangan_Action": item.keterangan_action or "",
            "Cluster": item.cluster_id or "",
            "Kategori_Cluster": item.kategori_cluster.value if item.kategori_cluster else "",
        })

    df = pd.DataFrame(rows)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    filename = f"data_troubleshoot_{datetime.now().strftime('%Y%m%d')}.xlsx"
    return send_file(
        output,
        download_name=filename,
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


# ============================================================================
# ASSIGNMENT SYSTEM ROUTES
# ============================================================================

@troubleshoot_bp.route("/assign/<int:id>", methods=["GET", "POST"])
@login_required
def assign(id):
    """Admin assigns a troubleshoot to a technician"""
    if current_user.role.value != "admin":
        flash("Hanya admin yang dapat mengassign troubleshoot.", "danger")
        return redirect(url_for("troubleshoot.index"))

    entry = Troubleshoot.query.get_or_404(id)
    form = AssignTroubleForm()
    
    # Populate choices with active technicians
    teknisi_list = User.query.filter_by(role="teknisi", is_active=True).all()
    form.assigned_to.choices = [(t.id, t.username) for t in teknisi_list]

    if form.validate_on_submit():
        try:
            entry.assigned_to = form.assigned_to.data
            db.session.commit()
            flash(f"Troubleshoot berhasil diassign ke {entry.assigned_user.username}.", "success")
            return redirect(url_for("troubleshoot.index"))
        except Exception:
            db.session.rollback()
            flash("Terjadi kesalahan saat mengassign troubleshoot.", "danger")

    return render_template("troubleshoot/assign.html", form=form, entry=entry)


@troubleshoot_bp.route("/my-tasks")
@login_required
def my_tasks():
    """Teknisi view their assigned tasks"""
    if current_user.role.value != "teknisi":
        flash("Hanya teknisi yang dapat melihat task yang diassign.", "danger")
        return redirect(url_for("troubleshoot.index"))

    page = request.args.get("page", 1, type=int)
    status_filter = request.args.get("status", "", type=str)

    query = Troubleshoot.query.filter_by(assigned_to=current_user.id)

    if status_filter:
        status_map = {
            "Pending": StatusTroubleEnum.Pending,
            "InProgress": StatusTroubleEnum.InProgress,
            "Completed": StatusTroubleEnum.Completed,
        }
        if status_filter in status_map:
            query = query.filter_by(status=status_map[status_filter])

    pagination = query.order_by(Troubleshoot.created_at.desc()).paginate(page=page, per_page=15)

    # Get summary statistics
    total_tasks = Troubleshoot.query.filter_by(assigned_to=current_user.id).count()
    pending_tasks = Troubleshoot.query.filter_by(assigned_to=current_user.id, status=StatusTroubleEnum.Pending).count()
    inprogress_tasks = Troubleshoot.query.filter_by(assigned_to=current_user.id, status=StatusTroubleEnum.InProgress).count()
    completed_tasks = Troubleshoot.query.filter_by(assigned_to=current_user.id, status=StatusTroubleEnum.Completed).count()

    stats = {
        "total": total_tasks,
        "pending": pending_tasks,
        "inprogress": inprogress_tasks,
        "completed": completed_tasks,
    }

    return render_template(
        "troubleshoot/my_tasks.html",
        pagination=pagination,
        status_filter=status_filter,
        stats=stats,
    )


@troubleshoot_bp.route("/update-status/<int:id>", methods=["GET", "POST"])
@login_required
def update_status(id):
    """Update troubleshoot status"""
    entry = Troubleshoot.query.get_or_404(id)

    # Check authorization: teknisi can only update their assigned tasks, admin can update any
    if current_user.role.value == "teknisi" and entry.assigned_to != current_user.id:
        flash("Anda tidak memiliki izin untuk update status troubleshoot ini.", "danger")
        return redirect(url_for("troubleshoot.index"))

    if current_user.role.value not in ["admin", "teknisi"]:
        flash("Hanya admin dan teknisi yang dapat update status.", "danger")
        return redirect(url_for("troubleshoot.index"))

    form = UpdateStatusForm()
    if form.validate_on_submit():
        try:
            status_map = {
                "Pending": StatusTroubleEnum.Pending,
                "In Progress": StatusTroubleEnum.InProgress,
                "Completed": StatusTroubleEnum.Completed,
            }
            entry.status = status_map.get(form.status.data)
            db.session.commit()
            flash("Status troubleshoot berhasil diperbarui.", "success")
            return redirect(url_for("troubleshoot.index"))
        except Exception:
            db.session.rollback()
            flash("Terjadi kesalahan saat update status.", "danger")

    if request.method == "GET":
        form.status.data = entry.status.value

    return render_template("troubleshoot/update_status.html", form=form, entry=entry)
