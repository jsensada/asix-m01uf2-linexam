#!/bin/bash

sudo DEBIAN_FRONTEND=noninteractive apt-get install dpkg-dev -y 

sudo mkdir /var/www/html/packages

# Custom helper-asix
sudo bash -c "cat <<EOF > helper-asix.sh
#!/bin/bash
echo \"UF2 - M01EF2 Exam (ASIX 2024)\"
EOF"
sudo chmod +x helper-asix.sh
sudo mkdir -p helper-asix-2.0/usr/local/bin
sudo cp helper-asix.sh helper-asix-2.0/usr/local/bin/helper-asix
sudo mkdir helper-asix-2.0/DEBIAN
sudo bash -c "cat <<EOF > helper-asix-2.0/DEBIAN/control
Package: helper-asix
Version: 2.0
Section: base
Priority: optional
Architecture: all
Depends: bash
Maintainer: Jordi Sensada <jsensada@fedac.cat>
Description: Helper Examen. Dummy version
EOF"
sudo dpkg-deb --build helper-asix-2.0

# Create packages repo
sudo mkdir -p /var/www/html/packages/
sudo mv helper-asix-2.0.deb /var/www/html/packages/
cd /var/www/html/packages/
sudo chmod 777 /var/www/html/packages
sudo dpkg-scanpackages . /dev/null | gzip -9c > /var/www/html/packages/Packages.gz
sudo chmod 755 /var/www/html/packages
sudo chmod 644 /var/www/html/packages/helper-asix-2.0.deb
cd -
exit 0