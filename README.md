# IoT System Monitor Backend

Bir sensörden (CPU/RAM/disk kullanımı) toplanan verinin MQTT üzerinden bir
backend'e taşındığı, PostgreSQL'e kaydedildiği ve FastAPI ile dışarıya
sunulduğu uçtan uca bir IoT veri işleme hattı. Backend altyapısı (veritabanı,
MQTT broker, API, dinleyici) Docker Compose ile 4 konteynerde çalışır;
sensör ise host makinenin gerçek kaynaklarını ölçebilmesi için bilinçli
olarak konteynerin dışında, native çalıştırılır.


## Mimari

[sensor (native)] --publish--> [mosquitto] --subscribe--> [listener] --write--> [postgres] <--read-- [api]

| Servis | Nerede çalışır | Görevi |
|---|---|---|
| `sensor` | Host (native, `py main.py`) | `psutil` ile CPU/RAM/disk okur, saniyede bir MQTT'ye yayınlar |
| `mosquitto` | Docker (`iot_mosquitto`) | MQTT broker |
| `listener` | Docker (`iot_listener`) | MQTT'yi dinler, gelen veriyi doğrulayıp PostgreSQL'e yazar |
| `api` | Docker (`iot_api`) | FastAPI — kayıtlı metrikleri REST üzerinden sunar |
| `postgres` | Docker (`iot_postgres`) | Veritabanı, şema `db/schema.sql`'den otomatik kurulur |

`api` ve `listener` aynı kod tabanını ve aynı Docker image'ini paylaşır,
yalnızca çalıştırdıkları komut farklıdır.


### Sensör neden konteynerde değil?

Konteynerize edilmiş bir izleme aracı, host'un gerçek CPU/RAM/disk
kullanımını değil, kendi cgroup sınırları içindeki (Docker Desktop'ın
Windows'ta çalıştırdığı WSL2 sanal makinesinin) kaynak kullanımını ölçer.
Bu, sensörün amacına (gerçek bilgisayar durumunu göstermek) ters
düştüğü için bilinçli olarak native çalıştırılıyor — mosquitto'nun
`1883` portu host'a açık olduğundan sensör `localhost:1883` üzerinden
brokera sorunsuz bağlanabiliyor.


## Teknolojiler

Python 3.12 · FastAPI · PostgreSQL 16 · Eclipse Mosquitto (MQTT) ·
psycopg3 + connection pooling · Docker Compose · pytest


## Çalıştırma

1. Proje kökünde bir `.env` dosyası oluştur:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=iot_backend
DB_USER=postgres
DB_PASSWORD=<kendi şifren>

(`DB_HOST` yalnızca Docker'sız yerel geliştirme için kullanılır;
   konteyner içi servisler birbirine `docker-compose.yml`'deki servis
   adlarıyla ulaşır, bkz. `DB_HOST: postgres`.)

2. Backend altyapısını ayağa kaldır:
```bash
   docker compose up --build -d
```

3. Sensörü native çalıştır (ayrı bir terminalde):
```bash
   py main.py
```

4. Servislerin durumunu kontrol et:
```bash
   docker compose ps
```

5. API'yi test et:
```bash
   curl http://localhost:8000/metrics/latest
```


## API Uç Noktaları

| Endpoint | Açıklama |
|---|---|
| `GET /` | Sağlık kontrolü / karşılama mesajı |
| `GET /metrics` | Kaydedilmiş tüm metrikler |
| `GET /metrics/latest` | En son kaydedilen metrik |
| `GET /dashboard` | Basit HTML dashboard |
| `GET /docs` | Otomatik oluşturulan Swagger/OpenAPI dokümantasyonu |


## Testler

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

Servis katmanı testleri gerçek bir veritabanı veya MQTT broker'ı
gerektirmez — repository'ler mock'lanarak izole şekilde çalışır.


## Öne Çıkan Tasarım Kararları

- **Katmanlı hata yönetimi**: repository → servis → MQTT/API sınırlarında
  özel exception tipleri (`backend/exceptions.py`) kullanılır; her katman
  hatayı kendi bağlamında (log seviyesi, HTTP status kodu) karşılar.
- **Test edilebilirlik**: `SystemMetricsService`, repository'leri
  constructor'dan enjekte edebilir; testler gerçek DB'ye dokunmaz.
- **Sensör bilinçli olarak native**: konteynerize edilmiş bir monitoring
  agent'ın host metriklerini değil, kendi kaynak sınırlarını ölçtüğü
  fark edilip mimari buna göre düzeltildi.


## Proje Yapısı

api/ FastAPI uygulaması
backend/ exception'lar, logging, DB bağlantısı, repository/servis katmanları
mqtt/ MQTT client/publisher/subscriber
sensor/ sistem metrik sensörü (native çalışır)
db/ şema ve seed SQL dosyaları
mosquitto/ MQTT broker config'i
tests/ pytest birim testleri
docker-compose.yml
Dockerfile api + listener için ortak image