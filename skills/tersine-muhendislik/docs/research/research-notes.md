# Research Notes / Araştırma Notları

> Module / Konu: Statik Analizde Shannon Entropisi ve Mmap Kullanımı
> Date / Tarih: 2026-06-09

---

## What I'm Investigating / Araştırdığım Konu

Klasik string çıkarma yöntemlerinin (örneğin Linux `strings` komutu) ürettiği "gürültüyü" (false positives) nasıl azaltabileceğimi araştırdım. Özellikle JWT token'ları, AWS anahtarları ve şifreleme key'lerini sıradan metinlerden ayırmanın statik bir yolunu bulmam gerekiyordu.

## Resources Found / Bulunan Kaynaklar

- [Shannon Entropy in Cybersecurity](https://en.wikipedia.org/wiki/Entropy_(information_theory)) — Karakter dizilerinin rastgelelik derecesini ölçmek için.
- [Python mmap documentation](https://docs.python.org/3/library/mmap.html) — Büyük dosyaları analiz ederken sistem belleğini yormamak için.

## Key Findings / Temel Bulgular

1. Standart İngilizce metinlerin entropisi genellikle 3.5 ile 4.0 arasında kalıyor. Ancak Base64 ile şifrelenmiş veya rastgele üretilmiş kriptografik anahtarların entropisi 4.5 ve üzerine çıkıyor. Kodda eşiği `4.6` olarak ayarlamak en optimum sonuçları verdi.
2. Android DEX dosyalarındaki stringlerin büyük bir kısmı UTF-16 formatında tutuluyor. ASCII regex'i tek başına çalıştırıldığında bu veriler tamamen gözden kaçıyor.

## Dead Ends / Çıkmaz Sokaklar

- Dosyaları satır satır okuyup analiz etmeye çalıştım ancak binary dosyalarda satır sonu kavramı (`\n`) beklediğim gibi çalışmadığı için script sonsuz döngüye girdi. Dosyayı tek bir byte yığını olarak `mmap` ile RAM'e almak sorunu çözdü.

## Questions Remaining / Kalan Sorular

- [ ] Obfuscation yapılmış (isimleri gizlenmiş) sınıfların veya metodların entropi skorları üzerinden otomatik olarak tespit edilmesi sağlanabilir mi?
