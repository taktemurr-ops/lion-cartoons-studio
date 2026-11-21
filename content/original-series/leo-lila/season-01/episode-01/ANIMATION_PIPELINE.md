# Lion Cartoons S01E01 — gerçek animasyon geliştirme

## Üretilen kaynak
İlk 10 saniyelik hareketli 3D sahnenin Blender Python kaynak dosyası sohbet ekinde: `scene01_blender.py`. Kodda Leo ve Lila'nın üç boyutlu temel gövdeleri, yüzleri, bahçe, icat, hareket eden tohum, kameranın keyframe hareketleri, ışık ve 24 FPS render kurulumu var.

## Net durum
- Blender kaynak kodu yazıldı ve Python sözdizimi kontrolünden geçti.
- Bu çalışma ortamında Blender kurulu olmadığı için sahne render edilmedi, .blend veya MP4 **üretilmedi**.
- Karakterler geçici temel geometrilerdir; profesyonel mesh/rig, animasyon, ses, müzik ve 7 dakikalık bölüm tamamlanmadı.
- Önceki slayt tarzı prototip bu serinin nihai ürünü değildir.

## Yerel render
Blender 4.x kurulu bilgisayarda:
```sh
blender -b -t 4 --python scene01_blender.py
```
Çıktı (Blender render tamamlanırsa): `output/scene01.blend`, `output/scene01_preview.mp4`.
Ses henüz yoktur. Bu çıktı bir teknik animasyon denemesidir, final çizgi film değildir.

## Sonraki teknik kalite aşamaları
1. Mesh topoloji ve orijinal karakter modelleme
2. Rig, IK/FK ve yüz blend-shape
3. Blocking, spline, overlap ve fiziksel komedi zamanlaması
4. Animasyon temizliği ve kamera devamlılığı
5. Doğal oyuncu sesleri ve özgün skorlama
6. Mix, render ve içerik QA
7. Onaydan sonra özel YouTube yükleme
