import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Profile from '../views/Profile.vue';
import { useAuthStore } from '../store/auth';

const routes = [
    { path: '/', component: Home, meta: { public: true } },
    { path: '/login', component: Login, meta: { public: true } },
    { path: '/profile', component: Profile }, // Protected route
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    if (!to.meta.public && !authStore.isAuthenticated) {
        next('/login'); // Redirect to login if not authenticated
    } else {
        next();
    }
});

export default router;
