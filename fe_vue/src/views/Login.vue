<template>
    <div class="container">
        <h1>Login</h1>
        <form @submit.prevent="handleLogin">
            <div class="mb-3">
                <label for="username" class="form-label">Username</label>
                <input v-model="username" type="text" class="form-control" id="username" required />
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input v-model="password" type="password" class="form-control" id="password" required />
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</template>
  
<script>
import { useAuthStore } from '../store/auth';

export default {
    data() {
        return {
        username: '',
        password: '',
        };
    },
    methods: {
        async handleLogin() {
        const authStore = useAuthStore();
        try {
            await authStore.login(this.username, this.password);
            this.$router.push('/profile'); // Redirect to profile after login
        } catch (error) {
            alert('Login failed');
        }
        },
    },
};
</script>
  