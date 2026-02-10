<template>
  <div class="auth-container">
    <!-- Animated Background -->
    <div class="bg-gradient"></div>
    <div class="noise-overlay"></div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <div class="auth-card">
        <!-- Logo/Brand -->
        <div class="brand-section">
          <div class="brand-icon"></div>
          <h1 class="brand-title">
            <span class="brand-play">Play</span><span class="brand-mate">mate</span>
          </h1>
          <p class="brand-subtitle">Masuk ke akun Anda</p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="auth-form">
          <!-- Email Input -->
          <div class="input-group">
            <label class="input-label">Email</label>
            <div class="input-wrapper">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" class="input-icon">
                <rect x="3" y="5" width="18" height="14" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M3 7L12 13L21 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <input
                v-model="email"
                type="email"
                placeholder="nama@email.com"
                class="auth-input"
                required
              />
            </div>
          </div>

          <!-- Password Input -->
          <div class="input-group">
            <label class="input-label">Password</label>
            <div class="input-wrapper">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" class="input-icon">
                <rect x="5" y="11" width="14" height="10" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M12 17V17.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M8 11V7C8 5.93913 8.42143 4.92172 9.17157 4.17157C9.92172 3.42143 10.9391 3 12 3C13.0609 3 14.0783 3.42143 14.8284 4.17157C15.5786 4.92172 16 5.93913 16 7V11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <input
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Masukkan password"
                class="auth-input password-input"
                required
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="toggle-password"
              >
                <span v-if="showPassword">👁️</span>
                <span v-else>🙈</span>
              </button>
            </div>
          </div>

          <!-- Error Message -->
          <div v-if="errorMessage" class="error-message">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M12 8V12M12 16H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>{{ errorMessage }}</span>
          </div>

          <!-- Login Button -->
          <button type="submit" class="auth-button primary" :disabled="isLoading">
            <span v-if="!isLoading">Masuk</span>
            <span v-else>Loading...</span>
            <svg v-if="!isLoading" width="18" height="18" viewBox="0 0 20 20" fill="none">
              <path d="M4 10H16M16 10L11 5M16 10L11 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </button>

          <!-- Register Button -->
          <button
            type="button"
            class="auth-button secondary"
            @click="goToRegister"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M16 21V19C16 17.9391 15.5786 16.9217 14.8284 16.1716C14.0783 15.4214 13.0609 15 12 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="8.5" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
              <path d="M20 8V14M17 11H23" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>Buat Akun Baru</span>
          </button>
        </form>
      </div>

      <!-- Footer -->
      <div class="auth-footer">
        <p>© 2024 Playmate. All rights reserved.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "@/services/api"

const router = useRouter()

const email = ref("")
const password = ref("")
const showPassword = ref(false)
const errorMessage = ref("")
const isLoading = ref(false)

function goToRegister() {
  router.push("/register")
}

async function handleLogin() {
  errorMessage.value = ""
  
  // Validasi input
  if (!email.value || !password.value) {
    errorMessage.value = "Email dan password wajib diisi"
    return
  }

  isLoading.value = true

  try {
    // Login via API
    const response = await api.post("/auth/login", {
      email: email.value,
      password: password.value
    })

    const userData = response.data

    // Simpan user data ke localStorage
    localStorage.setItem("user", JSON.stringify(userData))

    // Redirect berdasarkan role
    if (userData.role === "admin") {
      router.push("/admindashboard")
    } else {
      router.push("/")
    }

  } catch (error) {
    console.error("Login error:", error)
    
    // Tampilkan error message
    if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail
    } else if (error.response?.data?.message) {
      errorMessage.value = error.response.data.message
    } else {
      errorMessage.value = "Login gagal. Periksa email dan password Anda."
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.auth-container {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  font-family: 'DM Sans', sans-serif;
  background: #0a0a0a;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

/* Animated Background */
.bg-gradient {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 30%, rgba(255, 107, 107, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(78, 205, 196, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(255, 195, 113, 0.1) 0%, transparent 50%),
    linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
  animation: gradientShift 15s ease infinite;
  z-index: 0;
}

@keyframes gradientShift {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
}

.noise-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 1;
}

.content-wrapper {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 440px;
}

/* Auth Card */
.auth-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 48px;
  backdrop-filter: blur(20px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: cardFadeIn 0.8s ease;
}

@keyframes cardFadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Brand Section */
.brand-section {
  text-align: center;
  margin-bottom: 40px;
}

.brand-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  animation: iconFloat 3s ease infinite;
}

@keyframes iconFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.brand-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 36px;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-bottom: 8px;
}

.brand-play {
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-mate {
  color: #4ecdc4;
}

.brand-subtitle {
  font-size: 15px;
  color: #888;
  margin: 0;
}

/* Form */
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-label {
  font-size: 14px;
  font-weight: 600;
  color: #e0e0e0;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 16px;
  color: #666;
  pointer-events: none;
  z-index: 1;
}

.auth-input {
  width: 100%;
  padding: 16px 16px 16px 48px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #e0e0e0;
  font-size: 15px;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.3s ease;
}

.auth-input::placeholder {
  color: #666;
}

.auth-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(78, 205, 196, 0.5);
}

.password-input {
  padding-right: 50px;
}

.toggle-password {
  position: absolute;
  right: 16px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 18px;
  z-index: 1;
  padding: 4px;
  transition: transform 0.2s ease;
}

.toggle-password:hover {
  transform: scale(1.1);
}

/* Error Message */
.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: 10px;
  color: #ef4444;
  font-size: 14px;
}

/* Buttons */
.auth-button {
  width: 100%;
  padding: 16px 24px;
  border-radius: 12px;
  border: none;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  position: relative;
  overflow: hidden;
}

.auth-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.auth-button:hover:not(:disabled)::before {
  left: 100%;
}

.auth-button.primary {
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  color: white;
}

.auth-button.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
}

.auth-button.secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e0e0e0;
}

.auth-button.secondary:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(78, 205, 196, 0.3);
  transform: translateY(-2px);
}

.auth-button:active:not(:disabled) {
  transform: translateY(0);
}

/* Footer */
.auth-footer {
  margin-top: 24px;
  text-align: center;
  color: #666;
  font-size: 13px;
}

/* Responsive */
@media (max-width: 520px) {
  .auth-card {
    padding: 36px 28px;
  }

  .brand-title {
    font-size: 28px;
  }

  .brand-icon {
    width: 64px;
    height: 64px;
  }
}
</style>