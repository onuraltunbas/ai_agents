# 🤖 ONUR AI - Autonomous Local Multi-Agent Ecosystem

%100 Yerel (Offline), Gizlilik Odaklı, Sınırsız, Uzun Süreli Hafızalı ve Kendi Kendini Doğrulayan (Zero-Defect) Çoklu Yapay Zeka Ajan Sistemi.

Bu repository, başka herhangi bir Linux (Ubuntu/Debian) bilgisayara klonlanıp kurulduğunda, **tüm ayarlarınız, 6 uzman ajanınız, 14 modüler beceriniz (skills), SQLite kalıcı hafızanız ve 30.5B MoE modelinizle** birlikte eksiksiz olarak ayağa kalkacak şekilde tasarlanmıştır.

---

## 🏛️ Mimari Şema ve Ajanlar

```
                                      IRONMAN
                         (Tüm Sistemin Üst Orkestratörü)
                                         │
        ┌──────────────┬─────────────────┼─────────────────┬──────────────┐
        │              │                 │                 │              │
      COOKER        SELİMBEY          sohbET            DOKTOR         MÜREKKEP
    (Yazılım &     (Tasarım &        (Sohbet &         (Sağlık &      (Edebi Metin &
     Kodlama)        UI/UX)           Mentor)          Biohack)        Paraphrasing)
```

| Ajan | Komut | Model | Uzmanlık & Görev Tanımı |
| :--- | :--- | :--- | :--- |
| **`ironman`** | `ironman` veya `agent` | `qwen3-coder:30b` | **Supreme Meta-Orchestrator:** Karmaşık projeleri analiz eder, alt görevlere böler ve uzman ajanları (`cooker`, `selimbey`, `sohbet`, `doktor`, `murekkep`) koordine eder. |
| **`cooker`** | `cooker` | `qwen3-coder:30b` | **Master Coding Agent:** Sıfır hata (Zero-Defect) prensibiyle çalışan kıdemli yazılım mühendisi. ROS2, C/C++, modern Python, linter (`ruff`), tip denetimi (`mypy`) ve test (`pytest`) uzmanı. |
| **`selimbey`** | `selimbey` | `qwen3-coder:30b` | **Master UI/UX & Web Designer:** Modern karanlık temalar, responsive Tailwind CSS bileşenleri, HTML5/React şablonları, erişilebilir tasarım sistemleri ve görsel promptlar üretir. |
| **`sohbet`** | `sohbet` | `qwen3-coder:30b` | **Personal Mentor & Life Coach:** Feynman tekniğiyle karmaşık konuları basitleştiren, motive eden, yüksek duygusal zekalı ve esprili kişisel yol arkadaşı. |
| **`doktor`** | `doktor` | `qwen3-coder:30b` | **Clinical Health & Biohack:** Kanıta dayalı tıp literatürü, semptom analizi, beslenme, hipertrofi, dayanıklılık, uyku kalitesi ve biyohack protokolleri danışmanı. |
| **`murekkep`** | `murekkep` | `qwen3-coder:30b` | **Master Writer & Paraphraser:** Derin anlamsal yeniden yazım (semantic rewriting), sıfır intihal/tekrar, üslup dönüşümü (edebi, akademik, provokatif, samimi) ve zengin Türkçe metin yazarı. |

---

## 💻 Sistem Gereksinimleri

* **İşletim Sistemi:** Linux (Ubuntu 22.04 / 24.04 veya Debian tabanlı tüm dağıtımlar önerilir)
* **Ekran Kartı (GPU):** NVIDIA RTX Serisi (Örn: RTX 3060, 4060, 5060 veya üstü - en az 8 GB VRAM)
  * *Not:* 8 GB VRAM olan kartlarda model katmanlarının bir kısmı GPU'da (~6.6 GB), kalan katmanlar ve bağlam önbelleği sistem RAM'inde hibrit olarak çalışır.
* **Sistem Belleği (RAM):** 16 GB veya 32 GB RAM (32 GB önerilir)
* **Depolama:** En az 25 - 30 GB boş NVMe SSD alanı (Model ~18.5 GB, araçlar ~2 GB)

---

## ⚡ 1. YÖNTEM: Tek Tıkla Otomatik Kurulum (Önerilen)

Yeni bir bilgisayara geçtiğinizde terminali açın ve şu adımları uygulayın:

```bash
# 1. Repoyu klonlayın
git clone https://github.com/onuraltunbas/ai_agents.git
cd ai_agents

# 2. Kurulum betiğini çalıştırın
chmod +x install.sh
./install.sh
```

```bash
# 3. Ortam değişkenlerini yenileyin
source ~/.bashrc
```

**Kurulum Betiği Neler Yapar?**
1. Gerekli sistem paketlerini (`curl`, `git`, `python3`, `gcc`, `g++`, `sqlite3` vb.) kurar.
2. Python doğrulama araçlarını (`pytest`, `ruff`, `mypy`, `numpy`) hazırlar.
3. `Ollama` motorunu kurar, sistem servisini başlatır.
4. `qwen3-coder:30b` ve `nomic-embed-text` modellerini indirip, **32K Context** ve **6 CPU Thread** optimizasyonlu `Modelfile` ile derler.
5. `OpenCode CLI` motorunu kurar.
6. Ajanların sistem promptlarını, kurallarını (`instructions.md`) ve 14 adet uzmanlık becerisini (`skills/`) yapılandırır.
7. Uzun süreli SQLite hafızasını (`memory.db`) varsayılan tercihlerinizle (tip zorunluluğu, zero-defect kuralı, güvenlik kapısı) başlatır.
8. Terminal komutlarını (`ironman`, `cooker`, `selimbey`, `sohbet`, `doktor`, `murekkep`, `agent`) global olarak `~/.local/bin` dizinine ekler.

---

## 🛠️ 2. YÖNTEM: Manuel Adım Adım Kurulum

Eğer kurulumu adım adım kendiniz yönetmek isterseniz:

### Adım 1: Sistem Bağımlılıkları
```bash
sudo apt update -y
sudo apt install -y curl git python3 python3-pip python3-venv gcc g++ make sqlite3
python3 -m pip install --break-system-packages --user pytest ruff mypy numpy
```

### Adım 2: Ollama Motoru ve Servisi
```bash
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable --now ollama
```

### Adım 3: Modellerin İndirilmesi ve Modelfile Yapılandırması
```bash
ollama pull qwen3-coder:30b
ollama pull nomic-embed-text
ollama create qwen3-coder:30b -f Modelfile
```

### Adım 4: OpenCode CLI Kurulumu
```bash
curl -fsSL https://opencode.ai/install | bash
```

### Adım 5: Yapılandırma ve Becerilerin Kopyalanması
```bash
mkdir -p ~/.config/opencode/skills ~/.onur_ai/core
cp config/opencode.jsonc ~/.config/opencode/opencode.jsonc
cp config/instructions.md ~/.config/opencode/instructions.md
cp -r skills/* ~/.config/opencode/skills/
cp -r core/* ~/.onur_ai/core/
```

### Adım 6: Kalıcı Hafızanın Başlatılması
```bash
python3 core/seed_memory.py
```

### Adım 7: Komutların Global Yapılması
```bash
mkdir -p ~/.local/bin
cp bin/* ~/.local/bin/
chmod +x ~/.local/bin/*

# ~/.bashrc dosyasına ekleyin:
echo 'export PATH="$HOME/.opencode/bin:$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🎯 Kullanım ve Örnek Komutlar

Kurulum bittikten sonra terminalinizde herhangi bir dizindeyken doğrudan çağırabilirsiniz:

### 1. Yazılım Geliştirme & Hata Onarımı (`cooker`)
```bash
# Proje dizinine girip interaktif oturum açın:
cd /home/kullanici/projeler/web_app
cooker

# Veya tek satırda komut verin:
cooker "Bu projede eksik olan pytest testlerini yaz, ruff ve mypy linter hatalarını düzelt"
```

### 2. Modern Web & UI/UX Tasarımı (`selimbey`)
```bash
selimbey "Modern, karanlık temalı, cam efektli (glassmorphism) bir SaaS fiyatlandırma kartı tasarla (Tailwind CSS)"
```

### 3. Kişisel Sohbet & Mentor (`sohbet`)
```bash
sohbet "Feynman tekniğini kullanarak bana Transformer mimarisindeki Self-Attention mekanizmasını en basit haliyle anlat"
```

### 4. Kanıta Dayalı Sağlık & Biyohack (`doktor`)
```bash
doktor "REM ve derin uyku sürelerini artırmak için akşam rutini ve bilimsel takviye stratejisi hazırla"
```

### 5. Derin Metin Yazımı & Üslup Dönüşümü (`murekkep`)
```bash
murekkep "Şu metni tamamen özgün kelimelerle, tekrarlardan arındırılmış, akıcı ve edebi bir üslupla yeniden yaz"
```

### 6. Üst Düzey Orkestrasyon (`ironman`)
```bash
ironman "Bana hem FastAPI backend'i hem de modern Tailwind arayüzü olan otonom bir lisans yönetim sistemi tasarla ve görevleri dağıt"
```

---

## 🧩 Dahil Edilen 14 Uzmanlık Becerisi (`skills/`)

OpenCode ve ajanlar arka planda bu becerileri otomatik devreye sokar:
1. **`multi-agent-orchestrator`**: Görev analizi ve ajan yönlendirmesi
2. **`zero-defect-verification`**: AST -> Ruff -> Mypy -> Pytest/GCC doğrulama döngüsü
3. **`ros2-robotics-expert`**: ROS2 Humble/Jazzy, TF2, Nav2, açı normalizasyonu ve CAN haberleşmesi
4. **`low-level-systems`**: C11, C++20, pointer aritmetiği, bellek güvenliği ve lock-free algoritmalar
5. **`website-template-designer`**: Responsive landing page, Tailwind CSS, modern bileşenler
6. **`ui-ux-design-tokens`**: 60-30-10 renk dengesi, WCAG AAA kontrast, tipografi ve spacing
7. **`visual-asset-generator`**: Midjourney/FLUX görsel istemleri, saf SVG vektörler, CSS animasyonları
8. **`creative-rewriting-and-paraphrasing`**: Derin anlamsal yeniden yazım, intihal önleme
9. **`tone-and-style-adaptation`**: Akademik, edebi, ikna edici veya kurumsal üslup geçişleri
10. **`deep-study-mentor`**: Feynman tekniği, aktif hatırlama, Sokratik sorgulama
11. **`motivation-life-coach`**: Zihinsel odaklanma, alışkanlık takibi, günlük disiplin
12. **`witty-humor-banter`**: Sıcak, esprili ve doğal Türkçe sohbet
13. **`clinical-evidence-analysis`**: Kanıta dayalı klinik tıp literatürü analizi
14. **`nutrition-fitness-biohack`**: Hipertrofi, besin zamanlaması, biyohack ve uzun ömür (longevity)

---

## 🗄️ Dizin Yapısı

```
ai_agents/
├── Modelfile                     # 32K context ve 6 thread optimizasyonlu Ollama modeli tanımı
├── README.md                     # Kapsamlı dökümantasyon ve kurulum rehberi
├── install.sh                    # Tek tıkla otomatik kurulum betiği
├── bin/                          # Terminalden çağrılan ajan başlatıcıları
│   ├── agent
│   ├── cooker
│   ├── doktor
│   ├── ironman
│   ├── murekkep
│   ├── selimbey
│   └── sohbet
├── config/                       # OpenCode ve sistem yönergeleri
│   ├── instructions.md           # Temel ajan sistem talimatları
│   └── opencode.jsonc            # 6 ajanın sistem promptları ve Ollama ayarları
├── core/                         # Bağımsız Python çekirdek motoru
│   ├── guardian.py               # Git diff risk analizi ve güvenlik bekçisi
│   ├── memory.py                 # SQLite uzun süreli hafıza motoru
│   ├── onur_orchestrator.py      # Otonom hata tespit, onarım ve test döngüsü
│   ├── rag.py                    # nomic-embed-text tabanlı yerel kod vektör arama
│   ├── seed_memory.py            # Hafıza veritabanı varsayılan tercih yükleyicisi
│   └── verifier.py               # Ruff, Mypy, Pytest doğrulama kütüphanesi
└── skills/                       # 14 adet uzmanlık yönergesi (Markdown)
    ├── clinical-evidence-analysis
    ├── creative-rewriting-and-paraphrasing
    ├── deep-study-mentor
    ├── low-level-systems
    ├── motivation-life-coach
    ├── multi-agent-orchestrator
    ├── nutrition-fitness-biohack
    ├── ros2-robotics-expert
    ├── tone-and-style-adaptation
    ├── ui-ux-design-tokens
    ├── visual-asset-generator
    ├── website-template-designer
    ├── witty-humor-banter
    └── zero-defect-verification
```

---

## ❓ Sık Karşılaşılan Sorunlar ve Çözümleri

### 1. Komutlar bulunamadı hatası alıyorum (`command not found: cooker`)
Terminalinizi kapatıp açın veya şu komutu çalıştırın:
```bash
source ~/.bashrc
```

### 2. Ollama servisine bağlanılamıyor (`connection refused`)
Ollama servisinin durumunu kontrol edin ve başlatın:
```bash
sudo systemctl status ollama
sudo systemctl restart ollama
```

### 3. VRAM Yetersizliği / Yavaş Yanıt
RTX serisi 8 GB kartlarda modelin ~6.6 GB kısmı VRAM'e, kalanı sistem RAM'ine alınır. Sisteminizde en az 16 GB (tercihen 32 GB) RAM bulunmalıdır. Ayrıca `Modelfile` içindeki `num_thread` değerini işlemcinizin performans çekirdeği sayısına göre ayarlayabilirsiniz (varsayılan: 6).
