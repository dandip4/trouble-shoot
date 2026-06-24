document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss bootstrap alerts after 5 seconds.
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      bsAlert.close();
    }, 5000);
  });

  document.querySelectorAll('.btn-confirm-delete').forEach(function (button) {
    button.addEventListener('click', function (event) {
      if (!confirm('Yakin ingin melanjutkan aksi ini?')) {
        event.preventDefault();
      }
    });
  });
});
