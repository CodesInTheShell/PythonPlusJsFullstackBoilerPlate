import { defineStore } from 'pinia';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
    }),
    getters: {
        isAuthenticated: (state) => !!state.token,
    },
    actions: {
        async login(username, password) {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/login', {
            username,
            password,
            });
            this.token = response.data.token;
            localStorage.setItem('token', response.data.token);
            axios.defaults.headers.common['x-access-token'] = response.data.token;
        } catch (error) {
            throw new Error('Login failed');
        }
        },
        logout() {
            this.token = null;
            localStorage.removeItem('token');
            delete axios.defaults.headers.common['x-access-token'];
        },
    },
});
