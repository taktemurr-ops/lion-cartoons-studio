# Lion Cartoons — Üretim Hattı (LC-GP02)

## Gerçek durum
Bu depo bir **üretim altyapısı taslağıdır**. Senaryoların kayıt altına alınması, yapısal doğrulama ve YouTube OAuth yükleme kodu bulunur. Animasyon render motoru, TTS/müzik servisleri ve Google OAuth kimlik bilgileri bağlı değildir. GitHub Actions kendi başına tam çizgi film üretmez.

## Aşamalar
1. Fikir ve özgünlük incelemesi; benzer karakter, müzik, görsel veya senaryo kopyalama yok.
2. Yaş grubu ve eğitim çıktıları; her yaş grubu için ayrı tempo/dil.
3. Senaryo → sahne listesi → storyboard → çekim listesi.
4. Kilitlenmiş özgün karakter model paketi ve mekân kütüphanesi.
5. Animasyon ve efekt üretimi; her sahnenin tutarlılık kontrolü.
6. Özgün müzik/efekt ve lisans kaydı.
7. Türkçe seslendirme, zaman kodları, dudak senkronizasyonu.
8. Yerelleştirme: çeviri, uzman incelemesi, ses, altyazı.
9. QA kapısı: güvenlik, teknik çözünürlük, ses seviyesi, içeriğin doğruluğu, telif.
10. Onaylanmış ana MP4, kapak ve yayın metni; yalnızca yetkili YouTube OAuth ile önce **private** yükleme.

## Kalite kapısı
- Küfür, yetişkin içeriği, cinsel içerik, aşırı şiddet, korkutma, ayrımcılık bulunmamalı.
- Çocukları tehlikeli hareketleri taklit etmeye yönlendiren sahneler bulunmamalı.
- Eğitim bilgileri doğrulanmalı; aşırı uyaran ve ani yüksek ses kullanılmamalı.
- Yalnızca kullanım hakları doğrulanmış müzik/ses/görsel kullanılmalı.
- Çocuklara özel içerik ayarları doğrulanmalı.
- Tam bölümün insan incelemesi olmadan public yapılmamalı.

## Dosya durumu
content/episodes.json içindeki `status` üretim aşamasını belirtir; bunlar yayımlanmış içerik sayısı değildir.
