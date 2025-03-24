from collections import defaultdict, deque
import heapq
from matplotlib import pyplot as plt
import networkx as nx
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))
    
    def __lt__(self, other: 'Istasyon') -> bool:
        # Burada istasyonun id'sine göre karşılaştırma yapıyoruz
        return self.idx < other.idx

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None 
            #Verilen başlangıç noktasının ve hedef noktasının istasyonlar sözlük yapısı içerisinde olup olmadığını kontrol
            #eder ve nokta istasyon değil ise none dönderir.
        
        kuyruk = deque([(self.istasyonlar[baslangic_id], [])]) #Başlangıç noktası ile istasyonlar kuyruğu
        ziyaret_edildi = set() #İstasyonların ziyaret edilip edilmediğini bilgisini tutan küme
        
        while kuyruk: #Kuyruk boşalana kadar döngü başlatılır
            mevcut, yol = kuyruk.popleft() #Mevcut noktayı ve yolunu kuyruktan çeker
            if mevcut.idx == hedef_id: #Mevcut nokta hedef noktaya eşit ise yol bilgisine mevcut nokta yolunu ekleyip yazdırır.
                return yol + [mevcut]
            
            ziyaret_edildi.add(mevcut.idx) # Mevcut nokta hedef noktaya eişt değil ise o noktayı ziyaret edilenler dizisine ekler
            for komsu, _ in mevcut.komsular: #Mevcut noktanın tüm komşuları için döngüyü başlatır
                if komsu.idx not in ziyaret_edildi:
                    kuyruk.append((komsu, yol + [mevcut]))
                    #Komşu nokta ziyaret edilenler dizisinde değil ise komşu noktayı kuyruğa ekler ve yol bilgisine o komşuya gidilen yolu ekler
        
        return None

            

    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
         #Verilen başlangıç noktasının ve hedef noktasının istasyonlar sözlük yapısı içerisinde olup olmadığını kontrol eder 
         # ve nokta istasyon değil ise none dönderir.
        
        oncelikli_kuyruk = [(0, self.istasyonlar[baslangic_id], [])]  # (toplam_sure, istasyon, rota) 
        ziyaret_edildi = {}
        #Fonksiyon da kullanılması için öncelikli kuyruk ve ziyaret edildi kümesi oluşturulur.
        while oncelikli_kuyruk: # Oluşturulan öncelikli kuyruk boşalana kadar döngü başlatılır.
            sure, mevcut, yol = heapq.heappop(oncelikli_kuyruk) #süre, mevcut nokta ve noktaya giden yol kuyruktan çekilir.
            if mevcut.idx in ziyaret_edildi and ziyaret_edildi[mevcut.idx] <= sure:
                continue # kuyruktan çekilen nokta ziyaret edilenler dizisinde 
            #ve o dizinin mevcut elemanı süreden küçük ise döngü devam eder.
            
            ziyaret_edildi[mevcut.idx] = sure #mevcut nokta süresi, süre olarak alınır
            if mevcut.idx == hedef_id:
                return yol + [mevcut], sure
            #mevcut nokta hedef noktaya eşit ise yola mevcut nokta yolu eklenerek yol ve süre yazdırılır.
            for komsu, ekstra_sure in mevcut.komsular: #mevcut noktanın tüm komşuları için döngü başlatılır
                heapq.heappush(oncelikli_kuyruk, (sure + ekstra_sure, komsu, yol + [mevcut]))
                #mevcut noktanın komşu noktası için yeni süre ve yol hesaplanır.
                #Komşu nokta güncellenmiş süre ve rota bilgisi ile kuyruğa eklenir.
        
        return None
    
    def metro_gorsellestir(self, rota: Optional[List[Istasyon]] = None, baslik: Optional[str] = None): #Çıktıyı görselleştirme fonksiyonu
        if not rota:
            print("Görselleştirme için rota bulunamadı.")
            return
        
        G = nx.Graph()
        hat_colors = {"Kırmızı Hat": "red", "Mavi Hat": "blue", "Turuncu Hat": "orange"}  # Hat renkleri

        # Sadece rotadaki istasyonları ve bağlantıları ekle
        for i in range(len(rota) - 1):
            istasyon1 = rota[i]
            istasyon2 = rota[i + 1]
            G.add_node(istasyon1.idx, label=istasyon1.ad, color=hat_colors.get(istasyon1.hat, "gray"))
            G.add_node(istasyon2.idx, label=istasyon2.ad, color=hat_colors.get(istasyon2.hat, "gray"))
            G.add_edge(istasyon1.idx, istasyon2.idx)
        
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)  # İstasyonların konumlarını belirle
        labels = nx.get_node_attributes(G, 'label')
        node_colors = [nx.get_node_attributes(G, 'color')[node] for node in G.nodes()]
        
        # Rota çizimi
        nx.draw(G, pos, with_labels=True, labels=labels, node_color=node_colors, edge_color='green', width=2, node_size=700)
        if baslik:
            plt.title(baslik, fontsize=12, pad=20)
        else:
            plt.title("Metro Ağı - Algoritma Sonucu", fontsize=12, pad=20)
        
    
        plt.figtext(0.5, 0.01, baslik, ha="center", fontsize=10, bbox={"facecolor": "white", "alpha": 0.6, "pad": 5})
        
        plt.show()


# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        baslik = "AŞTİ'den OSB'ye en az aktarmalı rota: " + " -> ".join(i.ad for i in rota)
        metro.metro_gorsellestir(rota,baslik)
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
        baslik = f"AŞTİ'den OSB'ye en hızlı rota ({sure} dakika): "+ " -> ".join(i.ad for i in rota)
        metro.metro_gorsellestir(rota, baslik)
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        baslik = "Batıkent'ten Keçiören'e en az aktarmalı rota: " + " -> ".join(i.ad for i in rota)
        metro.metro_gorsellestir(rota,baslik)
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
        baslik = f"Batıkent'ten Keçiören'e en hızlı rota ({sure} dakika): "+ " -> ".join(i.ad for i in rota)
        metro.metro_gorsellestir(rota, baslik)
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        baslik = "Keçiören'den AŞTİ'ye en az aktarmalı rota: " + " -> ".join(i.ad for i in rota)
        metro.metro_gorsellestir(rota, baslik)
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
        baslik = f"Keçiören'den AŞTİ'ye en hızlı rota ({sure} dakika): "+ " -> ".join(i.ad for i in rota) 
        metro.metro_gorsellestir(rota, baslik)


   

