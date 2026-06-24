# 📋 Dokumentasi Aplikasi Troubleshoot Manajemen Jaringan

## 📑 Daftar Isi
1. [Pengenalan Project](#pengenalan-project)
2. [Setup & Instalasi](#setup--instalasi)
3. [Struktur Project](#struktur-project)
4. [Database Schema](#database-schema)
5. [Fitur-Fitur Utama](#fitur-fitur-utama)
6. [Sistem User & Role](#sistem-user--role)
7. [API Routes](#api-routes)
8. [Panduan Penggunaan](#panduan-penggunaan)
9. [Troubleshooting](#troubleshooting)
10. [Informasi Developer](#informasi-developer)

---

## 🎯 Pengenalan Project

### Overview
**Troubleshoot App** adalah aplikasi web berbasis Flask untuk manajemen dan analisis data troubleshoot jaringan. Aplikasi ini memungkinkan pengguna untuk mencatat masalah jaringan, menganalisis pola menggunakan K-Means clustering, dan menghasilkan laporan otomatis.

### Fitur Utama
- ✅ **Manajemen Data Troubleshoot** - Tambah, edit, hapus, dan cari data troubleshoot
- ✅ **Upload Excel Massal** - Import data troubleshoot dari file Excel
- ✅ **K-Means Clustering** - Analisis otomatis kategori troubleshoot (Ringan/Sedang/Berat)
- ✅ **Dashboard Analytics** - Visualisasi data dengan grafik dan statistik
- ✅ **Export Laporan** - Export hasil analisis ke format Excel (3 sheet)
- ✅ **Sistem User & Role** - 3 level akses (Admin, Teknisi, Manajer)
- ✅ **Manajemen Pelanggan & Perangkat** - CRUD untuk data master
- ✅ **Assign Troubleshoot** - Assign task ke teknisi dengan tracking status

### Tech Stack
- **Backend**: Flask 3.0.0
- **Database**: SQLite
- **Frontend**: Bootstrap 5, Chart.js
- **ML/Analytics**: scikit-learn, pandas, numpy
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Excel**: openpyxl

### Requirements
- Python 3.11+
- pip (Python package manager)
- 500MB disk space minimum

---

## 🚀 Setup & Instalasi

### Step 1: Clone/Download Project
```bash
cd d:\izal\troubleshootapp
```

### Step 2: Buat Virtual Environment
```bash
python -m venv .venv
```

### Step 3: Aktifkan Virtual Environment
**Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
.\.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Setup Database (Opsional)
Database akan otomatis dibuat saat pertama kali aplikasi dijalankan. Untuk seed data dummy:
```bash
python seed_dummy_data.py
```

### Step 6: Jalankan Aplikasi
```bash
python run.py
```

### Step 7: Akses di Browser
```
http://127.0.0.1:5000
```

### Credentials Default (Jika Seed Data)
| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| teknisi1 | teknisi123 | Teknisi |
| manajer1 | manajer123 | Manajer |

---

## 📁 Struktur Project

```
troubleshootapp/
├── app/                              # Main application package
│   ├── __init__.py                   # App initialization & blueprints
│   ├── config.py                     # Konfigurasi aplikasi
│   ├── forms.py                      # WTF Forms definitions
│   ├── utils.py                      # Helper functions
│   ├── cache/                        # Clustering cache folder
│   │   └── clustering_state.pkl      # Clustering artifacts (scaler, PCA)
│   ├── models/                       # Database models
│   │   ├── __init__.py
│   │   ├── user.py                   # User model & RoleEnum
│   │   ├── pelanggan.py              # Customer model
│   │   ├── perangkat.py              # Device model
│   │   ├── troubleshoot.py           # Troubleshoot model & enums
│   │   └── cluster_history.py        # Clustering history model
│   ├── routes/                       # Flask blueprints
│   │   ├── auth.py                   # Login/Register routes
│   │   ├── dashboard.py              # Dashboard analytics
│   │   ├── troubleshoot.py           # Troubleshoot CRUD
│   │   ├── clustering.py             # Clustering analysis
│   │   ├── laporan.py                # Report generation
│   │   ├── admin.py                  # User management
│   │   └── pelanggan.py              # Customer management
│   ├── services/                     # Business logic
│   │   ├── clustering_service.py     # K-Means clustering logic
│   │   └── export_service.py         # Excel export logic
│   ├── static/                       # Static files
│   │   ├── css/style.css             # Custom styles
│   │   └── js/main.js                # JavaScript utilities
│   └── templates/                    # HTML templates
│       ├── base.html                 # Base layout
│       ├── layout.html               # Sidebar layout
│       ├── auth/                     # Login/Register pages
│       ├── dashboard/                # Dashboard pages
│       ├── troubleshoot/             # Troubleshoot pages
│       ├── clustering/               # Clustering analysis page
│       ├── laporan/                  # Report pages
│       ├── pelanggan/                # Customer pages
│       ├── admin/                    # Admin pages
│       ├── errors/                   # Error pages (403, 404)
│       └── errors/
├── instance/                         # Instance folder
│   └── troubleshoot.db               # SQLite database file
├── uploads/                          # Uploaded file storage
├── run.py                            # Application entry point
├── requirements.txt                  # Dependencies
├── seed_dummy_data.py                # Seed database with sample data
├── README.md                         # Quick start guide
├── DOKUMENTASI.md                    # This documentation
└── troubleshoot.db                   # SQLite database (backup/main)
```

---

## 🗄️ Database Schema

### Model: User
```python
Columns:
  - id (PK)
  - username (UNIQUE)
  - email (UNIQUE)
  - password_hash
  - role (Enum: admin, teknisi, manajer)
  - is_active (Boolean)
  - created_at (DateTime)
```

### Model: Pelanggan (Customer)
```python
Columns:
  - id (PK)
  - nama (UNIQUE)
  - kontak (Phone)
  - email
  - lokasi (Location)
  - departemen (Department)
  - alamat (Address)
  - created_at, updated_at
Relations:
  - has_many Perangkat
  - has_many Troubleshoot
```

### Model: Perangkat (Device)
```python
Columns:
  - id (PK)
  - nama
  - tipe (Enum)
  - deskripsi
  - pelanggan_id (FK)
  - created_at, updated_at
Relations:
  - belongs_to Pelanggan
  - has_many Troubleshoot
```

### Model: Troubleshoot
```python
Columns:
  - id (PK)
  - no_spk (UNIQUE) - Service ticket number
  - nama_pelanggan
  - informasi_trouble (Text)
  - jenis_trouble (Enum: Human, Configuration Issue, Hardware Failure, Software Issue, Network Issue)
  - perangkat (Enum: PC, Laptop, Printer, Server, Firewall, Switch, Router, Accesspoint)
  - service (Enum: UP, DOWN)
  - tanggal_komplain (DateTime)
  - selesai_pengerjaan (DateTime, nullable)
  - durasi_pengerjaan (Integer - days)
  - keterangan_action (Text, nullable)
  - status (Enum: Pending, In Progress, Completed)
  - kategori_cluster (Enum: Ringan, Sedang, Berat)
  - cluster_id (Integer)
  - assigned_to (FK: User.id, nullable)
  - pelanggan_id (FK: Pelanggan.id, nullable)
  - perangkat_id (FK: Perangkat.id, nullable)
  - created_by (FK: User.id)
  - created_at, updated_at
Relations:
  - belongs_to Pelanggan
  - belongs_to Perangkat
  - belongs_to User (creator)
  - belongs_to User (assigned_to - teknisi)
```

### Model: ClusterHistory
```python
Columns:
  - id (PK)
  - jumlah_cluster (K value)
  - dbi_score (Davies-Bouldin Index)
  - silhouette_score (Silhouette coefficient)
  - tanggal_clustering (DateTime)
  - results (JSON - optional)
```

---

## ✨ Fitur-Fitur Utama

### 1. Manajemen Data Troubleshoot
**Lokasi**: `/troubleshoot/`

**Fitur**:
- 📝 **Tambah Data** - Form input untuk troubleshoot baru
- 📋 **List Data** - Tabel dengan pagination (15 data/halaman)
- 🔍 **Search** - Cari berdasarkan nama, jenis, perangkat
- ✏️ **Edit** - Edit data troubleshoot
- 🗑️ **Hapus** - Soft delete atau hard delete
- 👤 **Assign** - Assign ke teknisi
- 📊 **Status Update** - Update status progress

**Permission**:
- Admin: Full access semua data
- Teknisi: Hanya lihat/edit data yang di-assign ke mereka
- Manajer: Read-only semua data

### 2. Upload Excel Massal
**Lokasi**: `/troubleshoot/upload`

**Fitur**:
- 📁 **Upload File** - Select file Excel (.xlsx)
- ✔️ **Validasi** - Validasi struktur & data
- 📊 **Preview** - Lihat preview data sebelum import
- ⚡ **Bulk Insert** - Simpan semua data ke database

**Format Excel Required**:
| No SPK | Nama Pelanggan | Jenis Trouble | Perangkat | Durasi | Status |
|--------|---|---|---|---|---|
| SPK-001 | PT Maju Jaya | Hardware Failure | Server | 5 | Completed |

### 3. K-Means Clustering
**Lokasi**: `/clustering/`

**Fitur**:
- 📈 **Elbow Method** - Graph untuk menentukan K optimal
- 📊 **DBI Analysis** - Davies-Bouldin Index per K
- ⚙️ **Jalankan K-Means** - Eksekusi clustering dengan K pilihan
- 🎨 **PCA Visualization** - 2D visualization hasil clustering
- 💾 **Cluster History** - History hasil clustering sebelumnya

**Features Technical**:
- Preprocessing: Enum encoding + durasi normalisasi
- Scaler: StandardScaler
- Algorithm: K-Means dengan n_init=20
- Metrics: WCSS, Davies-Bouldin Index, Silhouette Score
- Kategori Assignment:
  - **Ringan**: avg_duration ≤ 2 hari
  - **Sedang**: 2 < avg_duration ≤ 5 hari
  - **Berat**: avg_duration > 5 hari

**Permission**:
- Admin: Bisa jalankan clustering
- Teknisi/Manajer: Hanya view results

### 4. Dashboard Analytics
**Lokasi**: `/dashboard`

**Widgets**:
- 📊 Total Troubleshoot (Card)
- 🟢 Pending Tasks (Card)
- 🟡 In Progress Tasks (Card)
- 🟢 Completed Tasks (Card)
- 📈 Trend Chart (7 hari terakhir)
- 🥧 Status Distribution Pie Chart
- 📊 Kategori Distribution Bar Chart
- 📋 Recent Activities List
- 🔥 Top Issues (most frequent)

### 5. Export Laporan
**Lokasi**: `/laporan/`

**Output Format**: Excel (.xlsx) dengan 3 sheet

**Sheet 1: Summary**
- Total data
- Breakdown by status
- Breakdown by kategori
- Average duration per kategori
- Timestamp export

**Sheet 2: Riwayat Cluster**
- History dari semua clustering runs
- K value, DBI score, Silhouette score
- Tanggal clustering

**Sheet 3: Detail Data**
- Semua troubleshoot records dengan formatting:
  - Column A-N: Detail troubleshoot
  - Color coding: Status-based
  - Borders & freeze panes

### 6. Sistem User & Role
**Lokasi**: `/admin/users`

**Roles Available**:
| Role | Akses |
|------|-------|
| **Admin** | Full system access, manage users, run clustering, view all data |
| **Teknisi** | Assigned tasks only, update status, view own data |
| **Manajer** | Read-only all data, view reports, analytics |

**User Management**:
- ➕ Create user baru
- ✏️ Edit user info
- 🔑 Reset password
- 🚫 Deactivate/Activate user
- 🗑️ Delete user

### 7. Manajemen Pelanggan & Perangkat
**Pelanggan** (`/pelanggan/`):
- CRUD customer data
- Store: Nama, kontak, email, lokasi, departemen, alamat

**Perangkat** (`/pelanggan/perangkat`):
- CRUD device data per customer
- Tipe: PC, Laptop, Printer, Server, Firewall, Switch, Router, Access Point

---

## 👥 Sistem User & Role

### Authentication Flow
1. User login dengan username/password
2. Validasi terhadap database
3. Session stored dengan Flask-Login
4. Role-based access control di setiap route

### Permission Matrix
```
Route/Feature          | Admin | Teknisi | Manajer
-------------------------------------------------
Dashboard              | ✓     | ✓       | ✓
Troubleshoot List      | ✓*    | ✓*      | ✓*
  (*) Admin: all, Teknisi: assigned, Manajer: all-readonly
Troubleshoot Add       | ✓     | ✓       | ✗
Troubleshoot Edit      | ✓*    | ✓*      | ✗
Clustering Run         | ✓     | ✗       | ✗
Clustering View        | ✓     | ✓       | ✓
Laporan Export         | ✓     | ✓       | ✓
Admin Users            | ✓     | ✗       | ✗
Pelanggan CRUD         | ✓     | ✓       | ✗
Perangkat CRUD         | ✓     | ✓       | ✗
```

### Decorator untuk Role Protection
```python
from app.utils import role_required

@route.route('/admin')
@role_required(['admin'])  # Hanya admin
def admin_page():
    pass

@route.route('/report')
@role_required(['admin', 'manajer'])  # Admin atau Manajer
def report_page():
    pass
```

---

## 🛣️ API Routes

### Authentication
```
POST   /auth/register          - Register user baru
POST   /auth/login             - Login user
GET    /auth/logout            - Logout user
```

### Dashboard
```
GET    /dashboard              - Main dashboard analytics
```

### Troubleshoot Management
```
GET    /troubleshoot/          - List all troubleshoot (paginated)
GET    /troubleshoot/tambah    - Form add troubleshoot
POST   /troubleshoot/tambah    - Save troubleshoot
GET    /troubleshoot/edit/<id> - Form edit troubleshoot
POST   /troubleshoot/edit/<id> - Update troubleshoot
POST   /troubleshoot/delete/<id> - Delete troubleshoot

GET    /troubleshoot/upload    - Form upload Excel
POST   /troubleshoot/upload    - Process Excel upload

GET    /troubleshoot/assign/<id> - Form assign task
POST   /troubleshoot/assign/<id> - Process assignment

GET    /troubleshoot/update-status/<id> - Form update status
POST   /troubleshoot/update-status/<id> - Update status

GET    /troubleshoot/export    - Export to Excel
```

### Clustering
```
GET    /clustering/            - Clustering analysis page
POST   /clustering/run         - Execute clustering [ADMIN ONLY]
GET    /clustering/elbow-data  - JSON elbow method data
GET    /clustering/pca-data    - JSON PCA visualization data
```

### Laporan (Reports)
```
GET    /laporan/               - Report list
POST   /laporan/export-all     - Export all data to Excel
GET    /laporan/riwayat-cluster - Cluster history report
```

### Admin Management
```
GET    /admin/users            - User list
GET    /admin/users/tambah     - Form add user
POST   /admin/users/tambah     - Create user
GET    /admin/users/edit/<id>  - Form edit user
POST   /admin/users/edit/<id>  - Update user
POST   /admin/users/delete/<id> - Delete user
```

### Customer Management
```
GET    /pelanggan/             - Customer list
GET    /pelanggan/tambah       - Form add customer
POST   /pelanggan/tambah       - Create customer
GET    /pelanggan/edit/<id>    - Form edit customer
POST   /pelanggan/edit/<id>    - Update customer
POST   /pelanggan/delete/<id>  - Delete customer

GET    /pelanggan/perangkat              - Device list
GET    /pelanggan/perangkat/tambah       - Form add device
POST   /pelanggan/perangkat/tambah       - Create device
GET    /pelanggan/perangkat/edit/<id>    - Form edit device
POST   /pelanggan/perangkat/edit/<id>    - Update device
POST   /pelanggan/perangkat/delete/<id>  - Delete device
```

### Error Handlers
```
403    - Forbidden (permission denied)
404    - Not Found
500    - Internal Server Error
```

---

## 📖 Panduan Penggunaan

### Workflow 1: Input Data Troubleshoot

#### Option A: Manual Input
1. Login sebagai Admin/Teknisi
2. Ke menu **Data Troubleshoot** → **Tambah Troubleshoot**
3. Isi form:
   - No SPK: SPK-001 (auto-generate atau manual)
   - Pilih Pelanggan dari dropdown
   - Pilih Perangkat dari dropdown
   - Isi Informasi Trouble, Jenis Trouble, Service
   - Set Tanggal Komplain
   - Klik **Simpan**

#### Option B: Upload Excel Massal
1. Siapkan file Excel dengan struktur:
   ```
   No SPK | Nama Pelanggan | Jenis Trouble | Perangkat | Durasi | Status
   ```
2. Ke **Data Troubleshoot** → **Upload Excel**
3. Select file → **Upload**
4. Verifikasi preview data
5. Klik **Konfirmasi** untuk import

### Workflow 2: Jalankan Clustering

1. **Prerequisite**: Minimal 10 data troubleshoot di database
2. Login sebagai **Admin**
3. Ke menu **Clustering**
4. Tunggu Elbow Method chart & DBI table ter-load (±2 detik)
5. Pilih jumlah cluster K dari dropdown (default: 3)
6. Klik **Jalankan Clustering**
7. Tunggu proses (±3-5 detik) hingga hasil muncul:
   - Distribusi per cluster
   - PCA scatter plot
   - Interpretasi cluster
8. Data troubleshoot sudah ter-update dengan:
   - cluster_id
   - kategori_cluster (Ringan/Sedang/Berat)

### Workflow 3: Assign Task ke Teknisi

1. Ke **Data Troubleshoot**
2. Cari troubleshoot yang ingin di-assign
3. Klik **Assign**
4. Pilih teknisi dari dropdown
5. Klik **Assign**
6. Troubleshoot sekarang di-assign dan teknisi bisa lihat di dashboardnya

### Workflow 4: Generate Laporan

1. Login sebagai Admin/Manajer
2. Ke menu **Laporan**
3. Pilih type laporan:
   - **Export Excel** - Download all data + summary
   - **Laporan Cluster** - Export cluster history
4. File Excel akan ter-download dengan 3 sheet

### Workflow 5: Manage User (Admin Only)

1. Login sebagai **Admin**
2. Ke menu **Kelola User**
3. **Tambah User**:
   - Username (unique)
   - Email (unique)
   - Password (min. 6 char)
   - Pilih Role: Admin/Teknisi/Manajer
   - Klik **Simpan**
4. **Edit User**: Klik Edit, ubah data, simpan
5. **Delete User**: Klik Delete untuk hapus user

---

## 🐛 Troubleshooting

### Problem 1: "ModuleNotFoundError: No module named 'flask'"
**Solusi**:
```bash
# Pastikan virtual env sudah activate
pip install -r requirements.txt
```

### Problem 2: "Database Locked" atau Database Error
**Solusi**:
```bash
# Delete database yang corrupt
rm instance/troubleshoot.db

# Restart aplikasi (akan auto-create DB baru)
python run.py
```

### Problem 3: Port 5000 Already in Use
**Solusi**:
```bash
# Cari process yang menggunakan port 5000
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Atau gunakan port berbeda
# Edit run.py -> app.run(port=5001)
```

### Problem 4: Data Dummy Tidak Muncul di UI
**Solusi**:
1. Verifikasi database sudah ter-seed:
   ```bash
   python -c "from app import create_app; from app.models import Troubleshoot; app = create_app(); 
   with app.app_context(): print(Troubleshoot.query.count())"
   ```
2. Jika count = 0, jalankan:
   ```bash
   python seed_dummy_data.py
   ```
3. Verifikasi database file:
   - Main: `troubleshoot.db` (di root folder)
   - Instance: `instance/troubleshoot.db`
   - Pastikan kedua file ter-sync (copy dari main ke instance jika perlu)

### Problem 5: Clustering Elbow Chart Tidak Muncul
**Solusi**:
1. Refresh halaman (F5 beberapa kali)
2. Tunggu 2-3 detik setelah halaman load
3. Check browser console (F12 → Console) untuk error JavaScript
4. Pastikan data troubleshoot sudah ada (min. 10 rows)

### Problem 6: "Permission Denied" saat akses menu
**Solusi**:
1. Verifikasi login dengan role yang tepat
2. Check kembali permission matrix
3. Logout dan login ulang
4. Clear browser cache (Ctrl+Shift+Delete)

### Problem 7: Excel Upload Gagal
**Solusi**:
1. Verifikasi format file Excel (.xlsx, bukan .xls)
2. Pastikan struktur sheet sesuai:
   ```
   Row 1: Headers (No SPK, Nama Pelanggan, ...)
   Row 2+: Data
   ```
3. Cek ukuran file tidak lebih dari 10MB
4. Verifikasi encoding: UTF-8 recommended

### Problem 8: Chart.js Grafik Blank
**Solusi**:
```bash
# Clear cache & reload
# Browser → F5 (atau Ctrl+F5)

# Atau dalam file JavaScript:
# Tambahkan delay before chart render
setTimeout(() => { renderChart(); }, 500);
```

---

## 👨‍💻 Informasi Developer

### Environment Variables (Optional)
Buat file `.env` di root folder:
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///troubleshoot.db
UPLOAD_FOLDER=uploads
```

### Konfigurasi File
**config.py**:
```python
SQLALCHEMY_DATABASE_URI  # Database connection string
SQLALCHEMY_TRACK_MODIFICATIONS  # SQLAlchemy tracking
UPLOAD_FOLDER  # Upload file destination
SECRET_KEY  # Session encryption key
```

### Testing Database
```bash
# Test connection
python -c "from app import create_app; app = create_app(); 
print(app.config['SQLALCHEMY_DATABASE_URI'])"

# Query data
python -c "from app import create_app; from app.models import Troubleshoot; 
app = create_app(); 
with app.app_context(): print(Troubleshoot.query.count())"
```

### Development Mode
```bash
# Run with debug on
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py

# Or Windows:
set FLASK_ENV=development
set FLASK_DEBUG=1
python run.py
```

### Useful Commands
```bash
# Create database tables
python -c "from app import create_app; from app.models import db; app = create_app(); 
with app.app_context(): db.create_all()"

# Seed admin user
python -c "from app import create_app, seed_admin; app = create_app(); 
with app.app_context(): seed_admin()"

# Count troubleshoot records
python -c "from app import create_app; from app.models import Troubleshoot; 
app = create_app(); 
with app.app_context(): print(f'Total: {Troubleshoot.query.count()}')"

# Clear clustering cache
rm app/cache/clustering_state.pkl
```

### Debug dengan Flask Shell
```bash
python -m flask shell

# Di dalam shell:
>>> from app.models import Troubleshoot, User
>>> User.query.all()  # List semua user
>>> Troubleshoot.query.count()  # Count troubleshoot
>>> Troubleshoot.query.first()  # Ambil 1 record pertama
```

### Adding New Feature Checklist
- [ ] Create model (if needed) di `app/models/`
- [ ] Create form (if needed) di `app/forms.py`
- [ ] Create blueprint di `app/routes/`
- [ ] Create templates di `app/templates/`
- [ ] Register blueprint di `app/__init__.py`
- [ ] Add permissions di `utils.py` (if role-based)
- [ ] Test CRUD operations
- [ ] Update navigation menu
- [ ] Update documentation

### Common Code Patterns

**Database Query**:
```python
from app.models import Troubleshoot

# Get all
records = Troubleshoot.query.all()

# Get with filter
records = Troubleshoot.query.filter_by(status='Pending').all()

# Get with pagination
pagination = Troubleshoot.query.paginate(page=1, per_page=15)
records = pagination.items

# Get one
record = Troubleshoot.query.get(1)
record = Troubleshoot.query.filter_by(no_spk='SPK-001').first()
```

**Save to Database**:
```python
# Create
new_record = Troubleshoot(no_spk='SPK-999', nama_pelanggan='...')
db.session.add(new_record)
db.session.commit()

# Update
record = Troubleshoot.query.get(1)
record.status = 'Completed'
db.session.commit()

# Delete
db.session.delete(record)
db.session.commit()
```

**Role Check**:
```python
from flask_login import current_user

if current_user.role.value == 'admin':
    # Admin only
    pass

if current_user.role.value in ['admin', 'manajer']:
    # Admin or Manajer
    pass
```

**Flash Message**:
```python
from flask import flash

flash('Success message', 'success')  # Green
flash('Error message', 'danger')     # Red
flash('Info message', 'info')        # Blue
```

---

## 📞 Support & Kontribusi

### Issue Reporting
Jika menemukan bug, lapor dengan:
1. Deskripsi masalah
2. Steps to reproduce
3. Error message (dari console/terminal)
4. Browser/OS information

### File Untuk Diperhatikan
- **run.py** - Aplikasi entry point
- **app/__init__.py** - Blueprint registration
- **app/config.py** - Konfigurasi utama
- **seed_dummy_data.py** - Data seeding script
- **requirements.txt** - Dependencies list

---

## 📄 License & Notes

### Created By
Troubleshoot Management System v1.0

### Last Updated
2026-06-24

### Version History
- v1.0 - Initial release dengan fitur CRUD, Clustering, Laporan

---

## 📚 Referensi & Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://www.sqlalchemy.org/)
- [Scikit-learn Clustering](https://scikit-learn.org/stable/modules/clustering.html)
- [Chart.js Documentation](https://www.chartjs.org/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)

---

**End of Documentation**
