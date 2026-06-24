from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func, extract

from ..models import Troubleshoot, ClusterHistory, db
from ..models.troubleshoot import KategoriClusterEnum, JenisTroubleEnum, PerangkatEnum


dashboard_bp = Blueprint("dashboard", __name__, template_folder="../templates")


@dashboard_bp.route("/dashboard")
@login_required
def index():
    # Filter data based on user role
    if current_user.role.value == "teknisi":
        # Technician only sees their assigned tasks
        query = Troubleshoot.query.filter_by(assigned_to=current_user.id)
    else:
        # Admin and Manajer see all data
        query = Troubleshoot.query

    total_data = query.count()

    per_kategori = {
        "Ringan": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Ringan).count(),
        "Sedang": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Sedang).count(),
        "Berat": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Berat).count(),
    }

    per_jenis_trouble = {
        "Human": query.filter(Troubleshoot.jenis_trouble == JenisTroubleEnum.Human).count(),
        "Configuration Issue": query.filter(Troubleshoot.jenis_trouble == JenisTroubleEnum.Configuration_Issue).count(),
        "Hardware Failure": query.filter(Troubleshoot.jenis_trouble == JenisTroubleEnum.Hardware_Failure).count(),
        "Software Issue": query.filter(Troubleshoot.jenis_trouble == JenisTroubleEnum.Software_Issue).count(),
        "Network Issue": query.filter(Troubleshoot.jenis_trouble == JenisTroubleEnum.Network_Issue).count(),
    }

    per_perangkat = {
        "PC": query.filter(Troubleshoot.perangkat == PerangkatEnum.PC).count(),
        "Laptop": query.filter(Troubleshoot.perangkat == PerangkatEnum.Laptop).count(),
        "Printer": query.filter(Troubleshoot.perangkat == PerangkatEnum.Printer).count(),
        "Server": query.filter(Troubleshoot.perangkat == PerangkatEnum.Server).count(),
        "Firewall": query.filter(Troubleshoot.perangkat == PerangkatEnum.Firewall).count(),
        "Switch": query.filter(Troubleshoot.perangkat == PerangkatEnum.Switch).count(),
        "Router": query.filter(Troubleshoot.perangkat == PerangkatEnum.Router).count(),
        "Accesspoint": query.filter(Troubleshoot.perangkat == PerangkatEnum.Accesspoint).count(),
    }

    trend_bulanan = []
    today = datetime.today()
    for offset in range(11, -1, -1):
        month = today.month - offset
        year = today.year
        if month <= 0:
            month += 12
            year -= 1
        month_label = datetime(year, month, 1).strftime("%b %Y")
        count = (
            query
            .filter(extract("year", Troubleshoot.created_at) == year)
            .filter(extract("month", Troubleshoot.created_at) == month)
            .count()
        )
        trend_bulanan.append({"bulan": month_label, "jumlah": count})

    rata_durasi_per_kategori = {}
    for kategori in [KategoriClusterEnum.Ringan, KategoriClusterEnum.Sedang, KategoriClusterEnum.Berat]:
        avg_duration = (
            query
            .filter(Troubleshoot.kategori_cluster == kategori)
            .with_entities(func.avg(Troubleshoot.durasi_pengerjaan))
            .scalar()
        )
        rata_durasi_per_kategori[kategori.value] = round(avg_duration or 0, 2)

    last_clustering = ClusterHistory.query.order_by(ClusterHistory.tanggal_clustering.desc()).first()
    last_clustering_info = None
    if last_clustering:
        last_clustering_info = {
            "tanggal": last_clustering.tanggal_clustering.strftime("%Y-%m-%d %H:%M:%S"),
            "k": last_clustering.jumlah_cluster,
            "dbi": last_clustering.dbi_score,
        }

    data_terbaru = query.order_by(Troubleshoot.created_at.desc()).limit(5).all()

    return render_template(
        "dashboard/index.html",
        total_data=total_data,
        per_kategori=per_kategori,
        per_jenis_trouble=per_jenis_trouble,
        per_perangkat=per_perangkat,
        trend_bulanan=trend_bulanan,
        rata_durasi_per_kategori=rata_durasi_per_kategori,
        last_clustering=last_clustering_info,
        data_terbaru=data_terbaru,
    )
