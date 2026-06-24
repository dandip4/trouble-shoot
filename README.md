# Troubleshoot App

Aplikasi manajemen troubleshoot berbasis Flask.

## Menjalankan Aplikasi
1. Pastikan Python 3.11+ sudah terpasang.
2. Buat virtual environment:
   ```bash
   python -m venv venv
   ```
3. Aktifkan virtual environment:
   - Windows PowerShell:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Command Prompt:
     ```cmd
     .\venv\Scripts\activate
     ```
4. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```
5. Jalankan aplikasi:
   ```bash
   py run.py
   ```
6. Buka browser di:
   ```text
   http://127.0.0.1:5000
   ```

## Checklist Testing
- [ ] Login dengan ketiga role berbeda
- [ ] Teknisi tidak bisa akses menu admin
- [ ] Upload Excel dan verifikasi data masuk DB
- [ ] Jalankan clustering dan cek hasil di dashboard
- [ ] Export laporan Excel berisi 3 sheet
- [ ] Nonaktifkan user dan pastikan tidak bisa login
