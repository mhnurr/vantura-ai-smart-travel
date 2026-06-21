<template>
    <section class="py-stack-lg px-container-padding bg-surface-container-low/50">
        <div class="text-center mb-stack-lg">
            <h2 class="font-headline-lg text-headline-lg text-on-background mb-2">Destinasi Wisata Yogyakarta</h2>
            <p class="font-body-md text-body-md text-on-surface-variant">Jelajahi keindahan budaya dan alam Yogyakarta
                bersama Vantura AI</p>
        </div>

        <!-- Carousel Container -->
        <div class="relative max-w-4xl mx-auto">
            <!-- Carousel Track -->
            <div class="overflow-hidden rounded-xl">
                <div class="flex transition-transform duration-500 ease-in-out"
                    :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
                    <div v-for="destination in destinations" :key="destination.id" class="w-full flex-shrink-0 px-4">
                        <div class="relative rounded-xl overflow-hidden cursor-pointer group"
                            @click="openModal(destination)">
                            <img :src="destination.image" :alt="destination.name"
                                class="w-full h-96 object-cover transition-transform duration-700 group-hover:scale-110"
                                loading="lazy" />
                            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent">
                            </div>

                            <!-- Badge Price -->
                            <div
                                class="absolute top-4 right-4 glass-panel backdrop-blur-[25px] px-4 py-2 rounded-full text-secondary-container font-bold text-sm shadow-lg">
                                {{ destination.price }}
                            </div>

                            <!-- Info -->
                            <div class="absolute bottom-6 left-6 right-6 text-white">
                                <p class="font-label-md text-label-md text-white/80">{{ destination.country }}</p>
                                <h3 class="font-headline-md text-headline-md">{{ destination.name }}</h3>
                                <div class="flex items-center gap-2 mt-2 text-sm">
                                    <span class="material-symbols-outlined text-sm text-primary-container"
                                        style="font-variation-settings: 'FILL' 1;">star</span>
                                    <span>{{ destination.rating }} ({{ destination.reviews }} reviews)</span>
                                </div>
                                <div class="mt-2 text-xs opacity-70 flex items-center gap-1">
                                    <span class="material-symbols-outlined text-xs">location_on</span>
                                    {{ destination.location }}
                                </div>
                            </div>

                            <!-- Hover Effect - View Detail -->
                            <div
                                class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-black/40">
                                <button
                                    class="bg-white text-primary font-bold px-6 py-3 rounded-full shadow-lg hover:scale-105 transition-transform">
                                    Lihat Detail
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Navigation Buttons -->
            <button @click="prevSlide"
                class="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white text-primary w-12 h-12 rounded-full shadow-lg flex items-center justify-center transition-all hover:scale-110 z-10"
                :disabled="currentIndex === 0" :class="{ 'opacity-50 cursor-not-allowed': currentIndex === 0 }">
                <span class="material-symbols-outlined">chevron_left</span>
            </button>

            <button @click="nextSlide"
                class="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 hover:bg-white text-primary w-12 h-12 rounded-full shadow-lg flex items-center justify-center transition-all hover:scale-110 z-10"
                :disabled="currentIndex === destinations.length - 1"
                :class="{ 'opacity-50 cursor-not-allowed': currentIndex === destinations.length - 1 }">
                <span class="material-symbols-outlined">chevron_right</span>
            </button>

            <!-- Dots Indicator -->
            <div class="flex justify-center gap-2 mt-6">
                <button v-for="(_, index) in destinations" :key="index" @click="currentIndex = index"
                    class="w-3 h-3 rounded-full transition-all duration-300" :class="[
                        currentIndex === index
                            ? 'bg-primary w-8'
                            : 'bg-gray-300 hover:bg-gray-400'
                    ]"></button>
            </div>
        </div>

        <!-- Modal -->
        <Teleport to="body">
            <div v-if="modalVisible"
                class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm"
                @click.self="closeModal">
                <div
                    class="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto transform transition-all duration-300 scale-100">
                    <!-- Close Button -->
                    <button @click="closeModal"
                        class="absolute top-4 right-4 z-10 bg-white/90 rounded-full p-2 hover:bg-white transition-colors shadow-lg">
                        <span class="material-symbols-outlined text-gray-600">close</span>
                    </button>

                    <!-- Modal Image -->
                    <div class="relative">
                        <img :src="selectedDestination?.image" :alt="selectedDestination?.name"
                            class="w-full h-80 object-cover rounded-t-2xl" />
                        <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-6">
                            <h3 class="text-2xl font-bold text-white">{{ selectedDestination?.name }}</h3>
                            <div class="flex items-center gap-2 text-white/90 mt-1">
                                <span class="material-symbols-outlined text-sm text-yellow-400"
                                    style="font-variation-settings: 'FILL' 1;">star</span>
                                <span>{{ selectedDestination?.rating }} ({{ selectedDestination?.reviews }}
                                    reviews)</span>
                                <span class="mx-2">•</span>
                                <span class="material-symbols-outlined text-sm">location_on</span>
                                <span>{{ selectedDestination?.location }}</span>
                            </div>
                        </div>
                    </div>

                    <!-- Modal Content -->
                    <div class="p-6">
                        <div class="flex items-center gap-4 mb-4 flex-wrap">
                            <span class="px-4 py-2 bg-primary/10 text-primary rounded-full text-sm font-semibold">
                                {{ selectedDestination?.country }}
                            </span>
                            <span
                                class="px-4 py-2 bg-secondary-container/10 text-secondary-container rounded-full text-sm font-semibold">
                                {{ selectedDestination?.price }}
                            </span>
                        </div>

                        <p class="text-gray-700 text-base leading-relaxed mb-4">
                            {{ selectedDestination?.description }}
                        </p>

                        <div class="flex flex-wrap gap-3 pt-4 border-t border-gray-100">
                            <!-- <button
                                class="gradient-cta text-white font-semibold px-6 py-2 rounded-full hover:scale-105 transition-transform">
                                Pesan Sekarang
                            </button>
                            <button
                                class="glass-panel text-primary font-semibold px-6 py-2 rounded-full border border-primary/30 hover:bg-white/20 transition-all">
                                Simpan ke Wishlist
                            </button> -->
                        </div>
                    </div>
                </div>
            </div>
        </Teleport>
    </section>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { destinations } from '../data/destinations'

export default {
    name: 'DestinationSection',
    setup() {
        const currentIndex = ref(0)
        const modalVisible = ref(false)
        const selectedDestination = ref(null)
        let autoplayInterval = null

        const nextSlide = () => {
            if (currentIndex.value < destinations.length - 1) {
                currentIndex.value++
            } else {
                currentIndex.value = 0
            }
        }

        const prevSlide = () => {
            if (currentIndex.value > 0) {
                currentIndex.value--
            } else {
                currentIndex.value = destinations.length - 1
            }
        }

        const openModal = (destination) => {
            selectedDestination.value = destination
            modalVisible.value = true
            document.body.style.overflow = 'hidden'
        }

        const closeModal = () => {
            modalVisible.value = false
            document.body.style.overflow = ''
            setTimeout(() => {
                selectedDestination.value = null
            }, 300)
        }

        // Auto-play carousel
        const startAutoplay = () => {
            autoplayInterval = setInterval(nextSlide, 4000)
        }

        const stopAutoplay = () => {
            if (autoplayInterval) {
                clearInterval(autoplayInterval)
                autoplayInterval = null
            }
        }

        onMounted(() => {
            startAutoplay()
        })

        onUnmounted(() => {
            stopAutoplay()
            document.body.style.overflow = ''
        })

        return {
            destinations,
            currentIndex,
            modalVisible,
            selectedDestination,
            nextSlide,
            prevSlide,
            openModal,
            closeModal
        }
    }
}
</script>

<style scoped>
/* Animasi untuk modal */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.scale-enter-active,
.scale-leave-active {
    transition: transform 0.3s ease;
}

.scale-enter-from,
.scale-leave-to {
    transform: scale(0.9);
}
</style>