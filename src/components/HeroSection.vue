<template>
    <section class="min-h-[870px] flex flex-col md:flex-row items-center px-container-padding py-stack-lg gap-stack-lg">
        <div class="w-full md:w-1/2 flex flex-col gap-stack-md">
            <div
                class="inline-flex items-center px-4 py-1 rounded-full bg-tertiary-fixed text-on-tertiary-fixed font-label-md text-label-md w-fit">
                ✨ Generative AI Travel Assistant
            </div>
            <h1 class="font-headline-xl text-headline-xl md:text-headline-xl leading-tight text-on-background">
                Rancang Perjalanan Impianmu dengan <span class="text-primary-container">Kekuatan AI</span>
            </h1>
            <p class="font-body-lg text-body-lg text-on-surface-variant max-w-xl">
                Vantura AI mengkurasi itinerary personal secara instan berdasarkan preferensi, budget, dan impian
                eksplorasimu. Mulai petualangan cerdasmu hari ini.
            </p>
            <div class="flex flex-wrap gap-4 pt-4">
                <router-link to="/planner">
                    <button
                        class="gradient-cta text-white font-headline-md text-headline-md px-8 py-4 rounded-lg neon-glow-teal hover:scale-105 transition-transform duration-300 active:scale-95">
                        Mulai Rencanakan
                    </button>
                </router-link>
                <!-- <button
                    class="glass-panel text-secondary font-headline-md text-headline-md px-8 py-4 rounded-lg border border-secondary/30 hover:bg-white/20 transition-all">
                    Lihat Demo
                </button> -->
            </div>
            <div class="flex items-center gap-4 mt-4">
                <div class="flex -space-x-3">
                    <img class="w-10 h-10 rounded-full border-2 border-surface"
                        src="https://lh3.googleusercontent.com/aida-public/AB6AXuArwan1RhnBZuZMLGVoidh-QakPyKdS0Kg8fBEAHorGG-3K60pyw60zVbotVeUssPDTzQRrClNXdQySOavnKCEsZcALFuiSiAGVf_A1ZLdt-znQDc6wtxN1tkJKjSEEdb86medUiQ-ya5YsOqa0ScLTaevwQfhEAEitk4GLm_YonlynbjyicaoVjzv5q_XCmtxIS2aFW6BR3L1CDFPgvLs4neII70GZFxqeEmR8KmK4zXJvrvA3M80ooFkgeI8x6qtepQ_FSIgdWQ"
                        alt="Traveler" />
                    <img class="w-10 h-10 rounded-full border-2 border-surface"
                        src="https://lh3.googleusercontent.com/aida-public/AB6AXuCXoSgsau5Woj0hO-2x-ShRKHfr75JbTXA0eq9GjpLv_mW62wzLcvoXy6f2bAR2um_NeJqPHUV93zsCCK8AX8CcSuEDF9RH9Z82KsR1rLCJtwJK_pALQgWlQa7FuSkUlT5ToUCui1pHLZ-TGl4-SQWD2cQgU_KBHmGsYSp3-2RqSkbJ2sAI9EfaecJPY8HrS46vFKg4cA989M-xzboNTytTO5Qf4I3cNlrTYZ2V_zLNyqjl5saM8NFicnxp49CdvOyIApuGhVp63g"
                        alt="Traveler" />
                    <img class="w-10 h-10 rounded-full border-2 border-surface"
                        src="https://lh3.googleusercontent.com/aida-public/AB6AXuBlCM42zsfhKkVWVl0WPFiY4yb89h2KSbzHMhFLllXvWSNTFIuHP5hV6DsDujLw8nNT92KCiOe3q_tCaGiBsekZCz3Xl-IY-d1dl5-ds5aSCEsfp71IOdb2wpnxDwdxpC_l_qYVZjKGl_m2OPbu-PiAzBrkUPhn9B-9G72HJUsaM7TycnenTjneFmOidslpmFzgFEy2hbpvXSmPwVEXWqqdPoXkjchJOTcwCCukQuRyPeLLddRwwDeHfV3qrmonJz9LudOcaBcGhg"
                        alt="Traveler" />
                </div>
                <p class="font-label-md text-label-md text-on-surface-variant">
                    <span class="font-bold text-primary">10,000+</span> wisatawan telah bergabung
                </p>
            </div>
        </div>

        <!-- Hero Image Mockup - Smart Itinerary Travel -->
        <div class="w-full md:w-1/2 relative flex justify-center items-center">
            <div class="absolute inset-0 bg-primary-container/10 blur-[100px] rounded-full"></div>
            <div
                class="glass-panel p-4 rounded-xl shadow-2xl relative z-10 w-full max-w-lg transform md:rotate-2 hover:rotate-0 transition-transform duration-500">
                <div class="flex items-center mb-4 bg-white/20 p-3 rounded-lg">
                    <div class="flex gap-2">
                        <div class="w-3 h-3 rounded-full bg-secondary"></div>
                        <div class="w-3 h-3 rounded-full bg-tertiary-container"></div>
                        <div class="w-3 h-3 rounded-full bg-primary-container"></div>
                    </div>
                    <div class="flex-1 flex justify-center">
                        <span class="text-[10px] font-label-md text-outline flex items-center gap-1">
                            <!-- <span class="material-symbols-outlined text-[12px]">smart_trip</span> -->
                            Smart Itinerary
                        </span>
                    </div>
                </div>

                <div class="relative rounded-lg overflow-hidden mb-4">
                    <img class="w-full h-auto rounded-lg shadow-inner"
                        src="https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800&h=500&fit=crop&crop=center"
                        alt="Smart Itinerary Travel" />
                    <div
                        class="absolute top-3 left-3 glass-panel backdrop-blur-[25px] px-3 py-1 rounded-full text-primary text-xs font-bold flex items-center gap-1 shadow-lg">
                        <span class="material-symbols-outlined text-[14px]"
                            style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
                        AI Powered
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-3">
                    <div
                        class="h-20 glass-panel rounded-lg flex items-center justify-center flex-col gap-1 border-primary-container/20 hover:bg-primary-container/5 transition-colors cursor-pointer">
                        <span class="material-symbols-outlined text-primary"
                            style="font-variation-settings: 'FILL' 1;">flight_takeoff</span>
                        <span class="text-[10px] font-label-md">Flight Confirmed</span>
                    </div>
                    <div
                        class="h-20 glass-panel rounded-lg flex items-center justify-center flex-col gap-1 border-secondary-container/20 hover:bg-secondary-container/5 transition-colors cursor-pointer">
                        <span class="material-symbols-outlined text-secondary"
                            style="font-variation-settings: 'FILL' 1;">hotel</span>
                        <span class="text-[10px] font-label-md">Eco Resort Booked</span>
                    </div>
                </div>
            </div>

            <div
                class="absolute -bottom-8 -left-8 glass-panel p-6 rounded-lg shadow-xl z-20 backdrop-blur-[25px] hidden lg:block border-primary/30 animate-bounce-slow">
                <div class="flex items-center gap-3">
                    <div class="p-2 bg-primary-container/20 rounded-full">
                        <span class="material-symbols-outlined text-primary-fixed-dim"
                            style="font-variation-settings: 'FILL' 1;">auto_awesome</span>
                    </div>
                    <div>
                        <p class="text-xs font-bold text-primary flex items-center gap-1">
                            AI Optimized!
                            <span class="material-symbols-outlined text-[12px]">check_circle</span>
                        </p>
                        <!-- <p class="text-[10px] text-on-surface-variant">Savings found: Rp 2.400.000</p> -->
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
export default {
    name: 'HeroSection'
}
</script>

<style scoped>
@keyframes bounce-slow {

    0%,
    100% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-10px);
    }
}

.animate-bounce-slow {
    animation: bounce-slow 3s ease-in-out infinite;
}
</style>