import pandas as pd
import numpy as np

print("📂 Memproses dataset wisata...")

# Load dataset mentah
df = pd.read_csv('wisata_indonesia_new.csv')

print(f"✅ Load {len(df)} data")

# ============================================
# 1. STANDARISASI KATEGORI
# ============================================
kategori_mapping = {
    'pantai': 'Pantai & Bahari',
    'air terjun': 'Air Terjun & Curug',
    'gunung': 'Gunung & Pendakian',
    'candi': 'Candi & Sejarah',
    'museum': 'Museum & Monumen',
    'taman': 'Taman & Rekreasi',
    'wisata alam': 'Wisata Alam',
    'wisata edukasi': 'Wisata Edukasi',
    'wisata religi': 'Wisata Religi',
    'wisata kuliner': 'Wisata Kuliner',
    'wisata kerajaan': 'Wisata Kerajaan',
    'wisata tematik': 'Wisata Tematik',
    'bukit': 'Bukit',
    'alun-alun': 'Alun-Alun',
    'mall': 'Mall',
    'monumen': 'Monumen',
    'kebun binatang': 'Kebun Binatang',
    'wahana keluarga': 'Wahana Keluarga',
    'lembah': 'Lembah',
    'rumah adat': 'Rumah Adat',
    'cafe view': 'Cafe View',
    'wisata lampion': 'Wisata Lampion',
    'wisata religi': 'Wisata Religi'
}

df['kategori_clean'] = df['kategori'].str.lower().replace(kategori_mapping)
df['kategori_clean'] = df['kategori_clean'].fillna(df['kategori'])

print("✅ Standarisasi kategori selesai")

# ============================================
# 2. ESTIMASI BIAYA REALISTIS
# ============================================
biaya_realistis = {
    'alun-alun': 0,
    'mall': 0,
    'wisata kuliner': 0,
    'pantai publik': 0,
    'candi': 10000,
    'museum': 8000,
    'monumen': 5000,
    'wisata religi': 5000,
    'kebun binatang': 15000,
    'air terjun': 15000,
    'bukit': 15000,
    'gunung': 20000,
    'wisata alam': 15000,
    'wahana keluarga': 25000,
    'wisata edukasi': 20000,
    'pantai': 15000,
    'taman': 10000
}

def get_biaya(row):
    kategori = str(row['kategori_clean']).lower()
    kategori_original = str(row['kategori']).lower()
    nama = str(row['nama_wisata']).lower()
    
    # Wisata gratis
    if any(x in kategori_original for x in ['mall', 'alun-alun', 'kuliner', 'pasar']):
        return 0
    if 'alun' in kategori_original:
        return 0
    if 'kuliner' in kategori:
        return 0
    
    # Pantai
    if 'pantai' in kategori or 'pantai' in kategori_original:
        if any(x in nama for x in ['kuta', 'sanur', 'nusa dua', 'dreamland', 'jimbaran', 'seminyak']):
            return 15000
        return 5000
    
    # Tempat ibadah
    if any(x in kategori for x in ['religi', 'masjid', 'gereja', 'pura', 'vihara']):
        return 0
    
    # Candi
    if 'candi' in kategori or 'candi' in kategori_original:
        return 10000
    
    # Museum
    if 'museum' in kategori or 'museum' in kategori_original:
        return 8000
    
    # Kategori lain
    for key, cost in biaya_realistis.items():
        if key in kategori or key in kategori_original:
            return cost
    
    # Default
    return 15000

df['estimasi_biaya_masuk'] = df.apply(get_biaya, axis=1)

print("✅ Estimasi biaya selesai")

# ============================================
# 3. POPULARITY SCORE
# ============================================
def hitung_popularity(row):
    skor = 0
    
    # Kategori populer
    kategori_populer = ['Pantai & Bahari', 'Taman & Rekreasi', 'Candi & Sejarah', 'Wisata Alam']
    if row['kategori_clean'] in kategori_populer:
        skor += 30
    
    # Lokasi strategis
    provinsi_populer = ['Bali', 'DI Yogyakarta', 'DKI Jakarta', 'Jawa Barat', 'Jawa Timur']
    if row['provinsi'] in provinsi_populer:
        skor += 25
    
    # Harga terjangkau
    if row['estimasi_biaya_masuk'] < 15000:
        skor += 25
    elif row['estimasi_biaya_masuk'] < 30000:
        skor += 15
    
    return min(skor, 100)

df['popularity_score'] = df.apply(hitung_popularity, axis=1)

print("✅ Popularity score selesai")

# ============================================
# 4. KATEGORI BUDGET
# ============================================
def kategorikan_budget(biaya):
    if biaya == 0:
        return 'GRATIS 🎉'
    elif biaya < 10000:
        return 'Ekonomis (Rp10rb)'
    elif biaya < 25000:
        return 'Standar (Rp10-25rb)'
    elif biaya < 50000:
        return 'Medium (Rp25-50rb)'
    else:
        return 'Premium (>Rp50rb)'

df['kategori_budget'] = df['estimasi_biaya_masuk'].apply(kategorikan_budget)

print("✅ Kategori budget selesai")

# ============================================
# 5. SIMPAN
# ============================================
# Pilih kolom yang akan disimpan
kolom_simpan = [
    'nama_wisata', 'kategori', 'kategori_clean', 'provinsi', 
    'kota_kabupaten', 'latitude', 'longitude', 'alamat',
    'deskripsi_bersih', 'estimasi_biaya_masuk', 'popularity_score', 
    'kategori_budget', 'Image_Path'
]

# Tambahkan kolom provinsi_clean dan kota_clean
df['provinsi_clean'] = df['provinsi']
df['kota_clean'] = df['kota_kabupaten']

df_final = df[kolom_simpan]

# Simpan ke file
df_final.to_csv('wisata_indonesia_clean_realcost.csv', index=False)
df_final.to_csv('wisata_indonesia_clean_accurate.csv', index=False)

print("="*50)
print("✅ Preprocessing selesai!")
print(f"📊 Total data: {len(df_final)} wisata")
print(f"💾 File disimpan:")
print(f"   - wisata_indonesia_clean_realcost.csv")
print(f"   - wisata_indonesia_clean_accurate.csv")
print("="*50)

# Tampilkan sample
print("\n📋 Sample data:")
print(df_final[['nama_wisata', 'kategori_clean', 'estimasi_biaya_masuk', 'popularity_score']].head(10))