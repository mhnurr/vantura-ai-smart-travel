<template>
    <section class="py-stack-lg px-container-padding">
        <div class="text-center mb-stack-lg">
            <h2 class="font-headline-lg text-headline-lg text-on-background">Apa Kata Mereka?</h2>
            <p class="font-body-md text-body-md text-on-surface-variant">Ribuan wisatawan telah menemukan cara baru
                untuk berkeliling dunia.</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 items-start">
            <div class="flex flex-col gap-6">
                <TestimonialCard v-for="testimonial in leftColumn" :key="testimonial.id" :testimonial="testimonial" />
            </div>
            <div class="flex flex-col gap-6 md:mt-12">
                <TestimonialCard v-for="testimonial in centerColumn" :key="testimonial.id" :testimonial="testimonial" />
                <div class="bg-primary p-8 rounded-lg text-white shadow-xl shadow-primary/20 transform -translate-y-4">
                    <h4 class="font-headline-md text-headline-md mb-2">Siap untuk Berangkat?</h4>
                    <p class="text-sm opacity-80 mb-6">Cobalah itinerary pertamamu hari ini sekarang juga.</p>
                    <!-- <button
                        class="w-full bg-white text-primary font-bold py-3 rounded-lg hover:bg-primary-fixed transition-colors">Daftar
                        Sekarang</button> -->
                </div>
            </div>
            <div class="flex flex-col gap-6">
                <TestimonialCard v-for="testimonial in rightColumn" :key="testimonial.id" :testimonial="testimonial" />
            </div>
        </div>
    </section>
</template>

<script>
import TestimonialCard from './TestimonialCard.vue'
import { testimonials } from '../data/testimonials'

export default {
    name: 'TestimonialSection',
    components: {
        TestimonialCard
    },
    computed: {
        leftColumn() {
            return testimonials.filter(t => t.column === 'left')
        },
        centerColumn() {
            return testimonials.filter(t => t.column === 'center')
        },
        rightColumn() {
            return testimonials.filter(t => t.column === 'right')
        }
    }
}
</script>