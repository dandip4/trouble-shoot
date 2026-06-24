from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from ..models import Pelanggan, Perangkat, db
from ..forms import PelangganForm, PerangkatForm

# Only admin and manajer can access these routes
pelanggan_bp = Blueprint("pelanggan", __name__, template_folder="../templates", url_prefix="/pelanggan")


@pelanggan_bp.before_request
@login_required
def check_admin_manajer():
    if current_user.role.value not in ["admin", "manajer"]:
        flash("Anda tidak memiliki akses ke halaman ini.", "danger")
        return redirect(url_for("troubleshoot.index"))


# ============================================================================
# PELANGGAN ROUTES
# ============================================================================

@pelanggan_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str).strip()

    query = Pelanggan.query

    if search:
        query = query.filter(
            Pelanggan.nama.ilike(f"%{search}%") |
            Pelanggan.kontak.ilike(f"%{search}%") |
            Pelanggan.lokasi.ilike(f"%{search}%")
        )

    pagination = query.order_by(Pelanggan.created_at.desc()).paginate(page=page, per_page=15)

    return render_template(
        "pelanggan/index.html",
        pagination=pagination,
        search=search,
    )


@pelanggan_bp.route("/tambah", methods=["GET", "POST"])
def tambah():
    form = PelangganForm()
    if form.validate_on_submit():
        if Pelanggan.query.filter_by(nama=form.nama.data).first():
            flash("Nama pelanggan sudah terdaftar.", "danger")
            return render_template("pelanggan/tambah.html", form=form)

        try:
            pelanggan = Pelanggan(
                nama=form.nama.data,
                kontak=form.kontak.data,
                email=form.email.data,
                lokasi=form.lokasi.data,
                departemen=form.departemen.data,
                alamat=form.alamat.data,
            )
            db.session.add(pelanggan)
            db.session.commit()
            flash("Pelanggan berhasil ditambahkan.", "success")
            return redirect(url_for("pelanggan.index"))
        except Exception:
            db.session.rollback()
            flash("Terjadi kesalahan saat menyimpan data.", "danger")

    return render_template("pelanggan/tambah.html", form=form)


@pelanggan_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    pelanggan = Pelanggan.query.get_or_404(id)
    form = PelangganForm(obj=pelanggan)

    if form.validate_on_submit():
        existing = Pelanggan.query.filter_by(nama=form.nama.data).first()
        if existing and existing.id != pelanggan.id:
            flash("Nama pelanggan sudah digunakan oleh data lain.", "danger")
            return render_template("pelanggan/edit.html", form=form, pelanggan=pelanggan)

        try:
            pelanggan.nama = form.nama.data
            pelanggan.kontak = form.kontak.data
            pelanggan.email = form.email.data
            pelanggan.lokasi = form.lokasi.data
            pelanggan.departemen = form.departemen.data
            pelanggan.alamat = form.alamat.data
            db.session.commit()
            flash("Pelanggan berhasil diperbarui.", "success")
            return redirect(url_for("pelanggan.index"))
        except Exception:
            db.session.rollback()
            flash("Terjadi kesalahan saat memperbarui data.", "danger")

    return render_template("pelanggan/edit.html", form=form, pelanggan=pelanggan)


@pelanggan_bp.route("/hapus/<int:id>", methods=["POST"])
def hapus(id):
    pelanggan = Pelanggan.query.get_or_404(id)
    try:
        db.session.delete(pelanggan)
        db.session.commit()
        flash("Pelanggan berhasil dihapus.", "success")
    except Exception:
        db.session.rollback()
        flash("Terjadi kesalahan saat menghapus data.", "danger")

    return redirect(url_for("pelanggan.index"))


# ============================================================================
# PERANGKAT ROUTES
# ============================================================================

@pelanggan_bp.route("/perangkat")
def perangkat_index():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str).strip()
    pelanggan_filter = request.args.get("pelanggan", "", type=str)

    query = Perangkat.query

    if search:
        query = query.filter(
            Perangkat.nama.ilike(f"%{search}%") |
            Perangkat.ip_address.ilike(f"%{search}%") |
            Perangkat.serial_number.ilike(f"%{search}%")
        )

    if pelanggan_filter:
        query = query.filter_by(pelanggan_id=pelanggan_filter)

    pagination = query.order_by(Perangkat.created_at.desc()).paginate(page=page, per_page=15)

    pelanggan_list = Pelanggan.query.all()

    return render_template(
        "pelanggan/perangkat_index.html",
        pagination=pagination,
        search=search,
        pelanggan_filter=pelanggan_filter,
        pelanggan_list=pelanggan_list,
    )


@pelanggan_bp.route("/perangkat/tambah", methods=["GET", "POST"])
def perangkat_tambah():
    form = PerangkatForm()
    pelanggan_list = Pelanggan.query.all()
    form.pelanggan_id.choices = [(p.id, p.nama) for p in pelanggan_list]

    if form.validate_on_submit():
        try:
            perangkat = Perangkat(
                nama=form.nama.data,
                ip_address=form.ip_address.data,
                mac_address=form.mac_address.data,
                location_code=form.location_code.data,
                tipe=form.tipe.data,
                serial_number=form.serial_number.data,
                status=form.status.data,
                keterangan=form.keterangan.data,
                pelanggan_id=form.pelanggan_id.data,
            )
            db.session.add(perangkat)
            db.session.commit()
            flash("Perangkat berhasil ditambahkan.", "success")
            return redirect(url_for("pelanggan.perangkat_index"))
        except Exception:
            db.session.rollback()
            flash("Terjadi kesalahan saat menyimpan data.", "danger")

    return render_template("pelanggan/perangkat_tambah.html", form=form)


@pelanggan_bp.route("/perangkat/edit/<int:id>", methods=["GET", "POST"])
def perangkat_edit(id):
    perangkat = Perangkat.query.get_or_404(id)
    form = PerangkatForm(obj=perangkat)
    pelanggan_list = Pelanggan.query.all()
    form.pelanggan_id.choices = [(p.id, p.nama) for p in pelanggan_list]

    if form.validate_on_submit():
        try:
            perangkat.nama = form.nama.data
            perangkat.ip_address = form.ip_address.data
            perangkat.mac_address = form.mac_address.data
            perangkat.location_code = form.location_code.data
            perangkat.tipe = form.tipe.data
            perangkat.serial_number = form.serial_number.data
            perangkat.status = form.status.data
            perangkat.keterangan = form.keterangan.data
            perangkat.pelanggan_id = form.pelanggan_id.data
            db.session.commit()
            flash("Perangkat berhasil diperbarui.", "success")
            return redirect(url_for("pelanggan.perangkat_index"))
        except Exception:
            db.session.rollback()
            flash("Terjadi kesalahan saat memperbarui data.", "danger")

    if request.method == "GET":
        form.pelanggan_id.data = perangkat.pelanggan_id

    return render_template("pelanggan/perangkat_edit.html", form=form, perangkat=perangkat)


@pelanggan_bp.route("/perangkat/hapus/<int:id>", methods=["POST"])
def perangkat_hapus(id):
    perangkat = Perangkat.query.get_or_404(id)
    try:
        db.session.delete(perangkat)
        db.session.commit()
        flash("Perangkat berhasil dihapus.", "success")
    except Exception:
        db.session.rollback()
        flash("Terjadi kesalahan saat menghapus data.", "danger")

    return redirect(url_for("pelanggan.perangkat_index"))
