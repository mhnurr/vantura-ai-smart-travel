<template>
    <nav
        class="fixed top-0 w-full z-50 flex justify-between items-center px-container-padding h-16 bg-white/60 backdrop-blur-[15px] border-b border-white/20 shadow-sm">
        <div class="flex items-center gap-base">
            <span class="font-headline-md text-headline-md font-bold text-primary">Vantura AI</span>
        </div>
        <!-- <div class="hidden md:flex gap-stack-md items-center">
            <a class="font-body-md text-body-md text-primary font-bold border-b-2 border-primary pb-1" href="#">Smart
                Planner</a>
            <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors"
                href="#">Budget</a>
            <a class="font-body-md text-body-md text-on-surface-variant hover:text-primary transition-colors"
                href="#">Weather</a>
        </div> -->
        <div class="flex items-center gap-base">
            <!-- <div class="relative hidden sm:block">
                <input
                    class="bg-white/40 border-none rounded-full px-4 py-2 text-sm focus:ring-2 ring-primary-container w-48"
                    placeholder="Cari destinasi..." type="text" />
                <span class="material-symbols-outlined absolute right-3 top-2 text-primary text-sm">search</span>
            </div> -->
            <button
                class="flex items-center gap-2 px-4 py-2 rounded-full hover:bg-white/10 transition-transform active:scale-95 duration-200">
                <!-- <span class="material-symbols-outlined text-primary-container">person</span> -->
                <!-- <span class="font-label-md text-label-md text-primary">Profile</span> -->
            </button>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'Navbar'
}
</script>