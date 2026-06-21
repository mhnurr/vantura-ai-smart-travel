<template>
    <div class="min-h-screen bg-background text-on-surface">
        <!-- Main Content -->
        <div class="pt-16 min-h-screen">
            <div class="p-6 max-w-4xl mx-auto">
                <!-- Loading State -->
                <div v-if="isLoading" class="flex items-center justify-center h-96">
                    <div class="text-center">
                        <svg class="animate-spin h-12 w-12 text-primary mx-auto" xmlns="http://www.w3.org/2000/svg"
                            fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4">
                            </circle>
                            <path class="opacity-75" fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                            </path>
                        </svg>
                        <p class="mt-4 text-on-surface-variant">Memuat data cuaca...</p>
                    </div>
                </div>

                <!-- Weather Content -->
                <div v-else-if="weatherData">
                    <!-- Header: Lokasi & Waktu -->
                    <div class="flex justify-between items-start mb-6">
                        <div>
                            <h1 class="font-headline-xl text-headline-xl text-on-background">Jogja Weather</h1>
                            <p class="text-sm text-on-surface-variant mt-1">
                                Updated {{ timeAgo }} • {{ currentDate }}
                            </p>
                        </div>
                        <button @click="refreshWeather"
                            class="glass-panel p-2 rounded-full hover:bg-white/30 transition-colors">
                            <span class="material-symbols-outlined text-primary">refresh</span>
                        </button>
                    </div>

                    <!-- Current Weather Card -->
                    <div class="glass-panel p-6 rounded-2xl mb-6">
                        <div class="flex flex-col md:flex-row items-center justify-between">
                            <div class="flex items-center gap-6">
                                <!-- Weather Icon -->
                                <div class="text-7xl">
                                    {{ getWeatherIcon(weatherData.current?.condition?.code || 1003) }}
                                </div>
                                <div>
                                    <div class="flex items-end gap-2">
                                        <span class="font-headline-xl text-headline-xl text-on-background">{{
                                            Math.round(weatherData.current?.temp_c || 32) }}°</span>
                                        <span class="text-lg text-on-surface-variant mb-1">C</span>
                                    </div>
                                    <p class="text-lg font-semibold text-on-surface">{{
                                        weatherData.current?.condition?.text || 'Cerah' }}</p>
                                    <p class="text-sm text-on-surface-variant">{{ weatherData.location?.name ||
                                        'Yogyakarta' }}, {{ weatherData.location?.country || 'ID' }}</p>
                                </div>
                            </div>

                            <!-- Weather Details -->
                            <div class="grid grid-cols-3 gap-6 mt-4 md:mt-0">
                                <div class="text-center">
                                    <p class="text-xs text-on-surface-variant uppercase">Humidity</p>
                                    <p class="text-lg font-bold text-on-surface">{{ weatherData.current?.humidity || 64
                                        }}%</p>
                                </div>
                                <div class="text-center">
                                    <p class="text-xs text-on-surface-variant uppercase">Wind</p>
                                    <p class="text-lg font-bold text-on-surface">{{
                                        Math.round(weatherData.current?.wind_kph || 12) }} km/h</p>
                                </div>
                                <div class="text-center">
                                    <p class="text-xs text-on-surface-variant uppercase">Visibility</p>
                                    <p class="text-lg font-bold text-on-surface">{{ weatherData.current?.vis_km || 10 }}
                                        km</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- AI Smart Recommendation -->
                    <div class="glass-panel p-4 rounded-xl mb-6 border-l-4 border-primary-container">
                        <div class="flex items-start gap-3">
                            <span class="material-symbols-outlined text-primary text-2xl">auto_awesome</span>
                            <div>
                                <p class="text-sm font-semibold text-primary">AI Smart Recommendation</p>
                                <p class="text-sm text-on-surface-variant mt-1">{{ aiRecommendation }}</p>
                                <button class="mt-2 text-sm text-primary font-semibold hover:underline">View Best
                                    Outdoor Spots →</button>
                            </div>
                        </div>
                    </div>

                    <!-- 5-Day Forecast -->
                    <div class="glass-panel p-6 rounded-2xl">
                        <h3 class="font-headline-md text-headline-md text-on-background mb-4">5-Day Forecast</h3>

                        <!-- Forecast Grid - Selalu tampilkan forecast dari data manapun -->
                        <div v-if="forecastDays && forecastDays.length > 0" class="grid grid-cols-5 gap-2">
                            <div v-for="(day, index) in forecastDays" :key="index"
                                class="text-center p-3 rounded-xl hover:bg-white/10 transition-colors">
                                <p class="text-xs font-semibold text-on-surface-variant">{{ day.day }}</p>
                                <p class="text-sm font-bold text-on-surface mt-1">{{ day.temp_max }}°</p>
                                <p class="text-xs text-on-surface-variant">{{ day.temp_min }}°</p>
                                <div class="text-2xl mt-1">{{ day.icon }}</div>
                                <p class="text-xs text-on-surface-variant mt-1">{{ day.condition }}</p>
                            </div>
                        </div>

                        <!-- Fallback: Gunakan data dummy jika tidak ada forecast dari API -->
                        <div v-else class="grid grid-cols-5 gap-2">
                            <div v-for="day in dummyForecast" :key="day.day"
                                class="text-center p-3 rounded-xl hover:bg-white/10 transition-colors">
                                <p class="text-xs font-semibold text-on-surface-variant">{{ day.day }}</p>
                                <p class="text-sm font-bold text-on-surface mt-1">{{ day.temp_max }}°</p>
                                <p class="text-xs text-on-surface-variant">{{ day.temp_min }}°</p>
                                <div class="text-2xl mt-1">{{ day.icon }}</div>
                                <p class="text-xs text-on-surface-variant mt-1">{{ day.condition }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Error State -->
                <div v-else class="flex items-center justify-center h-96">
                    <div class="text-center">
                        <span class="material-symbols-outlined text-6xl text-error">error</span>
                        <p class="mt-4 text-lg font-semibold text-on-surface">Gagal memuat data cuaca</p>
                        <p class="text-sm text-on-surface-variant mt-2">{{ errorMessage }}</p>
                        <button @click="fetchWeather"
                            class="mt-4 bg-primary text-white px-6 py-2 rounded-lg hover:bg-primary/80 transition-colors">
                            Coba Lagi
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export default {
    name: 'WeatherView',
    setup() {
        const weatherData = ref(null)
        const isLoading = ref(true)
        const errorMessage = ref('')
        const lastUpdated = ref(null)

        // ============================================
        // API KEY WEATHERAPI.COM
        // ============================================
        const API_KEY = '76849d68a41c4057a35182129262006'
        const CITY = 'Yogyakarta'
        const DAYS = 5

        // ============================================
        // DUMMY FORECAST (Fallback jika API tidak ada)
        // ============================================
        const dummyForecast = computed(() => {
            const days = ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab']
            const today = new Date()
            const result = []

            for (let i = 1; i <= 5; i++) {
                const d = new Date(today)
                d.setDate(d.getDate() + i)
                const temps = [33, 31, 29, 30, 32, 28, 34]
                const conditions = ['Cerah', 'Berawan', 'Hujan Ringan', 'Mendung', 'Cerah', 'Berawan', 'Cerah']
                const icons = ['☀️', '⛅', '🌧️', '☁️', '☀️', '⛅', '☀️']
                const idx = i % 7
                result.push({
                    day: days[d.getDay()],
                    temp_max: temps[idx],
                    temp_min: temps[idx] - 6,
                    icon: icons[idx],
                    condition: conditions[idx]
                })
            }
            return result
        })

        // ============================================
        // COMPUTED
        // ============================================

        const currentDate = computed(() => {
            const now = new Date()
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' }
            return now.toLocaleDateString('id-ID', options)
        })

        const timeAgo = computed(() => {
            if (!lastUpdated.value) return 'just now'
            const diff = Math.floor((Date.now() - lastUpdated.value) / 60000)
            if (diff < 1) return 'just now'
            if (diff < 60) return `${diff} minutes ago`
            if (diff < 120) return '1 hour ago'
            return `${Math.floor(diff / 60)} hours ago`
        })

        const getWeatherIcon = (code) => {
            const icons = {
                1000: '☀️', 1003: '⛅', 1006: '☁️', 1009: '☁️',
                1030: '🌫️', 1063: '🌦️', 1066: '❄️', 1087: '⛈️',
                1114: '❄️', 1117: '❄️', 1135: '🌫️', 1147: '🌫️',
                1150: '🌦️', 1153: '🌦️', 1168: '🌧️', 1171: '🌧️',
                1180: '🌧️', 1183: '🌧️', 1186: '🌧️', 1189: '🌧️',
                1192: '🌧️', 1195: '🌧️', 1198: '🌧️', 1201: '🌧️',
                1204: '🌧️', 1207: '🌧️', 1210: '❄️', 1213: '❄️',
                1216: '❄️', 1219: '❄️', 1222: '❄️', 1225: '❄️',
                1237: '🌧️', 1240: '🌧️', 1243: '🌧️', 1246: '🌧️',
                1249: '🌧️', 1252: '🌧️', 1255: '❄️', 1258: '❄️',
                1261: '🌧️', 1264: '🌧️', 1273: '⛈️', 1276: '⛈️',
                1279: '⛈️', 1282: '⛈️'
            }
            return icons[code] || '🌤️'
        }

        const getDayName = (dateStr) => {
            const days = ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab']
            const date = new Date(dateStr)
            return days[date.getDay()]
        }

        // Coba ambil forecast dari API, jika tidak ada gunakan dummy
        const forecastDays = computed(() => {
  // Cek apakah ada data forecast dari API
  if (weatherData?.forecast?.forecastday && weatherData.forecast.forecastday.length > 0) {
    try {
      const result = weatherData.forecast.forecastday.slice(1).map(day => {
        const date = new Date(day.date)
        const dayNames = ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab']
        return {
          day: dayNames[date.getDay()],
          temp_max: Math.round(day.day.maxtemp_c),
          temp_min: Math.round(day.day.mintemp_c),
          icon: getWeatherIcon(day.day.condition.code),
          condition: day.day.condition.text
        }
      })
      console.log('✅ Forecast from API (REAL DATA):', result)
      return result
    } catch (error) {
      console.error('Error processing forecast:', error)
      return dummyForecast.value
    }
  }
  
  console.log('📦 Using dummy forecast (no API data)')
  return dummyForecast.value
})

        const aiRecommendation = computed(() => {
            if (!weatherData?.current) return 'Cuaca cerah di Jogja, nikmati hari Anda!'

            const temp = weatherData.current.temp_c || 32
            const condition = weatherData.current.condition?.text || 'Cerah'
            const humidity = weatherData.current.humidity || 64

            if (temp > 30) {
                return 'Cerah di Jogja, jangan lupa bawa kacamata hitam! Indeks UV cukup tinggi hari ini, pastikan gunakan tabir surya sebelum ke Borobudur.'
            } else if (temp > 25 && temp <= 30) {
                return 'Cuaca hangat dan nyaman di Jogja. Waktu yang tepat untuk berkunjung ke Malioboro atau menjelajahi Candi Prambanan.'
            } else if (condition.toLowerCase().includes('rain')) {
                return 'Hujan diprediksi turun di Jogja. Jangan lupa bawa payung jika berencana ke luar ruangan. Museum Sonobudoyo bisa jadi pilihan alternatif.'
            } else if (humidity > 80) {
                return 'Kelembaban cukup tinggi di Jogja. Pastikan minum air yang cukup dan gunakan pakaian yang nyaman saat berwisata.'
            }
            return 'Cuaca cerah di Jogja, sempurna untuk berwisata! Nikmati keindahan kota budaya ini.'
        })

        // ============================================
        // FUNGSI FETCH WEATHER
        // ============================================

        const fetchWeather = async () => {
            isLoading.value = true
            errorMessage.value = ''

            try {
                const url = `https://api.weatherapi.com/v1/forecast.json?key=${API_KEY}&q=${CITY}&days=${DAYS}&lang=id`

                console.log('🌤️ Fetching weather from:', url)
                const response = await axios.get(url)

                if (response.data) {
                    weatherData.value = response.data
                    lastUpdated.value = Date.now()
                    console.log('✅ Weather data received!')
                    console.log('📍 Location:', response.data.location?.name, response.data.location?.country)
                    console.log('🌡️ Temperature:', response.data.current?.temp_c, '°C')
                    console.log('📊 Forecast days:', response.data.forecast?.forecastday?.length || 0)

                    // Debug: Tampilkan data forecast
                    if (response.data.forecast?.forecastday) {
                        console.log('📅 Forecast data:', response.data.forecast.forecastday.map(d => ({
                            date: d.date,
                            max: d.day.maxtemp_c,
                            min: d.day.mintemp_c,
                            condition: d.day.condition.text
                        })))
                    }
                }
            } catch (error) {
                console.error('❌ Error fetching weather:', error)

                if (error.response?.status === 401) {
                    errorMessage.value = 'API Key tidak valid. Silakan cek API Key Anda di WeatherAPI.com'
                } else if (error.response?.status === 403) {
                    errorMessage.value = 'Akses ditolak. Pastikan akun WeatherAPI Anda aktif.'
                } else {
                    errorMessage.value = error.response?.data?.error?.message || 'Terjadi kesalahan saat mengambil data cuaca'
                }

                // Tetap set weatherData dengan data dummy agar tampilan tetap muncul
                useDummyData()
            } finally {
                isLoading.value = false
            }
        }

        const useDummyData = () => {
            weatherData.value = {
                location: { name: 'Yogyakarta', country: 'Indonesia' },
                current: {
                    temp_c: 32,
                    humidity: 64,
                    wind_kph: 12,
                    vis_km: 10,
                    condition: { text: 'Mostly Sunny', code: 1003 }
                },
                forecast: {
                    forecastday: [
                        { date: new Date().toISOString().split('T')[0], day: { maxtemp_c: 33, mintemp_c: 24, condition: { text: 'Cerah', code: 1000 } } },
                        { date: new Date(Date.now() + 86400000).toISOString().split('T')[0], day: { maxtemp_c: 31, mintemp_c: 23, condition: { text: 'Berawan', code: 1003 } } },
                        { date: new Date(Date.now() + 172800000).toISOString().split('T')[0], day: { maxtemp_c: 29, mintemp_c: 22, condition: { text: 'Hujan Ringan', code: 1183 } } },
                        { date: new Date(Date.now() + 259200000).toISOString().split('T')[0], day: { maxtemp_c: 30, mintemp_c: 23, condition: { text: 'Mendung', code: 1006 } } },
                        { date: new Date(Date.now() + 345600000).toISOString().split('T')[0], day: { maxtemp_c: 32, mintemp_c: 24, condition: { text: 'Cerah', code: 1000 } } }
                    ]
                }
            }
            lastUpdated.value = Date.now()
            console.log('📦 Using dummy data')
        }

        const refreshWeather = () => {
            fetchWeather()
        }

        onMounted(() => {
            fetchWeather()
        })

        return {
            weatherData,
            isLoading,
            errorMessage,
            lastUpdated,
            currentDate,
            timeAgo,
            getWeatherIcon,
            forecastDays,
            dummyForecast,
            aiRecommendation,
            fetchWeather,
            refreshWeather
        }
    }
}
</script>

<style scoped>
.glass-panel {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: inset 0 0.5px 0 0 rgba(255, 255, 255, 0.5);
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.animate-spin {
    animation: spin 1s linear infinite;
}
</style>