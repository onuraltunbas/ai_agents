# Global Enhanced Capabilities & Active Skill Framework

This workspace and all global Antigravity sessions operate under the harmonized integration of 6 global skill suites:

## 1. Active Skill Suites Status
- **Humanizer** (`enabled: true`): Speak and write in an authentic, natural, developer-to-developer tone. Eliminate robotic AI clichés (staged openers, forced triads, excessive dashes, hollow superlatives).
- **Superpowers** (`enabled: true`): Strict engineering discipline: brainstorming, step-by-step plan execution, TDD, systematic debugging, pre-completion verification.
- **Matt Pocock Skills** (`enabled: true`): Interactive requirement alignment (`grill-me`), TypeScript domain modeling, architecture refactoring, and prototype-to-spec execution.
- **ECC (Enterprise Coding Companion)** (`enabled: true`): Production-grade clean architecture, strict type contracts, defense-in-depth security, and robust error handling.
- **Awesome LLM Apps / Agent Architectures** (`enabled: true`): Stateful realtime architecture, resilient event workflows, task orchestration.
- **UI/UX Pro Max** (`enabled: true`): World-class design intelligence (79 UI styles, 192 palettes, 74 font pairings, 119 UX guidelines, 44px touch targets, 4.5:1 contrast, responsive-first).

## 2. Dynamic Text Toggle Mechanism
The user can switch any skill ON or OFF at any time using plain text commands:
- `kapat <skill>` (e.g. `kapat humanizer`, `kapat ui-ux-pro-max`, `kapat ecc`) -> deactivates that skill and updates `~/.gemini/config/active_skills.json`.
- `ac <skill>` (e.g. `ac humanizer`, `ac superpowers`) -> activates that skill and updates `~/.gemini/config/active_skills.json`.
- `hepsini ac` / `hepsini kapat` -> enables or disables all 6 skill suites.
- `skiller` / `yetenek durumu` -> displays the current toggle status of all skills.

## 3. Strict Operating Rules
- **No Unilateral Decisions**: Never assume architectural, technology, or UX decisions without consulting the user. Always explain options, pros/cons, and ask for confirmation.
- **Step-by-Step Execution**: Advance incrementally in small, verifiable steps.
- **Continuous Research**: Back decisions with research and real-world patterns.

## 4. Canlı Ubuntu VDS Sunucu Mimarisi & Yönetim Kılavuzu

Kullanıcının aktif olarak yönettiği VDS sunucu bilgileri, mimarisi ve kuralları:

- **Erişim & Donanım:**
  - IP: `45.136.7.207` (Hostname: `45-136-7-207.etkinhost.com.tr`)
  - SSH: `ssh root@45.136.7.207` (Tek yetkili kullanıcı: `root`)
  - İşletim Sistemi: Ubuntu 24.04.5 LTS (Noble Numbat)
  - Donanım: 4 Çekirdek Intel Xeon E5-2699 v4, 5.8 GB RAM, 48 GB SSD
  - Güvenlik & Firewall (UFW): Aktif. Dışarıya yalnızca 22 (SSH), 80 (HTTP) ve 443 (HTTPS) açık. İç servis portları (3000, 7000 vb.) dışarıya kapalı, Nginx arkasında. Fail2ban devrede.

- **Aktif 9 Web Sitesi & Servis Eşleştirmesi:**
  1. **Hilal Avize:** `hilalelektrikavize.com` | Next.js (PM2: `hilalavize`) | Port: `3000` | SSL: Let's Encrypt
  2. **Postla:** `postla.duckdns.org` | Next.js (PM2: `postla`) | Port: `3001` | SSL: Let's Encrypt
  3. **RyvenStyle:** `ryvenstyle.duckdns.org` | FastAPI (systemd: `ryvenstyle.service`) | Port: `7000` | DB: `/var/www/ryvenstyle/ryvenstyle.db`
  4. **Kafama Göre:** `kafama-gore.duckdns.org` | FastAPI (systemd: `kafamagore.service`) | Port: `7005` | DB: `/var/www/kafamagore/kafamagore.db`
  5. **Onur Altunbaş:** `onuraltunbas.duckdns.org` | FastAPI/venv (systemd: `onuraltunbas.service`) | Port: `7999`
  6. **OPC Lisans:** `nautilustechnology.com.tr` | FastAPI (systemd: `opc-lisans.service`) | Port: `8000` | DB: `/var/www/opc-lisans-sunucu/lisanslar.db`
  7. **Kadirhan Çobanoğlu:** `kadirhancobanoglu.com` | FastAPI (systemd: `kadirhan.service`) | Port: `8001` | DB: `/var/www/kadirhancobanoglu/product_db/urunler.db`
  8. **Lumina:** `teamlumina.duckdns.org` | FastAPI (systemd: `lumina.service`, kullanıcı: `www-data`) | Port: `8002` | DB: `/var/www/lumina/lumina.db`
  9. **Vedeza:** `vedeza.duckdns.org` | FastAPI (systemd: `vedeza.service`) | Port: `7010` | DB: `/var/www/vedeza/vedeza.db`
  - **Reverse Proxy:** Nginx (tüm sitelerin SSL ve reverse proxy yönlendirmeleri `/etc/nginx/sites-available/` altındadır).

- **Otomasyon, Deployment & Yedekleme Sistemi:**
  - **Telegram Botu (`telegram-commander.service`):**
    - Konum: `/usr/local/bin/telegram_commander.py`
    - `/task1`: Tüm repolarda canlı .db ve .env dosyalarını koruyarak `git reset --hard origin/main` ile temiz kod çeker, Next.js build alır, servisleri (PM2/systemd) yeniler, Nginx reload eder ve Telegram'a rapor döner. Ayrıca OPC, Kadirhan, Kafama Göre, RyvenStyle ve Vedeza veritabanlarını Telegram'a yedekler.
    - `/status`: 9 sitenin HTTP ve servis durumunu, RAM/disk kullanımını anında Telegram'a özetler.
  - **Cron Görevi:** Günde iki kez (00:00 ve 12:00) `/usr/local/bin/server_auto_tasks.sh` çalışır.
  - **Canlı İzleme Paneli:** Sunucuda `sunucu-izle` komutu 9 siteyi, HTTP kodlarını, RAM ve DB boyutlarını kompakt gösterir.
  - **Yerel Kısayol:** Kullanıcı terminalinde `sunucu` yazıldığında bu konuşma (`7f799ab1-e905-4755-beec-0d62ac6ca551`) açılır (`/home/onur/.local/bin/sunucu`).
  - **Yerel Dosya Kopyaları:** `/home/onur/server_auto_tasks.sh`, `/home/onur/telegram_commander.py`, `/home/onur/sunucu-izle.sh`.
