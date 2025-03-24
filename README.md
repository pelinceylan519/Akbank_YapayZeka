# Akbank_YapayZeka
# Metro Ağı Rota Planlayıcı

## 1. Proje Başlığı ve Kısa Açıklama
**Metro Ağı Rota Planlayıcı**, belirlenen metro istasyonları arasında en hızlı ve en az aktarma ile gidilebilecek rotaları hesaplayan bir Python projesidir. Proje, istasyonlar arasındaki bağlantıları grafik veri yapısı olarak modelleyerek, BFS (Breadth-First Search) ve A* (A-Star) algoritmalarını kullanarak optimum rotaları bulur. Ayrıca NetworkX ve Matplotlib kütüphaneleriyle rotaları görselleştirir.

## 2. Kullanılan Teknolojiler ve Kütüphaneler
Proje, aşağıdaki Python kütüphanelerini kullanmaktadır:

- **collections**: `defaultdict` ile veri yapılarını oluşturmak ve `deque` ile BFS algoritmasında kuyruk yapısını kullanmak için kullanılır.
- **heapq**: A* algoritmasında öncelikli kuyruk (priority queue) veri yapısını yönetmek için kullanılır.
- **matplotlib.pyplot**: Metro ağını ve rotaları görselleştirmek için kullanılır.
- **networkx**: Metro ağı grafiğini oluşturmak ve çizmek için kullanılır.
- **typing**: Tür ipuçları sağlamak için kullanılır (Dict, List, Tuple, Optional gibi).

## 3. Algoritmaların Çalışma Mantığı

### BFS Algoritması (Breadth-First Search)
**Amaç:** En az aktarmalı rotayı bulmak için kullanılır.

**Çalışma Mantığı:**
- Başlangıç istasyonundan hareket ederek tüm komşuları sırayla ziyaret eder.
- Kuyruk (queue) veri yapısı kullanılarak en kısa adım sayısı ile hedefe ulaşılır.
- İlk bulunan çözüm, en az aktarma yapılan rota olarak kabul edilir.

### A* (A-Star) Algoritması
**Amaç:** En hızlı rotayı bulmak için kullanılır.

**Çalışma Mantığı:**
- Öncelikli kuyruk (priority queue) kullanarak en düşük maliyetli (süre bazlı) yolu seçer.
- `heapq` modülü ile en kısa sürede hedefe ulaşan yol hesaplanır.
- BFS'den farklı olarak, ziyaret edilen düğümler arasında en kısa sürede ulaşılabilir olanı önceliklendirir.

### Neden Bu Algoritmalar Kullanıldı?
- **BFS**, en az aktarma yapılan rotayı bulmak için uygundur çünkü her düğümü eşit seviyede genişleterek en kısa aktarma sayısına ulaşır.
- **A* algoritması**, süre bazlı en kısa rotayı bulmak için uygundur çünkü her düğümü en az toplam süreyle seçerek hedefe ulaşmayı garanti eder.

## 4. Örnek Kullanım ve Test Sonuçları
Projeyi çalıştırarak aşağıdaki test senaryolarını çalıştırabilirsiniz:

### Örnek Senaryolar:
1. **AŞTİ'den OSB'ye en hızlı ve en az aktarmalı rota**
2. **Batıkent'ten Keçiören'e en hızlı ve en az aktarmalı rota**
3. **Keçiören'den AŞTİ'ye en hızlı ve en az aktarmalı rota**

Çıktılar:
- En az aktarmalı rota metin olarak yazdırılır.
- En hızlı rota süresi ve istasyon sırası gösterilir.
- Görselleştirme sayesinde rotalar grafik olarak gösterilir.

## 5. Test Senaryoları
Projede kullanılan fonksiyonların doğruluğunu test etmek için aşağıdaki test senaryoları uygulanmıştır:

### Senaryo 1: AŞTİ'den OSB'ye Yolculuk
- **Giriş:** `en_az_aktarma_bul("M1", "K4")`
- **Beklenen Çıktı:** En az aktarma yapılan istasyon listesi.
- **Giriş:** `en_hizli_rota_bul("M1", "K4")`
- **Beklenen Çıktı:** En kısa süreli rota ve toplam süre.

### Senaryo 2: Batıkent'ten Keçiören'e Yolculuk
- **Giriş:** `en_az_aktarma_bul("T1", "T4")`
- **Beklenen Çıktı:** En az aktarma yapılan istasyon listesi.
- **Giriş:** `en_hizli_rota_bul("T1", "T4")`
- **Beklenen Çıktı:** En kısa süreli rota ve toplam süre.

### Senaryo 3: Keçiören'den AŞTİ'ye Yolculuk
- **Giriş:** `en_az_aktarma_bul("T4", "M1")`
- **Beklenen Çıktı:** En az aktarma yapılan istasyon listesi.
- **Giriş:** `en_hizli_rota_bul("T4", "M1")`
- **Beklenen Çıktı:** En kısa süreli rota ve toplam süre.

## 6. Projeyi Geliştirme Fikirleri
- **Gerçek zamanlı trafik verisi entegrasyonu:** Güncel yoğunluk ve gecikmelere göre rotaları dinamik olarak hesaplama.
- **Harita entegrasyonu:** Metro istasyonlarının gerçek konumlarını harita üzerinde göstermek.
- **Kullanıcı dostu arayüz:** Web veya mobil uygulama üzerinden rota planlama.
- **Daha fazla ulaşım ağı desteği:** Otobüs, tramvay, ve diğer toplu taşıma araçlarını sisteme dahil etme.

Bu proje, metro yolculuklarını daha verimli hale getirmek için temel bir altyapı sunmaktadır. İleriye dönük olarak, gerçek zamanlı veri desteğiyle daha gelişmiş bir ulaşım planlama sistemi oluşturulabilir.

