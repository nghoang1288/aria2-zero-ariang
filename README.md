# aria2-zero + AriaNg WebUI + SMB Server in Docker

## Repository Overview

This repository contains all the necessary source configurations to build a unified, multi-platform Docker container combining **aria2-zero**, **AriaNg WebUI**, and a **Samba (SMB) Server**.

The goal of this project is to simplify self-hosted downloading by enabling:
* **Zero-Config Downloading**: Control your downloads from a premium Web UI (AriaNg) served natively.
* **Instant File Sharing**: Access completed downloads instantly on Windows Explorer, macOS Finder, or network-enabled media players (VLC, Kodi, Infuse) via SMB.
* **Multi-Arch Support**: Runs seamlessly on standard `x86_64` (Intel/AMD) machines as well as `arm64` (Apple Silicon, Raspberry Pi 4/5) devices.
* **Port Consolidation**: Nginx handles proxying to combine both the Web UI and JSON-RPC traffic on a single port (port `80`), solving CORS and mixed-content issues.

A lightweight, multi-architecture (`amd64` / `arm64`) Docker container that bundles:
1. **aria2-zero**: A high-performance download utility (compiled via MSVC/xmake fork).
2. **AriaNg WebUI**: A modern, responsive web-based frontend for Aria2.
3. **SMB (Samba) Server**: An integrated network share to access downloaded files easily.

Nginx is used to host AriaNg and reverse-proxy the JSON-RPC interface, letting you control downloading and view files securely over a single port.

## Ports
* `80`: Web UI (AriaNg) and reverse proxied JSON-RPC (`/jsonrpc`)
* `6800`: Direct Aria2 RPC port (optional)
* `445`: SMB (Samba) Server port

## Volumes
* `/config`: Location of `aria2.conf` and download session records (`aria2.session`).
* `/downloads`: Directory where downloads are stored and shared over SMB.

---

## Running the Container

### 1. Simple Run (Guest SMB Access - Public)
Run this command to start the container. The network share will be publicly accessible (no credentials needed) on your local network:

```bash
docker run -d \
  --name aria2-box \
  -p 8080:80 \
  -p 6800:6800 \
  -p 445:445 \
  -v /path/to/downloads:/downloads \
  -v /path/to/config:/config \
  --restart unless-stopped \
  illusion1208/aria2-zero-ariang:latest
```

### 2. Secure Run (Authenticated SMB Access & RPC Password)
For safety, you can add an RPC secret and secure the SMB share using credentials:

```bash
docker run -d \
  --name aria2-box \
  -p 8080:80 \
  -p 6800:6800 \
  -p 445:445 \
  -v /path/to/downloads:/downloads \
  -v /path/to/config:/config \
  -e ARIA2_RPC_SECRET=mysecurepassword \
  -e SMB_USER=aria2 \
  -e SMB_PASSWORD=secretshare \
  --restart unless-stopped \
  illusion1208/aria2-zero-ariang:latest
```

---

## Configuration Variables

| Variable | Description | Default |
| --- | --- | --- |
| `ARIA2_RPC_SECRET` | Secret token (password) for Aria2 JSON-RPC authentication | None |
| `SMB_USER` | Username required to access the SMB network share | Guest Access |
| `SMB_PASSWORD` | Password required to access the SMB network share | Guest Access |

---

## Connecting to the Services

### 1. AriaNg Web Interface
Open your web browser and navigate to:
`http://<Docker-Host-IP>:8080`

AriaNg will load. In the settings page:
1. Go to **AriaNg Settings** -> **RPC (localhost:6800)**.
2. If you configured Nginx reverse proxy, change the port to **8080** and path to **jsonrpc**.
3. If you configured `ARIA2_RPC_SECRET`, enter your secret token in the **Aria2 RPC Secret** field.
4. Reload the page to connect.

### 2. Mounting the SMB Share

#### Windows
1. Open File Explorer.
2. In the address bar, type `\\<Docker-Host-IP>\downloads` and press Enter.
3. If you set `SMB_USER` and `SMB_PASSWORD`, enter them when prompted.

#### macOS
1. In Finder, press `Cmd + K` or select **Go** -> **Connect to Server...**
2. Enter `smb://<Docker-Host-IP>/downloads` and click Connect.
3. If you configured credentials, select **Registered User** and enter the username and password.
