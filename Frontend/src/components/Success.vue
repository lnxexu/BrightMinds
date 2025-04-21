<template>
    <div class="success-container">
        <div class="success-card">
            <i class="fas fa-check-circle success-icon"></i>
            <h2>Account Verified Successfully!</h2>
            <p>Your account has been successfully verified and is now ready to use.</p>
            <router-link to="/" class="login-button">
                Proceed to Login
            </router-link>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Success'
}
</script>

<style scoped>
.success-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f5f5f5;
}

.success-card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
    max-width: 400px;
}

.success-icon {
    color: #4CAF50;
    font-size: 4rem;
    margin-bottom: 1rem;
}

h2 {
    color: #333;
    margin-bottom: 1rem;
}

p {
    color: #666;
    margin-bottom: 1.5rem;
}

.login-button {
    display: inline-block;
    padding: 0.8rem 1.5rem;
    background-color: #4CAF50;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.3s;
}

.login-button:hover {
    background-color: #45a049;
}
</style>