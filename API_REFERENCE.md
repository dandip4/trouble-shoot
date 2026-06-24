# 🔌 API Reference & Integration Guide

## API Endpoints Documentation

### Base URL
```
http://127.0.0.1:5000
```

### Response Format
Semua API endpoint menggunakan format JSON untuk data responses.

**Standar Success Response**:
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

**Standar Error Response**:
```json
{
  "success": false,
  "message": "Error description",
  "errors": [ ... ]
}
```

---

## 🔐 Authentication Endpoints

### 1. Register User
```http
POST /auth/register
Content-Type: application/x-www-form-urlencoded

username=newuser&email=user@example.com&password=pass123&password_confirm=pass123
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Registration successful, please login"
}
```

**Response (400 Bad Request)**:
```json
{
  "success": false,
  "message": "Username already exists",
  "errors": ["username"]
}
```

### 2. Login User
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123&remember=on
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin",
    "email": "admin@troubleshoot.com"
  }
}
```

**Response (401 Unauthorized)**:
```json
{
  "success": false,
  "message": "Invalid username or password"
}
```

### 3. Logout
```http
GET /auth/logout
```

**Response (302 Redirect to Login)**:
```
Redirects to /auth/login
```

---

## 📊 Troubleshoot Endpoints

### 1. Get Troubleshoot List (Paginated)
```http
GET /troubleshoot/?page=1&search=&kategori=
```

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| page | int | 1 | Page number |
| search | string | "" | Search by customer name, type, device |
| kategori | string | "" | Filter by category (Ringan/Sedang/Berat) |

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": 1,
        "no_spk": "SPK-20260326-3769",
        "nama_pelanggan": "PT Sejahtera Mitra",
        "jenis_trouble": "Software Issue",
        "perangkat": "Router",
        "durasi_pengerjaan": 7,
        "kategori_cluster": "Sedang",
        "assigned_to": "teknisi1",
        "status": "In Progress",
        "created_at": "2026-03-26T10:30:00"
      }
    ],
    "total": 142,
    "pages": 10,
    "current_page": 1
  }
}
```

### 2. Create Troubleshoot
```http
POST /troubleshoot/tambah
Content-Type: application/x-www-form-urlencoded

no_spk=SPK-999&pelanggan_id=1&perangkat_id=2&
informasi_trouble=Network+down&jenis_trouble=Network+Issue&
perangkat_tipe=Server&service=DOWN&tanggal_komplain=2026-06-24&
durasi_pengerjaan=3&keterangan_action=Restart+device
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Troubleshoot created successfully",
  "data": {
    "id": 143,
    "no_spk": "SPK-999"
  }
}
```

**Response (400 Bad Request)**:
```json
{
  "success": false,
  "message": "SPK already exists",
  "errors": ["no_spk"]
}
```

### 3. Get Troubleshoot Detail
```http
GET /troubleshoot/edit/<id>
```

**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "no_spk": "SPK-20260326-3769",
    "nama_pelanggan": "PT Sejahtera Mitra",
    "informasi_trouble": "Network not responding",
    "jenis_trouble": "Software Issue",
    "perangkat": "Router",
    "durasi_pengerjaan": 7,
    "status": "In Progress",
    "created_by": 1,
    "assigned_to": null
  }
}
```

### 4. Update Troubleshoot
```http
POST /troubleshoot/edit/<id>
Content-Type: application/x-www-form-urlencoded

informasi_trouble=Network+fixed&status=Completed&durasi_pengerjaan=5
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Troubleshoot updated successfully"
}
```

### 5. Delete Troubleshoot
```http
POST /troubleshoot/delete/<id>
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Troubleshoot deleted successfully"
}
```

### 6. Assign Troubleshoot
```http
POST /troubleshoot/assign/<id>
Content-Type: application/x-www-form-urlencoded

assigned_to=2
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Troubleshoot assigned successfully to teknisi1"
}
```

### 7. Update Status
```http
POST /troubleshoot/update-status/<id>
Content-Type: application/x-www-form-urlencoded

status=Completed&selesai_pengerjaan=2026-06-24&durasi_pengerjaan=5
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Status updated successfully"
}
```

### 8. Export Troubleshoot to Excel
```http
GET /troubleshoot/export
```

**Response (200 OK)**:
```
File download: troubleshoot_export_YYYY-MM-DD.xlsx
```

---

## 📤 Upload Endpoints

### 1. Upload Excel File
```http
POST /troubleshoot/upload
Content-Type: multipart/form-data

file=<binary_excel_file>
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "File uploaded and processed successfully",
  "data": {
    "total_rows": 50,
    "imported": 48,
    "errors": 2,
    "error_details": [
      {
        "row": 5,
        "error": "Duplicate no_spk: SPK-001"
      }
    ]
  }
}
```

**Response (400 Bad Request)**:
```json
{
  "success": false,
  "message": "Invalid file format. Only .xlsx allowed"
}
```

---

## 🎯 Clustering Endpoints

### 1. Get Clustering Page
```http
GET /clustering/
```

**Response (200 OK)**:
```html
HTML page dengan elbow chart dan form
```

### 2. Get Elbow Data (JSON)
```http
GET /clustering/elbow-data
```

**Response (200 OK)**:
```json
[
  {
    "k": 2,
    "wcss": 1792.814,
    "dbi": 2.9631
  },
  {
    "k": 3,
    "wcss": 1600.0006,
    "dbi": 2.2631
  },
  ...
]
```

### 3. Run K-Means Clustering
```http
POST /clustering/run
Content-Type: application/x-www-form-urlencoded
Authorization: Admin only

k=3
```

**Response (200 OK)**:
```json
{
  "success": true,
  "result": {
    "k": 3,
    "dbi": 2.2631,
    "silhouette": 0.4523,
    "distribution": [
      {
        "cluster": 1,
        "count": 45,
        "kategori": "Ringan"
      },
      {
        "cluster": 2,
        "count": 52,
        "kategori": "Sedang"
      },
      {
        "cluster": 3,
        "count": 45,
        "kategori": "Berat"
      }
    ]
  },
  "last_history": {
    "tanggal": "2026-06-24 10:30:00",
    "k": 3,
    "dbi": 2.2631,
    "silhouette": 0.4523
  }
}
```

**Response (403 Forbidden)**:
```json
{
  "success": false,
  "message": "Only admin can run clustering"
}
```

**Response (400 Bad Request)**:
```json
{
  "success": false,
  "message": "Data too small for clustering (minimum 10 rows required)"
}
```

### 4. Get PCA Data
```http
GET /clustering/pca-data
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "cluster": 1,
    "pc1": -2.345,
    "pc2": 1.234,
    "jenis_trouble": "Hardware Failure",
    "perangkat": "Server",
    "durasi": 5
  },
  ...
]
```

---

## 📋 Dashboard Endpoints

### 1. Get Dashboard Data
```http
GET /dashboard
```

**Response (200 OK)**:
```json
{
  "total_troubleshoot": 142,
  "pending_count": 45,
  "in_progress_count": 52,
  "completed_count": 45,
  "distribution": {
    "Pending": 45,
    "In Progress": 52,
    "Completed": 45
  },
  "kategori_distribution": {
    "Ringan": 40,
    "Sedang": 60,
    "Berat": 42
  },
  "recent_activities": [...]
}
```

---

## 📊 Report Endpoints

### 1. Export All to Excel
```http
POST /laporan/export-all
```

**Response (200 OK)**:
```
File download: report_YYYY-MM-DD.xlsx (3 sheets)
```

### 2. Get Cluster History
```http
GET /laporan/riwayat-cluster
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "jumlah_cluster": 3,
    "dbi_score": 2.2631,
    "silhouette_score": 0.4523,
    "tanggal_clustering": "2026-06-24 10:30:00"
  }
]
```

---

## 👥 User Management Endpoints

### 1. Get User List
```http
GET /admin/users
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@troubleshoot.com",
    "role": "admin",
    "is_active": true,
    "created_at": "2026-01-01T00:00:00"
  },
  ...
]
```

### 2. Create User
```http
POST /admin/users/tambah
Content-Type: application/x-www-form-urlencoded
Authorization: Admin only

username=newuser&email=newuser@example.com&password=pass123&role=teknisi
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "User created successfully"
}
```

### 3. Update User
```http
POST /admin/users/edit/<id>
Content-Type: application/x-www-form-urlencoded
Authorization: Admin only

email=newemail@example.com&is_active=true
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "User updated successfully"
}
```

### 4. Delete User
```http
POST /admin/users/delete/<id>
Authorization: Admin only
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

---

## 🏢 Customer Management Endpoints

### 1. Get Customer List
```http
GET /pelanggan/
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "nama": "PT Maju Jaya",
    "kontak": "081234567890",
    "email": "info@majujaya.com",
    "lokasi": "Jakarta Selatan",
    "departemen": "IT Department",
    "created_at": "2026-01-01T00:00:00"
  }
]
```

### 2. Create Customer
```http
POST /pelanggan/tambah
Content-Type: application/x-www-form-urlencoded

nama=PT+NewCompany&kontak=081234567890&email=info@newcompany.com&
lokasi=Jakarta&departemen=IT&alamat=Jl.+Sudirman+No.123
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Customer created successfully"
}
```

### 3. Get Customer Detail
```http
GET /pelanggan/edit/<id>
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "nama": "PT Maju Jaya",
  "kontak": "081234567890",
  "email": "info@majujaya.com",
  "lokasi": "Jakarta Selatan",
  "departemen": "IT Department",
  "alamat": "Jl. Sudirman No.123"
}
```

### 4. Update Customer
```http
POST /pelanggan/edit/<id>
Content-Type: application/x-www-form-urlencoded

nama=PT+UpdatedName&lokasi=Jakarta+Pusat
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Customer updated successfully"
}
```

### 5. Delete Customer
```http
POST /pelanggan/delete/<id>
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Customer deleted successfully"
}
```

---

## 🖥️ Device Management Endpoints

### 1. Get Device List
```http
GET /pelanggan/perangkat
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "nama": "Server Main",
    "tipe": "Server",
    "deskripsi": "Main database server",
    "pelanggan_id": 1,
    "created_at": "2026-01-01T00:00:00"
  }
]
```

### 2. Create Device
```http
POST /pelanggan/perangkat/tambah
Content-Type: application/x-www-form-urlencoded

nama=New+Device&tipe=PC&deskripsi=Office+PC&pelanggan_id=1
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Device created successfully"
}
```

### 3. Update Device
```http
POST /pelanggan/perangkat/edit/<id>
Content-Type: application/x-www-form-urlencoded

nama=Updated+Device+Name&tipe=Server
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Device updated successfully"
}
```

### 4. Delete Device
```http
POST /pelanggan/perangkat/delete/<id>
```

**Response (200 OK)**:
```json
{
  "success": true,
  "message": "Device deleted successfully"
}
```

---

## 🔗 Integration Examples

### JavaScript Fetch Example
```javascript
// Get troubleshoot list
fetch('/troubleshoot/')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// Create new troubleshoot
const formData = new FormData();
formData.append('no_spk', 'SPK-999');
formData.append('pelanggan_id', '1');
formData.append('informasi_trouble', 'Network issue');

fetch('/troubleshoot/tambah', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

### Python Requests Example
```python
import requests

BASE_URL = 'http://127.0.0.1:5000'

# Login
session = requests.Session()
response = session.post(f'{BASE_URL}/auth/login', data={
    'username': 'admin',
    'password': 'admin123'
})

# Get troubleshoot list
response = session.get(f'{BASE_URL}/troubleshoot/?page=1')
data = response.json()
print(data)

# Create troubleshoot
response = session.post(f'{BASE_URL}/troubleshoot/tambah', data={
    'no_spk': 'SPK-999',
    'pelanggan_id': '1',
    'informasi_trouble': 'Network issue'
})
```

### cURL Examples
```bash
# Login
curl -X POST http://127.0.0.1:5000/auth/login \
  -d "username=admin&password=admin123"

# Get troubleshoot list
curl http://127.0.0.1:5000/troubleshoot/?page=1

# Run clustering
curl -X POST http://127.0.0.1:5000/clustering/run \
  -d "k=3"

# Upload file
curl -X POST http://127.0.0.1:5000/troubleshoot/upload \
  -F "file=@data.xlsx"
```

---

## ⚠️ Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid input data |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Permission denied / insufficient role |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Duplicate data (e.g., duplicate SPK) |
| 422 | Unprocessable Entity | Validation error |
| 500 | Server Error | Internal server error |

---

## 📝 Rate Limiting
Saat ini tidak ada rate limiting. Dalam production, pertimbangkan:
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: current_user.id)

@app.route('/troubleshoot/run', methods=['POST'])
@limiter.limit("5 per minute")
def run_clustering():
    pass
```

---

## 🔒 Security Notes

1. **CSRF Protection** - Semua POST request harus include CSRF token (otomatis dalam form)
2. **SQL Injection** - Menggunakan SQLAlchemy ORM (safe)
3. **Password Hashing** - Menggunakan werkzeug.security generate_password_hash
4. **Session Management** - Flask-Login menangani session
5. **HTTPS** - Dalam production, gunakan HTTPS
6. **Secrets** - Store SECRET_KEY di environment variable, jangan di code

---

End of API Documentation
