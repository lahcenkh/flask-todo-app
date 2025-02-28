# Flask Todo App Deployment Guide

## Overview
This repository contains a simple **Flask Todo App** deployed on **Rocky Linux** using **MySQL, Nginx, and Gunicorn**. This guide provides step-by-step instructions for setting up and running the application in a production environment.

## Features
- Task management (Add, View, Delete)
- Uses MySQL as the database
- Deployed with **Gunicorn** and **Nginx**
- SELinux and Firewall configuration for security

## Prerequisites
Before setting up the application, ensure you have the following:
- **Rocky Linux 8/9** server with root or sudo access
- **Python 3.12+** installed
- **MySQL Server** installed
- **Git, Nginx, and Gunicorn** installed

## Installation & Setup
### 1. Update System Packages
```bash
sudo dnf update -y
```

### 2. Install Dependencies
```bash
sudo dnf install epel-release -y
sudo dnf install htop vim unzip python3.12 python3.12-pip mysql-server mysql python3.12-devel gcc nginx git -y
```

### 3. Configure Firewall
```bash
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --add-service=https --permanent
sudo firewall-cmd --reload
```

### 4. Set Up MySQL Database
```bash
sudo systemctl enable --now mysqld
sudo mysql_secure_installation
```
Run the following MySQL commands to create a database and user:
```sql
CREATE DATABASE todo_db;
CREATE USER 'flaskapp'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON todo_db.* TO 'flaskapp'@'%';
FLUSH PRIVILEGES;
```

### 5. Clone the Repository
```bash
cd /usr/share/nginx/html/
sudo git clone https://github.com/yourusername/flask-todo-app.git flask_todo_app
cd flask_todo_app
```

### 6. Set Up Virtual Environment & Install Dependencies
```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

### 7. Configure Gunicorn with systemd
Create a systemd service file:
```bash
sudo vim /etc/systemd/system/flask_todo_app.service
```
Add the following content:
```ini
[Unit]
Description=Flask Todo App
After=network.target

[Service]
User=nginx
Group=nginx
WorkingDirectory=/usr/share/nginx/html/flask_todo_app
Environment="PATH=/usr/share/nginx/html/flask_todo_app/venv/bin"
ExecStart=/usr/share/nginx/html/flask_todo_app/venv/bin/gunicorn --workers 3 --bind unix:flask_todo_app.sock -m 007 app:app
EnvironmentFile=/usr/share/nginx/html/flask_todo_app/.env

[Install]
WantedBy=multi-user.target
```
Start and enable the service:
```bash
sudo systemctl daemon-reload
sudo systemctl start flask_todo_app
sudo systemctl enable flask_todo_app
```

### 8. Configure Nginx as a Reverse Proxy
Create an Nginx config file:
```bash
sudo vim /etc/nginx/conf.d/flask_todo_app.conf
```
Add the following:
```nginx
server {
    listen 80;
    server_name your_domain_or_IP;

    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://unix:/usr/share/nginx/html/flask_todo_app/flask_todo_app.sock;
    }
}
```
Test and restart Nginx:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### 9. Configure SELinux
```bash
semanage fcontext -a -t bin_t "/usr/share/nginx/html/flask_todo_app/venv/bin(/.*)?"
semanage fcontext -a -t etc_t /usr/share/nginx/html/flask_todo_app/.env
restorecon -Rv /usr/share/nginx/html/flask_todo_app/venv/bin
restorecon -v /usr/share/nginx/html/flask_todo_app/.env
```

### 10. Start the Application
```bash
sudo systemctl restart flask_todo_app
sudo systemctl restart nginx
```

## Troubleshooting
### Fix 502 Bad Gateway Error
If you get a **502 Bad Gateway** error, try disabling SELinux temporarily:
```bash
sudo setenforce 0
```
To permanently allow necessary permissions:
```bash
ausearch -c 'nginx' --raw | audit2allow -M flask_todo_app
semodule -X 300 -i flask_todo_app.pp
sudo setenforce 1
```
Restart services:
```bash
sudo systemctl restart nginx flask_todo_app
```

# Blog Post
check out full blog post: (Deploying a Flask Todo App with MySQL, Nginx, and Gunicorn on Rocky Linux)[https://netopsautomation.com]
