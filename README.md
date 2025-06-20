# Gelişmiş To-Do List Uygulaması (Python & Tkinter)

Bu proje, Python'un `tkinter` ve `ttkbootstrap` kütüphaneleri kullanılarak geliştirilmiş, modern ve zengin özelliklere sahip bir masaüstü yapılacaklar listesi uygulamasıdır. Kullanıcıların görevlerini listeler halinde organize etmelerine, alt görevler oluşturmalarına ve görevlerini etkin bir şekilde yönetmelerine olanak tanır.



## 🚀 Özellikler

- **Modern ve Duyarlı Arayüz:** `ttkbootstrap` kullanılarak oluşturulmuş şık ve temiz bir kullanıcı arayüzü.
- **Açık ve Koyu Tema Desteği:** Kullanıcılar, tek bir tıkla aydınlık (`litera`) ve karanlık (`darkly`) temalar arasında geçiş yapabilir.
- **Çoklu Liste Yönetimi:** Farklı projeler veya kategoriler için birden çok yapılacaklar listesi oluşturma, silme ve bunlar arasında geçiş yapma.
- **Hiyerarşik Görev Yapısı (Alt Görevler):** Karmaşık görevleri daha küçük, yönetilebilir alt görevlere bölme imkanı.
- **Görev Detayları:**
  - **Öncelik Atama:** Görevlere "Yüksek", "Normal", "Düşük" gibi öncelik seviyeleri belirleme.
  - **Son Tarih (Due Date):** Her göreve bir bitiş tarihi ekleme.
  - **Not Ekleme:** Görevlerle ilgili detaylı notlar veya açıklamalar için çok satırlı metin alanı.
- **Toplu İşlemler:** `Ctrl` tuşu ile birden fazla görev seçerek toplu olarak silme veya tamamlama.
- **Veri Kalıcılığı:** Tüm görevler ve listeler, uygulama kapatıldığında `tasks.json` dosyasına kaydedilir ve yeniden açıldığında geri yüklenir.
- **Geriye Dönük Uyumluluk:** Uygulamanın eski versiyonlarından kalan görev verilerini otomatik olarak yeni formata dönüştürür.

## 🛠️ Kullanılan Teknolojiler

- **Python 3.x**
- **Tkinter:** Python'un standart GUI (Grafiksel Kullanıcı Arayüzü) kütüphanesi.
- **ttkbootstrap:** `tkinter` için modern temalar ve widget'lar sağlayan harici bir kütüphane.

## ⚙️ Kurulum ve Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin. Projenin bağımlılıklarını sisteminizden izole etmek için bir **sanal ortam (virtual environment)** kullanılması şiddetle tavsiye edilir.

### 1. Projeyi Klonlama veya İndirme

Öncelikle, bu depoyu bilgisayarınıza klonlayın veya ZIP olarak indirin.
```bash
git clone https://github.com/firatyerlikaya/Todo-List-App.git
cd Todo-List-App
```

### 2. Sanal Ortam Oluşturma ve Aktif Etme

Proje klasörünün içindeyken bir sanal ortam oluşturun.

```bash
# Sanal ortamı "venv" adıyla oluştur
python -m venv venv
```

Ardından, oluşturduğunuz sanal ortamı işletim sisteminize göre aktif hale getirin.

- **Windows için:**
  ```powershell
  .\venv\Scripts\activate
  ```

- **macOS / Linux için:**
  ```bash
  source venv/bin/activate
  ```

Komut satırınızın başında `(venv)` ibaresini gördüğünüzde sanal ortam aktif demektir.

### 3. Bağımlılıkları Yükleme

Projenin çalışması için gerekli ttkbootstrap kütüphanesini indirin.

```bash
pip install ttkbootstrap
```

### 4. Uygulamayı Başlatma

Tüm kurulumlar tamamlandıktan sonra, uygulamayı aşağıdaki komutla başlatabilirsiniz:

```bash
python todo_app.py
```

### 5. Sanal Ortamı Kapatma (Deaktif Etme)

Uygulama ile işiniz bittiğinde, sanal ortamdan çıkmak için komut satırına aşağıdaki komutu yazmanız yeterlidir:

```bash
deactivate
```
