<template>
  <div class="playmate-container">
    <!-- Animated Background -->
    <div class="bg-gradient"></div>
    <div class="noise-overlay"></div>
    
    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Loading State -->
      <div v-if="!user" class="state-message">
        <div class="loader"></div>
        <p>Memuat profile...</p>
      </div>

      <!-- Profile Content -->
      <div v-else class="profile-content">
        <!-- Header -->
        <header class="profile-header">
          <h1 class="page-title">
            <span class="title-icon">👤</span>
            <span>Profile Saya</span>
          </h1>
          <div class="title-underline"></div>
        </header>

        <!-- Profile Card -->
        <div class="profile-card">
          <div class="card-glow"></div>
          
          <!-- Avatar Section -->
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <img 
                :src="user.photo || defaultPhoto" 
                :alt="user.name"
                class="avatar-image"
              />
              <div class="avatar-ring"></div>
            </div>
            <h2 class="user-name">{{ user.name }}</h2>
            <p class="user-email">{{ user.email }}</p>
          </div>

          <!-- Info Grid -->
          <div class="info-grid">
            <div class="info-item">
              <div class="info-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M16 7C16 9.20914 14.2091 11 12 11C9.79086 11 8 9.20914 8 7C8 4.79086 9.79086 3 12 3C14.2091 3 16 4.79086 16 7Z" stroke="currentColor" stroke-width="2"/>
                  <path d="M12 14C8.13401 14 5 17.134 5 21H19C19 17.134 15.866 14 12 14Z" stroke="currentColor" stroke-width="2"/>
                </svg>
                <span>User ID</span>
              </div>
              <div class="info-value">{{ user.id }}</div>
            </div>

            <div class="info-item">
              <div class="info-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M20 21V19C20 16.7909 18.2091 15 16 15H8C5.79086 15 4 16.7909 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                  <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                </svg>
                <span>Provider</span>
              </div>
              <div class="info-value provider">{{ user.provider }}</div>
            </div>

            <div class="info-item">
              <div class="info-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <rect x="3" y="4" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2"/>
                  <path d="M16 2V6M8 2V6M3 10H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <span>Tanggal Lahir</span>
              </div>
              <div class="info-value">{{ formatDate(user.birth_date) }}</div>
            </div>

            <div class="info-item">
              <div class="info-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/>
                  <path d="M12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
                <span>Login Pertama</span>
              </div>
              <div class="info-value">{{ formatDateTime(user.first_login_at) }}</div>
            </div>

            <div class="info-item">
              <div class="info-label">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M2 17L12 22L22 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M2 12L12 17L22 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span>Akun Dibuat</span>
              </div>
              <div class="info-value">{{ formatDateTime(user.created_at) }}</div>
            </div>
          </div>

          <!-- Action Button -->
          <button class="back-btn" @click="$router.push('/')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M19 12H5M5 12L12 19M5 12L12 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span>Kembali ke Home</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Profile",
  data() {
    return {
      user: null,
      defaultPhoto: "https://ui-avatars.com/api/?background=4ecdc4&color=fff&name=User&size=200"
    };
  },
  mounted() {
    const storedUser = localStorage.getItem("user");
    
    if (!storedUser) {
      this.$router.push("/login");
      return;
    }
    
    this.user = JSON.parse(storedUser);
  },
  methods: {
    formatDate(date) {
      if (!date) return "-";
      return new Date(date).toLocaleDateString("id-ID", {
        day: 'numeric',
        month: 'long',
        year: 'numeric'
      });
    },
    formatDateTime(date) {
      if (!date) return "-";
      return new Date(date).toLocaleString("id-ID", {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.playmate-container {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  font-family: 'DM Sans', sans-serif;
  background: #0a0a0a;
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
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
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
  max-width: 800px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Loading State */
.state-message {
  text-align: center;
  padding: 100px 20px;
  animation: fadeIn 0.6s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.loader {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top-color: #4ecdc4;
  border-radius: 50%;
  margin: 0 auto 20px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.state-message p {
  color: #888;
  font-size: 16px;
}

/* Profile Content */
.profile-content {
  animation: fadeInUp 0.8s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Profile Header */
.profile-header {
  text-align: center;
  margin-bottom: 50px;
}

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(36px, 6vw, 48px);
  font-weight: 700;
  color: #fff;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.title-icon {
  font-size: clamp(40px, 6vw, 52px);
  display: inline-block;
  animation: pulse 2s ease infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.title-underline {
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #ff6b6b 0%, #4ecdc4 100%);
  margin: 0 auto;
  border-radius: 2px;
  animation: expandLine 1s ease;
}

@keyframes expandLine {
  from { width: 0; }
  to { width: 80px; }
}

/* Profile Card */
.profile-card {
  position: relative;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 48px 40px;
  overflow: hidden;
  transition: all 0.4s ease;
}

.card-glow {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  height: 200px;
  background: radial-gradient(circle, rgba(78, 205, 196, 0.15) 0%, transparent 70%);
  pointer-events: none;
}

.profile-card:hover {
  border-color: rgba(78, 205, 196, 0.2);
  box-shadow: 0 20px 60px rgba(78, 205, 196, 0.1);
}

/* Avatar Section */
.avatar-section {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
  z-index: 1;
}

.avatar-wrapper {
  position: relative;
  display: inline-block;
  margin-bottom: 24px;
}

.avatar-image {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid rgba(78, 205, 196, 0.3);
  position: relative;
  z-index: 1;
  animation: avatarFadeIn 1s ease;
}

@keyframes avatarFadeIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.avatar-ring {
  position: absolute;
  top: -8px;
  left: -8px;
  right: -8px;
  bottom: -8px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
  opacity: 0.2;
  animation: ringPulse 3s ease infinite;
}

@keyframes ringPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 0.2;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.3;
  }
}

.user-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px 0;
}

.user-email {
  font-size: 15px;
  color: #4ecdc4;
  margin: 0;
}

/* Info Grid */
.info-grid {
  display: grid;
  gap: 20px;
  margin-bottom: 32px;
}

.info-item {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 16px;
  padding: 20px 24px;
  transition: all 0.3s ease;
}

.info-item:hover {
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(255, 255, 255, 0.1);
  transform: translateX(4px);
}

.info-label {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
  margin-bottom: 10px;
}

.info-label svg {
  color: #4ecdc4;
}

.info-value {
  font-size: 16px;
  color: #e0e0e0;
  font-weight: 500;
}

.info-value.provider {
  text-transform: capitalize;
  color: #4ecdc4;
  font-weight: 600;
}

/* Back Button */
.back-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 24px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.03);
  color: #e0e0e0;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'DM Sans', sans-serif;
}

.back-btn:hover {
  background: rgba(78, 205, 196, 0.1);
  border-color: rgba(78, 205, 196, 0.3);
  color: #4ecdc4;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(78, 205, 196, 0.15);
}

.back-btn svg {
  transition: transform 0.3s ease;
}

.back-btn:hover svg {
  transform: translateX(-4px);
}

/* Responsive */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 40px 20px;
  }

  .profile-card {
    padding: 32px 24px;
  }

  .avatar-image {
    width: 120px;
    height: 120px;
  }

  .user-name {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 32px;
  }

  .profile-card {
    padding: 28px 20px;
  }

  .avatar-image {
    width: 100px;
    height: 100px;
  }

  .info-item {
    padding: 16px 20px;
  }
}
</style>