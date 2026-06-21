<template>
    <div class="glass-panel p-6 rounded-lg transition-all border-l-4" :class="borderColorClass">
        <p class="font-body-md text-body-md mb-4 italic">"{{ testimonial.text }}"</p>
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full flex items-center justify-center font-bold" :class="bgColorClass">
                {{ testimonial.initials }}
            </div>
            <div>
                <p class="text-sm font-bold">{{ testimonial.name }}</p>
                <p class="text-[10px] text-on-surface-variant">{{ testimonial.role }}</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TestimonialCard',
    props: {
        testimonial: {
            type: Object,
            required: true
        }
    },
    computed: {
        borderColorClass() {
            return `border-${this.testimonial.color}`
        },
        bgColorClass() {
            return `bg-${this.testimonial.color}/20 text-${this.testimonial.color}`
        }
    }
}
</script>