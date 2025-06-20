# Yapılacaklar Listesi Uygulaması

Bu, Python ve `tkinter` (Tkinter-bootstrap temalarıyla) kullanılarak geliştirilmiş basit bir yapılacaklar listesi uygulamasıdır. Kullanıcıların görevleri yönetmesine, alt görevler eklemesine, öncelik belirlemesine, son tarihler eklemesine, notlar almasına ve farklı görev listeleri oluşturmasına olanak tanır.

## Özellikler

-   **Görev Yönetimi:** Görev ekleme, silme, tamamlama ve tamamlanmamış olarak işaretleme.
-   **Alt Görevler:** Ana görevlere alt görevler ekleyebilme özelliği.
-   **Görev Detayları:** Her göreve öncelik (Yüksek, Normal, Düşük), son tarih ve notlar ekleyebilme.
-   **Çoklu Görev Listeleri:** Farklı kategorilerde veya projeler için ayrı görev listeleri oluşturma ve yönetme.
-   **Sıralama Seçenekleri:** Görevleri eklenme sırasına, son tarihe, önceliğe veya isme göre sıralama.
-   **Tema Seçimi:** Açık ve koyu tema arasında geçiş yapabilme.
-   **Kalıcılık:** Uygulama kapatıldığında görevlerin `tasks.json` dosyasına kaydedilmesi ve tekrar açıldığında yüklenmesi.

## Kurulum ve Çalıştırma

Bu uygulamayı çalıştırmak için sisteminizde Python 3 yüklü olmalıdır.

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/firatyerlikaya/Todo-List-App.git
    cd Todo-List-App
    ```

2.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install ttkbootstrap
    ```

3.  **Uygulamayı Çalıştırın:**
    ```bash
    python todo_app.py
    ```

## Kullanım

-   **Yeni Görev Ekleme:** "Görev Metni" kutusuna görevinizi yazın, önceliği ve son tarihi seçin, ardından "Görev Ekle" butonuna tıklayın.
-   **Alt Görev Ekleme:** Bir ana görevi seçin ve "Alt Görev Ekle" butonuna tıklayın.
-   **Görevi Düzenleme:** Göreve çift tıklayarak metnini, son tarihini ve notlarını düzenleyebilirsiniz.
-   **Görevi Tamamlama/Tamamlanmadı Olarak İşaretleme:** Bir veya daha fazla görevi seçin ve ilgili "Tamamlandı" veya "Tamamlanmadı" butonlarına tıklayın.
-   **Yeni Liste Oluşturma:** "Yeni Liste" butonuna tıklayarak yeni bir görev listesi oluşturun.
-   **Listeler Arasında Geçiş:** "Aktif Liste" açılır menüsünden farklı görev listeleri arasında geçiş yapın.
-   **Sıralama:** "Sırala" açılır menüsünden görevleri istediğiniz kritere göre sıralayın.
-   **Tamamlananları Temizle:** Mevcut listedeki tüm tamamlanmış görevleri siler.
-   **Tümünü Sil:** Mevcut listedeki tüm görevleri siler.

## Katkıda Bulunma

Geliştirmeye katkıda bulunmaktan çekinmeyin! Her türlü öneri veya hata bildirimi kabul edilir.

1.  Bu depoyu (repository) fork edin.
2.  Yeni bir dal (branch) oluşturun: `git checkout -b feature/your-feature-name`
3.  Değişikliklerinizi yapın ve commit edin: `git commit -m 'Add some feature'`
4.  Dalı push edin: `git push origin feature/your-feature-name`
5.  Bir Pull Request oluşturun.

## Lisans

Bu proje eğitim amaçlıdır. İhtiyacınıza göre kullanıp değiştirebilirsiniz.
