<template>
    <main class="pt-16 overflow-x-hidden">
        <HeroSection />
        <DestinationSection />
        <TestimonialSection />
    </main>
</template>

<script>
import HeroSection from '../components/HeroSection.vue'
import DestinationSection from '../components/DestinationSection.vue'
import TestimonialSection from '../components/TestimonialSection.vue'
import Footer from '../components/Footer.vue'
export default {
    name: 'HomeView',
    components: {
        HeroSection,
        DestinationSection,
        TestimonialSection,
        Footer
    },
    mounted() {
        // Smooth scroll behavior
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault()
                const target = document.querySelector(this.getAttribute('href'))
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    })
                }
            })
        })
    }
}
</script>