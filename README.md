# Simple-Python-Flask-HTTP-Server-for-CIMC-map-www-reimage-ISO

## Dependencies:
  - python  ```pip install python```
  - flask   ```pip install flask```

## What this script does?

This script starts a HTTP server listening on port 80 on all interfaces. (you may modify http port 80 to other ports if 80 is blocked by firewall).

It was created to be a simple/lightweight HTTP server to reimage APICs/Nexus Dashboard servers.

## How to use it?

A folder named "iso_share" will be created in same folder where this script in run, all ISOs or any other files served by HTTP server should be placed inside this folder.

## How to run it:

```python cimc_http_server_v2.py```

  or

```python3 cimc_http_server_v2.py```
