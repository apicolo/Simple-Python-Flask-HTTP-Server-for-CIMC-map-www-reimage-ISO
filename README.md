# Simple-Python-Flask-HTTP-Server-for-CIMC-map-www-reimage-ISO

## Dependencies:
  - Python 3.6+  ```pip install python```
  - flask   ```pip install flask```

## What this script does?

This script starts a HTTP server listening on port 80 on all interfaces. (you may modify http port 80 to other ports if 80 is blocked by firewall).

It was created to be a simple/lightweight HTTP server to reimage APICs/Nexus Dashboard servers.

## How to use it?

A folder named "iso_share" will be created in same folder where this script in run, all ISOs or any other files served by HTTP server should be placed inside this folder.

No username/password is required when mounting ISO files served by this HTTP server, just hit ```<enter>/<enter>``` when asked by CIMC:

```
system# scope vmedia
system /vmedia # map-www volume_name http://http_server_ip_and_path iso_file_name
Server username: <enter>
Server password: <enter>
```

You cannot run this script from within APICs or Nexus Dashboard servers.

## How to run it:

```python cimc_http_server_v2.py```

or

```python cimc_http_server_v2.py [-h] [-p PORT] [-d DIR]```

### Command-Line Arguments

| Parameter | Short Flag | Long Flag | Description | Default |
| :--- | :--- | :--- | :--- | :--- |
| **Help** | `-h` | `--help` | Show help message and exit | — |
| **Port** | `-p` | `--port` | HTTP port for the server to listen on | `80` |
| **Directory** | `-d` | `--dir` | Local path containing ISO image files | `./iso` |

---

## Usage Examples

### 1. View Help Menu
```bash
python cimc_http_server_v2.py -h
```

### 2. Run with Defaults (Port 80, `./iso` Directory)
```bash
python cimc_http_server_v2.py
```

### 3. Specify Custom Port and Custom Directory
```bash
python cimc_http_server_v2.py -p 9000 -d /var/www/iso_images
```

### 4. Running on Windows
```cmd
python cimc_http_server_v2.py --port 80 --dir C:\ISO_Store
```

---

## Procedure for Re-Imaging Cisco Nexus Dashboard Nodes Using an HTTP Server
https://www.cisco.com/c/en/us/support/docs/cloud-systems-management/application-policy-infrastructure-controller-apic/224568-procedure-for-re-imaging-cisco-nexus.html
