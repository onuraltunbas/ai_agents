# Binary Analiz Raporu — Safa Hacıbayramoğlu

## Hedef Bilgisi / Target Info
- Hedef / Target: `sample_malware.apk`
- Tespit Edilen Tür / File Type: APK / ZIP Archive
- Boyut / Size: 12.4 MB
- Araç / Tool: Static String Extractor & Classifier

## Risk Skoru / Risk Score: 92/100

## Bulgular / Findings

### [Kritik] Yüksek Entropili Gizli Veri (High Entropy Secret)
- Değer / Value: `AKIAIOSFODNN7EXAMPLE` (Maskelenmiş)
- Shannon Entropisi: **4.82**
- Risk: Tespit edilen entropi skoru bunun standart bir metin değil, muhtemelen bir AWS Access Key veya simetrik şifreleme anahtarı olduğunu gösteriyor. Kaynak koda gömülmesi kritik bir zafiyettir.

### [Yüksek] Şüpheli API Çağrıları (Suspicious Execution)
- Tespit Edilenler / Detected: 
  - `Runtime.getRuntime().exec`
  - `DexClassLoader`
- Risk: Statik analiz sırasında dinamik kod çalıştırma ve shell komutu yürütme kütüphanelerinin kullanıldığı tespit edildi. Zararlı yazılım (malware) davranışı sergiliyor olabilir.

### [Orta] Gömülü İç URL ve IP'ler
- Değer / Value: `10.0.2.15`, `http://dev-test-server.local/api/v1/keys`
- Risk: Geliştirme ortamına ait ağ altyapı bilgileri dışarı sızıyor.

## Özet / Summary
Proje kapsamında geliştirilen sezgisel motor, standart regex analizinden kaçabilecek yüksek entropili kriptografik sırları ve çalışma zamanı (runtime) kod enjeksiyonu metodlarını başarıyla tespit etmiştir.
