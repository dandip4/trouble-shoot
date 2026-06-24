# ⚡ Quick Reference & Cheat Sheet

## 🎯 Quick Start (5 Minutes)

```bash
# 1. Setup environment
cd d:\izal\troubleshootapp
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run app
python run.py

# 4. Open browser
# http://127.0.0.1:5000

# 5. Login with test credentials
# Username: admin / Password: admin123
```

---

## 📚 Documentation Files Quick Links

| File | Purpose |
|------|---------|
| **DOKUMENTASI.md** | Complete documentation (Setup, Features, Usage) |
| **API_REFERENCE.md** | All API endpoints with examples |
| **DATABASE_SCHEMA.md** | Database structure and ERD |
| **DEPLOYMENT.md** | Production deployment guide |
| **README.md** | Original quick start |
| **requirements.txt** | Python dependencies |

---

## 🔑 Default Credentials

| User | Username | Password | Role |
|------|----------|----------|------|
| Admin | `admin` | `admin123` | Admin |
| Technician | `teknisi1` | `teknisi123` | Teknisi |
| Manager | `manajer1` | `manajer123` | Manajer |

---

## 🗺️ Navigation Map

```
Dashboard (/)
├── Data Troubleshoot (/troubleshoot/)
│   ├── Tambah (/troubleshoot/tambah)
│   ├── Upload Excel (/troubleshoot/upload)
│   ├── Export (/troubleshoot/export)
│   └── Edit/Assign/Delete
├── Clustering (/clustering/)
│   ├── Elbow Chart
│   ├── DBI Analysis
│   └── Run K-Means
├── Laporan (/laporan/)
│   ├── Export All
│   └── Cluster History
├── Kelola Pelanggan (/pelanggan/)
│   ├── List Customers
│   ├── Tambah Pelanggan
│   └── Edit/Delete
├── Kelola Perangkat (/pelanggan/perangkat)
│   ├── List Devices
│   ├── Tambah Perangkat
│   └── Edit/Delete
└── Kelola User (/admin/users) [Admin Only]
    ├── List Users
    ├── Tambah User
    └── Edit/Delete
```

---

## 🔐 Permission Quick Matrix

```
Route                    Admin  Teknisi  Manajer
────────────────────────────────────────────────
Dashboard               ✅     ✅       ✅
Troubleshoot List*      ✅     ✅*      ✅
Troubleshoot Add        ✅     ✅       ❌
Clustering View         ✅     ✅       ✅
Clustering Run          ✅     ❌       ❌
Laporan Export          ✅     ✅       ✅
Kelola User             ✅     ❌       ❌
Pelanggan CRUD          ✅     ✅       ❌
Perangkat CRUD          ✅     ✅       ❌

* = Admin: all | Teknisi: assigned only | Manajer: all readonly
```

---

## 🚀 Common Tasks

### 1️⃣ Add New Troubleshoot Record
```
1. Login as Admin/Teknisi
2. Click "Data Troubleshoot" → "Tambah Troubleshoot"
3. Fill form fields
4. Click "Simpan"
```

### 2️⃣ Upload Troubleshoot from Excel
```
1. Prepare Excel file (headers: No SPK, Nama Pelanggan, etc.)
2. Go to "Data Troubleshoot" → "Upload Excel"
3. Select file → Upload
4. Verify preview → Confirm
```

### 3️⃣ Run Clustering Analysis
```
1. Login as Admin
2. Go to "Clustering"
3. Select K value (e.g., 3)
4. Click "Jalankan Clustering"
5. Wait for results (3-5 seconds)
6. View cluster distribution & PCA chart
```

### 4️⃣ Assign Task to Technician
```
1. Go to "Data Troubleshoot"
2. Find record → Click "Assign"
3. Select technician from dropdown
4. Click "Assign"
5. Technician sees task in their dashboard
```

### 5️⃣ Export Report to Excel
```
1. Go to "Laporan"
2. Click "Export Excel"
3. Choose sheet type:
   - Summary (statistics)
   - Cluster History (previous runs)
   - Detail Data (all records)
4. File downloads automatically
```

### 6️⃣ Manage Users (Admin)
```
1. Go to "Kelola User"
2. Click "Tambah User"
3. Fill: Username, Email, Password, Role
4. Click "Simpan"
5. To edit: Click Edit → Change fields → Simpan
6. To delete: Click Delete → Confirm
```

### 7️⃣ Manage Customers
```
1. Go to "Kelola Pelanggan"
2. Add: Click "Tambah" → Fill form → Simpan
3. Edit: Click row → Modify → Simpan
4. Delete: Click Delete → Confirm
```

### 8️⃣ Manage Devices
```
1. Go to "Kelola Perangkat"
2. Add: Click "Tambah" → Select customer → Fill form
3. Edit: Click row → Modify → Simpan
4. Delete: Click Delete → Confirm
```

---

## 🐛 Common Issues & Quick Fixes

| Issue | Quick Fix |
|-------|-----------|
| Can't login | Check username/password, verify user is active |
| Permission denied | Login with admin account or check role permissions |
| Data not showing | Refresh page (F5), check database has data |
| Clustering chart blank | Wait 2-3 seconds for page load, refresh browser |
| Upload failing | Check file is .xlsx format, under 10MB |
| Port 5000 in use | `netstat -ano \| findstr :5000` then kill process |
| Database error | Delete DB file and restart (will recreate) |

---

## 💾 Database Commands

```bash
# Check database integrity
python -c "from app import create_app; from app.models import Troubleshoot; 
app = create_app(); 
with app.app_context(): print(f'Total: {Troubleshoot.query.count()}')"

# Seed test data
python seed_dummy_data.py

# Query examples (in Flask shell)
python -m flask shell
>>> from app.models import Troubleshoot, User
>>> User.query.all()  # List all users
>>> Troubleshoot.query.count()  # Count records
>>> Troubleshoot.query.filter_by(status='Pending').all()  # Filter
>>> exit()
```

---

## 📁 Key Files Reference

```
app/
├── __init__.py          # App init & blueprints
├── config.py            # Configuration
├── forms.py             # Form definitions
├── utils.py             # Helper functions
├── models/
│   ├── user.py          # User model
│   ├── troubleshoot.py  # Troubleshoot model
│   ├── pelanggan.py     # Customer model
│   └── perangkat.py     # Device model
├── routes/
│   ├── auth.py          # Login/Register
│   ├── troubleshoot.py  # CRUD routes
│   ├── clustering.py    # Clustering routes
│   └── laporan.py       # Report routes
├── services/
│   ├── clustering_service.py   # Clustering logic
│   └── export_service.py       # Excel export
└── templates/           # HTML templates

run.py                   # Application entry point
requirements.txt         # Dependencies
seed_dummy_data.py       # Test data seeding
DOKUMENTASI.md           # Full documentation
```

---

## 🔧 Configuration Quick Reference

### Environment Variables
```python
FLASK_ENV              # development or production
FLASK_DEBUG            # True/False for debug mode
SECRET_KEY             # Session encryption key
DATABASE_URL           # Database connection string
UPLOAD_FOLDER          # Directory for file uploads
```

### config.py Settings
```python
SQLALCHEMY_DATABASE_URI    # Database location
SQLALCHEMY_TRACK_MODIFICATIONS  # Default: False
MAX_CONTENT_LENGTH         # Max file size
UPLOAD_EXTENSIONS          # Allowed file types
```

---

## 🎨 Frontend Routing

### CSS Files
- `app/static/css/style.css` - Custom styles
- Bootstrap 5 (CDN)

### JavaScript Files
- `app/static/js/main.js` - Utilities
- Chart.js (CDN) - Charts
- jQuery (Bootstrap dependency)

### Template Structure
```html
base.html                    # Base layout
├── layout.html            # Main layout with sidebar
├── auth/
│   ├── login.html
│   └── register.html
├── dashboard/
│   └── index.html
├── troubleshoot/
│   ├── index.html         # List
│   ├── tambah.html        # Add
│   └── edit.html          # Edit
├── clustering/
│   └── index.html         # Analysis
└── errors/
    ├── 403.html
    └── 404.html
```

---

## 🔄 Common API Calls

```bash
# Get troubleshoot list
curl http://127.0.0.1:5000/troubleshoot/

# Get elbow data (JSON)
curl http://127.0.0.1:5000/clustering/elbow-data

# Run clustering (POST)
curl -X POST http://127.0.0.1:5000/clustering/run \
  -d "k=3"

# Export to Excel
curl http://127.0.0.1:5000/troubleshoot/export \
  -o troubleshoot_export.xlsx
```

---

## 📊 Database Quick Stats Query

```sql
-- Total records
SELECT COUNT(*) as total FROM troubleshoot;

-- By status
SELECT status, COUNT(*) as count 
FROM troubleshoot GROUP BY status;

-- By category
SELECT kategori_cluster, COUNT(*) as count 
FROM troubleshoot GROUP BY kategori_cluster;

-- By customer
SELECT nama_pelanggan, COUNT(*) as count 
FROM troubleshoot GROUP BY nama_pelanggan 
ORDER BY count DESC LIMIT 10;
```

---

## ⚙️ Troubleshooting Steps

### Application Won't Start
```bash
# Check Python version
python --version  # Should be 3.11+

# Check virtual env activated
pip list  # Should show installed packages

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Database Issues
```bash
# Check database exists
ls -la instance/troubleshoot.db

# Recreate if corrupted
rm instance/troubleshoot.db
python run.py  # Will auto-create new DB

# Restore from backup
cp backup/troubleshoot.db.20260624 instance/troubleshoot.db
```

### Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Or use different port
export FLASK_RUN_PORT=5001
python run.py
```

---

## 💡 Pro Tips

1. **Development Speed**:
   - Enable debug mode: `FLASK_DEBUG=1`
   - Use Flask shell for testing: `python -m flask shell`

2. **Database**:
   - Backup regularly: `cp instance/troubleshoot.db backup/`
   - Clean old files: `rm uploads/*.xlsx` (keep space)

3. **Security**:
   - Change default passwords immediately
   - Set strong SECRET_KEY in production
   - Use HTTPS in production

4. **Performance**:
   - Use pagination for large datasets
   - Cache frequently accessed data
   - Index commonly filtered columns

5. **Debugging**:
   - Check browser console (F12) for errors
   - Check Flask logs in terminal
   - Use Flask debugger for tracebacks

---

## 📞 Getting Help

### Documentation Files
- **Setup Issue?** → Read `DOKUMENTASI.md` → Setup & Instalasi
- **Feature Not Working?** → Check `DOKUMENTASI.md` → Panduan Penggunaan
- **API Question?** → Read `API_REFERENCE.md`
- **Database Question?** → Check `DATABASE_SCHEMA.md`
- **Deployment?** → Use `DEPLOYMENT.md`

### Common Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "No such table: troubleshoot" | DB not initialized | Restart app or recreate DB |
| "Unique constraint failed" | Duplicate data | Check SPK, username, email |
| "Permission denied" | Insufficient role | Login with admin account |
| "File not allowed" | Wrong file type | Upload .xlsx format only |
| "Database is locked" | Concurrent access | Restart application |

---

## 🎓 Learning Path

1. **Beginner**: Read README.md + DOKUMENTASI.md
2. **Intermediate**: Explore API_REFERENCE.md, try CRUD operations
3. **Advanced**: Study DATABASE_SCHEMA.md, modify code
4. **DevOps**: Review DEPLOYMENT.md for production setup

---

## 📋 Maintenance Checklist

### Daily
- [ ] Monitor error logs
- [ ] Check backup status

### Weekly
- [ ] Review database size
- [ ] Check system resources (CPU, memory, disk)

### Monthly
- [ ] Clean old logs
- [ ] Verify backup integrity
- [ ] Update dependencies: `pip list --outdated`

### Quarterly
- [ ] Security audit
- [ ] Performance tuning
- [ ] Database optimization

---

End of Quick Reference
