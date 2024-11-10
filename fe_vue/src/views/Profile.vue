<template>
    <div class="container">
        <h1>Profile</h1>
        <p v-if="user">Welcome, {{ user.username }}!</p>
        <button @click="logout" class="btn btn-danger">Logout</button>
    </div>
  </template>
  
<script>
import { useAuthStore } from '../store/auth';
import axios from 'axios';

export default {
    data() {
    return {
        user: null,
    };
    },
    async created() {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/user/me', {
        headers: { 'x-access-token': useAuthStore().token },
        });
        this.user = response.data;
    } catch (error) {
        alert('Failed to load user data');
        this.$router.push('/login');
    }
    },
    methods: {
        logout() {
            useAuthStore().logout();
            this.$router.push('/login');
        },
    },
};
</script>
  