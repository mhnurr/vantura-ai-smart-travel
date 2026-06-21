<template>
    <div class="min-h-screen bg-background text-on-surface">
        <!-- TopNavBar -->
        <!-- <header
            class="fixed top-0 w-full z-50 flex justify-between items-center px-container-padding h-16 bg-white/60 backdrop-blur-[15px] shadow-sm border-b border-white/20">
            <router-link to="/"
                class="flex items-center gap-2 hover:scale-105 transition-transform duration-200 cursor-pointer">
                <span class="material-symbols-outlined text-primary">arrow_back</span>
                <span class="font-headline-md text-headline-md font-bold text-primary">Vantura AI</span>
            </router-link>
            <div class="flex items-center gap-4"></div>
        </header> -->

        <!-- Sidebar -->
        <aside @mouseenter="sidebarOpen = true" @mouseleave="sidebarOpen = false"
            class="fixed left-0 top-0 z-40 h-screen transition-all duration-500 ease-in-out mt-16 overflow-hidden"
            :class="sidebarOpen ? 'w-64' : 'w-16'">
            <div class="h-full bg-white/80 backdrop-blur-[25px] border-r border-white/20 shadow-xl relative">
                <div class="p-4">
                    <div class="h-8 mb-6"></div>
                    <nav class="space-y-1">
                        <!-- Planner - Active -->
                        <div class="relative group">
                            <router-link to="/planner" 
                                class="flex items-center gap-3 px-3 py-2.5 rounded-r-lg transition-all duration-300 cursor-pointer relative"
                                :class="sidebarOpen ? 'bg-primary-container/20 text-on-primary-container border-r-4 border-primary' : 'text-on-surface-variant hover:bg-white/10'">
                                <span class="material-symbols-outlined flex-shrink-0" :class="sidebarOpen ? 'text-primary' : 'text-on-surface-variant group-hover:text-primary'">map</span>
                                <span v-show="sidebarOpen" class="font-label-md whitespace-nowrap">Planner</span>
                                <div v-if="!sidebarOpen" class="absolute left-0 top-0 h-full w-1 bg-primary/30 rounded-r-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                            </router-link>
                        </div>

                        <!-- Weather -->
                        <div class="relative group">
                            <router-link to="/weather" 
                                class="flex items-center gap-3 px-3 py-2.5 rounded-r-lg transition-all duration-300 cursor-pointer relative text-on-surface-variant hover:bg-white/10">
                                <span class="material-symbols-outlined flex-shrink-0 group-hover:text-primary transition-colors">cloudy_snowing</span>
                                <span v-show="sidebarOpen" class="font-label-md whitespace-nowrap">Weather</span>
                                <div v-if="!sidebarOpen" class="absolute left-0 top-0 h-full w-1 bg-primary/30 rounded-r-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                            </router-link>
                        </div>
                    </nav>
                </div>

                <!-- Settings -->
                <div class="absolute bottom-0 left-0 right-0 p-4">
                    <div class="flex justify-center">
                        <button class="w-10 h-10 rounded-full hover:bg-white/10 flex items-center justify-center transition-all group">
                            <span class="material-symbols-outlined text-on-surface-variant group-hover:text-primary transition-colors text-sm">settings</span>
                        </button>
                    </div>
                </div>
            </div>
        </aside>

        <!-- Main Content -->
        <main class="pt-16 min-h-screen flex flex-col md:flex-row" :class="sidebarOpen ? 'lg:ml-64' : 'lg:ml-16'">
            <!-- Left Panel -->
            <section class="w-full md:w-[35%] lg:w-[30%] p-gutter flex flex-col gap-gutter">
                <div class="glass-panel p-stack-md rounded-lg flex flex-col gap-stack-md">
                    <h1 class="font-headline-lg text-headline-lg text-primary">Where to next?</h1>

                    <!-- Destination Search dengan Autocomplete -->
                    <div class="space-y-2">
                        <label class="font-label-md text-on-surface-variant">DESTINATION</label>
                        <div class="relative">
                            <input v-model="destination" @input="searchDestinations" @focus="showSuggestions = true"
                                @blur="setTimeout(() => showSuggestions = false, 300)"
                                class="w-full bg-white/40 border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary-container focus:border-transparent outline-none transition-all font-body-md"
                                placeholder="Cari Wisata di Yogyakarta..." type="text">
                            <span class="material-symbols-outlined absolute right-4 top-3 text-outline">location_on</span>

                            <!-- Autocomplete Suggestions -->
                            <div v-if="showSuggestions && filteredDestinations.length > 0"
                                class="absolute z-50 w-full mt-1 glass-panel-elevated rounded-xl max-h-60 overflow-y-auto shadow-lg">
                                <div v-for="dest in filteredDestinations" :key="dest" @click="selectDestination(dest)"
                                    class="px-4 py-2 hover:bg-primary-container/20 cursor-pointer transition-colors flex items-center gap-2">
                                    <span class="material-symbols-outlined text-primary text-sm">place</span>
                                    <span>{{ dest }}</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Days Selection -->
                    <div class="space-y-2">
                        <label class="font-label-md text-on-surface-variant">JUMLAH HARI</label>
                        <div class="grid grid-cols-3 gap-2">
                            <button v-for="day in [1, 2, 3]" :key="day" @click="selectedDays = day"
                                class="py-2 rounded-lg transition-all duration-200" :class="selectedDays === day
                                    ? 'bg-primary text-white font-bold'
                                    : 'glass-panel hover:bg-white/30'">
                                {{ day }} Hari
                            </button>
                        </div>
                    </div>

                    <!-- Calendar -->
                    <div class="space-y-2">
                        <label class="font-label-md text-on-surface-variant">DATES</label>
                        <div @click="showCalendar = !showCalendar"
                            class="glass-panel rounded-xl p-4 flex items-center justify-between cursor-pointer hover:bg-white/50 transition-colors relative">
                            <div class="flex items-center gap-3">
                                <span class="material-symbols-outlined text-primary">calendar_month</span>
                                <span class="text-body-md">{{ formattedDateRange }}</span>
                            </div>
                            <span class="material-symbols-outlined text-outline"
                                :class="{ 'rotate-180': showCalendar }">chevron_right</span>
                        </div>

                        <!-- Dropdown Kalender -->
                        <div v-if="showCalendar" class="glass-panel-elevated rounded-xl p-4 mt-2 animate-slideDown">
                            <div class="flex items-center justify-between mb-4 gap-2">
                                <button @click="prevMonth" class="p-2 hover:bg-white/20 rounded-lg transition-colors">
                                    <span class="material-symbols-outlined">chevron_left</span>
                                </button>
                                <div class="flex items-center gap-2">
                                    <select v-model="selectedMonth" @change="changeMonth(selectedMonth)"
                                        class="bg-white/40 border border-outline-variant rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-container focus:border-transparent outline-none transition-all font-body-md cursor-pointer">
                                        <option v-for="(month, index) in monthNames" :key="index" :value="index">
                                            {{ month }}
                                        </option>
                                    </select>
                                    <select v-model="selectedYear" @change="changeYear(selectedYear)"
                                        class="bg-white/40 border border-outline-variant rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-primary-container focus:border-transparent outline-none transition-all font-body-md cursor-pointer">
                                        <option v-for="year in yearOptions" :key="year" :value="year">
                                            {{ year }}
                                        </option>
                                    </select>
                                </div>
                                <button @click="nextMonth" class="p-2 hover:bg-white/20 rounded-lg transition-colors">
                                    <span class="material-symbols-outlined">chevron_right</span>
                                </button>
                            </div>
                            <div class="grid grid-cols-7 gap-1 mb-2">
                                <div v-for="day in dayNames" :key="day"
                                    class="text-center text-xs font-label-md text-on-surface-variant py-1">
                                    {{ day }}
                                </div>
                            </div>
                            <div class="grid grid-cols-7 gap-1">
                                <div v-for="date in calendarDays" :key="date.date" @click="selectDate(date)"
                                    class="text-center py-2 rounded-lg cursor-pointer transition-all duration-200 text-sm"
                                    :class="[
                                        date.isCurrentMonth ? 'text-on-surface' : 'text-on-surface-variant/40',
                                        date.isToday ? 'border-2 border-primary' : '',
                                        date.isSelected ? 'bg-primary text-white font-bold' : 'hover:bg-primary-container/20',
                                        date.isDisabled ? 'opacity-40 cursor-not-allowed' : ''
                                    ]" :style="date.isDisabled ? 'pointer-events: none;' : ''">
                                    {{ date.day }}
                                </div>
                            </div>
                            <div class="mt-4 flex justify-end gap-2">
                                <button @click="resetToToday"
                                    class="text-sm text-on-surface-variant hover:text-primary transition-colors px-3 py-1">
                                    Hari Ini
                                </button>
                                <button @click="resetDates"
                                    class="text-sm text-on-surface-variant hover:text-primary transition-colors px-3 py-1">
                                    Reset
                                </button>
                                <button @click="showCalendar = false"
                                    class="text-sm bg-primary text-white px-4 py-1 rounded-lg hover:bg-primary/80 transition-colors">
                                    Tutup
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Budget Slider -->
                    <div class="space-y-4">
                        <div class="flex justify-between items-end">
                            <label class="font-label-md text-on-surface-variant uppercase">Budget Total</label>
                            <span class="font-headline-md text-primary">Rp {{ formatCurrency(budget) }}</span>
                        </div>
                        <input v-model="budget"
                            class="w-full h-2 rounded-lg appearance-none cursor-pointer custom-slider" max="6000000"
                            min="3000000" step="100000" type="range">
                        <div class="flex justify-between text-label-md text-outline">
                            <span>Rp 3.000.000</span>
                            <span>Rp 6.000.000</span>
                        </div>
                    </div>

                    <!-- Transportation -->
                    <div class="space-y-3">
                        <label class="font-label-md text-on-surface-variant uppercase">Transportation</label>
                        <div class="grid grid-cols-3 gap-3">
                            <button v-for="transport in transports" :key="transport.id"
                                @click="selectedTransport = transport.id"
                                class="p-4 rounded-xl flex flex-col items-center gap-2 transition-all duration-300"
                                :class="selectedTransport === transport.id
                                    ? 'glass-panel-elevated border-2 border-primary ring-2 ring-primary/20'
                                    : 'glass-panel border border-white/20 hover:scale-105'">
                                <span class="material-symbols-outlined"
                                    :class="selectedTransport === transport.id ? 'text-primary active-glow' : 'text-on-surface-variant'">{{ transport.icon }}</span>
                                <span class="text-label-md"
                                    :class="selectedTransport === transport.id ? 'text-primary font-bold' : 'text-on-surface-variant'">{{ transport.label }}</span>
                            </button>
                        </div>
                    </div>

                    <button @click="generateItinerary" :disabled="isLoading"
                        class="mt-4 w-full bg-primary text-on-primary font-bold py-4 rounded-xl shadow-[0_0_20px_rgba(0,105,109,0.3)] hover:brightness-110 active:scale-[0.98] transition-all flex items-center justify-center gap-2 group"
                        :class="{ 'opacity-70 cursor-not-allowed': isLoading }">
                        <span v-if="!isLoading"
                            class="material-symbols-outlined group-hover:rotate-12 transition-transform">auto_awesome</span>
                        <span v-if="!isLoading">Generate Itinerary</span>
                        <span v-else class="flex items-center gap-2">
                            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                                viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                                </path>
                            </svg>
                            Memproses...
                        </span>
                    </button>
                </div>

                <!-- Contextual Information -->
                <div class="glass-panel p-4 rounded-lg flex items-center gap-4 border-l-4 border-primary-container">
                    <div class="pulse-gen">
                        <span class="material-symbols-outlined text-primary-container"
                            style="font-variation-settings: 'FILL' 1;">info</span>
                    </div>
                    <p class="text-label-md text-on-surface-variant">AI sedang menganalisis biaya dan pola musiman untuk
                        tanggal Anda.</p>
                </div>
            </section>

            <!-- Right Panel - MAP -->
            <section class="flex-1 p-gutter h-full min-h-[500px]">
                <div class="w-full h-full relative rounded-lg overflow-hidden glass-panel">
                    <!-- Peta Leaflet -->
                    <div ref="mapContainer" id="map" class="w-full h-full" style="min-height: 500px;"></div>
                    
                    <!-- Legend / Info Overlay -->
                    <div v-if="showResults && recommendations.length > 0" 
                         class="absolute bottom-4 left-4 right-4 z-[1000] glass-panel-elevated p-3 rounded-lg">
                        <div class="flex items-center justify-between text-xs">
                            <div class="flex items-center gap-2">
                                <span class="w-3 h-3 rounded-full bg-green-500 inline-block"></span>
                                <span>Start</span>
                            </div>
                            <div class="flex items-center gap-2" v-for="(item, idx) in recommendations" :key="idx">
                                <span class="w-3 h-3 rounded-full" 
                                      :class="['bg-blue-500', 'bg-yellow-500', 'bg-red-500'][idx]"></span>
                                <span class="truncate max-w-[60px]">{{ item.nama }}</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <span class="w-3 h-3 rounded-full bg-purple-500 inline-block"></span>
                                <span>End</span>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        </main>

        <!-- Results Section - Tampilan Rekomendasi -->
        <section v-if="showResults && recommendations.length > 0" class="w-full p-gutter mt-4 animate-slideDown"
            id="results-section">
            <div class="glass-panel-elevated rounded-xl p-stack-lg">
                <h2 class="font-headline-lg text-headline-lg text-primary mb-4 flex items-center gap-2">
                    <span class="material-symbols-outlined">recommend</span>
                    Rekomendasi Wisata untuk Anda
                </h2>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div v-for="(item, index) in recommendations" :key="index"
                        class="glass-panel rounded-lg p-4 hover:shadow-xl transition-all duration-300 cursor-pointer"
                        @click="focusOnMarker(index)">
                        <div class="flex items-start justify-between mb-2">
                            <div class="flex items-center gap-2">
                                <span class="text-sm font-bold text-primary-container bg-primary-container/10 px-2 py-1 rounded-full">
                                    #{{ index + 1 }}
                                </span>
                                <span v-if="item.is_preferred" 
                                      class="text-xs bg-primary text-white px-2 py-1 rounded-full animate-pulse">
                                    ⭐ Pilihan Anda
                                </span>
                            </div>
                            <span class="text-xs bg-secondary-container/10 text-secondary-container px-2 py-1 rounded-full">
                                {{ item.kategori }}
                            </span>
                        </div>
                        <h3 class="font-headline-md text-headline-md text-on-background">{{ item.nama }}</h3>
                        <p class="text-sm text-on-surface-variant mt-1">{{ item.lokasi }}</p>
                        <div class="flex items-center gap-2 mt-2">
                            <span class="material-symbols-outlined text-yellow-400 text-sm"
                                style="font-variation-settings: 'FILL' 1;">star</span>
                            <span class="text-sm font-semibold">{{ item.rating ? item.rating.toFixed(1) : '4.5' }}</span>
                            <span class="text-xs text-on-surface-variant">/ 5.0</span>
                        </div>
                        <div class="mt-2 flex items-center gap-2 text-sm">
                            <span class="material-symbols-outlined text-primary text-sm">payments</span>
                            <span class="font-bold text-primary">Rp {{ formatCurrency(item.harga) }}</span>
                        </div>
                        <div class="mt-3 text-xs text-on-surface-variant border-t border-outline-variant pt-2">
                            <span class="material-symbols-outlined text-sm">directions</span>
                            <span class="ml-1">Transportasi: {{ item.transportasi === 'walk' ? 'Jalan Kaki' : item.transportasi === 'moto' ? 'Motor' : 'Mobil' }}</span>
                        </div>
                        <p class="text-xs text-on-surface-variant mt-2 line-clamp-2">{{ item.deskripsi || 'Wisata menarik untuk dikunjungi di Yogyakarta' }}</p>
                    </div>
                </div>

                <!-- Total Budget -->
                <div class="mt-4 p-4 bg-primary-container/10 rounded-lg">
                    <div class="flex justify-between items-center">
                        <span class="font-label-md text-on-surface-variant">Total Estimasi Biaya:</span>
                        <span class="font-headline-md text-primary">
                            Rp {{ formatCurrency(recommendations.reduce((sum, r) => sum + (r.harga || 0), 0)) }}
                        </span>
                    </div>
                    <div class="flex justify-between items-center mt-1 text-sm">
                        <span class="text-on-surface-variant">Sisa Budget:</span>
                        <span class="font-semibold"
                            :class="budget - recommendations.reduce((sum, r) => sum + (r.harga || 0), 0) >= 0 ? 'text-green-600' : 'text-red-600'">
                            Rp {{ formatCurrency(budget - recommendations.reduce((sum, r) => sum + (r.harga || 0), 0)) }}
                        </span>
                    </div>
                </div>

                <div class="mt-4 flex justify-end">
                    <button @click="closeResults"
                        class="text-sm text-on-surface-variant hover:text-primary transition-colors px-4 py-2 rounded-lg glass-panel">
                        Tutup Rekomendasi
                    </button>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import axios from 'axios'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix untuk icon Leaflet default
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

export default {
    name: 'PlannerView',
    setup() {
        // ============================================
        // STATE
        // ============================================

        const sidebarOpen = ref(true)
        const destination = ref('')
        const budget = ref(4000000)
        const selectedDays = ref(1)
        const selectedTransport = ref('walk')

        // Calendar
        const showCalendar = ref(false)
        const startDate = ref(new Date())
        const endDate = ref(new Date())
        const currentMonth = ref(new Date().getMonth())
        const currentYear = ref(new Date().getFullYear())
        const selectedMonth = ref(new Date().getMonth())
        const selectedYear = ref(new Date().getFullYear())

        // Autocomplete
        const showSuggestions = ref(false)
        const filteredDestinations = ref([])
        const allDestinations = ref([])

        // Results
        const recommendations = ref([])
        const isLoading = ref(false)
        const showResults = ref(false)

        // Map
        const mapContainer = ref(null)
        let map = null
        let markers = []
        let routeLayer = null

        // ============================================
        // DATA STATIS
        // ============================================

        const dayNames = ['Min', 'Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab']
        const monthNames = [
            'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
            'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
        ]

        const transports = [
            { id: 'walk', icon: 'directions_walk', label: 'Jalan Kaki' },
            { id: 'moto', icon: 'motorcycle', label: 'Motor' },
            { id: 'car', icon: 'directions_car', label: 'Mobil' }
        ]

        // ============================================
        // COMPUTED
        // ============================================

        const yearOptions = computed(() => {
            const currentYear = new Date().getFullYear()
            const years = []
            for (let i = currentYear - 5; i <= currentYear + 5; i++) {
                years.push(i)
            }
            return years
        })

        const formatDateToIndonesian = (date) => {
            const day = date.getDate()
            const month = monthNames[date.getMonth()]
            const year = date.getFullYear()
            return `${day} ${month} ${year}`
        }

        const formattedDateRange = computed(() => {
            const start = formatDateToIndonesian(startDate.value)
            const end = formatDateToIndonesian(endDate.value)
            return `${start} - ${end}`
        })

        const calendarDays = computed(() => {
            const days = []
            const firstDay = new Date(currentYear.value, currentMonth.value, 1).getDay()
            const daysInMonth = new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
            const today = new Date()
            today.setHours(0, 0, 0, 0)

            const prevMonthDays = new Date(currentYear.value, currentMonth.value, 0).getDate()
            for (let i = firstDay - 1; i >= 0; i--) {
                const day = prevMonthDays - i
                const date = new Date(currentYear.value, currentMonth.value - 1, day)
                days.push({ day, date, isCurrentMonth: false, isToday: false, isSelected: false, isDisabled: false })
            }

            for (let i = 1; i <= daysInMonth; i++) {
                const date = new Date(currentYear.value, currentMonth.value, i)
                date.setHours(0, 0, 0, 0)
                const isToday = date.getTime() === today.getTime()
                const isSelected = date >= startDate.value && date <= endDate.value
                const isDisabled = date < today
                days.push({ day: i, date, isCurrentMonth: true, isToday, isSelected, isDisabled })
            }

            const remainingDays = 42 - days.length
            for (let i = 1; i <= remainingDays; i++) {
                const date = new Date(currentYear.value, currentMonth.value + 1, i)
                days.push({ day: i, date, isCurrentMonth: false, isToday: false, isSelected: false, isDisabled: false })
            }

            return days
        })

        // ============================================
        // FUNGSI CALENDAR
        // ============================================

        const prevMonth = () => {
            if (currentMonth.value === 0) {
                currentMonth.value = 11
                currentYear.value--
            } else {
                currentMonth.value--
            }
            selectedMonth.value = currentMonth.value
            selectedYear.value = currentYear.value
        }

        const nextMonth = () => {
            if (currentMonth.value === 11) {
                currentMonth.value = 0
                currentYear.value++
            } else {
                currentMonth.value++
            }
            selectedMonth.value = currentMonth.value
            selectedYear.value = currentYear.value
        }

        const changeMonth = (month) => {
            currentMonth.value = parseInt(month)
            selectedMonth.value = parseInt(month)
        }

        const changeYear = (year) => {
            currentYear.value = parseInt(year)
            selectedYear.value = parseInt(year)
        }

        const selectDate = (date) => {
            if (date.isDisabled) return
            const clickedDate = new Date(date.date)
            clickedDate.setHours(0, 0, 0, 0)

            if (!startDate.value || (startDate.value && endDate.value && startDate.value.getTime() === endDate.value.getTime())) {
                startDate.value = clickedDate
                endDate.value = clickedDate
            } else if (clickedDate < startDate.value) {
                startDate.value = clickedDate
            } else {
                endDate.value = clickedDate
            }
        }

        const resetToToday = () => {
            const today = new Date()
            today.setHours(0, 0, 0, 0)
            startDate.value = today
            endDate.value = today
            currentMonth.value = today.getMonth()
            currentYear.value = today.getFullYear()
            selectedMonth.value = today.getMonth()
            selectedYear.value = today.getFullYear()
        }

        const resetDates = () => {
            const today = new Date()
            today.setHours(0, 0, 0, 0)
            startDate.value = today
            endDate.value = today
        }

        watch(currentMonth, (newVal) => {
            selectedMonth.value = newVal
        })
        watch(currentYear, (newVal) => {
            selectedYear.value = newVal
        })

        // ============================================
        // FUNGSI MAP
        // ============================================

        const initMap = () => {
            if (map) return
            
            const centerLat = -7.797068
            const centerLng = 110.370529
            
            map = L.map(mapContainer.value, {
                zoomControl: true,
                fadeAnimation: true,
                zoomAnimation: true
            }).setView([centerLat, centerLng], 12)
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap',
                maxZoom: 19,
                minZoom: 10
            }).addTo(map)
            
            // Add zoom control
            L.control.zoom({
                position: 'topright'
            }).addTo(map)
        }

        const clearMap = () => {
            if (markers.length > 0) {
                markers.forEach(marker => map.removeLayer(marker))
                markers = []
            }
            if (routeLayer) {
                map.removeLayer(routeLayer)
                routeLayer = null
            }
        }

        const createCustomIcon = (color, number, isStart = false, isEnd = false) => {
            const svg = `
                <svg xmlns="http://www.w3.org/2000/svg" width="36" height="44" viewBox="0 0 36 44">
                    <path d="M18 44 C18 44 0 28 0 18 C0 8 8 0 18 0 C28 0 36 8 36 18 C36 28 18 44 18 44 Z" 
                          fill="${color}" stroke="white" stroke-width="2"/>
                    <text x="18" y="26" text-anchor="middle" font-size="14" font-weight="bold" fill="white">
                        ${number}
                    </text>
                </svg>
            `
            return L.icon({
                iconUrl: `data:image/svg+xml;base64,${btoa(svg)}`,
                iconSize: [36, 44],
                iconAnchor: [18, 44],
                popupAnchor: [0, -44]
            })
        }

        const updateMap = () => {
            if (!map) initMap()
            if (!map || !recommendations.value.length) return
            
            clearMap()
            
            const points = []
            const colors = ['#22c55e', '#3b82f6', '#eab308', '#ef4444']
            const iconColors = ['#22c55e', '#3b82f6', '#eab308', '#ef4444']
            
            recommendations.value.forEach((item, index) => {
                if (item.latitude && item.longitude) {
                    const lat = parseFloat(item.latitude)
                    const lng = parseFloat(item.longitude)
                    
                    if (!isNaN(lat) && !isNaN(lng) && lat !== 0 && lng !== 0) {
                        const isStart = index === 0 && item.is_preferred
                        const isEnd = index === recommendations.value.length - 1
                        const color = colors[index] || '#8b5cf6'
                        
                        const icon = createCustomIcon(
                            color,
                            index + 1,
                            isStart,
                            isEnd
                        )
                        
                        const popupContent = `
                            <div class="font-bold">${item.nama}</div>
                            <div class="text-sm">${item.kategori}</div>
                            <div class="text-sm text-gray-600">${item.lokasi}</div>
                            <div class="text-sm font-bold text-green-600">Rp ${formatCurrency(item.harga)}</div>
                        `
                        
                        const marker = L.marker([lat, lng], { icon })
                            .bindPopup(popupContent)
                            .addTo(map)
                        
                        markers.push(marker)
                        points.push([lat, lng])
                    }
                }
            })
            
            // Draw route line
            if (points.length >= 2) {
                const routeLine = L.polyline(points, {
                    color: '#00696d',
                    weight: 4,
                    opacity: 0.7,
                    dashArray: '8, 8',
                    lineJoin: 'round'
                }).addTo(map)
                routeLayer = routeLine
                
                // Fit bounds to show all markers and route
                const bounds = L.latLngBounds(points)
                map.fitBounds(bounds, { padding: [50, 50], maxZoom: 14 })
            } else if (points.length === 1) {
                map.setView(points[0], 14)
            }
        }

        const focusOnMarker = (index) => {
            if (index < markers.length && markers[index]) {
                markers[index].openPopup()
                map.setView(markers[index].getLatLng(), 16, {
                    animate: true,
                    duration: 0.5
                })
            }
        }

        const closeResults = () => {
            showResults.value = false
            clearMap()
            if (map) {
                map.setView([-7.797068, 110.370529], 12)
            }
        }

        // ============================================
        // FUNGSI API
        // ============================================

        const formatCurrency = (value) => {
            return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")
        }

        const fetchDestinations = async () => {
            try {
                const response = await axios.get('http://localhost:5000/api/destinations')
                if (response.data.success) {
                    allDestinations.value = response.data.destinations
                }
            } catch (error) {
                console.error('Error fetching destinations:', error)
                allDestinations.value = [
                    'Candi Borobudur', 'Candi Prambanan', 'Malioboro',
                    'Pantai Parangtritis', 'Taman Sari', 'Gunung Merapi',
                    'Bukit Bintang', 'Pantai Indrayanti', 'Candi Ratu Boko',
                    'Museum Sonobudoyo', 'Kraton Yogyakarta', 'Taman Pintar'
                ]
            }
        }

        const searchDestinations = async () => {
            if (destination.value.length > 0) {
                try {
                    const response = await axios.get(`http://localhost:5000/api/destinations/search?q=${encodeURIComponent(destination.value)}&limit=10`)
                    if (response.data.success) {
                        filteredDestinations.value = response.data.results
                        showSuggestions.value = true
                    }
                } catch (error) {
                    if (allDestinations.value.length === 0) {
                        await fetchDestinations()
                    }
                    filteredDestinations.value = allDestinations.value.filter(d =>
                        d.toLowerCase().includes(destination.value.toLowerCase())
                    ).slice(0, 10)
                    showSuggestions.value = true
                }
            } else {
                filteredDestinations.value = []
                showSuggestions.value = false
            }
        }

        const selectDestination = (dest) => {
            destination.value = dest
            showSuggestions.value = false
        }

        const generateItinerary = async () => {
            if (!destination.value) {
                alert('Silakan pilih destinasi wisata terlebih dahulu!')
                return
            }

            isLoading.value = true
            showResults.value = false

            try {
                const response = await axios.post('http://localhost:5000/api/recommend', {
                    destination: destination.value,
                    budget: budget.value,
                    days: selectedDays.value,
                    transport: selectedTransport.value
                })

                if (response.data.success) {
                    recommendations.value = response.data.recommendations
                    showResults.value = true

                    await nextTick()
                    
                    setTimeout(() => {
                        initMap()
                        updateMap()
                        
                        const resultsElement = document.getElementById('results-section')
                        if (resultsElement) {
                            resultsElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
                        }
                    }, 500)
                } else {
                    alert('Gagal mendapatkan rekomendasi: ' + response.data.error)
                }
            } catch (error) {
                console.error('Error:', error)
                alert('Terjadi kesalahan saat menghubungi server. Pastikan backend berjalan.')
            } finally {
                isLoading.value = false
            }
        }

        // ============================================
        // LIFE CYCLE
        // ============================================

        onMounted(() => {
            fetchDestinations()
            initMap()
        })

        // ============================================
        // RETURN
        // ============================================

        return {
            sidebarOpen,
            destination,
            budget,
            selectedDays,
            selectedTransport,
            transports,
            showCalendar,
            startDate,
            endDate,
            currentMonth,
            currentYear,
            selectedMonth,
            selectedYear,
            dayNames,
            monthNames,
            yearOptions,
            formattedDateRange,
            calendarDays,
            formatDateToIndonesian,
            prevMonth,
            nextMonth,
            changeMonth,
            changeYear,
            selectDate,
            resetToToday,
            resetDates,
            showSuggestions,
            filteredDestinations,
            searchDestinations,
            selectDestination,
            recommendations,
            isLoading,
            showResults,
            formatCurrency,
            generateItinerary,
            fetchDestinations,
            mapContainer,
            focusOnMarker,
            closeResults,
            updateMap
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

.glass-panel-elevated {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(25px);
    -webkit-backdrop-filter: blur(25px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8px 32px 0 rgba(0, 105, 109, 0.1);
}

.custom-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 24px;
    height: 24px;
    background: #ffffff;
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2), inset 0 0 2px rgba(255, 255, 255, 0.8);
}

.custom-slider {
    background: linear-gradient(to right, #00696d, #fd6a49);
}

.active-glow {
    filter: drop-shadow(0 0 8px #00bec4);
}

@keyframes pulse-teal {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}

.pulse-gen {
    animation: pulse-teal 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes float {
    0% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-20px) rotate(2deg); }
    100% { transform: translateY(0px) rotate(0deg); }
}

.animate-float {
    animation: float 6s ease-in-out infinite;
}

.animate-bounce {
    animation: bounce 3s ease-in-out infinite;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

.animate-slideDown {
    animation: slideDown 0.3s ease-out forwards;
}

aside::-webkit-scrollbar {
    display: none;
}

aside {
    -ms-overflow-style: none;
    scrollbar-width: none;
    transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.rotate-180 {
    transform: rotate(180deg);
    transition: transform 0.3s ease;
}

select {
    appearance: auto;
    -webkit-appearance: auto;
    min-width: 100px;
}

select:focus {
    outline: none;
}

.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.animate-spin {
    animation: spin 1s linear infinite;
}

/* Map container */
#map {
    width: 100%;
    height: 100%;
    min-height: 500px;
    border-radius: 0.75rem;
    z-index: 1;
}

/* Leaflet popup custom */
:deep(.leaflet-popup-content) {
    font-family: 'Be Vietnam Pro', sans-serif;
    min-width: 180px;
}

:deep(.leaflet-popup-content-wrapper) {
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

:deep(.leaflet-popup-tip) {
    background: rgba(255, 255, 255, 0.95);
}

/* Legend overlay */
.legend-overlay {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 10px 16px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
}
</style>