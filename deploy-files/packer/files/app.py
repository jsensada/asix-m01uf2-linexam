import time, subprocess, os, requests, ssl, socket, datetime, dns.resolver, fnmatch, urllib3
from prometheus_client import start_http_server, Gauge
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Final mark
final_mark_computed = Gauge('final_mark_computed', 'Final mark from checks')
# Packages checks
packages_installed_nginx = Gauge('packages_installed_nginx', 'Check if nginx is installed')
packages_installed_bind9 = Gauge('packages_installed_bind9', 'Check if bind9 is installed')
packages_installed_helper = Gauge('packages_installed_helper', 'Check if helper-asix is installed')
# Web server checks
webserver_html_content = Gauge('webserver_html_content', 'Check if html content exists and contains index.html')
webserver_redirect_http_https = Gauge('webserver_redirect_http_https', 'Check if nginx redirects from http to https')
webserver_name = Gauge('webserver_name', 'Check if nginx resolves to the name expected')
webserver_ssl_certificate = Gauge('webserver_ssl_certificate', 'Check if nginx resolves with a ssl certificate')
webserver_content = Gauge('webserver_content', 'Check if nginx resolves with the content expected')
# Backup checks
backup_file_content = Gauge('backup_file_content', 'Check if backup.html has changed')
backup_targz_exists = Gauge('backup_targz_exists', 'Check tar.gz in /opt/backups')
backup_script_exists = Gauge('backup_script_exists', 'Check if /usr/local/bin/backup.sh exists')
backup_cron_definition = Gauge('backup_cron_definition', 'Check if cron has been specified')
# Logrotate checks
logrotate_config_nginx = Gauge('logrotate_config_nginx', 'Check if nginx contains the expected lines for custom log')
logrotate_working = Gauge('logrotate_working', 'Check if logrotate directory contains linuf2 files')
logrotate_rotation = Gauge('logrotate_rotation', 'Check if there is a file rotated')
# DNS checks
dns_etc_hosts = Gauge('dns_etc_hosts', 'Check if there is the expected entry on /etc/hosts')
dns_linuf2 = Gauge('dns_linuf2', 'Check dns entry of linuf2.examenxarxa.com')
dns_xarxa = Gauge('dns_xarxa', 'Check dns entry of xarxa.uf2.net')
dns_linuf2_uf2 = Gauge('dns_linuf2_uf2', 'Check dns entry of linuf2.uf2.net')
dns_pass = Gauge('dns_pass', 'Check dns entry of pass.examenxarxa.com')
dns_fail = Gauge('dns_fail', 'Check dns entry of fail.examenxarxa.com')

def check_packages_installed_nginx():
    expected_version = "1.18.0"
    try:
        result = subprocess.run(['nginx', '-v'], stderr=subprocess.PIPE, text=True)
        output = result.stderr
        if result.returncode != 0:
            print("NGINX is not installed or there was an error running the command.")
            return 0, 0
        if "nginx version: nginx/" in output:
            version = output.split("/")[-1].split()[0].strip()
            if version == expected_version:
                print(f"NGINX is installed with the expected version {version}.")
                return 1, 0.25
            else:
                print(f"NGINX version mismatch: Expected {expected_version}, but found {version}.")
                return 0, 0
        else:
            print("Unable to parse NGINX version.")
            return 0, 0
    except FileNotFoundError:
        print("NGINX is not installed.")
        return 0, 0

def check_packages_installed_bind9():
    expected_version = "9.18"
    try:
        result = subprocess.run(['named', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        if result.returncode != 0:
            print("BIND9 is not installed or there was an error running the command.")
            return 0, 0
        if "BIND" in output:
            version = output.split()[1]
            if version.startswith(expected_version):
                print(f"BIND9 is installed with the expected version {version}.")
                return 1, 0.5
            else:
                print(f"BIND9 version mismatch: Expected {expected_version}, but found {version}.")
                return 0, 0
        else:
            print("Unable to parse BIND9 version.")
            return 0, 0
    except FileNotFoundError:
        print("BIND9 is not installed.")
        return 0, 0

def check_packages_installed_helper():
    try:
        result = subprocess.run(['bash','-c','/usr/local/bin/helper-asix'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        if result.returncode != 0:
            print("Helper-asix is not installed.")
            return 0, 0
        if output.startswith("UF2 - M01EF2 Exam"):
            print(f"Helper-asix is installed and returns: {result.stdout}")
            return 1, 0.75
    except FileNotFoundError:
        print("Helper-asix is not installed.")
        return 0, 0

def check_html_content_and_index():
    directory = '/var/www/exam'
    filename = 'index.html'
    if os.path.isdir(directory):
        if os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                print(f"The file {filename} exists in {directory}.")
                return 1, 0.4
            else:
                print(f"The file {filename} does not exist in {directory}.")
                return 0, 0
        else:
            print(f"The directory {directory} is empty.")
            return 0, 0
    else:
        print(f"The directory {directory} does not exist.")
        return 0, 0

def check_redirect_http_https():
    try:
        response = requests.get(f'http://127.0.0.1', allow_redirects=False)
        response_linuf2 = requests.get(f'http://linuf2.examenxarxa.com', allow_redirects=False)
        if response.status_code in [301, 302] or response_linuf2.status_code in [301, 302]:
            location = response.headers.get('Location', '')
            location_linuf2 = response_linuf2.headers.get('Location', '')
            if location.startswith('https://') or location_linuf2.startswith('https://'):
                print('linuf2.examenxarxa.com or localhost redirects')
                return 1, 0.4
            else:
                print("Does not redirect to HTTPS")
                return 0, 0
        else:
            print("No redirection from HTTP to HTTPS.")
            return 0, 0
    except requests.RequestException as e:
        print(str(e))
        return 0, 0

def check_webserver_name(directory='/etc/nginx/sites-enabled', expected_name='linuf2.examenxarxa.com'):
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        return 0, 0
    files = os.listdir(directory)
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        try:
            with open(file_path, 'r') as file:
                contents = file.read()
                if expected_name in contents:
                    print(f"Server name {expected_name} is set in {file_name}.")
                    return 1, 0.4
        except Exception as e:
            print(f"Error reading {file_name}: {str(e)}")
            return 0, 0
    print(f"Server name {expected_name} is not set in any config file.")
    return 0, 0

def check_ssl_certificate():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE 
    try:
        with socket.create_connection(('127.0.0.1', 443)) as sock:
            with context.wrap_socket(sock, server_hostname='127.0.0.1') as ssock:
                print(f"SSL/TLS is available on localhost:443.")
                return 1, 0.4 
    except ssl.SSLError as e:
        print(f"SSL error: {str(e)}")
        return 0, 0
    except Exception as e:
        print(f"General error: {str(e)}")
        return 0, 0

def check_content_contains_text( text='M01-UF2'):
    try:
        http_response = requests.get(f'http://127.0.0.1', verify=False)
        https_response = requests.get(f'https://127.0.0.1', verify=False)
        linuf2http_response = requests.get(f'http://linuf2.examenxarxa.com', verify=False)
        linuf2https_response = requests.get(f'https://linuf2.examenxarxa.com', verify=False)

        if text in http_response.text or text in https_response.text or text in linuf2http_response.text or text in linuf2https_response.text:
            print(f"Text found as expected")
            return 1, 0.4
        else:
            return 0, 0
    except requests.RequestException as e:
        print(str(e))
        return 0, 0

import os

def check_backup_file_content(directory='/var/www/exam', filename='backup.html', search_text='EL_TEU_NOM'):
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            contents = file.read()
            if search_text in contents:
                print(f"The file {filename} contains the text '{search_text}'.")
                return 0, 0
            else:
                print(f"The file {filename} does not contain the text '{search_text}'.")
                return 1, 0.5
    else:
        print(f"The file {filename} does not exist in {directory}.")
        return 0, 0

def check_backup_targz_exists(directory='/opt/backups'):
    if os.path.isdir(directory):
        for file in os.listdir(directory):
            if file.endswith('.tar.gz'):
                print(f"Found tar.gz file: {file}")
                return 1, 0.5
        print("No tar.gz files found in the directory.")
        return 0, 0
    else:
        print("Directory does not exist.")
        return 0, 0

def check_backup_script_exists(directory='/usr/local/bin/', filename='backup.sh'):
    file_path = os.path.join(directory, filename)
    if os.path.exists(file_path):
        print(f"File {filename} exists.")
        return 1, 0.5
    else:
        print(f"File {filename} does not exist.")
        return 0, 0

def check_backup_cron_definition(search_pattern='0 */2 * * *'):
    try:
        result = subprocess.run(['sudo', 'crontab', '-l'], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            if search_pattern in result.stdout:
                print("Cron job matching the pattern found.")
                return 1, 0.5
            else:
                print("No cron job matches the pattern.")
                return 0, 0
        else:
            print(f"Error accessing cron jobs: {result.stderr}")
            return 0, 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 0, 0

def check_logrotate_config_nginx(directory='/etc/nginx/sites-enabled', expected_line='/var/log/nginx/linuf2-access.log'):
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        return 0, 0
    files = os.listdir(directory)
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        try:
            with open(file_path, 'r') as file:
                contents = file.read()
                if expected_line in contents:
                    print(f"Log entry {expected_line} is set in {file_name}.")
                    return 1, 0.5
        except Exception as e:
            print(f"Error reading {file_name}: {str(e)}")
            return 0, 0
    print(f"Log entry {expected_line} is not set in any config file.")
    return 0, 0

def check_logrotate_working(directory='/etc/logrotate.d/', expected_line='/var/log/nginx/linuf2-access.log'):
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        return 0, 0
    files = os.listdir(directory)
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        try:
            with open(file_path, 'r') as file:
                contents = file.read()
                if expected_line in contents:
                    result = subprocess.run(['sudo', 'logrotate', '-f', '/etc/logrotate.conf'], stderr=subprocess.PIPE, text=True)
                    if result.returncode != 0:
                        print(f"Logrotation of {expected_line} is set in any config file and works")
                        return 1, 0.5
                    else:
                        print(f"Logrotation of {expected_line} is set in any config file but it doesn't works")
                        return 0, 0,2
        except Exception as e:
            print(f"Error reading {file_name}: {str(e)}")
            return 0, 0
    print(f"Logrotation of {expected_line} is not set in any config file.")
    return 0, 0

def check_logrotate_rotation(directory='/var/log/nginx/'):
    if os.path.isdir(directory):
        for file in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file)) and fnmatch.fnmatch(file, 'linuf2-access.log.1.gz'):
                print(f"Found linuf2-access.log rotated: {file}")
                return 1, 0.5
        print("No linuf2-access.log files rotated found in the directory.")
        return 0, 0
    else:
        print("Directory does not exist.")
        return 0, 0

def check_etc_hosts(file_path='/etc/hosts', expected_line='linuf2.examenxarxa.com'):
    try:
        with open(file_path, 'r') as file:
            contents = file.read()
            if expected_line in contents:
                print(f"/etc/hosts contains an entry for: {expected_line}.")
                return 1, 1
            else:
                print(f"/etc/hosts doesn't contain an entry for: {expected_line}.")
                return 0, 0
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}")
        return 0, 0

def check_dns_entry(domain, dns_server='127.0.0.1', record_type='A'):
    try:
        result = subprocess.run(['nslookup', f"-type={record_type}", domain, dns_server], capture_output=True, text=True)
        if result.returncode == 0:
            print(result.stdout.strip())
            return 1, 0.4
        else:
            print("Error during DNS lookup.")
            return 0, 0
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0, 0

def get_ip_address():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('192.0.2.1', 80))
            ip = s.getsockname()[0]
        return ip
    except Exception as e:
        return f"Failed to get IP address: {str(e)}"
    
if __name__ == '__main__':
    start_http_server(8000)
    local_ip = get_ip_address()
    print(local_ip)
    
    while True:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Starting the check at {current_time}")
        final_mark = 0
        #
        result_packages_installed_nginx, mark = check_packages_installed_nginx()
        final_mark = final_mark + mark
        packages_installed_nginx.set(result_packages_installed_nginx)
        print(final_mark)
        #
        result_packages_installed_bind9, mark = check_packages_installed_bind9()
        final_mark = final_mark + mark
        packages_installed_bind9.set(result_packages_installed_bind9)
        print(final_mark)
        #
        result_packages_installed_helper, mark = check_packages_installed_helper()
        final_mark = final_mark + mark
        packages_installed_helper.set(result_packages_installed_helper)
        print(final_mark)
        #
        result_webserver_html_content, mark = check_html_content_and_index()
        final_mark = final_mark + mark
        webserver_html_content.set(result_webserver_html_content)
        print(final_mark)
        # 
        result_webserver_redirect_http_https, mark = check_redirect_http_https()
        final_mark = final_mark + mark
        webserver_redirect_http_https.set(result_webserver_redirect_http_https)
        print(final_mark)
        # 
        result_webserver_name, mark = check_webserver_name()
        final_mark = final_mark + mark
        webserver_name.set(result_webserver_name)
        print(final_mark)
        # 
        result_webserver_ssl_certificate, mark = check_ssl_certificate()
        final_mark = final_mark + mark
        webserver_ssl_certificate.set(result_webserver_ssl_certificate)
        print(final_mark)
        # 
        result_webserver_content, mark = check_content_contains_text()
        final_mark = final_mark + mark
        webserver_content.set(result_webserver_content)
        print(final_mark)
        #
        result_backup_file_content, mark = check_backup_file_content()
        final_mark = final_mark + mark
        backup_file_content.set(result_backup_file_content)
        print(final_mark)
        #
        result_backup_targz_exists, mark = check_backup_targz_exists()
        final_mark = final_mark + mark
        backup_targz_exists.set(result_backup_targz_exists)
        print(final_mark)
        #
        result_backup_script_exists, mark = check_backup_script_exists()
        final_mark = final_mark + mark
        backup_script_exists.set(result_backup_script_exists)
        print(final_mark)
        #
        result_backup_cron_definition, mark = check_backup_cron_definition()
        final_mark = final_mark + mark
        backup_cron_definition.set(result_backup_cron_definition)
        print(final_mark)
        #
        result_logrotate_config_nginx, mark = check_logrotate_config_nginx()
        final_mark = final_mark + mark
        logrotate_config_nginx.set(result_logrotate_config_nginx)
        print(final_mark)
        #
        result_logrotate_working, mark = check_logrotate_working()
        final_mark = final_mark + mark
        logrotate_working.set(result_logrotate_working)
        print(final_mark)
        #
        result_logrotate_rotation, mark = check_logrotate_rotation()
        final_mark = final_mark + mark
        logrotate_rotation.set(result_logrotate_rotation)
        print(final_mark)
        #
        result_dns_etc_hosts, mark = check_etc_hosts()
        final_mark = final_mark + mark
        dns_etc_hosts.set(result_dns_etc_hosts)
        print(final_mark)
        #
        result_dns_linuf2, mark = check_dns_entry('linuf2.examenxarxa.com', '127.0.0.1', 'A')
        final_mark = final_mark + mark
        dns_linuf2.set(result_dns_linuf2)
        print(final_mark)
        #
        result_dns_xarxa, mark = check_dns_entry('xarxa.uf2.net', '127.0.0.1', 'CNAME')
        final_mark = final_mark + mark
        dns_xarxa.set(result_dns_xarxa)
        print(final_mark)
        #
        result_dns_linuf2_uf2, mark = check_dns_entry('linuf2.uf2.net', '127.0.0.1', 'A')
        final_mark = final_mark + mark
        dns_linuf2_uf2.set(result_dns_linuf2_uf2)
        print(final_mark)
        #
        result_dns_pass, mark = check_dns_entry('pass.examenxarxa.com', '127.0.0.1', 'A')
        final_mark = final_mark + mark
        dns_pass.set(result_dns_pass)
        print(final_mark)
        #
        result_dns_fail, mark = check_dns_entry('fail.examenxarxa.com','127.0.0.1', 'CNAME')
        final_mark = final_mark + mark
        dns_fail.set(result_dns_fail)
        print(final_mark)
        print("----------")
        final_mark_computed.set(final_mark)
        time.sleep(30)
