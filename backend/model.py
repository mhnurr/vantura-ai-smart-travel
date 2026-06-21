import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

class TravelRecommender:
    def __init__(self, csv_path='wisata_indonesia_clean_realcost.csv'):
        """Inisialisasi recommender dengan dataset"""
        # Cek apakah file ada
        if not os.path.exists(csv_path):
            print(f"⚠️ File {csv_path} tidak ditemukan! Coba gunakan file alternatif...")
            # Coba cari file lain
            alt_files = ['wisata_indonesia_clean_accurate.csv', 'wisata_indonesia_clean.csv', 'wisata_indonesia_new.csv']
            for alt in alt_files:
                if os.path.exists(alt):
                    csv_path = alt
                    print(f"✅ Menggunakan file: {csv_path}")
                    break
        
        self.df = pd.read_csv(csv_path)
        self.prepare_data()
        
    def prepare_data(self):
        """Persiapan data untuk rekomendasi"""
        # Bersihkan data
        self.df = self.df.dropna(subset=['nama_wisata', 'kategori_clean', 'estimasi_biaya_masuk'])
        
        # Buat fitur untuk rekomendasi berbasis konten
        # Gabungkan beberapa kolom menjadi satu teks untuk TF-IDF
        self.df['features'] = self.df['kategori_clean'].fillna('') + ' ' + \
                              self.df['provinsi_clean'].fillna('') + ' ' + \
                              self.df['kota_kabupaten'].fillna('') + ' ' + \
                              self.df['deskripsi_bersih'].fillna('')
        
        # TF-IDF Vectorizer untuk rekomendasi berbasis konten
        self.tfidf = TfidfVectorizer(stop_words='indonesian', max_features=500)
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['features'])
        
        # Normalisasi budget
        max_budget = self.df['estimasi_biaya_masuk'].max()
        min_budget = self.df['estimasi_biaya_masuk'].min()
        if max_budget > min_budget:
            self.df['budget_normalized'] = (self.df['estimasi_biaya_masuk'] - min_budget) / (max_budget - min_budget)
        else:
            self.df['budget_normalized'] = 0
        
        # Normalisasi popularity score (jika ada)
        if 'popularity_score' in self.df.columns:
            max_pop = self.df['popularity_score'].max()
            if max_pop > 0:
                self.df['popularity_norm'] = self.df['popularity_score'] / max_pop
            else:
                self.df['popularity_norm'] = 0.5
        else:
            self.df['popularity_norm'] = 0.5
        
        print(f"✅ Data siap: {len(self.df)} destinasi wisata")
        
        # Tampilkan beberapa kota yang tersedia
        cities = self.df['kota_kabupaten'].unique()
        print(f"📍 Kota yang tersedia: {', '.join(cities[:10])}...")
        
    def get_recommendations(self, budget, transport='jalan', days=1, top_n=3, city_filter=None):
        """
        Mendapatkan rekomendasi wisata berdasarkan budget dan preferensi
        
        Parameters:
        - budget: total budget dalam Rupiah
        - transport: jenis transportasi ('jalan', 'moto', 'car')
        - days: jumlah hari
        - top_n: jumlah rekomendasi
        - city_filter: filter kota (opsional)
        
        Returns:
        - list rekomendasi wisata
        """
        budget_per_day = budget / days
        
        # Filter dasar
        filtered_df = self.df.copy()
        
        # Filter berdasarkan kota jika ada
        if city_filter:
            # Filter kota di Yogyakarta dan sekitarnya
            yogyakarta_cities = ['Yogyakarta', 'Sleman', 'Bantul', 'Gunungkidul', 'Kulon Progo', 
                                'Magelang', 'Klaten', 'Surakarta', 'Semarang', 'Boyolali', 
                                'Solo', 'Surakarta', 'Salatiga']
            filtered_df = filtered_df[
                filtered_df['kota_kabupaten'].str.contains('|'.join(yogyakarta_cities), case=False, na=False)
            ]
        
        # Filter berdasarkan budget (maksimal 80% dari budget per hari)
        max_budget_per_wisata = budget_per_day * 0.8
        filtered_df = filtered_df[filtered_df['estimasi_biaya_masuk'] <= max_budget_per_wisata]
        
        # Jika tidak ada hasil, ambil yang termurah
        if len(filtered_df) == 0:
            filtered_df = self.df.nsmallest(top_n * 3, 'estimasi_biaya_masuk')
        
        # Hitung skor untuk rekomendasi
        # Kombinasi: popularity (60%) + budget (40%)
        filtered_df['score'] = (filtered_df['popularity_norm'] * 0.6 + 
                                (1 - filtered_df['budget_normalized']) * 0.4)
        
        # Urutkan berdasarkan skor tertinggi
        recommendations = filtered_df.nlargest(top_n * 3, 'score')
        
        # Pilih yang paling beragam (berbeda kategori)
        selected = []
        used_categories = set()
        
        for _, row in recommendations.iterrows():
            if len(selected) >= top_n:
                break
            kategori = row['kategori_clean']
            if kategori not in used_categories or len(used_categories) >= top_n:
                selected.append(row.to_dict())
                used_categories.add(kategori)
        
        # Jika masih kurang, tambahkan dari rekomendasi awal
        if len(selected) < top_n:
            for _, row in recommendations.iterrows():
                if len(selected) >= top_n:
                    break
                if row.to_dict() not in selected:
                    selected.append(row.to_dict())
        
        # Format output
        result = []
        for item in selected:
            result.append({
                'nama': item['nama_wisata'],
                'kategori': item.get('kategori_clean', item.get('kategori', 'Wisata')),
                'lokasi': f"{item.get('kota_kabupaten', '')}, {item.get('provinsi_clean', '')}",
                'harga': int(item.get('estimasi_biaya_masuk', 0)),
                'rating': float(item.get('popularity_score', 50)) / 10,
                'deskripsi': item.get('deskripsi_bersih', 'Wisata menarik untuk dikunjungi di Yogyakarta'),
                'latitude': float(item.get('latitude', 0)),
                'longitude': float(item.get('longitude', 0)),
                'estimasi_waktu': self.get_estimated_time(item.get('kategori_clean', '')),
                'transportasi': transport,
                'gambar': item.get('Image_Path', ''),
                'popularity': int(item.get('popularity_score', 0))
            })
        
        return result
    
    def get_estimated_time(self, kategori):
        """Estimasi waktu kunjungan berdasarkan kategori"""
        times = {
            'Candi & Sejarah': '2-3 jam',
            'Pantai & Bahari': '3-4 jam',
            'Gunung & Pendakian': '4-5 jam',
            'Museum & Monumen': '1-2 jam',
            'Taman & Rekreasi': '2-3 jam',
            'Wisata Kuliner': '1-2 jam',
            'Desa & Agrowisata': '2-3 jam',
            'Danau & Waduk': '2-3 jam',
            'Air Terjun & Curug': '1-2 jam',
            'Wisata Belanja': '1-2 jam',
            'wisata alam': '2-3 jam',
            'wisata edukasi': '1-2 jam',
            'wisata religi': '1-2 jam',
            'wisata kerajaan': '2-3 jam',
            'bukit': '2-3 jam',
            'gunung': '4-5 jam',
            'pantai': '2-3 jam',
            'candi': '2-3 jam',
            'museum': '1-2 jam',
            'taman': '1-2 jam'
        }
        for key, time in times.items():
            if key.lower() in kategori.lower() or kategori.lower() in key.lower():
                return time
        return '2-3 jam'
    
    def get_route_order(self, recommendations):
        """Urutkan rekomendasi berdasarkan jarak (sederhana)"""
        # Jika ada koordinat, urutkan berdasarkan jarak dari pusat kota
        if all('latitude' in r and 'longitude' in r for r in recommendations):
            # Pusat Yogyakarta
            center_lat = -7.797068
            center_lon = 110.370529
            
            def distance_from_center(item):
                lat = item.get('latitude', center_lat)
                lon = item.get('longitude', center_lon)
                return ((lat - center_lat)**2 + (lon - center_lon)**2)**0.5
            
            recommendations.sort(key=distance_from_center)
        
        return recommendations

    def get_all_destinations(self):
        """Mendapatkan semua nama destinasi untuk autocomplete"""
        return self.df['nama_wisata'].tolist()
    
    def search_destinations(self, query, limit=10):
        """Mencari destinasi berdasarkan query"""
        if not query:
            return []
        query_lower = query.lower()
        matches = self.df[self.df['nama_wisata'].str.lower().str.contains(query_lower, na=False)]
        return matches['nama_wisata'].tolist()[:limit]