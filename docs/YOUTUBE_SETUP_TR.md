# YouTube Yetkilendirmesi — Güvenli Kurulum

Windsor.ai bağlantısı **analiz ve bazı kanal düzenlemeleri** içindir; yeni video yükleme yetkisi vermez.

Bu repodaki scripts/upload_youtube.py, YouTube Data API OAuth erişimi ile kullanılabilir fakat erişim hâlen kurulmuş değildir.

1. Google Cloud Console'da kendin kontrol ettiğin projeyi aç, YouTube Data API v3'ü etkinleştir.
2. OAuth izin ekranı ve Desktop client oluştur; indirilen dosyayı yalnızca bilgisayarında `client_secret.json` olarak tut.
3. İlk OAuth girişini aynı kanalı yöneten Google hesabıyla gerçekleştir.
4. `python scripts/upload_youtube.py --file PATH_TO_REVIEWED_MP4 --title "Başlık" --made-for-kids --expected-channel-id KANAL_ID` komutuyla önce dry-run yap.
5. Gerçek yükleme için `--publish` gerekir. Varsayılan gizlilik `private`'tır. Yanlış kanala yüklememek için beklenen kanal ID'si zorunludur.
6. GitHub Actions için token yapılandırılırsa Secret olarak sakla; tokenları commit'leme.

**Not:** Bu prosedür kullanıcı adına otomatik Google yetkisi vermez. Kanalın izin ekranının kullanıcı tarafından onaylanması gerekir.
