# Heuristic Analyzer Module / Sezgisel Analiz Modülü

## Purpose / Amaç

Bu modül, binary dosyaların içindeki verileri sıradan regex eşleşmelerinin ötesinde analiz eder. Dosya başlıklarını (Magic Bytes) tanımlar, UTF-16 stringleri kurtarır ve rastgele görünen verilerin içerisinden yüksek entropili kriptografik sırları matematiksel olarak ayıklar.

## How It Works / Nasıl Çalışır

1. **Magic Bytes Algılama:** Dosyanın uzantısına bakmaksızın ilk 16 byte'ını okur ve hex karşılıklarından dosyanın gerçek yapısını (ELF, PE, DEX, APK) tespit eder.
2. **Memory Mapping (mmap):** Dosya `read()` ile belleğe kopyalanmak yerine doğrudan OS seviyesinde belleğe haritalanır (`mmap.ACCESS_READ`). Bu sayede büyük boyutlu binary'ler çok hızlı okunur.
3. **UTF-16 & ASCII Parsing:** Çoğu basit araç sadece ASCII okurken, bu modül `(?:[\x20-\x7E]\x00){5,}` pattern'i ile Windows ve Android dosyalarına özgü UTF-16LE karakterleri de tespit eder.
4. **Shannon Entropy Testi:** Regex filtrelerinden kaçan uzun stringler için her karakterin bulunma olasılığı logaritmik olarak hesaplanır. Skor > 4.6 ise bu string "Hardcoded Secret" olarak işaretlenir.

## Usage / Kullanım

```bash
python src/main.py -f target_binary.dex -o reports/analysis_result.json
