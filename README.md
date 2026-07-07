# Mini E-Ticaret Uygulaması

Basit bir e-ticaret örneği: ürün listeleme, session tabanlı sepet, admin paneli ve mock ödeme.

Öne çıkanlar:
- Django + PostgreSQL (docker-compose ile)
- Docker + docker-compose
- Testler

Çalıştırma (Docker):

```bash
cp .env.example .env
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

Medya (ürün görselleri) için `media/` dizini container içinde `MEDIA_ROOT` olarak tutulur.
Geliştirme ortamında `DEBUG=1` bırakın; prodüksiyon için bir static/media sunucusu (nginx vb.) önerilir.

API:

- Ürün listesi: `GET /api/products/`
- Ürün detayı: `GET /api/products/{id}/`
- Kategori listesi: `GET /api/categories/`

DRF yüklendiyse ve sunucu çalışıyorsa `api/` altında otomatik browsable API de çalışacaktır.

Demo veri oluşturma:

```bash
docker-compose exec web python ecommerce/manage.py seed_demo
python ecommerce/manage.py seed_demo
```

Komut aşağıdaki öğeleri ekler (eğer mevcut değilse):
- Süper kullanıcı: `admin` / `adminpass`
- Demo kullanıcı: `demo` / `demopass`
- Kategoriler, ürünler, basit görseller ve tek bir varyant

Testler (local environment için):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python ecommerce/manage.py migrate
python ecommerce/manage.py test
```
