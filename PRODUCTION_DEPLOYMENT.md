# Production Deployment Guide

## Overview
This guide covers multiple options for deploying the Market Analyzer app in a production environment.

---

## Option 1: Windows Production Server (Waitress)

**Best for:** Windows servers, simple deployment

### Setup

1. Install production dependencies:
```bash
pip install waitress
```

2. Run the production server:
```bash
python waitress_server.py
```

The app will run on `http://0.0.0.0:5000` by default.

### Configure Port
Set the PORT environment variable:
```bash
set PORT=8080
python waitress_server.py
```

### Run as Windows Service

Create a Windows service using NSSM:
```bash
# Download NSSM from https://nssm.cc/download
nssm install MarketAnalyzer "C:\Python313\python.exe" "C:\Users\Manny\market-analyzer\waitress_server.py"
nssm start MarketAnalyzer
```

---

## Option 2: Linux Production Server (Gunicorn)

**Best for:** Linux servers, cloud deployments

### Setup

1. Install Gunicorn:
```bash
pip install gunicorn
```

2. Run with Gunicorn:
```bash
gunicorn --config gunicorn_config.py wsgi:app
```

### Custom Configuration
```bash
gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 wsgi:app
```

### Systemd Service (Linux)

Create `/etc/systemd/system/market-analyzer.service`:

```ini
[Unit]
Description=Market Analyzer Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/market-analyzer
Environment="PATH=/opt/market-analyzer/venv/bin"
ExecStart=/opt/market-analyzer/venv/bin/gunicorn --config gunicorn_config.py wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable market-analyzer
sudo systemctl start market-analyzer
sudo systemctl status market-analyzer
```

---

## Option 3: Docker Deployment

**Best for:** Containerized environments, cloud platforms

### Build and Run

1. Build the Docker image:
```bash
docker build -t market-analyzer .
```

2. Run the container:
```bash
docker run -d -p 5000:5000 --name market-analyzer market-analyzer
```

### Using Docker Compose

```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f
```

Stop:
```bash
docker-compose down
```

---

## Option 4: Cloud Deployments

### Heroku

1. Create `Procfile`:
```
web: gunicorn --config gunicorn_config.py wsgi:app
```

2. Deploy:
```bash
heroku create market-analyzer-app
git push heroku main
```

### AWS EC2

1. Launch EC2 instance (Ubuntu)
2. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip nginx
pip3 install -r requirements-prod.txt
```

3. Configure Nginx as reverse proxy:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

4. Run with Gunicorn + Systemd

### Azure App Service

1. Create Azure App Service (Python)
2. Deploy via Git or Azure CLI
3. Set startup command: `gunicorn --config gunicorn_config.py wsgi:app`

### Google Cloud Run

1. Build and push Docker image:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/market-analyzer
```

2. Deploy:
```bash
gcloud run deploy market-analyzer \
  --image gcr.io/PROJECT_ID/market-analyzer \
  --platform managed \
  --port 5000
```

### DigitalOcean App Platform

1. Connect your Git repository
2. Set build command: `pip install -r requirements-prod.txt`
3. Set run command: `python waitress_server.py`

---

## Production Configuration

### Environment Variables

Create `.env` file:
```env
PORT=5000
HOST=0.0.0.0
FLASK_ENV=production
UPDATE_INTERVAL=300
```

### Security Considerations

1. **Use HTTPS**: Always use SSL/TLS in production
2. **API Rate Limiting**: Consider adding rate limiting
3. **Authentication**: Add authentication if needed
4. **CORS**: Configure CORS properly for your domain
5. **Secrets Management**: Use environment variables for API keys

### Performance Optimization

1. **Enable Caching**: Results are cached by default
2. **Workers**: Adjust worker count based on CPU cores
3. **Database**: Consider adding Redis for caching
4. **CDN**: Use CDN for static assets if needed

### Monitoring

1. **Health Check Endpoint**: `/api/health`
2. **Logging**: Logs are sent to stdout/stderr
3. **Metrics**: Consider adding Prometheus metrics
4. **Alerts**: Set up monitoring alerts

---

## Reverse Proxy Setup (Nginx)

### Nginx Configuration

Create `/etc/nginx/sites-available/market-analyzer`:

```nginx
upstream market_analyzer {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://market_analyzer;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /opt/market-analyzer/static;
        expires 30d;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/market-analyzer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Testing Production Setup

1. Test health endpoint:
```bash
curl http://localhost:5000/api/health
```

2. Test analysis:
```bash
curl http://localhost:5000/api/analyze
```

3. Load testing:
```bash
# Install Apache Bench
ab -n 1000 -c 10 http://localhost:5000/
```

---

## Backup and Maintenance

### Backup Portfolio Data
```bash
# Backup
cp portfolio.json portfolio.json.backup

# Restore
cp portfolio.json.backup portfolio.json
```

### Update Application
```bash
git pull origin main
pip install -r requirements-prod.txt
sudo systemctl restart market-analyzer
```

### Logs
```bash
# Systemd logs
sudo journalctl -u market-analyzer -f

# Docker logs
docker logs -f market-analyzer

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 5000
netstat -ano | findstr :5000  # Windows
lsof -i :5000                 # Linux

# Kill process
taskkill /PID <PID> /F        # Windows
kill -9 <PID>                 # Linux
```

### Permission Denied
```bash
# Linux: Run as non-root user
sudo chown -R $USER:$USER /opt/market-analyzer
```

### Dependencies Issues
```bash
# Reinstall all dependencies
pip install --force-reinstall -r requirements-prod.txt
```

---

## Quick Production Start

**Windows:**
```bash
pip install waitress
python waitress_server.py
```

**Linux:**
```bash
pip install gunicorn
gunicorn --config gunicorn_config.py wsgi:app
```

**Docker:**
```bash
docker-compose up -d
```

Your production Market Analyzer is now running! 🚀
