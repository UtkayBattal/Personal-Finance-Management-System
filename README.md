# 💰 Personal Finance Management System

Modern ve kullanıcı dostu bir kişisel finans yönetim sistemi. Flask web framework'ü kullanılarak geliştirilmiş, SQLite veritabanı ile desteklenen ve makine öğrenmesi algoritmaları ile gelecek harcama tahminleri sunan kapsamlı bir finansal takip uygulaması.

## 🚀 Özellikler

### 📊 Temel Fonksiyonlar
- **Gelir-Gider Takibi**: Detaylı kategori bazlı gelir ve gider kayıtları
- **Bütçe Yönetimi**: Aylık ve yıllık bütçe planlaması ve takibi
- **İstatistiksel Analiz**: Kategori bazlı harcama analizi ve görselleştirme
- **Gelişmiş Arama**: Çoklu kriter ile işlem arama ve filtreleme

### 🤖 Makine Öğrenmesi Özellikleri
- **SARIMA Tahmin Modeli**: Geçmiş verilere dayalı 6 aylık harcama tahminleri
- **Akıllı Bütçe Uyarıları**: Bütçe limitlerine yaklaşma durumunda otomatik uyarılar
- **Trend Analizi**: Aylık ve günlük harcama trendlerinin analizi

### 🎨 Kullanıcı Deneyimi
- **Modern UI/UX**: Glassmorphism tasarım ile modern arayüz
- **Responsive Tasarım**: Mobil ve masaüstü uyumlu tasarım
- **Gerçek Zamanlı Grafikler**: Chart.js ile interaktif veri görselleştirme
- **Otomatik Bildirimler**: Başarı/hata mesajları ile kullanıcı geri bildirimi

## 🛠️ Teknoloji Stack'i

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM (Object-Relational Mapping)
- **Flask-Migrate**: Veritabanı migration yönetimi
- **Flask-Login**: Kullanıcı oturum yönetimi
- **Werkzeug**: Güvenli şifre hash'leme

### Frontend
- **HTML5/CSS3**: Modern web standartları
- **JavaScript (ES6+)**: Dinamik arayüz işlevselliği
- **Chart.js**: İnteraktif grafik ve çizelgeler
- **Font Awesome**: İkon kütüphanesi
- **Google Fonts (Poppins)**: Modern tipografi

### Veri Analizi ve ML
- **Pandas**: Veri manipülasyonu ve analizi
- **NumPy**: Sayısal hesaplamalar
- **Statsmodels**: SARIMA zaman serisi analizi
- **Scikit-learn**: Makine öğrenmesi araçları

### Veritabanı
- **SQLite**: Hafif ve taşınabilir veritabanı
- **Alembic**: Veritabanı migration sistemi

## 📁 Proje Yapısı

```
Personal-Finance-Management-System/
├── app/                          # Ana uygulama paketi
│   ├── __init__.py              # Flask app factory ve konfigürasyon
│   ├── models.py                # Veritabanı modelleri (User, Transaction, Budget)
│   ├── routes.py                # URL routing ve view fonksiyonları
│   └── forms.py                 # WTForms ile form tanımları
├── templates/                   # Jinja2 HTML şablonları
│   ├── index.html              # Ana sayfa
│   ├── auth.html               # Giriş/kayıt sayfası
│   ├── dashboard.html          # Ana kontrol paneli
│   ├── add_transaction.html    # İşlem ekleme sayfası
│   └── add_budget.html         # Bütçe ekleme sayfası
├── static/                     # Statik dosyalar (CSS, JS, resimler)
│   ├── dashboard.css           # Dashboard stil dosyası
│   ├── index.css              # Ana sayfa stil dosyası
│   ├── auth.css               # Kimlik doğrulama sayfası stilleri
│   ├── add_transaction.css    # İşlem ekleme sayfası stilleri
│   └── add_budget.css         # Bütçe ekleme sayfası stilleri
├── migrations/                 # Veritabanı migration dosyaları
│   ├── env.py                 # Alembic konfigürasyonu
│   ├── alembic.ini            # Alembic ayarları
│   └── script.py.mako         # Migration şablonu
├── instance/                   # Uygulama instance dosyaları
│   └── finance.db             # SQLite veritabanı dosyası
├── run.py                      # Uygulama başlatma dosyası
├── system_test.py             # Kapsamlı test suite
└── app_debug.log              # Uygulama log dosyası
```

## 🔧 Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.8+
- pip (Python paket yöneticisi)

### Adım 1: Projeyi Klonlayın
```bash
git clone https://github.com/UtkayBattal/Personal-Finance-Management-System.git
cd Personal-Finance-Management-System
```

### Adım 2: Sanal Ortam Oluşturun (Önerilen)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### Adım 3: Gerekli Paketleri Yükleyin
```bash
pip install flask
pip install flask-sqlalchemy
pip install flask-migrate
pip install flask-login
pip install flask-wtf
pip install wtforms
pip install pandas
pip install numpy
pip install statsmodels
pip install scikit-learn
pip install werkzeug
```

### Adım 4: Veritabanını Başlatın
```bash
# Migration klasörünü başlat
flask db init

# İlk migration'ı oluştur
flask db migrate -m "Initial migration"

# Migration'ı uygula
flask db upgrade
```

### Adım 5: Uygulamayı Çalıştırın
```bash
python run.py
```

Uygulama `http://localhost:5000` adresinde çalışacaktır.

## 📊 Veritabanı Şeması

### User Tablosu
- `id`: Birincil anahtar
- `username`: Kullanıcı adı (benzersiz)
- `email`: E-posta adresi (benzersiz)
- `password`: Hash'lenmiş şifre
- `is_active`: Aktif durum
- `created_at`: Hesap oluşturma tarihi

### Transaction Tablosu
- `id`: Birincil anahtar
- `category`: İşlem kategorisi
- `amount`: İşlem miktarı
- `date`: İşlem tarihi
- `type`: İşlem tipi (income/expense)
- `user_id`: Kullanıcı referansı (Foreign Key)

### Budget Tablosu
- `id`: Birincil anahtar
- `category`: Bütçe kategorisi
- `amount`: Bütçe miktarı
- `period`: Bütçe periyodu (Monthly/Yearly)
- `date`: Bütçe oluşturma tarihi
- `user_id`: Kullanıcı referansı (Foreign Key)

## 🎯 Kullanım Kılavuzu

### 1. Hesap Oluşturma ve Giriş
- Ana sayfadan "Get Started" butonuna tıklayın
- Kullanıcı adı, e-posta ve şifre ile hesap oluşturun
- Giriş yapın ve dashboard'a erişin

### 2. İşlem Ekleme
- Dashboard'da "Add Transaction" sekmesini seçin
- İşlem tipini (Gelir/Gider) seçin
- Kategori ve miktarı girin
- "Add" butonuna tıklayın

### 3. Bütçe Yönetimi
- "Budget" sekmesini seçin
- Kategori, miktar ve periyodu belirleyin
- Bütçe limitlerini takip edin

### 4. İstatistiksel Analiz
- "Statistics" sekmesini seçin
- Grafik türünü seçin (Gider/Gelir/Bütçe)
- Zaman periyodunu belirleyin
- Detaylı analizleri görüntüleyin

### 5. İşlem Arama
- "Search Transaction" sekmesini seçin
- Arama kriterlerini belirleyin
- Sonuçları filtreleyin

## 🧪 Test Sistemi

Proje kapsamlı bir test suite'i içerir (`system_test.py`):

### Test Kategorileri
1. **Birim Testleri**: Model oluşturma ve doğrulama
2. **Performans Testleri**: SARIMA tahmin ve dashboard yükleme
3. **Güvenlik Testleri**: Şifre güvenliği ve yetkisiz erişim
4. **Kullanıcı Deneyimi Testleri**: Form validasyonu ve hata yönetimi
5. **Veri Doğrulama Testleri**: İşlem ve bütçe kontrolleri

### Test Çalıştırma
```bash
python system_test.py
```

## 🔒 Güvenlik Özellikleri

- **Şifre Hash'leme**: PBKDF2-SHA256 ile güvenli şifre saklama
- **Session Yönetimi**: Flask-Login ile güvenli oturum kontrolü
- **CSRF Koruması**: WTForms ile form güvenliği
- **Input Validasyonu**: Tüm kullanıcı girdilerinin doğrulanması
- **SQL Injection Koruması**: SQLAlchemy ORM ile güvenli veritabanı sorguları

## 📈 Makine Öğrenmesi Özellikleri

### SARIMA Tahmin Modeli
- **Zaman Serisi Analizi**: Geçmiş harcama verilerine dayalı tahmin
- **Mevsimsel Düzeltme**: Aylık döngülerin analizi
- **6 Aylık Tahmin**: Gelecek harcamaların öngörülmesi
- **Güven Aralıkları**: Tahminlerin güvenilirlik analizi

### Akıllı Uyarı Sistemi
- **Bütçe Limit Kontrolü**: %80 ve %100 limit uyarıları
- **Trend Analizi**: Harcama artış/azalış trendleri
- **Anomali Tespiti**: Olağandışı harcama kalıpları

## 🎨 Tasarım Özellikleri

### Glassmorphism Tasarım
- **Şeffaf Kartlar**: Modern cam efekti ile kartlar
- **Backdrop Filter**: Bulanık arka plan efektleri
- **Gradient Arka Planlar**: Çok katmanlı renk geçişleri
- **Responsive Grid**: Esnek düzen sistemi

### Renk Paleti
- **Primary**: #1a365d (Koyu mavi)
- **Secondary**: #2c5282 (Orta mavi)
- **Accent**: #48bb78 (Yeşil)
- **Background**: rgba(247, 250, 252, 0.85) (Açık gri)

## 🚀 Performans Optimizasyonları

- **Veritabanı İndeksleme**: Sık sorgulanan alanlar için indeksler
- **Lazy Loading**: İlişkili verilerin ihtiyaç halinde yüklenmesi
- **Caching**: Statik verilerin önbelleklenmesi
- **Query Optimization**: Veritabanı sorgularının optimize edilmesi

## 🔧 Geliştirme ve Katkıda Bulunma

### Geliştirme Ortamı Kurulumu
1. Projeyi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

### Kod Standartları
- **PEP 8**: Python kod stil rehberi
- **Type Hints**: Fonksiyon parametrelerinde tip belirtimi
- **Docstrings**: Fonksiyon ve sınıf dokümantasyonu
- **Error Handling**: Kapsamlı hata yönetimi

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 👨‍💻 Geliştirici

**Utkay Güngör Battal**
- GitHub: [@UtkayBattal](https://github.com/UtkayBattal)
- LinkedIn: [Utkay Güngör Battal](https://www.linkedin.com/in/utkay-güngör-battal-951497263/)

## 🙏 Teşekkürler

- **Flask Community**: Harika web framework
- **Chart.js**: İnteraktif grafik kütüphanesi
- **Font Awesome**: İkon kütüphanesi
- **Google Fonts**: Poppins font ailesi
- **Statsmodels**: Zaman serisi analizi araçları

## 📞 İletişim

Sorularınız, önerileriniz veya hata raporları için:
- GitHub Issues kullanın
- E-posta gönderin
- LinkedIn üzerinden iletişime geçin

---

**Not**: Bu proje eğitim amaçlı geliştirilmiştir. Gerçek finansal verileriniz için ek güvenlik önlemleri alınması önerilir.
