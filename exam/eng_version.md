####  MP01: Operating Systems Implementation
# LPIC-2 Exam
### UF2: Information and Resource Management in a Network
**Exam Access:**
For this exam, you will have a Linux Ubuntu 22.04 LTS machine.

Additionally, there will be a common auxiliary machine for the entire class that will provide DNS packages and services. It will not be necessary to access this machine at any time.

Access your machine via SSH by typing the following commands:

```bash
ssh -i ~/.ssh/id_rsa NAME@IP
```

- Where NAME is the initial of your first name and last name. Example: jsensada
- Where IP is the public IP provided at the start of the exam

During the class, a web service will be available to monitor your progress. You can also access it from your browser using the given IP. The username is the same as the machine (same password).

**Exam:**
On the server, there is a directory `/opt/exam` where all the web content is located. Make this web operational using the name: `linuf2.examenxarxa.com` and ensure it meets all the requirements to be used in a production environment:

- Package installation (1.5 points)
- Web server (2 points)
- Backups (2 points)
- Web server log rotation (1.5 points)
- DNS management (3 points)

Execute all commands with your user. If you need administrator permissions, use `sudo` before the command, do not execute everything as root. To validate the results, submit a text file corresponding to the output of your history.

To help you complete all tasks, here is a step-by-step guide.

## Package Installation (1.5 points)

Install the following packages:

- `nginx-asix`: 1.18.0-6ubuntu14.3
- `bind9-asix`: 1:9.18.1-1ubuntu1
- `helper-asix`: latest

As you can see, these packages are not standard. They are available in the repository: `apt.archive.asix.com`.

If you don't know how to install them, you can use `nginx` and `bind9` from the normal repositories.

## Web Server (2 points)

Configure the `nginx` server so that the HTML content available in `/opt/exam` is served from `/var/www/exam`.

Additionally, apply the following conditions:

- Web server: `linuf2.examenxarxa.com`
- HTTP to HTTPS redirection
- SSL certificate with the web server name `linuf2.examenxarxa.com`

## Backups (1.5 points)

Create a bash script to back up the content of `/var/www/exam`. The script name should be `backup.sh` and it should be saved in `/usr/local/bin/backup.sh`.

To do it correctly:

1. The backup should be compressed in `tar.gz`.
2. It should be saved in `/opt/backups`.
3. It should have a name that identifies the date: `backup_YYYY-MM-DD_HH-MM-SS.tar.gz`.

To validate it:

1. Modify the content of the `backup.html` file found in `/var/www/asix/backup.html` (Put your name in it).
2. Run the backup script: `/usr/local/bin/backup.sh`.
3. Validate that a file has been created: `/opt/backups/backup_YYYY-MM-DD_HH-MM-SS.tar.gz`.

## Recurring Backups (0.5 points)

Using the same script created earlier `/usr/local/bin/backup.sh`, create a cron job to back up `/var/www/exam` every 2 hours. Remember that the script should be executed as the root user.

## Log Rotation (1.5 points)

Modify the `nginx` virtual host serving the web, and for the HTTPS configuration, add the following lines:

```nginx
access_log /var/log/nginx/linuf2-access.log;
error_log /var/log/nginx/linuf2-error.log;
```

This will make the logs for your `linuf2` web automatically saved in these two additional files instead of the generic `nginx` files. Restart the `nginx` service to apply the changes correctly. Once you have the logs in the expected files, create a special `logrotate` configuration for them as follows:

1. Rotate the logs daily.
2. Keep only 2 rotated logs.
3. Compress the rotated log files.
4. Set special permissions: 644 (with your username and group).

## DNS Management (3 points)

Create 2 master DNS zones:

- `examenxarxa.com`
  - Default TTL of 300 seconds

- `uf2.net`
  - Default TTL of 14400 seconds

Additionally, create the following DNS entries according to the table:

| Name                      | Type  | TTL        | IP / Address            |
|---------------------------|-------|------------|-------------------------|
| `linuf2.examenxarxa.com`  | A     | default    | (Machine IP)            |
| `xarxa.uf2.net`           | CNAME | 120 seconds| `linuf2.examenxarxa.com`|
| `linuf2.uf2.net`          | A     | default    | 192.168.1.24            |
| `pass.examenxarxa.com`    | A     | 60 seconds | 10.10.2.0               |
| `fail.examenxarxa.com`    | CNAME | 7200 seconds| google.com             |

Override the `linuf2.examenxarxa.com` entry so that ONLY from the local machine it resolves to `127.0.0.1`.

Change the machine's DNS server to the `bind9` service on your machine.
```

Let me know if you need any further modifications or additional information.