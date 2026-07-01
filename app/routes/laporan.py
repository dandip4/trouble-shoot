from datetime import datetime
from urllib.parse import urlencode
from flask import Blueprint, render_template, request, send_file, url_for
from flask_login import login_required, current_user

from ..models import Troubleshoot, ClusterHistory
from ..models.troubleshoot import KategoriClusterEnum, JenisTroubleEnum, PerangkatEnum
from ..services.export_service import ExportService

laporan_bp = Blueprint("laporan", __name__, template_folder="../templates", url_prefix="/laporan")


def get_kategori_enum(value):
    if not value:
        return None
    try:
        return KategoriClusterEnum(value)
    except ValueError:
        return None


def build_filter(query):
    dari = request.args.get("dari")
    sampai = request.args.get("sampai")
    jenis = request.args.getlist("jenis")
    perangkat = request.args.getlist("perangkat")
    kategori = request.args.get("kategori", "Semua")

    if dari:
        try:
            tanggal_dari = datetime.strptime(dari, "%Y-%m-%d")
            query = query.filter(Troubleshoot.created_at >= tanggal_dari)
        except ValueError:
            pass
    if sampai:
        try:
            tanggal_sampai = datetime.strptime(sampai, "%Y-%m-%d")
            query = query.filter(Troubleshoot.created_at <= tanggal_sampai)
        except ValueError:
            pass
    if jenis:
        enum_jenis = []
        for value in jenis:
            key = value.replace(" ", "_")
            try:
                enum_jenis.append(JenisTroubleEnum[key])
            except KeyError:
                continue
        if enum_jenis:
            query = query.filter(Troubleshoot.jenis_trouble.in_(enum_jenis))
    if perangkat:
        enum_perangkat = []
        for value in perangkat:
            try:
                enum_perangkat.append(PerangkatEnum[value])
            except KeyError:
                continue
        if enum_perangkat:
            query = query.filter(Troubleshoot.perangkat.in_(enum_perangkat))
    if kategori and kategori != "Semua":
        kategori_enum = get_kategori_enum(kategori)
        if kategori_enum is not None:
            query = query.filter(Troubleshoot.kategori_cluster == kategori_enum)

    # Technician only sees their assigned tasks
    if current_user.role.value == "teknisi":
        query = query.filter(Troubleshoot.assigned_to == current_user.id)

    return query


@laporan_bp.route("/")
@login_required
def index():
    query = build_filter(Troubleshoot.query)
    page = request.args.get("page", 1, type=int)
    pagination = query.order_by(Troubleshoot.created_at.desc()).paginate(page=page, per_page=15)
    rows = pagination.items

    summary = {
        "kategori": {
            "Ringan": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Ringan).count(),
            "Sedang": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Sedang).count(),
            "Berat": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Berat).count(),
            "Sangat Berat": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Sangat_Berat).count(),
        },
        "jenis": {},
        "perangkat": {},
    }

    jenis_options = ["Human", "Configuration Issue", "Hardware Failure", "Software Issue", "Network Issue"]
    perangkat_options = ["PC", "Laptop", "Printer", "Server", "Firewall", "Switch", "Router", "Accesspoint"]

    for jenis in jenis_options:
        try:
            summary["jenis"][jenis] = query.filter(Troubleshoot.jenis_trouble == JenisTroubleEnum[jenis.replace(" ", "_")]).count()
        except KeyError:
            summary["jenis"][jenis] = 0
    for perangkat in perangkat_options:
        try:
            summary["perangkat"][perangkat] = query.filter(Troubleshoot.perangkat == PerangkatEnum[perangkat]).count()
        except KeyError:
            summary["perangkat"][perangkat] = 0

    clustering_rows = ClusterHistory.query.order_by(ClusterHistory.tanggal_clustering.desc()).all()
    preserved_args = {k: v for k, v in request.args.to_dict(flat=False).items() if k != "page"}
    export_url = url_for("laporan.export_excel", **preserved_args)
    query_string = urlencode([(key, value) for key, values in preserved_args.items() for value in values])

    return render_template(
        "laporan/index.html",
        pagination=pagination,
        rows=rows,
        summary=summary,
        jenis_options=jenis_options,
        perangkat_options=perangkat_options,
        clustering_rows=clustering_rows,
        export_url=export_url,
        selected_kategori=request.args.get("kategori", "Semua"),
        selected_jenis=request.args.getlist("jenis"),
        selected_perangkat=request.args.getlist("perangkat"),
        dari=request.args.get("dari", ""),
        sampai=request.args.get("sampai", ""),
        query_string=query_string,
    )


@laporan_bp.route("/export-excel")
@login_required
def export_excel():
    query = build_filter(Troubleshoot.query)
    rows = query.order_by(Troubleshoot.created_at.desc()).all()

    dari = request.args.get("dari", "")
    sampai = request.args.get("sampai", "")
    periode = f"{dari}_{sampai}" if dari or sampai else datetime.now().strftime("%Y%m%d")

    summary = {
        "kategori": {
            "Ringan": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Ringan).count(),
            "Sedang": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Sedang).count(),
            "Berat": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Berat).count(),
            "Sangat Berat": query.filter(Troubleshoot.kategori_cluster == KategoriClusterEnum.Sangat_Berat).count(),
        },
        "jenis": {},
        "perangkat": {},
    }
    jenis_options = ["Human", "Configuration Issue", "Hardware Failure", "Software Issue", "Network Issue"]
    perangkat_options = ["PC", "Laptop", "Printer", "Server", "Firewall", "Switch", "Router", "Accesspoint"]
    for jenis in jenis_options:
        try:
            summary["jenis"][jenis] = query.filter(Troubleshoot.jenis_trouble == JenisTroubleEnum[jenis.replace(" ", "_")]).count()
        except KeyError:
            summary["jenis"][jenis] = 0
    for perangkat in perangkat_options:
        try:
            summary["perangkat"][perangkat] = query.filter(Troubleshoot.perangkat == PerangkatEnum[perangkat]).count()
        except KeyError:
            summary["perangkat"][perangkat] = 0

    last_clustering = ClusterHistory.query.order_by(ClusterHistory.tanggal_clustering.desc()).first()
    clustering_info = None
    if last_clustering:
        clustering_info = {
            "tanggal": last_clustering.tanggal_clustering.strftime("%Y-%m-%d %H:%M:%S"),
            "k": last_clustering.jumlah_cluster,
            "dbi": last_clustering.dbi_score,
            "silhouette": last_clustering.silhouette_score,
        }

    export_service = ExportService()
    output = export_service.generate_report(rows, summary, clustering_info, periode)
    filename = f"laporan_troubleshoot_{periode}.xlsx"
    return send_file(
        output,
        download_name=filename,
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@laporan_bp.route("/riwayat-cluster")
@login_required
def riwayat_cluster():
    clustering_rows = ClusterHistory.query.order_by(ClusterHistory.tanggal_clustering.desc()).all()
    return render_template("laporan/riwayat_cluster.html", clustering_rows=clustering_rows)
