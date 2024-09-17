#!/bin/bash

# Update und grundlegende Pakete installieren
sudo apt update -y
sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-dev
sudo apt install -y mariadb-server supervisor nginx git
# Git Repository klonen
git clone https://github.com/9saile9/microblog.git
cd microblog
echo Repository geklont
# Virtuelle Umgebung erstellen und aktivieren
python3 -m venv venv
source venv/bin/activate
# Notwendige Python-Pakete installieren
pip3 install wheel
pip3 install -r requirements.txt
pip3 install gunicorn pymysql cryptography
echo Python Pakete installiert
# Kreieren der Tabellen
mysql -u root -e "CREATE DATABASE microblog CHARACTER SET utf8 COLLATE utf8_bin;"
mysql -u root -e "CREATE USER 'microblog'@'localhost' IDENTIFIED BY 'Password';"
mysql -u root -e "GRANT ALL PRIVILEGES ON microblog.* TO 'microblog'@'localhost';"
mysql -u root -e "FLUSH PRIVILEGES;"
echo Datenbank angelegt
# .env-Datei erstellen mit dem generierten MariaDB-Passwort
cat <<EOT >> .env
SECRET_KEY=49347611a88144e5a7d964c7d8f75506
DATABASE_URL=mysql+pymysql://microblog:Password@localhost:3306/microblog
EOT
echo .env Datei angelegt
# FLASK_APP Variable dauerhaft setzen
echo "export FLASK_APP=microblog.py" >> ~/.profile
echo variable gesetzt
# Datenbankmigration
flask db init || echo "Migrationen bereits initialisiert"
flask db migrate -m "Initial migration"
flask db upgrade
echo Datenbankmigration abgeschlossen
# Supervisor-Konfiguration f�r Gunicorn einrichten
sudo bash -c 'cat <<EOT > /etc/supervisor/conf.d/microblog.conf
[program:microblog]
command=/root/microblog/venv/bin/gunicorn -b localhost:8000 -w 4 microblog:app
directory=/root/microblog
user=root
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
EOT'
echo microblog.conf angelegt
# Supervisor neu starten und Status �berpr�fen
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl status
echo supervisor l�uft
# NGINX-Konfiguration
# L�sche die Standard-NGINX-Konfiguration
sudo rm /etc/nginx/sites-enabled/default
# Neue NGINX-Konfiguration f�r die App anlegen
sudo bash -c 'cat <<EOT > /etc/nginx/sites-available/microblog
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    location /static/ {
        alias /path/to/your/repository/app/static/;
        expires 30d;
    }
}
EOT'
# NGINX-Konfiguration aktivieren
sudo ln -s /etc/nginx/sites-available/microblog /etc/nginx/sites-enabled/
echo nginx konfiguriert
# NGINX neu starten
sudo service nginx restart
sudo ufw allow 80/tcp
# Abschlussmeldung
echo "Web-App-Installation abgeschlossen!"
