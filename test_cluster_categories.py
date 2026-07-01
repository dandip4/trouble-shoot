from app.models.troubleshoot import KategoriClusterEnum


def test_cluster_categories_include_four_levels():
    assert KategoriClusterEnum.Ringan.value == "Ringan"
    assert KategoriClusterEnum.Sedang.value == "Sedang"
    assert KategoriClusterEnum.Berat.value == "Berat"
    assert KategoriClusterEnum.Sangat_Berat.value == "Sangat Berat"
