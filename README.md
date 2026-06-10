# aria2-zero + AriaZero WebUI + SMB Server in Docker

## Repository Overview

This repository contains all the necessary source configurations to build a unified, multi-platform Docker container combining **aria2-zero**, the premium custom **AriaZero WebUI**, and a **Samba (SMB) Server**.

The goal of this project is to simplify self-hosted downloading by enabling:
* **Zero-Config Downloading**: Control your downloads from a premium custom React Web UI (AriaZero) served natively.
* **Instant File Sharing**: Access completed downloads instantly on Windows Explorer, macOS Finder, or network-enabled media players (VLC, Kodi, Infuse) via SMB.
* **Multi-Arch Support**: Runs seamlessly on standard `x86_64` (Intel/AMD) machines as well as `arm64` (Apple Silicon, Raspberry Pi 4/5) devices.
* **Port Consolidation**: Nginx handles proxying to combine both the Web UI and JSON-RPC traffic on a single port (port `80`), solving CORS and mixed-content issues.

A lightweight, multi-architecture (`amd64` / `arm64`) Docker container that bundles:
1. **aria2-zero**: A high-performance download utility.
2. **AriaZero WebUI**: A modern, responsive React + TypeScript frontend with a Nordic Frost aesthetic.
3. **SMB (Samba) Server**: An integrated network share to access downloaded files easily.

Nginx is used to host AriaZero and reverse-proxy the JSON-RPC interface, letting you control downloading and view files securely over a single port.

## Ports
* `80`: Web UI (AriaZero) and reverse proxied JSON-RPC (`/jsonrpc`)
* `6800`: Direct Aria2 RPC port (optional)
* `445`: SMB (Samba) Server port

## Volumes
* `/config`: Location of `aria2.conf` and download session records (`aria2.session`).
* `/downloads`: Directory where downloads are stored and shared over SMB.

---

## Running the Container

### 1. Simple Run
Start the container with default Samba credentials (`admin` / `123456`):

```bash
docker run -d \
  --name aria2-zero-ariazero \
  -p 16980:80 \
  -p 16800:6800 \
  -p 445:445 \
  -v /path/to/downloads:/downloads \
  -v /path/to/config:/config \
  --restart unless-stopped \
  illusion1208/aria2-zero-ariazero:latest
```

### 2. Secure Run (Custom SMB Credentials & RPC Password)
For safety, you can add an RPC secret and secure the SMB share using custom credentials:

```bash
docker run -d \
  --name aria2-zero-ariazero \
  -p 16980:80 \
  -p 16800:6800 \
  -p 445:445 \
  -v /path/to/downloads:/downloads \
  -v /path/to/config:/config \
  -e ARIA2_RPC_SECRET=mysecurepassword \
  -e SMB_USER=customuser \
  -e SMB_PASSWORD=secretshare \
  --restart unless-stopped \
  illusion1208/aria2-zero-ariazero:latest
```

---

## Configuration Variables

| Variable | Description | Default |
| --- | --- | --- |
| `ARIA2_RPC_SECRET` | Secret token (password) for Aria2 JSON-RPC authentication | None |
| `SMB_USER` | Username required to access the SMB network share | `admin` |
| `SMB_PASSWORD` | Password required to access the SMB network share | `123456` |

---

## Connecting to the Services

### 1. AriaZero Web Interface
Open your web browser and navigate to:
`http://<Docker-Host-IP>:16980`

AriaZero WebUI will load. It is fully zero-config and will automatically establish a WebSocket JSON-RPC connection using the credentials and host information injected at startup.

### 2. Mounting the SMB Share

#### Windows
1. Open File Explorer.
2. In the address bar, type `\\<Docker-Host-IP>\downloads` and press Enter.
3. Enter the configured SMB credentials (`admin` / `123456` by default) when prompted.

#### macOS
1. In Finder, press `Cmd + K` or select **Go** -> **Connect to Server...**
2. Enter `smb://<Docker-Host-IP>/downloads` and click Connect.
3. Select **Registered User** and enter the username and password.
