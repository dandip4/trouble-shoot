# 🗄️ Database Schema & Data Model Documentation

## Database Overview

**Type**: SQLite  
**Location**: `instance/troubleshoot.db` (production) / `troubleshoot.db` (development)  
**ORM**: SQLAlchemy with Flask-SQLAlchemy

---

## 📊 Entity Relationship Diagram (ERD)

```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ username        │◄──────────────┐
│ email           │               │
│ password_hash   │               │
│ role            │               │
│ is_active       │               │
│ created_at      │               │
└─────────────────┘               │
          │                       │
          │ created_by (1:N)      │
          │                       │
          │                  ┌────┴────────────┐
          │                  │  Troubleshoot   │
          │ assigned_to (1:N)├─────────────────┤
          └──────────────────┤ id (PK)         │
                             │ no_spk          │
                             │ nama_pelanggan  │
                             │ durasi_pengerjaan
                             │ status          │
                             │ cluster_id      │
                             │ kategori_cluster│
                             │ created_by (FK) │
                             │ assigned_to (FK)│
                             │ pelanggan_id(FK)│
                             │ perangkat_id(FK)│
                             │ created_at      │
                             └────┬────────────┘
                                  │
                  ┌───────────────┼───────────────┐
                  │ (1:N)         │ (1:N)         │
                  │               │               │
        ┌─────────▼───────┐  ┌────▼───────────────┐
        │    Pelanggan    │  │    Perangkat       │
        ├─────────────────┤  ├────────────────────┤
        │ id (PK)         │  │ id (PK)            │
        │ nama (UNIQUE)   │  │ nama               │
        │ kontak          │  │ tipe (Enum)        │
        │ email           │  │ deskripsi          │
        │ lokasi          │  │ pelanggan_id (FK)  │
        │ departemen      │  │ created_at         │
        │ alamat          │  └────────────────────┘
        │ created_at      │
        │ updated_at      │
        └─────────────────┘

┌──────────────────────────┐
│    ClusterHistory        │
├──────────────────────────┤
│ id (PK)                  │
│ jumlah_cluster (K)       │
│ dbi_score                │
│ silhouette_score         │
│ tanggal_clustering       │
└──────────────────────────┘
```

---

## 📋 Detailed Table Schema

### 1. User Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(64) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    role ENUM('admin', 'teknisi', 'manajer') NOT NULL,
    is_active BOOLEAN DEFAULT True NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes
CREATE INDEX ix_user_username ON user(username);
CREATE INDEX ix_user_email ON user(email);
```

**Fields Description**:
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | INTEGER | PK, AUTO | Auto-incremented user ID |
| username | VARCHAR(64) | UNIQUE, NOT NULL | Username for login |
| email | VARCHAR(120) | UNIQUE, NOT NULL | Email address |
| password_hash | VARCHAR(256) | NOT NULL | Hashed password (werkzeug.security) |
| role | ENUM | NOT NULL | User role: admin/teknisi/manajer |
| is_active | BOOLEAN | DEFAULT True | User account status |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |

**Sample Data**:
```
id=1, username='admin', role='admin', is_active=True
id=2, username='teknisi1', role='teknisi', is_active=True
id=3, username='manajer1', role='manajer', is_active=True
```

---

### 2. Pelanggan Table (Customers)
```sql
CREATE TABLE pelanggan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama VARCHAR(150) UNIQUE NOT NULL,
    kontak VARCHAR(20) NOT NULL,
    email VARCHAR(120),
    lokasi VARCHAR(255) NOT NULL,
    departemen VARCHAR(100),
    alamat TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes
CREATE INDEX ix_pelanggan_nama ON pelanggan(nama);
CREATE INDEX ix_pelanggan_lokasi ON pelanggan(lokasi);
```

**Fields Description**:
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | INTEGER | PK, AUTO | Customer ID |
| nama | VARCHAR(150) | UNIQUE, NOT NULL | Company name |
| kontak | VARCHAR(20) | NOT NULL | Phone number |
| email | VARCHAR(120) | | Email address |
| lokasi | VARCHAR(255) | NOT NULL | City/Location |
| departemen | VARCHAR(100) | | Department/Division |
| alamat | TEXT | | Full address |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |
| updated_at | DATETIME | DEFAULT NOW | Last update timestamp |

**Sample Data**:
```
id=1, nama='PT Maju Jaya', kontak='081234567890', lokasi='Jakarta Selatan'
id=2, nama='PT Sejahtera Mitra', kontak='082345678901', lokasi='Jakarta Pusat'
...
```

---

### 3. Perangkat Table (Devices)
```sql
CREATE TABLE perangkat (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama VARCHAR(150) NOT NULL,
    tipe ENUM('PC', 'Laptop', 'Printer', 'Server', 'Firewall', 'Switch', 'Router', 'Accesspoint') NOT NULL,
    deskripsi TEXT,
    pelanggan_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY(pelanggan_id) REFERENCES pelanggan(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX ix_perangkat_pelanggan_id ON perangkat(pelanggan_id);
CREATE INDEX ix_perangkat_tipe ON perangkat(tipe);
```

**Fields Description**:
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | INTEGER | PK, AUTO | Device ID |
| nama | VARCHAR(150) | NOT NULL | Device name |
| tipe | ENUM | NOT NULL | Device type |
| deskripsi | TEXT | | Device description |
| pelanggan_id | INTEGER | FK NOT NULL | Related customer |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |
| updated_at | DATETIME | DEFAULT NOW | Last update timestamp |

**Enum Values for tipe**:
- PC
- Laptop
- Printer
- Server
- Firewall
- Switch
- Router
- Accesspoint

---

### 4. Troubleshoot Table (Main)
```sql
CREATE TABLE troubleshoot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    no_spk VARCHAR(80) UNIQUE NOT NULL,
    nama_pelanggan VARCHAR(150) NOT NULL,
    informasi_trouble TEXT NOT NULL,
    jenis_trouble ENUM('Human', 'Configuration Issue', 'Hardware Failure', 'Software Issue', 'Network Issue') NOT NULL,
    perangkat ENUM('PC', 'Laptop', 'Printer', 'Server', 'Firewall', 'Switch', 'Router', 'Accesspoint') NOT NULL,
    service ENUM('UP', 'DOWN') NOT NULL,
    tanggal_komplain DATETIME NOT NULL,
    selesai_pengerjaan DATETIME,
    durasi_pengerjaan INTEGER,
    keterangan_action TEXT,
    cluster_id INTEGER,
    kategori_cluster ENUM('Ringan', 'Sedang', 'Berat'),
    status ENUM('Pending', 'In Progress', 'Completed') DEFAULT 'Pending' NOT NULL,
    assigned_to INTEGER,
    pelanggan_id INTEGER,
    perangkat_id INTEGER,
    created_by INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    
    FOREIGN KEY(assigned_to) REFERENCES user(id),
    FOREIGN KEY(created_by) REFERENCES user(id),
    FOREIGN KEY(pelanggan_id) REFERENCES pelanggan(id),
    FOREIGN KEY(perangkat_id) REFERENCES perangkat(id)
);

-- Indexes
CREATE INDEX ix_troubleshoot_no_spk ON troubleshoot(no_spk);
CREATE INDEX ix_troubleshoot_status ON troubleshoot(status);
CREATE INDEX ix_troubleshoot_cluster_id ON troubleshoot(cluster_id);
CREATE INDEX ix_troubleshoot_created_by ON troubleshoot(created_by);
CREATE INDEX ix_troubleshoot_assigned_to ON troubleshoot(assigned_to);
CREATE INDEX ix_troubleshoot_created_at ON troubleshoot(created_at);
```

**Fields Description**:
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | INTEGER | PK, AUTO | Record ID |
| no_spk | VARCHAR(80) | UNIQUE, NOT NULL | Service ticket number |
| nama_pelanggan | VARCHAR(150) | NOT NULL | Customer name |
| informasi_trouble | TEXT | NOT NULL | Detailed issue description |
| jenis_trouble | ENUM | NOT NULL | Issue type/category |
| perangkat | ENUM | NOT NULL | Device type |
| service | ENUM | NOT NULL | Service status UP/DOWN |
| tanggal_komplain | DATETIME | NOT NULL | Complaint date |
| selesai_pengerjaan | DATETIME | | Completion date |
| durasi_pengerjaan | INTEGER | | Working duration (days) |
| keterangan_action | TEXT | | Action notes |
| cluster_id | INTEGER | | Cluster assignment ID |
| kategori_cluster | ENUM | | Cluster category (Ringan/Sedang/Berat) |
| status | ENUM | DEFAULT Pending | Current status |
| assigned_to | INTEGER | FK | Assigned technician (user.id) |
| pelanggan_id | INTEGER | FK | Related customer |
| perangkat_id | INTEGER | FK | Related device |
| created_by | INTEGER | FK NOT NULL | Creator user ID |
| created_at | DATETIME | DEFAULT NOW | Creation timestamp |
| updated_at | DATETIME | DEFAULT NOW | Last update timestamp |

**Enum Values**:

*jenis_trouble*:
- Human
- Configuration Issue
- Hardware Failure
- Software Issue
- Network Issue

*perangkat*:
- PC, Laptop, Printer, Server, Firewall, Switch, Router, Accesspoint

*service*:
- UP (Service running)
- DOWN (Service down)

*kategori_cluster*:
- Ringan (≤2 days)
- Sedang (2-5 days)
- Berat (>5 days)

*status*:
- Pending (Waiting)
- In Progress (Being worked on)
- Completed (Done)

---

### 5. ClusterHistory Table
```sql
CREATE TABLE cluster_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    jumlah_cluster INTEGER NOT NULL,
    dbi_score FLOAT NOT NULL,
    silhouette_score FLOAT NOT NULL,
    tanggal_clustering DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes
CREATE INDEX ix_cluster_history_tanggal ON cluster_history(tanggal_clustering);
```

**Fields Description**:
| Field | Type | Constraint | Description |
|-------|------|-----------|-------------|
| id | INTEGER | PK, AUTO | History ID |
| jumlah_cluster | INTEGER | NOT NULL | K value used |
| dbi_score | FLOAT | NOT NULL | Davies-Bouldin Index score |
| silhouette_score | FLOAT | NOT NULL | Silhouette coefficient |
| tanggal_clustering | DATETIME | DEFAULT NOW | Clustering execution timestamp |

**Sample Data**:
```
id=1, jumlah_cluster=3, dbi_score=2.2631, silhouette_score=0.4523, tanggal='2026-06-24 10:30:00'
id=2, jumlah_cluster=4, dbi_score=1.8514, silhouette_score=0.5234, tanggal='2026-06-24 11:45:00'
```

---

## 🔑 Foreign Key Relationships

### One-to-Many Relationships

**User → Troubleshoot (created_by)**
```
user.id (1) ──────→ (N) troubleshoot.created_by
```
- One user can create many troubleshoot records
- ON DELETE RESTRICT (cannot delete user with created records)

**User → Troubleshoot (assigned_to)**
```
user.id (1) ──────→ (N) troubleshoot.assigned_to
```
- One technician can be assigned many tasks
- ON DELETE SET NULL (if technician deleted, tasks become unassigned)

**Pelanggan → Troubleshoot**
```
pelanggan.id (1) ──────→ (N) troubleshoot.pelanggan_id
```
- One customer can have many troubleshoot records
- ON DELETE CASCADE (if customer deleted, all related troubleshoots deleted)

**Pelanggan → Perangkat**
```
pelanggan.id (1) ──────→ (N) perangkat.pelanggan_id
```
- One customer can have many devices
- ON DELETE CASCADE (if customer deleted, all devices deleted)

**Perangkat → Troubleshoot**
```
perangkat.id (1) ──────→ (N) troubleshoot.perangkat_id
```
- One device can have many troubleshoot records
- ON DELETE SET NULL

---

## 📈 Data Statistics & Queries

### Useful SQL Queries

**1. Total Troubleshoot by Status**
```sql
SELECT status, COUNT(*) as total
FROM troubleshoot
GROUP BY status
ORDER BY total DESC;
```

**2. Top Issues by Customer**
```sql
SELECT nama_pelanggan, COUNT(*) as total
FROM troubleshoot
GROUP BY nama_pelanggan
ORDER BY total DESC
LIMIT 10;
```

**3. Average Duration by Category**
```sql
SELECT kategori_cluster, AVG(durasi_pengerjaan) as avg_duration
FROM troubleshoot
WHERE kategori_cluster IS NOT NULL
GROUP BY kategori_cluster;
```

**4. Technician Workload**
```sql
SELECT u.username, COUNT(t.id) as assigned_tasks
FROM user u
LEFT JOIN troubleshoot t ON t.assigned_to = u.id
WHERE u.role = 'teknisi'
GROUP BY u.id
ORDER BY assigned_tasks DESC;
```

**5. Recent Clustering Results**
```sql
SELECT * FROM cluster_history
ORDER BY tanggal_clustering DESC
LIMIT 5;
```

**6. Most Common Trouble Type**
```sql
SELECT jenis_trouble, COUNT(*) as total
FROM troubleshoot
GROUP BY jenis_trouble
ORDER BY total DESC;
```

**7. Devices by Type**
```sql
SELECT tipe, COUNT(*) as total
FROM perangkat
GROUP BY tipe
ORDER BY total DESC;
```

**8. Pending Tasks Assigned**
```sql
SELECT u.username, COUNT(t.id) as pending
FROM user u
LEFT JOIN troubleshoot t ON t.assigned_to = u.id
WHERE t.status = 'Pending'
GROUP BY u.id;
```

---

## 🔄 Data Relationships Examples

### Create Troubleshoot Record (Complete Flow)

```python
from app.models import Troubleshoot, Pelanggan, User, db

# 1. Find customer
customer = Pelanggan.query.get(1)

# 2. Find creator user
creator = User.query.get(1)  # admin

# 3. Create troubleshoot
troubleshoot = Troubleshoot(
    no_spk='SPK-20260624-001',
    nama_pelanggan=customer.nama,
    informasi_trouble='Network down at main office',
    jenis_trouble='Network Issue',
    perangkat='Server',
    service='DOWN',
    tanggal_komplain=datetime.now(),
    durasi_pengerjaan=3,
    created_by=creator.id,
    pelanggan_id=customer.id
)

# 4. Save to database
db.session.add(troubleshoot)
db.session.commit()

# 5. Access related data
print(f"Created by: {troubleshoot.user.username}")
print(f"Customer: {troubleshoot.pelanggan_ref.nama}")
```

### Assign Task to Technician

```python
# 1. Find technician
technician = User.query.filter_by(username='teknisi1').first()

# 2. Find troubleshoot
troubleshoot = Troubleshoot.query.get(1)

# 3. Assign
troubleshoot.assigned_to = technician.id
db.session.commit()

# 4. Verify
print(f"Assigned to: {troubleshoot.assigned_user.username}")
```

### Run Clustering & Update Categories

```python
# After clustering runs, troubleshoot records are updated:
troubleshoots = Troubleshoot.query.all()
for ts in troubleshoots:
    if ts.cluster_id:  # Has cluster assignment
        print(f"{ts.no_spk}: Cluster {ts.cluster_id}, Kategori: {ts.kategori_cluster.value}")
```

---

## 📊 Database Optimization Tips

### Indexes
- ✅ Already created on frequently queried fields:
  - user.username, user.email
  - pelanggan.nama, pelanggan.lokasi
  - troubleshoot.no_spk, troubleshoot.status, troubleshoot.created_at
  - perangkat.pelanggan_id

### Query Optimization
```python
# ❌ Bad: N+1 query problem
troubles = Troubleshoot.query.all()
for t in troubles:
    print(t.user.username)  # Separate query for each user

# ✅ Good: Eager loading
troubles = Troubleshoot.query.options(
    db.joinedload('user')
).all()
for t in troubles:
    print(t.user.username)  # No additional queries
```

### Pagination
```python
# ✅ Always paginate large result sets
page = request.args.get('page', 1, type=int)
pagination = Troubleshoot.query.paginate(page=page, per_page=15)
records = pagination.items
total = pagination.total
```

---

## 🔒 Data Integrity Rules

### Constraints Enforced

1. **Unique Constraints**:
   - User.username must be unique
   - User.email must be unique
   - Pelanggan.nama must be unique
   - Troubleshoot.no_spk must be unique

2. **Not Null Constraints**:
   - All required fields must have value
   - Foreign keys for related records
   - Timestamps (created_at, updated_at)

3. **Foreign Key Cascades**:
   - Delete Pelanggan → Cascades to Perangkat & Troubleshoot
   - Delete Perangkat → Sets Troubleshoot.perangkat_id to NULL
   - Delete User (assigned) → Sets Troubleshoot.assigned_to to NULL

4. **Enum Constraints**:
   - Status must be: Pending, In Progress, or Completed
   - Role must be: admin, teknisi, or manajer
   - Category must be: Ringan, Sedang, or Berat

---

## 📁 Database File Management

### File Locations
- **Development**: `/troubleshoot.db` (500KB-5MB typical size)
- **Production**: `instance/troubleshoot.db`
- **Backup**: Create manual backups regularly

### Backup Procedure
```bash
# Backup current database
cp instance/troubleshoot.db instance/troubleshoot.db.backup.$(date +%Y%m%d-%H%M%S)

# Restore from backup
cp instance/troubleshoot.db.backup.20260624-100000 instance/troubleshoot.db
```

---

## 🔄 Migration & Schema Changes

### Adding a New Column
```python
# 1. Update model
class Troubleshoot(db.Model):
    new_field = db.Column(db.String(100))

# 2. Option A: Drop & recreate (development only)
with app.app_context():
    db.drop_all()
    db.create_all()

# 3. Option B: Migrate existing data (production)
# Manual ALTER TABLE or use Alembic for migrations
ALTER TABLE troubleshoot ADD COLUMN new_field VARCHAR(100);
```

---

End of Database Documentation
