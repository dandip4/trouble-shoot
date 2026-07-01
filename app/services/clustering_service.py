import os
import pickle

import numpy as np
import pandas as pd
from flask import current_app
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import davies_bouldin_score, silhouette_score

from ..models import Troubleshoot, ClusterHistory, db
from ..models.troubleshoot import JenisTroubleEnum, PerangkatEnum, KategoriClusterEnum


class ClusteringService:
    def __init__(self):
        self.feature_columns = [
            "durasi_pengerjaan",
            "jenis_human",
            "jenis_configuration_issue",
            "jenis_hardware_failure",
            "jenis_software_issue",
            "jenis_network_issue",
            "perangkat_pc",
            "perangkat_laptop",
            "perangkat_printer",
            "perangkat_server",
            "perangkat_firewall",
            "perangkat_switch",
            "perangkat_router",
            "perangkat_accesspoint",
        ]

    def _load_data(self):
        rows = Troubleshoot.query.all()
        if not rows:
            return pd.DataFrame()

        data = []
        for item in rows:
            row = {
                "id": item.id,
                "durasi_pengerjaan": item.durasi_pengerjaan or 0,
                "jenis_human": int(item.jenis_trouble == JenisTroubleEnum.Human),
                "jenis_configuration_issue": int(item.jenis_trouble == JenisTroubleEnum.Configuration_Issue),
                "jenis_hardware_failure": int(item.jenis_trouble == JenisTroubleEnum.Hardware_Failure),
                "jenis_software_issue": int(item.jenis_trouble == JenisTroubleEnum.Software_Issue),
                "jenis_network_issue": int(item.jenis_trouble == JenisTroubleEnum.Network_Issue),
                "perangkat_pc": int(item.perangkat == PerangkatEnum.PC),
                "perangkat_laptop": int(item.perangkat == PerangkatEnum.Laptop),
                "perangkat_printer": int(item.perangkat == PerangkatEnum.Printer),
                "perangkat_server": int(item.perangkat == PerangkatEnum.Server),
                "perangkat_firewall": int(item.perangkat == PerangkatEnum.Firewall),
                "perangkat_switch": int(item.perangkat == PerangkatEnum.Switch),
                "perangkat_router": int(item.perangkat == PerangkatEnum.Router),
                "perangkat_accesspoint": int(item.perangkat == PerangkatEnum.Accesspoint),
                "cluster_id": item.cluster_id,
                "kategori_cluster": item.kategori_cluster.value if item.kategori_cluster else None,
                "jenis_trouble_value": item.jenis_trouble.value,
                "perangkat_value": item.perangkat.value,
                "durasi_value": item.durasi_pengerjaan or 0,
            }
            data.append(row)

        return pd.DataFrame(data)

    def _prepare_features(self, df):
        return df[self.feature_columns].astype(float)

    def _get_cache_folder(self):
        cache_folder = current_app.config.get(
            "CLUSTERING_CACHE_FOLDER",
            os.path.join(os.path.dirname(__file__), "..", "cache"),
        )
        cache_folder = os.path.abspath(cache_folder)
        os.makedirs(cache_folder, exist_ok=True)
        return cache_folder

    def _get_cache_path(self):
        return os.path.join(self._get_cache_folder(), "clustering_state.pkl")

    def _save_clustering_artifacts(self, scaler, pca):
        with open(self._get_cache_path(), "wb") as f:
            pickle.dump({
                "scaler": scaler,
                "pca": pca,
                "feature_columns": self.feature_columns,
            }, f)

    def _load_clustering_artifacts(self):
        cache_path = self._get_cache_path()
        if not os.path.exists(cache_path):
            return None
        with open(cache_path, "rb") as f:
            data = pickle.load(f)
        if data.get("feature_columns") != self.feature_columns:
            return None
        return data

    def run_clustering(self, selected_k=3):
        df = self._load_data()
        if df.empty or len(df) < 2:
            raise ValueError("Data terlalu sedikit untuk clustering")

        if selected_k != 4:
            raise ValueError(
                "Kategori Ringan/Sedang/Berat/Sangat Berat hanya didukung untuk k=4. "
                "Gunakan selected_k=4 atau sesuaikan skema label untuk k lain."
            )

        features = self._prepare_features(df)
        scaler = StandardScaler()
        X = scaler.fit_transform(features)

        kmeans = KMeans(n_clusters=selected_k, random_state=42, n_init=20)
        labels = kmeans.fit_predict(X)

        dbi = davies_bouldin_score(X, labels)
        silhouette = silhouette_score(X, labels)

        df["cluster_id"] = labels + 1
        cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
        pca = PCA(n_components=2)
        pca.fit(X)

        # ------------------------------------------------------------
        # Hitung rata-rata durasi tiap cluster
        # ------------------------------------------------------------
        cluster_avg = []
        for cluster_idx in range(selected_k):
            cluster_mask = df["cluster_id"] == cluster_idx + 1
            cluster_durations = df[cluster_mask]["durasi_value"]
            avg_duration = cluster_durations.mean() if len(cluster_durations) > 0 else 0
            cluster_avg.append({"cluster": cluster_idx + 1, "avg_duration": avg_duration})

        # ------------------------------------------------------------
        # Urutkan cluster dari durasi terendah -> tertinggi, lalu beri
        # label RELATIF terhadap hasil clustering saat ini (bukan
        # threshold angka mutlak yang bisa jadi tidak relevan kalau
        # distribusi data berubah)
        # ------------------------------------------------------------
        cluster_avg_sorted = sorted(cluster_avg, key=lambda x: x["avg_duration"])
        label_urutan = ["Ringan", "Sedang", "Berat", "Sangat Berat"]

        cluster_info = []
        for rank, item in enumerate(cluster_avg_sorted):
            cluster_info.append({
                "cluster": item["cluster"],
                "avg_duration": round(item["avg_duration"], 2),
                "kategori": label_urutan[rank],
            })

        distribution = []
        for cluster_idx in range(selected_k):
            count = int((df["cluster_id"] == cluster_idx + 1).sum())
            kategori = next((c["kategori"] for c in cluster_info if c["cluster"] == cluster_idx + 1), "")
            distribution.append({"cluster": cluster_idx + 1, "count": count, "kategori": kategori})

        try:
            updates = []
            for _, row in df.iterrows():
                updates.append({
                    "id": int(row["id"]),
                    "cluster_id": int(row["cluster_id"]),
                    "kategori_cluster": KategoriClusterEnum(
                        next(c["kategori"] for c in cluster_info if c["cluster"] == int(row["cluster_id"]))
                    ),
                })

            db.session.bulk_update_mappings(Troubleshoot, updates)

            history = ClusterHistory(
                jumlah_cluster=selected_k,
                dbi_score=round(dbi, 4),
                silhouette_score=round(silhouette, 4),
            )
            db.session.add(history)
            self._save_clustering_artifacts(scaler, pca)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

        return {
            "k": selected_k,
            "dbi": round(dbi, 4),
            "silhouette": round(silhouette, 4),
            "distribution": distribution,
            "centroids": cluster_info,
        }

    def get_elbow_data(self):
        df = self._load_data()
        if df.empty or len(df) < 2:
            return []

        features = self._prepare_features(df)
        scaler = StandardScaler()
        X = scaler.fit_transform(features)

        results = []
        for k in range(2, 10):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=20)
            labels = kmeans.fit_predict(X)
            wcss = float(kmeans.inertia_)
            dbi = float(davies_bouldin_score(X, labels))
            results.append({"k": k, "wcss": round(wcss, 4), "dbi": round(dbi, 4)})

        return results

    def get_pca_data(self):
        df = self._load_data()
        if df.empty or len(df) < 2 or df["cluster_id"].isnull().all():
            return []

        features = self._prepare_features(df)
        artifacts = self._load_clustering_artifacts()
        if artifacts is not None:
            scaler = artifacts["scaler"]
            pca = artifacts["pca"]
            X = scaler.transform(features)
            components = pca.transform(X)
        else:
            scaler = StandardScaler()
            X = scaler.fit_transform(features)
            pca = PCA(n_components=2)
            components = pca.fit_transform(X)

        output = []
        for i, row in enumerate(df.itertuples(index=False)):
            output.append({
                "pc1": round(float(components[i][0]), 4),
                "pc2": round(float(components[i][1]), 4),
                "cluster": int(row.cluster_id),
                "kategori": row.kategori_cluster,
                "jenis_trouble": row.jenis_trouble_value,
                "perangkat": row.perangkat_value,
                "durasi": int(row.durasi_value),
            })

        return output
