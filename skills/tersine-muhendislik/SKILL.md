---
name: tersine-muhendislik
description: Static binary string extraction, magic byte file classification, Shannon entropy secret scanning, and reverse engineering heuristic analysis for APK, DEX, ELF, PE, and AXML binaries. Use when analyzing compiled binaries, auditing APKs/native libraries, hunting hardcoded keys/secrets/tokens, detecting suspicious API calls (exec, DexClassLoader, Cipher), or extracting network indicators (URLs, IPs, emails).
---

# Tersine Mühendislik & Heuristic Binary String Analyzer

Bu yetenek (skill), derlenmiş binary dosyalar (Android APK/DEX/AXML, Linux ELF, Windows PE) üzerinde gelişmiş statik analiz, bellek haritalı string ayıklama, Shannon Entropisi ile gömülü kriptografik sır tespiti ve şüpheli API çağrısı analizi gerçekleştirmek için kullanılır.

İstinye Üniversitesi BGT210 Tersine Mühendislik projesi temel alınarak oluşturulmuştur.

---

## 1. Yeteneğin Temel Özellikleri

1. **Magic Bytes & Format Tespiti:**
   - Dosya uzantısına bağımlı kalmadan ilk 16 bayt okunarak gerçek format tespit edilir:
     - `PK\x03\x04` -> APK / ZIP Archive
     - `\x7fELF` -> ELF (Linux / Android Native `.so`)
     - `MZ` -> PE (Windows Executable `.exe` / `.dll`)
     - `dex\n` -> DEX (Android Dalvik Executable)
     - `\x03\x00\x08\x00` -> AXML (Android Binary XML)

2. **Yüksek Performanslı Bellek Haritalama (`mmap`):**
   - Dosyaları standart `read()` ile RAM'e kopyalayıp şişirmek yerine doğrudan işletim sistemi seviyesinde `mmap.ACCESS_READ` ile belleğe bağlar. GB mertebesindeki büyük dosyalarda bile sıfır bellek yüküyle çalışır.

3. **Çift Karakter Kodlama Desteği (ASCII + UTF-16LE):**
   - Standart Linux `strings` araçları çoğunlukla yalnızca ASCII okurken, Windows ve Android (özellikle DEX/Manifest) stringleri UTF-16LE kodlaması ile saklar.
   - ASCII pattern: `[ -~]{5,}`
   - UTF-16LE pattern: `(?:[\x20-\x7E]\x00){5,}`

4. **Shannon Entropisi ile Kriptografik Sır Analizi:**
   - Rastgelelik ve karmaşıklık derecesi matematiksel olarak hesaplanır:
     $$H(X) = -\sum_{i=1}^{n} P(x_i) \log_2 P(x_i)$$
   - Standart İngilizce ve kaynak kod metinleri genellikle 3.5 - 4.0 aralığındadır.
   - Base64 kodlu anahtarlar, JWT tokenlar, AWS Access Key'ler veya simetrik şifreleme anahtarları **4.6 ve üzeri** entropi skoruna sahiptir.
   - Eşik değeri `> 4.6` ve boşluk içermeyen $\ge 20$ karakter uzunluğundaki diziler "High Entropy Secret" olarak bayraklanır.

5. **Şüpheli API ve Zararlı Yazılım Göstergeleri:**
   - Dinamik kod çalıştırma, shell çalıştırma ve kriptografi API'leri taranır:
     - `Runtime.getRuntime().exec`
     - `exec` / `system`
     - `DexClassLoader`
     - `Cipher.getInstance`
     - `MessageDigest`

6. **Ağ ve Tehdit Göstergeleri (IoC - Indicators of Compromise):**
   - `http://` ve `https://` URL'leri
   - IPv4 adresleri
   - E-posta adresleri

---

## 2. Hızlı Kullanım / CLI

Sistemdeki analiz motorunu doğrudan çağırmak için:

```bash
# Hedef binary'yi analiz edip JSON raporu üretme
python3 /home/onur/.gemini/repos/tersine-muhendislik-final/src/main.py -f <hedef_dosya> -o <cikti_raporu.json>

# Örnek APK analizi:
python3 /home/onur/.gemini/repos/tersine-muhendislik-final/src/main.py -f app-release.apk -o reports/apk_analiz.json

# Örnek ELF/Linux binary analizi:
python3 /home/onur/.gemini/repos/tersine-muhendislik-final/src/main.py -f /usr/bin/target_bin -o reports/elf_analiz.json
```

---

## 3. Python Kod İçi Entegrasyon

Ajan ortamında veya Python betiklerinde analiz sınıfını doğrudan kullanabilirsiniz:

```python
import sys
sys.path.append("/home/onur/.gemini/repos/tersine-muhendislik-final/src")
from main import HeuristicStringAnalyzer, calculate_entropy, get_file_type

# Tekil string entropi hesaplama
score = calculate_entropy("AKIAIOSFODNN7EXAMPLE") # > 4.6 -> Şüpheli anahtar

# Dosya analizi
analyzer = HeuristicStringAnalyzer("/path/to/binary")
analyzer.analyze()
report = analyzer.get_report()

print("Format:", report["metadata"]["file_type"])
print("Gizli Veriler:", report["high_entropy_secrets"])
print("Şüpheli API'ler:", report["suspicious_api_calls"])
print("URL'ler:", report["urls"])
print("IP'ler:", report["ips"])
```

---

## 4. Analiz Bulgularını Yorumlama Rehberi

| Bulgu Türü | Eşik / Örnek | Risk Düzeyi | Aksiyon |
| :--- | :--- | :--- | :--- |
| **High Entropy Secret** | Entropi $> 4.6$, Boyut $\ge 20$ | **Kritik** | Gömülü AWS anahtarı, private key, JWT veya API token'ı kontrol et. |
| **Suspicious Execution API** | `Runtime.getRuntime`, `DexClassLoader` | **Yüksek** | Dinamik kod yükleme (dropper/stager) veya shell çalıştırma kontrolü yap. |
| **Kriptografik API** | `Cipher.getInstance`, `MessageDigest` | **Orta** | Kullanılan şifreleme algoritması (AES, DES, MD5, SHA-256) incelenmeli. |
| **Harici URL / IP** | `http://...`, `x.x.x.x` | **Orta / Bilgi** | C2 (Command & Control) adresi veya sızan geliştirme sunucusu kontrolü yap. |

---

## 5. Tamamlayıcı Tersine Mühendislik Araçları

Bu statik analiz motoru ile birlikte kullanılabilecek Linux araçları:
- `file <hedef>`: MIME/magic byte doğrulama
- `readelf -h -S <elf>`: ELF header ve section bilgileri
- `objdump -d -M intel <elf>`: Disassembly analizi
- `apktool d <apk>`: Android kaynaklarını ve Smali kodunu açma
- `jadx -d out <apk/dex>`: Java kaynak koduna dönüştürme (Decompile)
- `ghidra` / `radare2` / `r2`: İleri seviye statik ve sembolik analiz
