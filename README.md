# Cloud Resume Challenge — Self Hosted

Live at [headless-user.cc](https://headless-user.cc)

Forrest Brazeal's Cloud Resume Challenge asks you to build a resume site with a visitor counter and deploy it using real infrastructure. Most people reach for AWS. I used a machine in my room instead.

This was my first time seriously using Docker, setting up a tunnel, and building a CI/CD pipeline. I wanted to understand how the pieces fit together without a managed service doing the hard parts for me.

---

## Stack

| Layer | Choice |
|---|---|
| Frontend | HTML / CSS / JS |
| Web Server | Nginx |
| Backend | Python + FastAPI |
| Database | SQLite |
| Orchestration | Docker Compose |
| Dev Environment | Docker + DevPod |
| Tunneling | Cloudflare Tunnel |
| CI/CD | GitHub Actions (self-hosted runner) |

---

## How It Works

### Request Flow

```
Browser
  │
  ▼
Cloudflare (DNS + TLS termination)
  │
  ▼
cloudflared (tunnel daemon, container)
  │
  ▼
Nginx (frontend container)
  │
  ├── serves index.html
  └── proxies /api/count → rate limiter → FastAPI (backend container)
                                                │
                                                ▼
                                            SQLite (bind mounted from host disk)
```

- Cloudflare handles TLS — the origin just serves plain HTTP
- No inbound ports open on my machine, ever
- The visitor counter survives container rebuilds because `visitors.db` is bind-mounted from the host
- `/api/count` is rate limited at Nginx — 1 request/second per IP, burst of 5

---

### Container Architecture

```
Host Machine
│
├── Docker Compose
│     ├── frontend  — Nginx, serves HTML, rate limits + proxies /api/count
│     ├── backend   — FastAPI, /count endpoint, reads/writes visitors.db
│     └── cloudflared — outbound tunnel to Cloudflare edge
│
└── GitHub Actions Runner (systemd service)
      - polls GitHub, runs docker compose up --build -d on push
```

- Containers talk to each other over Docker's internal network by container name
- Nothing is exposed to the internet directly — all traffic goes through Cloudflare

---

### CI/CD Flow

```
git push origin master
  │
  ▼
GitHub queues a job
  │
  ▼
Self-hosted runner on the homelab picks it up
  │
  ▼
docker compose up --build -d
  │
  ▼
New containers are live
```

- GitHub never connects to my machine — the runner polls outbound
- It runs as a systemd service so it's always on, even after a reboot

---

## Tradeoffs

**Self-hosted vs cloud**
- I wanted to see what managed services actually do under the hood
- Everything here is explicit — Nginx config, tunnel setup, runner installation, all done by hand
- The tradeoff is reliability: no failover, no SLA. If the machine goes down, the site goes down

**SQLite vs Postgres**
- The counter is one integer getting incremented. Postgres would be overkill
- SQLite is just a file — zero operational overhead, no extra container, no connection strings
- It'd be a problem at scale. At homelab scale, it isn't

**Cloudflare Tunnel vs port forwarding**
- Port forwarding means an open router port, an exposed home IP, and managing TLS yourself
- The tunnel connects outbound only — no open ports, no exposed IP, TLS is free
- For a home connection, there's no real argument for port forwarding

**Docker Compose vs Kubernetes**
- I looked at k3s early on and dropped it
- Three containers on one machine don't need an orchestrator
- Kubernetes solves multi-node scheduling, rolling deploys, service meshes — none of which I need yet

**Plain HTML vs React**
- The resume is a static document with no state and no routing
- React would add a build step and a bundler for no actual benefit

---

## Project Structure

```
crc/
  .devcontainer/       ← DevPod dev environment
  .github/
    workflows/
      cicd.yml         ← docker compose up on push to master
  frontend/
    Dockerfile
    default            ← Nginx config
    rate_limit.conf    ← Nginx rate limiting (1r/s per IP, burst 5)
    index.html
  backend/
    Dockerfile
    main.py            ← FastAPI /count endpoint
    visitors.db        ← SQLite, bind mounted from host
  docker-compose.yml
  .env                 ← tunnel token, not committed
```
