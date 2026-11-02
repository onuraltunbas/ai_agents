# ROADMAP — Advanced Binary String Extraction Engine

> Course / Ders: Reverse Engineering (BGT210) · Istinye University
> Instructor / Danışman: Keyvan Arasteh

---

## Phase 0 / Faz 0: Understand Before You Build / Yazmadan Önce Anla

Tek satır kod yazmadan önce şu soruları yanıtladım:

- What is the project? / Proje nedir? -> Sadece string çıkaran değil, çıkarılan stringin anlamsal önemini (entropisini) ölçen bir analiz motoru.
- How does it work? / Nasıl çalışır? -> Dosyayı `mmap` ile RAM'e alır. Regex ile ASCII ve UTF-16 stringleri bulur. Anlamsız karakter yığınları ile gerçek kriptografik anahtarları ayırmak için Shannon Entropisi hesaplar.
- What are the inputs/outputs? / Girdiler/çıktılar neler? -> Girdi: Herhangi bir binary. Çıktı: Entropi skorları ve şüpheli API'leri içeren JSON raporu.
- What tools will I use and why? / Hangi araçları kullanacağım ve neden? -> Harici kütüphane bağımlılığı yaratmamak için saf Python (mmap, math, re, json).

---

## Phase 1 / Faz 1: Research & Investigation / Araştırma ve Keşif

> Folder / Klasör: `docs/research/`

| Topic / Konu | Status / Durum | Notes / Notlar |
|--------------|----------------|----------------|
| mmap vs f.read() | ✅ Tamamlandı | Büyük APK'larda f.read() belleği şişiriyordu, mmap'e geçildi. |
| Magic Bytes Tespiti | ✅ Tamamlandı | Dosya uzantısına güvenmek yerine header okuma mantığı eklendi. |
| Shannon Entropisi | ✅ Tamamlandı | Base64 regex'in çok fazla false-positive vermesini çözmek için entropi matematiği entegre edildi. |

---

## Phase 2 / Faz 2: Environment Setup / Ortam Kurulumu

- [x] Isolated lab environment (Docker / VM) / İzole lab ortamı
- [x] Tools installed and verified / Araçlar kuruldu ve test edildi
- [x] `.env.example` created / oluşturuldu

---

## Phase 3 / Faz 3: Implementation / Uygulama

### Module / Modül: Heuristic Analyzer

1. Step 1 / Adım 1 — Magic byte kontrolü ve mmap ile dosya yükleme
2. Step 2 / Adım 2 — UTF-16 ve ASCII regex ayıklaması
3. Step 3 / Adım 3 — IP/URL sınıflandırması ve yüksek entropili (gizli) veri tespiti

---

## Phase 4 / Faz 4: Testing & Reporting / Test ve Raporlama

- [x] Ran tests against target/sample / Hedef/örnek üzerinde testler çalıştırıldı
- [x] Documented all findings with evidence / Tüm bulgular kanıtlarıyla belgelendi
- [x] Wrote final report (Markdown) / Final raporu yazıldı

---

## Phase 5 / Faz 5: Delivery / Teslim

- [x] GitHub repository is clean and organized / Repo temiz ve düzenli
- [x] README.md complete / eksiksiz
- [x] Docker verified (`docker-compose up`) / doğrulandı
- [x] Instructor invited as collaborator / Danışman collaborator olarak eklendi → **keyvanarasteh**

---

## What I Learned / Öğrendiklerim

Sadece Base64 pattern'i aramanın statik analizde yetersiz kaldığını fark ettim. Rastgele byte dizileri Base64 gibi görünebiliyordu. Shannon Entropisini koda entegre ettikten sonra, entropi skoru 4.6'nın üzerinde olan stringleri filtreleyerek gerçek API anahtarlarını ve şifreleri çok daha yüksek bir doğrulukla bulabildiğimi gördüm. Ayrıca `mmap` kullanımı I/O performansını ciddi şekilde artırdı.
