<template>
  <div id="app" class="bg-surface text-on-surface">
    <!-- Navbar -->
    <header class="fixed top-0 w-full z-50 flex justify-between items-center px-container-padding h-16 bg-white/60 backdrop-blur-[15px] shadow-sm border-b border-white/20">
      <!-- Tampilkan tombol kembali jika bukan di home -->
      <router-link v-if="$route.name !== 'home'" to="/" 
        class="flex items-center gap-2 hover:scale-105 transition-transform duration-200 cursor-pointer">
        <span class="material-symbols-outlined text-primary">arrow_back</span>
        <span class="font-headline-md text-headline-md font-bold text-primary">Vantura AI</span>
      </router-link>
      
      <!-- Tampilkan logo saja di home -->
      <span v-else class="font-headline-md text-headline-md font-bold text-primary">Vantura AI</span>
      
      <div class="flex items-center gap-4"></div>
    </header>

    <!-- Sidebar - HANYA di Planner dan Weather -->
    <aside v-if="$route.name === 'planner' || $route.name === 'weather'" 
           @mouseenter="sidebarOpen = true" 
           @mouseleave="sidebarOpen = false"
      class="fixed left-0 top-0 z-40 h-screen transition-all duration-500 ease-in-out mt-16 overflow-hidden"
      :class="sidebarOpen ? 'w-64' : 'w-16'">
      <div class="h-full bg-white/80 backdrop-blur-[25px] border-r border-white/20 shadow-xl relative">
        <div class="p-4">
          <div class="h-8 mb-6"></div>
          <nav class="space-y-1">
            <router-link to="/planner" 
              class="flex items-center gap-3 px-3 py-2.5 rounded-r-lg transition-all duration-300 cursor-pointer relative"
              :class="[
                $route.path === '/planner' && sidebarOpen ? 'bg-primary-container/20 text-on-primary-container border-r-4 border-primary' : 'text-on-surface-variant hover:bg-white/10'
              ]">
              <span class="material-symbols-outlined flex-shrink-0" 
                :class="$route.path === '/planner' && sidebarOpen ? 'text-primary' : 'text-on-surface-variant group-hover:text-primary'">map</span>
              <span v-show="sidebarOpen" class="font-label-md whitespace-nowrap">Planner</span>
              <div v-if="!sidebarOpen && $route.path !== '/planner'" 
                class="absolute left-0 top-0 h-full w-1 bg-primary/30 rounded-r-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </router-link>

            <router-link to="/weather" 
              class="flex items-center gap-3 px-3 py-2.5 rounded-r-lg transition-all duration-300 cursor-pointer relative"
              :class="[
                $route.path === '/weather' && sidebarOpen ? 'bg-primary-container/20 text-on-primary-container border-r-4 border-primary' : 'text-on-surface-variant hover:bg-white/10'
              ]">
              <span class="material-symbols-outlined flex-shrink-0" 
                :class="$route.path === '/weather' && sidebarOpen ? 'text-primary' : 'text-on-surface-variant group-hover:text-primary'">cloudy_snowing</span>
              <span v-show="sidebarOpen" class="font-label-md whitespace-nowrap">Weather</span>
              <div v-if="!sidebarOpen && $route.path !== '/weather'" 
                class="absolute left-0 top-0 h-full w-1 bg-primary/30 rounded-r-full opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </router-link>
          </nav>
        </div>

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
    <main class="pt-16 min-h-screen" :class="(sidebarOpen && ($route.name === 'planner' || $route.name === 'weather')) ? 'lg:ml-64' : ''">
      <router-view />
    </main>

    <!-- Footer HANYA di Home -->
    <Footer v-if="$route.name === 'home'" />
  </div>
</template>

<script>
import { ref } from 'vue'
import Footer from './components/Footer.vue'

export default {
  name: 'App',
  components: {
    Footer
  },
  setup() {
    const sidebarOpen = ref(true)
    return { sidebarOpen }
  }
}
</script>

<style scoped>
aside::-webkit-scrollbar {
  display: none;
}
aside {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
aside {
  transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>