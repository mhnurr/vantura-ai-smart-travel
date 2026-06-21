<template>
    <footer
        class="w-full py-stack-lg px-container-padding flex flex-col md:flex-row justify-between items-center bg-surface-container border-t border-outline-variant mt-stack-lg">
        <div class="flex flex-col gap-2 mb-stack-md md:mb-0">
            <span class="font-headline-md text-headline-md font-bold text-primary">Vantura AI</span>
            <p class="font-body-md text-body-md text-on-surface-variant">© 2026 Vantura AI Travel. All rights reserved.
            </p>
        </div>
        <div class="flex gap-stack-md">
            <a class="font-label-md text-label-md text-on-surface-variant hover:text-secondary-container transition-opacity"
                href="#">Privacy Policy</a>
            <a class="font-label-md text-label-md text-on-surface-variant hover:text-secondary-container transition-opacity"
                href="#">Terms of Service</a>
            <a class="font-label-md text-label-md text-on-surface-variant hover:text-secondary-container transition-opacity"
                href="#">Contact Us</a>
        </div>
        <!-- <div class="flex gap-4 mt-stack-md md:mt-0"> -->
            <!-- <button
                class="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow-sm hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-primary"></span>
            </button>
            <button
                class="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow-sm hover:scale-110 transition-transform">
                <span class="material-symbols-outlined text-primary"></span>
            </button> -->
        <!-- </div> -->
    </footer>
</template>

<script>
export default {
    name: 'Footer'
}
</script>