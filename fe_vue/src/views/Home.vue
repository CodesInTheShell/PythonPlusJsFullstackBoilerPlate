<template>
    <div class="container">
        <h1>Welcome</h1>
        <button class="btn btn-primary" @click="$router.push('/login')">Go to Login</button>
    </div>
</template>
  
<script>
    export default {
        name: 'Home',
    };
</script>
  