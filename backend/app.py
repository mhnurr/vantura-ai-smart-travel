from flask import Flask, request, jsonify
from flask_cors import CORS
from recommender import TravelRecommender
import os

app = Flask(__name__)
CORS(app)

# Inisialisasi recommender
print("🚀 Memulai Vantura AI Backend API...")
print("📍 Mencari dataset...")

try:
    recommender = TravelRecommender()
    print(f"✅ Dataset berhasil dimuat! Total: {len(recommender.df)} destinasi")
except Exception as e:
    print(f"❌ Error loading dataset: {str(e)}")
    import traceback
    traceback.print_exc()
    recommender = None

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    """Endpoint untuk mendapatkan rekomendasi wisata"""
    try:
        if recommender is None:
            return jsonify({
                'success': False,
                'error': 'Dataset tidak tersedia'
            }), 500
            
        data = request.json
        destination = data.get('destination', '')
        budget = float(data.get('budget', 4000000))
        days = int(data.get('days', 1))
        transport = data.get('transport', 'jalan')
        
        print(f"📝 Request: destination={destination}, budget={budget}, days={days}, transport={transport}")
        
        # Dapatkan rekomendasi dengan preferensi destinasi
        recommendations = recommender.get_recommendations(
            budget=budget,
            transport=transport,
            days=days,
            top_n=3,
            city_filter=destination if destination else None,
            preferred_destination=destination  # <-- Kirim destinasi yang dipilih user
        )
        
        total_harga = sum(r['harga'] for r in recommendations)
        
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'total_budget': total_harga,
            'transport': transport,
            'days': days,
            'sisa_budget': budget - total_harga
        })
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    """Get daftar destinasi untuk autocomplete"""
    try:
        if recommender is None:
            return jsonify({
                'success': False,
                'error': 'Dataset tidak tersedia'
            }), 500
            
        query = request.args.get('q', '')
        if query:
            destinations = recommender.search_destinations(query, 20)
        else:
            destinations = recommender.get_all_destinations()[:100]
            
        return jsonify({
            'success': True,
            'destinations': destinations,
            'total': len(destinations)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/destinations/search', methods=['GET'])
def search_destinations():
    """Search destinations with query"""
    try:
        if recommender is None:
            return jsonify({
                'success': False,
                'error': 'Dataset tidak tersedia'
            }), 500
            
        query = request.args.get('q', '')
        limit = int(request.args.get('limit', 10))
        
        results = recommender.search_destinations(query, limit)
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    status = 'ok' if recommender is not None else 'no_dataset'
    return jsonify({
        'status': status,
        'dataset': 'loaded' if recommender is not None else 'not_loaded',
        'total_destinations': len(recommender.df) if recommender else 0
    })

if __name__ == '__main__':
    print("="*50)
    print("🚀 Vantura AI Backend API")
    print("📍 http://localhost:5000")
    print("="*50)
    app.run(debug=True, host='0.0.0.0', port=5000)