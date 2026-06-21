<template>
    <div
        class="flex-none w-72 h-96 relative rounded-lg overflow-hidden snap-start group cursor-pointer shadow-lg hover:shadow-primary-container/20 transition-shadow">
        <img class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
            :src="destination.image" :alt="destination.name" />
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div>
        <div
            class="absolute top-4 right-4 glass-panel backdrop-blur-[25px] px-3 py-1 rounded-full text-secondary-container font-bold text-sm shadow-lg">
            {{ destination.price }}
        </div>
        <div class="absolute bottom-6 left-6 text-white">
            <p class="font-label-md text-label-md text-white/80">{{ destination.country }}</p>
            <h3 class="font-headline-md text-headline-md">{{ destination.name }}</h3>
            <div class="flex items-center gap-1 mt-2 text-xs">
                <span class="material-symbols-outlined text-sm text-primary-container"
                    style="font-variation-settings: 'FILL' 1;">star</span>
                <span>{{ destination.rating }} ({{ destination.reviews }} reviews)</span>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DestinationCard',
    props: {
        destination: {
            type: Object,
            required: true
        }
    }
}
</script>