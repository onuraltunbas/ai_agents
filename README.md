# 🤖 ONUR AI - Autonomous Local Multi-Agent Ecosystem

%100 Yerel (Offline), Gizlilik Odaklı, Sınırsız ve Kendi Kendini Doğrulayan (Zero-Defect) Çoklu Ajan Sistemi.

Bu sistem, yerel bir **30B LLM (Qwen3-Coder 30B)** motoru üzerinde çalışan, birbirleriyle haberleşebilen, uzun süreli hafızaya (SQLite) ve yerel RAG yeteneğine sahip 5 uzman yapay zeka ajanından oluşur.

---

## 👑 Ajanlar ve Rolleri

```
                                 IRONMAN
                        (Tüm Sistemin Üst Yöneticisi)
                                    │
       ┌──────────────┬─────────────┴─────────────┬──────────────┐
       │              │                           │              │
     COOKER        SELİMBEY                    sohbET          DOKTOR
   (Yazılım &     (Tasarım &                  (Sohbet &       (Sağlık &
    Kodlama)        UI/UX)                     Mentor)        Biohack)
```

| Ajan | Uzmanlık & Görev Tanımı | Komut |
| :--- | :--- | :--- |
| **`ironman`** | **Supreme Meta-Orchestrator:** Karmaşık projeleri alt görevlere bölüp diğer tüm ajanları koordine eder. | `ironman` veya `agent` |
| **`cooker`** | **Master Coding Agent:** Sıfır hata prensibiyle çalışan yazılım mühendisi (ROS2, C/C++, Python, Linter & Testler). | `cooker` |
| **`selimbey`** | **Master UI/UX Designer:** Modern landing page'ler, responsive Tailwind CSS şablonları ve renk sistemleri tasarlar. | `selimbey` |
| **`sohbet`** | **Personal Mentor & Life Coach:** Feynman tekniğiyle ders anlatan, motive eden ve esprili kişisel yol arkadaşı. | `sohbet` |
| **`doktor`** | **Clinical Health & Biohack:** Kanıta dayalı tıp literatürü, semptom analizi, beslenme, spor ve uyku uzmanı. | `doktor` |

---

## ⚡ 1-Tıkla Kolay Kurulum (Tüm Linux / Ubuntu Sistemler İçin)

Herhangi bir Linux bilgisayarda tek bir komutla sıfırdan kurmak için:

```bash
# 1. Repoyu klonla
git clone https://github.com/onuraltunbas/ai_agents.git
cd ai_agents

# 2. Kurulum betiğini çalıştır
chmod +x install.sh
./install.sh
```

> **Kurulum Neler Yapar?**
> 1. Gerekli sistem araçlarını (`gcc`, `g++`, `python3`, `ruff`, `mypy`, `pytest`) kurar.
> 2. `Ollama` ve `OpenCode CLI` motorunu kurar.
> 3. `qwen3-coder:30b` ve `nomic-embed-text` modellerini indirip 64K context ve termal optimizasyonla yapılandırır.
> 4. Tüm ajanları, skilleri ve terminal komutlarını global olarak hazır hale getirir.

---

## 🚀 Kullanım Örnekleri

Kurulum bittikten sonra terminalinizde herhangi bir klasördeyken doğrudan ajanları çağırabilirsiniz:

### 1. Yazılım & Proje Geliştirme (`cooker`)
```bash
cd /projenin/bulundugu/klasor
cooker
# veya tek komutla:
cooker "Bu repository'deki kodları incele, eksik pytest testlerini yaz ve hataları onar"
```

### 2. Web & UI/UX Tasarımı (`selimbey`)
```bash
selimbey "Modern, karanlık temalı bir SaaS landing page için responsive Tailwind CSS şablonu oluştur"
```

### 3. Kişisel Sohbet & Ders Çalışma (`sohbet`)
```bash
sohbet "Feynman tekniğiyle bana Kalman filtresinin mantığını en basit haliyle anlat"
```

### 4. Sağlık & Beslenme Danışmanlığı (`doktor`)
```bash
doktor "Derin uyku süresini artırmak için kanıta dayalı akşam protokolleri nelerdir?"
```

### 5. Tüm Ekibi Yöneten Üst Ajan (`ironman`)
```bash
ironman "Bana hem Tailwind arayüzü hem de arkasında FastAPI lisans sunucusu olan tam bir proje tasarla"
```

---

## 🛡️ Temel Özellikler

* **%100 Yerel & Gizli:** Kodlarınız veya sohbetleriniz asla buluta gitmez, sıfır internet bağımlılığıyla çalışır.
* **Sıfır Maliyet:** Token ücreti veya abonelik yoktur.
* **Kalıcı Hafıza:** Tercihlerinizi ve mimari kararlarınızı SQLite veritabanında saklayarak zamanla sizin tarzınızı öğrenir.
* **Sıfır Hata Doğrulama:** Kod yazıldıktan sonra linter ve test döngüsünden geçirilmeden teslim edilmez.

---

## 💻 Önerilen Sistem Gereksinimleri

* **İşletim Sistemi:** Linux (Ubuntu/Debian vb.)
* **Ekran Kartı:** NVIDIA RTX Serisi (En az 8 GB VRAM önerilir - RTX 3060/4060/5060 vb.)
* **RAM:** 16 GB veya 32 GB RAM
* **Disk:** ~25 GB boş SSD alanı
