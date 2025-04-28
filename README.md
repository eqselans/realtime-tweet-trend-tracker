# Realtime Tweet Trend Tracker

## 📚 Proje Açıklaması

**Realtime Tweet Trend Tracker**, gerçek zamanlı sosyal medya verilerini (tweet simülasyonları) Kafka üzerinden toplayıp, Spark Streaming ile işleyerek en çok geçen kelimeleri analiz eden ve sonuçları Streamlit üzerinden görselleştiren bir trend takip sistemidir.

Bu proje, veri akışı ve işlenmesi konularında Kafka ve Spark gibi büyük veri araçlarının kullanımını, aynı zamanda hızlı prototipleme için Streamlit ile veri görselleştirmeyi göstermektedir.

---

## 🧱 Mimari Bileşenler

```
Kafka Producer (Fake Tweet Üretimi) 
    ↓
Apache Kafka Topic (tweets) 
    ↓
Spark Streaming (spark_streaming.py)
    - Kafka'dan veri okuma
    - Hashtag'leri ayrıştırma
    - Kelime frekans analizi
    - Parquet dosyalarına yazma
    ↓
Parquet Dosyaları (.parquet)
    ↓
Streamlit Uygulaması (streamlit_app.py)
    - Parquet dosyalarını okuma
    - Hashtag frekanslarını gruplayıp sıralama
    - Bar chart ile görselleştirme
    - 10 saniyede bir sayfa yenileme
```

---

## ⚙️ Kullanılan Teknolojiler

- **Apache Kafka** (Veri Akışı)
- **Apache Spark Streaming** (Gerçek Zamanlı Veri İşleme)
- **Streamlit** (Veri Görselleştirme)
- **Docker & Docker Compose** (Orkestrasyon)
- **Python** (Producer & Streamlit Uygulaması)

---

## 🚀 Kurulum Talimatları

### 1. Depoyu Klonla
```bash
git clone https://github.com/eqselans/realtime-tweet-trend-tracker.git
cd realtime-tweet-trend-tracker
```

### 2. Docker Compose Ortamını Başlat
```bash
docker-compose up --build
```

### 3. Spark Streaming Job'u Çalıştır
```bash
docker exec -it spark-container-name spark-submit /app/spark_streaming.py
```

### 4. Kafka Producer'ı Başlat
```bash
python ./fake_tweet_producer.py
```

### 5. Streamlit Dashboard'u Başlat
```bash
streamlit run streamlit_app.py
```

---

## 📊 Özellikler

- Gerçek zamanlı hashtag trend analizi
- En çok geçen hashtaglerin bar grafiği
- 10 saniyede bir otomatik yenilenen dashboard
- Kafka üzerinden gerçek zamanlı veri akışı
- Spark Structured Streaming ile veri işleme
- Parquet dosyaları ile veri saklama

---

## 📁 Proje Yapısı

```
/producer
  ├── fake_tweet_producer.py   # Kafka producer ile tweet simülasyonu
/spark
  ├── spark_streaming.py       # Spark Structured Streaming jobu
streamlit_app.py               # Streamlit dashboard uygulaması
/docker-compose.yml            # Tüm servislerin orkestrasyonu
/output                        # Spark'ın yazdığı .parquet dosyaları
/checkpoint                    # Spark checkpoint verileri
```

---

## 👤 Geliştirici

**Emirhan Aksu**

---
## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.
