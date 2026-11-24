# TÜRKAİ'yi iPhone uygulaması yapmak (bilgisayarsız, sadece telefonla)

İki parça var:
1. **Sunucu** (TÜRKAİ'nin beyni): ücretsiz bir bulut hizmetinde (Render) çalışır.
2. **iPhone uygulaması** (kabuk): GitHub Actions ile imzasız IPA olarak derlenir; sen imzalayıp yüklersin. Uygulama açılınca sunucuya bağlanır.

## 0) Depoyu hazırla (bir kez)
1. GitHub'da **Private** yeni bir depo aç ("Add a README" işaretli olsun).
2. **Add file → Upload files** ile bu zip'i **olduğu gibi** yükle → **Commit changes**.
3. **Add file → Create new file** → ad kutusuna `.github/workflows/ios.yml` yaz → içine, bu zip'in içindeki `turkai-main/.github/workflows/ios.yml` dosyasının içeriğini yapıştır → **Commit changes**.
   (GitHub, zip'in içindeki workflow'u çalıştıramaz; bu dosyanın depoda ayrıca durması şart. Zip'i açma işini de bu dosya yapar.)
4. **Actions → iOS imzasız IPA → Run workflow**. İlk iş zip'i açıp dosyaları depoya koyar (zip silinir), ikinci iş IPA'yı derler (10–20 dk).
5. Hata olursa Artifacts'taki `derleme-kayitlari` dosyasını gönder.

## 1) Sunucuyu kur (Render, ücretsiz)
Önce 0. bölümdeki ilk iş bitmiş olmalı: depoda `render.yaml`, `server`, `web` klasörleri görünsün.
1. **render.com** → hesap aç → **New → Blueprint** → GitHub depoyu seç → **Apply**.
2. Sorduğu alanları doldur:
   - `ABACUS_API_KEY`: apps.abacus.ai → LLM APIs'ten aldığın RouteLLM anahtarı (boş bırakırsan DEMO modunda çalışır).
   - `USER_NAME`: TÜRKAİ'nin sana nasıl hitap edeceği.
   - `ELEVENLABS_API_KEY`, `YOUTUBE_API_KEY`: istersen, boş bırakılabilir.
3. `ACCESS_TOKEN` otomatik üretilir. Render panelinde **Environment** bölümünden değerini kopyala (uygulamada gerekecek).
4. Yayın bitince üstte `https://turkai-xxxx.onrender.com` gibi bir adres görünür.

Ücretsiz planın sınırları: 15 dakika kullanılmazsa uyur (ilk açılış ~1 dk sürer); konuşma geçmişi ve kitaplık gibi kayıtlar sunucu yeniden başlayınca silinir (kalıcı disk ücretli).

## 2) IPA'yı indir
Actions'ta biten çalıştırmayı aç → **Artifacts → TURKAI-imzasiz-ipa** dosyasını indir, kendi imzalama aracınla imzala ve yükle.

## 3) İlk açılış
Uygulamayı açınca **sunucu adresini** (Render adresi) ve **erişim anahtarını** (`ACCESS_TOKEN`) gir. Bir kez girmen yeter; sonrakilerde 1,5 sn içinde bağlanır. Adresi değiştirmek için açılışta **Adresi değiştir**'e dokun.

## Bilinmesi gerekenler
- Mikrofon ve kamera izinlerini iPhone ilk kullanımda sorar.
- Uygulama içi tarayıcıda (WKWebView) Safari'nin "Web Konuşma Tanıma"sı yoktur; ses girişi sunucu tarafı ses tanımayla çalışır, biraz daha gecikmeli olabilir.
- Arka planda dinleme ve ekran kapalıyken çalışma sınırlıdır; iOS web sayfalarını arka planda durdurur.
- Uygulama sunucuya bağlı bir kabuktur: internet ve çalışan sunucu şart.
