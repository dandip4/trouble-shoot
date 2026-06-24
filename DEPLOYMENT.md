# 🚀 Deployment & Production Guide

## Pre-Deployment Checklist

- [ ] Database seeded dengan data development
- [ ] All dependencies di requirements.txt
- [ ] SECRET_KEY di environment variable (bukan hardcoded)
- [ ] DEBUG mode OFF di production
- [ ] Static files compiled
- [ ] All tests passed
- [ ] Backup database created
- [ ] Firewall rules configured
- [ ] HTTPS certificate prepared
- [ ] Email configuration (if needed)

---

## 📦 Environment Setup

### Production Configuration

**File: `.env.production`**
```env
# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-super-secure-random-key-here-min-32-chars
SERVER_NAME=troubleshoot.yourdomain.com

# Database
DATABASE_URL=sqlite:////data/troubleshoot.db

# Upload folder
UPLOAD_FOLDER=/data/uploads

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/troubleshoot/app.log

# Security
MAX_CONTENT_LENGTH=52428800  # 50MB file upload limit
UPLOAD_EXTENSIONS=xlsx,xls
```

### Generate Secure Secret Key
```python
import secrets
secret_key = secrets.token_hex(32)
print(secret_key)  # Use this in .env file
```

---

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p /data/uploads /var/log/troubleshoot

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "run:app"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./instance:/data
      - ./logs:/var/log/troubleshoot
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=sqlite:////data/troubleshoot.db
      - UPLOAD_FOLDER=/data/uploads
    restart: unless-stopped
    networks:
      - troubleshoot-net

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - web
    networks:
      - troubleshoot-net

networks:
  troubleshoot-net:
    driver: bridge
```

### Build & Run
```bash
docker-compose build
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop
docker-compose down
```

---

## 🌐 Nginx Configuration

**File: `nginx.conf`**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream flask_app {
        server web:5000;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name troubleshoot.yourdomain.com;
        return 301 https://$server_name$request_uri;
    }

    # HTTPS server
    server {
        listen 443 ssl http2;
        server_name troubleshoot.yourdomain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        # Security headers
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        client_max_body_size 50M;

        location / {
            proxy_pass http://flask_app;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 120s;
        }

        location /static/ {
            alias /app/app/static/;
            expires 30d;
        }
    }
}
```

---

## 🔧 Systemd Service (Linux)

**File: `/etc/systemd/system/troubleshoot.service`**
```ini
[Unit]
Description=Troubleshoot Management Application
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/troubleshoot
Environment="FLASK_ENV=production"
Environment="SECRET_KEY=your-secret-key"
ExecStart=/var/www/troubleshoot/.venv/bin/gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 127.0.0.1:5000 \
    --timeout 120 \
    --access-logfile /var/log/troubleshoot/access.log \
    --error-logfile /var/log/troubleshoot/error.log \
    run:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Commands
```bash
# Reload systemd
sudo systemctl daemon-reload

# Start service
sudo systemctl start troubleshoot

# Enable auto-start
sudo systemctl enable troubleshoot

# Check status
sudo systemctl status troubleshoot

# View logs
sudo journalctl -u troubleshoot -f

# Stop service
sudo systemctl stop troubleshoot
```

---

## 📊 Production Database Setup

### SQLite in Production (Small Scale)
```python
# config.py for production
import os

class ProductionConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:////data/troubleshoot.db'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # WAL mode for better concurrent access
    SQLALCHEMY_ENGINE_OPTIONS = {
        'connect_args': {'check_same_thread': False},
        'poolclass': NullPool,
    }
```

### PostgreSQL in Production (Better for Scale)
```python
# config.py - switch to PostgreSQL
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'postgresql://user:password@localhost:5432/troubleshoot'

# Install driver
# pip install psycopg2-binary
```

### Database Backup Script
```bash
#!/bin/bash
# backup-db.sh

BACKUP_DIR="/backups/troubleshoot"
DATE=$(date +%Y%m%d-%H%M%S)
DB_FILE="/data/troubleshoot.db"

# Create backup
cp "$DB_FILE" "$BACKUP_DIR/troubleshoot.db.$DATE"

# Keep only last 30 days
find "$BACKUP_DIR" -name "troubleshoot.db.*" -mtime +30 -delete

# Upload to remote storage (optional)
# aws s3 cp "$BACKUP_DIR/troubleshoot.db.$DATE" s3://my-backups/

echo "Backup completed: $DATE"
```

### Cron Backup Schedule
```bash
# Backup every day at 2 AM
0 2 * * * /var/www/troubleshoot/backup-db.sh

# Backup every 6 hours
0 */6 * * * /var/www/troubleshoot/backup-db.sh
```

---

## 🔍 Monitoring & Logging

### Gunicorn with Logging
```bash
gunicorn \
    --workers 4 \
    --worker-class sync \
    --bind 0.0.0.0:5000 \
    --timeout 120 \
    --access-logfile /var/log/troubleshoot/access.log \
    --error-logfile /var/log/troubleshoot/error.log \
    --loglevel info \
    run:app
```

### Application Logging
```python
# app/__init__.py
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app():
    app = Flask(__name__)
    
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/troubleshoot.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Troubleshoot app startup')
    
    return app
```

### Health Check Endpoint
```python
# app/routes/health.py
from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    return jsonify({'status': 'ok'}), 200
```

---

## 🔒 Security Checklist

### Application Security
- [ ] DEBUG = False
- [ ] SECRET_KEY = secure random string
- [ ] HTTPS enabled
- [ ] CSRF protection on forms
- [ ] SQL injection protected (using ORM)
- [ ] XSS protected (template escaping)
- [ ] Password hashing (werkzeug.security)
- [ ] Session timeout configured
- [ ] File upload validation

### Server Security
- [ ] Firewall rules configured
- [ ] Only necessary ports open (80, 443)
- [ ] SSH key authentication
- [ ] Fail2ban or similar
- [ ] Regular OS updates
- [ ] Log monitoring
- [ ] Backup automated
- [ ] SSL/TLS certificate valid
- [ ] File permissions correct

### Configuration Security
```python
# app/config.py - Production
class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set!
    
    # Security headers
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "200 per day, 50 per hour"
    
    # File upload
    MAX_CONTENT_LENGTH = 52428800  # 50MB
    UPLOAD_ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
```

---

## 📈 Performance Optimization

### Enable Compression
```python
from flask_compress import Compress

app = Flask(__name__)
Compress(app)
```

### Cache Configuration
```python
# app/config.py
CACHE_TYPE = 'simple'
CACHE_DEFAULT_TIMEOUT = 300

# Use in routes
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/troubleshoot')
@cache.cached(timeout=300)
def troubleshoot_list():
    pass
```

### CDN for Static Files
```html
<!-- templates/base.html -->
<!-- Use CDN for Bootstrap, Chart.js, etc. -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@3.7.0/dist/chart.min.js"></script>
```

### Database Connection Pooling
```python
from sqlalchemy.pool import QueuePool

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'poolclass': QueuePool,
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

---

## 🚨 Error Handling & Recovery

### Error Pages
```python
# app/__init__.py
@app.errorhandler(500)
def server_error(error):
    app.logger.error(f'Server error: {error}')
    return render_template('errors/500.html'), 500

@app.errorhandler(503)
def service_unavailable(error):
    return render_template('errors/503.html'), 503
```

### Database Recovery
```bash
# If database corrupted
rm instance/troubleshoot.db

# Restore from backup
cp /backups/troubleshoot.db.20260624-020000 instance/troubleshoot.db

# Restart service
sudo systemctl restart troubleshoot
```

### Out of Disk Space
```bash
# Check disk usage
df -h

# Clear old logs
find /var/log/troubleshoot -name "*.log" -mtime +30 -delete

# Clear cache
rm -rf /tmp/flask_*
```

---

## 📱 Scaling for Large Scale

### Horizontal Scaling
```yaml
# docker-compose.yml with multiple instances
services:
  web1:
    build: .
    expose:
      - "5000"
  
  web2:
    build: .
    expose:
      - "5000"
  
  web3:
    build: .
    expose:
      - "5000"
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web1
      - web2
      - web3
```

### Load Balancer (Nginx)
```nginx
upstream flask_backend {
    server web1:5000;
    server web2:5000;
    server web3:5000;
}

server {
    listen 80;
    location / {
        proxy_pass http://flask_backend;
    }
}
```

### Shared Storage for Uploads
```bash
# Use NFS or cloud storage
# uploads/ mounted from NFS share
mount -t nfs server:/exports/uploads /app/uploads
```

### Distributed Database
- Switch from SQLite to PostgreSQL
- Setup replication/backup
- Configure connection pooling

---

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Code tested locally
- [ ] All dependencies pinned in requirements.txt
- [ ] Database migrations ready
- [ ] Environment variables documented
- [ ] Backup created
- [ ] Firewall rules prepared
- [ ] SSL certificate ready

### Deployment
- [ ] Pull latest code
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Set environment variables
- [ ] Run migrations (if any)
- [ ] Collect static files
- [ ] Start application
- [ ] Verify health check
- [ ] Run smoke tests

### Post-Deployment
- [ ] Monitor logs
- [ ] Check performance metrics
- [ ] Verify all features work
- [ ] Test login with each role
- [ ] Test file upload
- [ ] Test clustering
- [ ] Test report export
- [ ] Verify backups running

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| 502 Bad Gateway | Check if Flask app running: `curl http://localhost:5000` |
| 503 Service Unavailable | Increase worker count or resources |
| Database locked | Restart application, check backups |
| Out of memory | Reduce worker count, enable swap |
| Slow response | Check database queries, enable caching |
| SSL certificate error | Renew certificate, check expiration |
| Upload failing | Check file size limit, disk space |

---

## 📞 Support Information

### Logs Location
- Application: `/var/log/troubleshoot/app.log`
- Nginx: `/var/log/nginx/error.log`
- Systemd: `journalctl -u troubleshoot`

### Health Check
```bash
curl https://troubleshoot.yourdomain.com/health
```

### Debug Mode (Development Only)
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

---

End of Deployment Guide
