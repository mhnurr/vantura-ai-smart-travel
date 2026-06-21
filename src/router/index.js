import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PlannerView from '../views/PlannerView.vue'
import WeatherView from '../views/WeatherView.vue'

const routes = [{
        path: '/',
        name: 'home',
        component: HomeView
    },
    {
        path: '/planner',
        name: 'planner',
        component: PlannerView
    },
    {
        path: '/weather',
        name: 'weather',
        component: WeatherView
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router