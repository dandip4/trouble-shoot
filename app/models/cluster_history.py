from . import db


class ClusterHistory(db.Model):
    __tablename__ = "cluster_history"

    id = db.Column(db.Integer, primary_key=True)
    jumlah_cluster = db.Column(db.Integer, nullable=False)
    dbi_score = db.Column(db.Float, nullable=False)
    silhouette_score = db.Column(db.Float, nullable=False)
    tanggal_clustering = db.Column(db.DateTime, server_default=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    user = db.relationship("User", backref=db.backref("cluster_histories", lazy="select"), lazy="select")

    def __repr__(self):
        return f"<ClusterHistory {self.id} clusters={self.jumlah_cluster}>"
