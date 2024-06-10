#!/bin/bash
sudo bash -c 'echo 10.204.0.29 apt.archive.asix.com >> /etc/hosts'
sudo bash -c 'echo 127.0.0.1 linuf2.examenxarxa.com >> /etc/hosts'
## Vars definitions:
GRAFANA_HOST=34.175.206.30
## HTML content:
sudo mkdir -p /opt/exam
sudo bash -c "cat <<EOF > /opt/exam/index.html
<!DOCTYPE html>
<html>
<head>
  <title>LPIC2 Exam (2024)</title>
  <link rel=\"stylesheet\" href=\"style.css\">
</head>
<body>
  <header>
    <h1>Hola, benvingut a la web del M01-UF2!</h1>
  </header>
  <main>
    <p>Si vols saber com ho portes, accedeix a la web del monitor:</p>
    <p>Usuari: el teu nom </p>
    <p>Contrassenya: el teu nom </p>
    <form action=\"http://${GRAFANA_HOST}:3000\">
      <input type=\"submit\" value=\"Accedeix a Grafana\" />
    </form>
  </main>
  <footer>
    <p>&copy; 2024 Jordi Sensada (ISO, ASIX Fedac Xarxa Berga)</p>
  </footer>
</body>
</html>
EOF"

sudo bash -c "cat <<EOF > /opt/exam/style.css
/* CSS styles for LPIC2 Exam website */
body {
  font-family: Arial, sans-serif;
  background-color: #f2f2f2;
}
header {
  background-color: #333;
  color: #fff;
  padding: 20px;
}
h1 {
  margin: 0;
}
main {
  padding: 20px;
}
footer {
  background-color: #333;
  color: #fff;
  padding: 20px;
  text-align: center;
}
EOF"

sudo bash -c "cat <<EOF > /opt/exam/backup.html
EL_TEU_NOM
EOF"

## Validator content:
sudo DEBIAN_FRONTEND=noninteractive apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install python3 python3-pip -y
sudo mkdir /opt/validator-app
sudo mv /tmp/app.py /opt/validator-app
sudo adduser validator --gecos "" --disabled-password && sudo usermod -aG sudo validator && echo "validator ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/validator
sudo pip install -r /tmp/requirements.txt
sudo chown -R validator:validator /opt/validator-app
sudo mv /tmp/exam-validator.service /etc/systemd/system/exam-validator.service
sudo systemctl daemon-reload
sudo systemctl start exam-validator.service
sudo systemctl status exam-validator.service
sudo systemctl enable exam-validator.service

## Student User:
sudo useradd -m -d /home/student -s /bin/bash student
sudo usermod -a -G sudo student
sudo usermod --password $(echo student | openssl passwd -1 -stdin) student