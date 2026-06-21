import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import os

class TravelRecommender:
    def __init__(self, csv_path='wisata_indonesia_clean_realcost.csv'):
        """Inisialisasi recommender dengan dataset hasil preprocessing"""
        
        # Cari file dengan prioritas: clean_realcost > clean_accurate > new
        possible_files = [
            csv_path,
            'wisata_indonesia_clean_realcost.csv',
            'wisata_indonesia_clean_accurate.csv',
            'wisata_indonesia_new.csv'
        ]
        
        found = False
        for f in possible_files:
            if os.path.exists(f):
                csv_path = f
                found = True
                break
        
        if not found:
            print("⚠️ Dataset tidak ditemukan! Menggunakan data dummy...")
            self.create_dummy_data()
            return
        
        print(f"📂 Memuat dataset: {csv_path}")
        self.df = pd.read_csv(csv_path)
        
        # Cek kolom yang tersedia
        print(f"📋 Kolom tersedia: {list(self.df.columns)}")
        
        # Jika file mentah (wisata_indonesia_new.csv), lakukan preprocessing
        if 'kategori_clean' not in self.df.columns:
            print("🔄 Melakukan preprocessing untuk dataset mentah...")
            self.df = self.preprocess_data(self.df)
        
        # Tambahkan kolom yang diperlukan jika tidak ada
        if 'provinsi_clean' not in self.df.columns and 'provinsi' in self.df.columns:
            self.df['provinsi_clean'] = self.df['provinsi']
        elif 'provinsi_clean' not in self.df.columns:
            self.df['provinsi_clean'] = 'DIY'
            
        if 'kota_clean' not in self.df.columns and 'kota_kabupaten' in self.df.columns:
            self.df['kota_clean'] = self.df['kota_kabupaten']
        elif 'kota_clean' not in self.df.columns:
            self.df['kota_clean'] = 'Yogyakarta'
            
        if 'deskripsi_bersih' not in self.df.columns:
            self.df['deskripsi_bersih'] = ''
            
        if 'kategori_clean' not in self.df.columns and 'kategori' in self.df.columns:
            self.df['kategori_clean'] = self.df['kategori']
        
        self.prepare_data()
    
    def create_dummy_data(self):
        """Buat data dummy jika dataset tidak ditemukan"""
        dummy_data = {
            'nama_wisata': [
                'Candi Borobudur', 'Candi Prambanan', 'Malioboro',
                'Pantai Parangtritis', 'Taman Sari', 'Gunung Merapi',
                'Bukit Bintang', 'Pantai Indrayanti', 'Museum Sonobudoyo',
                'Kraton Yogyakarta', 'Taman Pintar', 'Pantai Sadranan'
            ],
            'kategori_clean': [
                'Candi & Sejarah', 'Candi & Sejarah', 'Wisata Kuliner',
                'Pantai & Bahari', 'Taman & Rekreasi', 'Gunung & Pendakian',
                'Bukit', 'Pantai & Bahari', 'Museum & Monumen',
                'Wisata Kerajaan', 'Wisata Edukasi', 'Pantai & Bahari'
            ],
            'provinsi_clean': ['DIY'] * 12,
            'kota_kabupaten': [
                'Magelang', 'Sleman', 'Yogyakarta',
                'Bantul', 'Yogyakarta', 'Sleman',
                'Gunungkidul', 'Gunungkidul', 'Yogyakarta',
                'Yogyakarta', 'Yogyakarta', 'Gunungkidul'
            ],
            'estimasi_biaya_masuk': [50000, 50000, 0, 15000, 15000, 35000, 15000, 15000, 8000, 15000, 15000, 15000],
            'popularity_score': [95, 90, 85, 80, 75, 85, 70, 80, 70, 85, 75, 75],
            'latitude': [-7.6079, -7.7522, -7.7932, -8.0273, -7.7496, -7.5413, -7.8461, -8.1499, -7.8023, -7.8029, -7.8010, -8.1458],
            'longitude': [110.2038, 110.4915, 110.3658, 110.3370, 110.3972, 110.4462, 110.4797, 110.6113, 110.3644, 110.3652, 110.3678, 110.6044],
            'deskripsi_bersih': [
                'Candi Buddha terbesar di dunia',
                'Candi Hindu terbesar di Indonesia',
                'Jalan ikonik di Yogyakarta',
                'Pantai eksotis dengan pasir hitam',
                'Bekas taman keraton yang indah',
                'Gunung berapi aktif dengan sunrise spektakuler',
                'Bukit dengan pemandangan indah',
                'Pantai dengan pasir putih yang indah',
                'Museum dengan koleksi budaya Jawa',
                'Istana resmi Kesultanan Yogyakarta',
                'Taman edukasi interaktif',
                'Pantai dengan pemandangan menakjubkan'
            ]
        }
        self.df = pd.DataFrame(dummy_data)
        self.prepare_data()
        print("✅ Data dummy berhasil dibuat")
    
    def preprocess_data(self, df):
        """Preprocessing untuk dataset mentah"""
        # Mapping kategori
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
            'monumen': 'Monumen'
        }
        
        df['kategori_clean'] = df['kategori'].str.lower().replace(kategori_mapping)
        df['kategori_clean'] = df['kategori_clean'].fillna(df['kategori'])
        
        # Estimasi biaya sederhana
        def get_biaya(row):
            kat = str(row['kategori_clean']).lower()
            if 'alun' in kat or 'mall' in kat or 'kuliner' in kat:
                return 0
            elif 'pantai' in kat:
                return 15000
            elif 'candi' in kat:
                return 10000
            elif 'museum' in kat:
                return 8000
            elif 'gunung' in kat:
                return 20000
            else:
                return 15000
        
        df['estimasi_biaya_masuk'] = df.apply(get_biaya, axis=1)
        
        # Popularity score
        def get_pop(row):
            skor = 30 if row['kategori_clean'] in ['Pantai & Bahari', 'Taman & Rekreasi', 'Candi & Sejarah'] else 0
            skor += 25 if row['provinsi'] in ['Bali', 'DI Yogyakarta', 'DKI Jakarta', 'Jawa Barat', 'Jawa Timur'] else 0
            skor += 25 if row['estimasi_biaya_masuk'] < 15000 else (15 if row['estimasi_biaya_masuk'] < 30000 else 0)
            return min(skor, 100)
        
        df['popularity_score'] = df.apply(get_pop, axis=1)
        
        df['provinsi_clean'] = df['provinsi']
        df['kota_clean'] = df['kota_kabupaten']
        df['deskripsi_bersih'] = df.get('deskripsi_bersih', '')
        
        print(f"✅ Preprocessing selesai! {len(df)} data siap")
        return df
    
    def prepare_data(self):
        """Persiapan data untuk rekomendasi"""
        # Pastikan kolom yang diperlukan ada
        required_cols = ['nama_wisata', 'kategori_clean', 'estimasi_biaya_masuk']
        for col in required_cols:
            if col not in self.df.columns:
                print(f"⚠️ Kolom '{col}' tidak ditemukan, membuat kolom default...")
                if col == 'kategori_clean':
                    self.df['kategori_clean'] = 'Wisata'
                elif col == 'estimasi_biaya_masuk':
                    self.df['estimasi_biaya_masuk'] = 15000
        
        # Bersihkan data
        self.df = self.df.dropna(subset=['nama_wisata', 'kategori_clean', 'estimasi_biaya_masuk'])
        
        # Pastikan kolom provinsi_clean ada
        if 'provinsi_clean' not in self.df.columns:
            if 'provinsi' in self.df.columns:
                self.df['provinsi_clean'] = self.df['provinsi']
            else:
                self.df['provinsi_clean'] = 'DIY'
        
        if 'kota_kabupaten' not in self.df.columns:
            self.df['kota_kabupaten'] = 'Yogyakarta'
        
        if 'deskripsi_bersih' not in self.df.columns:
            self.df['deskripsi_bersih'] = ''
        
        if 'popularity_score' not in self.df.columns:
            self.df['popularity_score'] = 50
        
        # Buat fitur untuk rekomendasi berbasis konten
        self.df['features'] = (
            self.df['kategori_clean'].fillna('') + ' ' + 
            self.df['provinsi_clean'].fillna('') + ' ' + 
            self.df['kota_kabupaten'].fillna('') + ' ' + 
            self.df['deskripsi_bersih'].fillna('')
        )
        
        self.tfidf = TfidfVectorizer(max_features=500)
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['features'])
        
        # Normalisasi budget
        max_budget = self.df['estimasi_biaya_masuk'].max()
        min_budget = self.df['estimasi_biaya_masuk'].min()
        if max_budget > min_budget:
            self.df['budget_normalized'] = (self.df['estimasi_biaya_masuk'] - min_budget) / (max_budget - min_budget)
        else:
            self.df['budget_normalized'] = 0
        
        # Normalisasi popularity
        if 'popularity_score' in self.df.columns:
            max_pop = self.df['popularity_score'].max()
            if max_pop > 0:
                self.df['popularity_norm'] = self.df['popularity_score'] / max_pop
            else:
                self.df['popularity_norm'] = 0.5
        else:
            self.df['popularity_norm'] = 0.5
        
        print(f"✅ Data siap: {len(self.df)} destinasi wisata")
        print(f"📋 Kolom: {list(self.df.columns)}")
        
    def get_recommendations(self, budget, transport='jalan', days=1, top_n=3, city_filter=None, preferred_destination=None):
        """
        Mendapatkan rekomendasi wisata berdasarkan budget dan preferensi
        
        Parameters:
        - budget: total budget dalam Rupiah
        - transport: jenis transportasi ('jalan', 'moto', 'car')
        - days: jumlah hari
        - top_n: jumlah rekomendasi
        - city_filter: filter kota (opsional)
        - preferred_destination: nama destinasi yang dipilih user (opsional)
        """
        
        budget_per_day = budget / days
        
        # Filter dasar - kota di Yogyakarta dan sekitarnya
        yogyakarta_cities = ['Yogyakarta', 'Sleman', 'Bantul', 'Gunungkidul', 'Kulon Progo', 
                            'Magelang', 'Klaten', 'Surakarta', 'Semarang', 'Boyolali', 'Solo']
        
        filtered_df = self.df[
            self.df['kota_kabupaten'].str.contains('|'.join(yogyakarta_cities), case=False, na=False)
        ].copy()
        
        # ============================================
        # PRIORITAS 1: Cari destinasi yang dipilih user
        # ============================================
        selected_destination = None
        if preferred_destination:
            # Cari destinasi yang cocok dengan nama yang dipilih
            dest_match = filtered_df[
                filtered_df['nama_wisata'].str.lower().str.contains(preferred_destination.lower(), na=False)
            ]
            
            if len(dest_match) > 0:
                # Ambil yang paling cocok
                selected_destination = dest_match.iloc[0].to_dict()
                print(f"✅ Destinasi utama ditemukan: {selected_destination['nama_wisata']}")
            else:
                # Coba cari di semua data (tidak terbatas Yogyakarta)
                dest_match_all = self.df[
                    self.df['nama_wisata'].str.lower().str.contains(preferred_destination.lower(), na=False)
                ]
                if len(dest_match_all) > 0:
                    selected_destination = dest_match_all.iloc[0].to_dict()
                    print(f"✅ Destinasi utama ditemukan (dari semua data): {selected_destination['nama_wisata']}")
                else:
                    print(f"⚠️ Destinasi '{preferred_destination}' tidak ditemukan dalam dataset")
        
        # ============================================
        # PRIORITAS 2: Filter berdasarkan budget
        # ============================================
        max_budget_per_wisata = budget_per_day * 0.8
        
        # Jika ada destinasi yang dipilih, tetap masukkan meskipun melebihi budget
        if selected_destination:
            # Hapus destinasi yang dipilih dari filtered_df untuk menghindari duplikat
            filtered_df = filtered_df[
                filtered_df['nama_wisata'] != selected_destination['nama_wisata']
            ]
            
            # Tambahkan destinasi yang dipilih ke dalam list rekomendasi
            selected_destination['score'] = 100  # Skor maksimal
            selected_destination['is_preferred'] = True
        
        # Filter berdasarkan budget untuk rekomendasi lainnya
        filtered_df = filtered_df[filtered_df['estimasi_biaya_masuk'] <= max_budget_per_wisata]
        
        # Jika tidak ada hasil, ambil yang termurah
        if len(filtered_df) == 0:
            filtered_df = self.df.nsmallest(top_n * 3, 'estimasi_biaya_masuk')
        
        # ============================================
        # PRIORITAS 3: Hitung skor untuk rekomendasi
        # ============================================
        filtered_df['score'] = (filtered_df['popularity_norm'] * 0.6 + 
                                (1 - filtered_df['budget_normalized']) * 0.4)
        
        # ============================================
        # PRIORITAS 4: Pilih rekomendasi
        # ============================================
        recommendations = []
        
        # Tambahkan destinasi yang dipilih user sebagai #1
        if selected_destination:
            recommendations.append(selected_destination)
            used_categories = {selected_destination.get('kategori_clean', '')}
        else:
            used_categories = set()
        
        # Urutkan filtered_df berdasarkan skor
        sorted_df = filtered_df.sort_values('score', ascending=False)
        
        # Pilih sisanya dengan kategori berbeda
        for _, row in sorted_df.iterrows():
            if len(recommendations) >= top_n:
                break
            kategori = row['kategori_clean']
            if kategori not in used_categories or len(used_categories) >= top_n:
                row_dict = row.to_dict()
                row_dict['is_preferred'] = False
                recommendations.append(row_dict)
                used_categories.add(kategori)
        
        # Jika masih kurang, tambahkan dari rekomendasi awal tanpa filter kategori
        if len(recommendations) < top_n:
            for _, row in sorted_df.iterrows():
                if len(recommendations) >= top_n:
                    break
                already_added = any(r['nama_wisata'] == row['nama_wisata'] for r in recommendations)
                if not already_added:
                    row_dict = row.to_dict()
                    row_dict['is_preferred'] = False
                    recommendations.append(row_dict)
        
        # ============================================
        # PRIORITAS 5: Format output
        # ============================================
        result = []
        for item in recommendations:
            result.append({
                'nama': item['nama_wisata'],
                'kategori': item.get('kategori_clean', 'Wisata'),
                'lokasi': f"{item.get('kota_kabupaten', '')}, {item.get('provinsi_clean', 'DIY')}",
                'harga': int(item.get('estimasi_biaya_masuk', 0)),
                'rating': float(item.get('popularity_score', 50)) / 10,
                'deskripsi': item.get('deskripsi_bersih', 'Wisata menarik untuk dikunjungi di Yogyakarta'),
                'latitude': float(item.get('latitude', 0)),
                'longitude': float(item.get('longitude', 0)),
                'estimasi_waktu': self.get_estimated_time(item.get('kategori_clean', '')),
                'transportasi': transport,
                'popularity': int(item.get('popularity_score', 0)),
                'is_preferred': item.get('is_preferred', False)
            })
        
        return result
    
    def get_estimated_time(self, kategori):
        """Estimasi waktu kunjungan"""
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
            'Wisata Kerajaan': '2-3 jam',
            'Wisata Edukasi': '1-2 jam',
            'Bukit': '2-3 jam',
            'Wisata Alam': '2-3 jam',
            'Wisata Religi': '1-2 jam'
        }
        for key, time in times.items():
            if key.lower() in str(kategori).lower() or str(kategori).lower() in key.lower():
                return time
        return '2-3 jam'
    
    def get_all_destinations(self):
        """Mendapatkan semua nama destinasi"""
        return self.df['nama_wisata'].tolist()
    
    def search_destinations(self, query, limit=10):
        """Mencari destinasi berdasarkan query"""
        if not query:
            return []
        query_lower = query.lower()
        matches = self.df[self.df['nama_wisata'].str.lower().str.contains(query_lower, na=False)]
        return matches['nama_wisata'].tolist()[:limit]