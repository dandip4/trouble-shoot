from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from ..utils import role_required
from ..services.clustering_service import ClusteringService
from ..models import Troubleshoot, ClusterHistory, db

clustering_bp = Blueprint("clustering", __name__, template_folder="../templates", url_prefix="/clustering")


@clustering_bp.route("/")
@login_required
def index():
    total_rows = Troubleshoot.query.count()
    last_history = ClusterHistory.query.order_by(ClusterHistory.tanggal_clustering.desc()).first()
    cluster_counts = []
    if total_rows > 0:
        rows = (
            db.session.query(Troubleshoot.cluster_id, db.func.count(Troubleshoot.id))
            .group_by(Troubleshoot.cluster_id)
            .all()
        )
        for cluster_id, count in rows:
            cluster_counts.append({
                "cluster": cluster_id,
                "count": count,
            })

    return render_template(
        "clustering/index.html",
        last_history=last_history,
        total_rows=total_rows,
        cluster_counts=cluster_counts,
    )


@clustering_bp.route("/run", methods=["POST"])
@role_required(["admin"])
def run_clustering():
    selected_k = request.form.get("k", 3, type=int)
    total_rows = Troubleshoot.query.count()
    if total_rows < 10:
        return jsonify(success=False, message="Data terlalu sedikit untuk clustering"), 400

    try:
        service = ClusteringService()
        result = service.run_clustering(selected_k)
        last_history = ClusterHistory.query.order_by(ClusterHistory.tanggal_clustering.desc()).first()
        return jsonify(
            success=True,
            result=result,
            last_history={
                "tanggal": last_history.tanggal_clustering.strftime("%Y-%m-%d %H:%M:%S") if last_history else None,
                "k": last_history.jumlah_cluster if last_history else None,
                "dbi": last_history.dbi_score if last_history else None,
                "silhouette": last_history.silhouette_score if last_history else None,
            },
        )
    except ValueError as e:
        return jsonify(success=False, message=str(e)), 400
    except Exception:
        return jsonify(success=False, message="Terjadi kesalahan saat menjalankan clustering."), 500


@clustering_bp.route("/elbow-data")
@login_required
def elbow_data():
    service = ClusteringService()
    data = service.get_elbow_data()
    return jsonify(data)


@clustering_bp.route("/pca-data")
@login_required
def pca_data():
    service = ClusteringService()
    data = service.get_pca_data()
    return jsonify(data)
