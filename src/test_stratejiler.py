import os
import ast

STRATEJILER_DIZINI = r"c:\Users\MS\Desktop\151-trading-strategies\src\strategies"

# Sonuçları gruplamak için listeler oluşturuyoruz
tek_sinyalliler = []
coklu_agirliklar = []
digerleri = []

# Klasörü tarıyoruz
for kok_dizin, _, dosyalar in os.walk(STRATEJILER_DIZINI):
    for dosya in dosyalar:
        if dosya.endswith(".py") and not dosya.startswith("__"):
            dosya_yolu = os.path.join(kok_dizin, dosya)
            
            with open(dosya_yolu, "r", encoding="utf-8") as f:
                icerik = f.read()
            
            try:
                kod_agaci = ast.parse(icerik)
            except Exception as e:
                print(f"Hata: {dosya} okunurken hata oluştu: {e}")
                continue
            
            # Response sınıflarını arıyoruz
            for dugum in ast.walk(kod_agaci):
                if isinstance(dugum, ast.ClassDef) and dugum.name.endswith("Response"):
                    # Sınıf içindeki değişkenleri topluyoruz
                    alanlar = []
                    for alt_dugum in dugum.body:
                        if isinstance(alt_dugum, ast.AnnAssign) and isinstance(alt_dugum.target, ast.Name):
                            alanlar.append(alt_dugum.target.id)
                        elif isinstance(alt_dugum, ast.Assign):
                            for hedef in alt_dugum.targets:
                                if isinstance(hedef, ast.Name):
                                    alanlar.append(hedef.id)
                    
                    # Dosya adını ve sınıfı kaydediyoruz
                    goreceli_yol = os.path.relpath(dosya_yolu, STRATEJILER_DIZINI)
                    veri = (goreceli_yol, dugum.name, alanlar)
                    
                    # Hangi gruba girdiğini kontrol ediyoruz
                    if "signal" in alanlar:
                        tek_sinyalliler.append(veri)
                    elif "weights" in alanlar:
                        coklu_agirliklar.append(veri)
                    else:
                        digerleri.append(veri)

# Raporu Ekrana Yazdırıyoruz
print("=== STRATEJİ ANALİZ SONUÇLARI ===\n")

print(f"1. Doğrudan tekil 'signal' döndürenler ({len(tek_sinyalliler)} adet):")
for yol, sinif, _ in tek_sinyalliler[:5]: # İlk 5 tanesini gösterelim örnek olarak
    print(f"   - {yol} ({sinif})")
print("   ... ve diğerleri.\n")

print(f"2. Ağırlık ('weights') döndürenler ({len(coklu_agirliklar)} adet):")
for yol, sinif, alanlar in coklu_agirliklar:
    print(f"   - {yol} ({sinif}) -> Alanlar: {alanlar}")
print("\n")

print(f"3. Farklı yapıda çıktı verenler ({len(digerleri)} adet):")
for yol, sinif, alanlar in digerleri[:5]:
    print(f"   - {yol} ({sinif}) -> Alanlar: {alanlar}")
