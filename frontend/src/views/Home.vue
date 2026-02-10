<template>
  <div class="playmate-container">
    <!-- Animated Background -->
    <div class="bg-gradient"></div>
    <div class="noise-overlay"></div>
    
    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Hero Section -->
      <header class="hero-section">
        <div class="hero-content">
          <h1 class="brand-title">
            <span class="brand-play">Play</span><span class="brand-mate">mate</span>
          </h1>
          
          <p v-if="isLoggedIn" class="welcome-text">
            <span class="wave-emoji">👋</span>
            Halo, <strong class="user-highlight">{{ userName }}</strong>
          </p>
        </div>
      </header>

      <!-- Wallet Section -->
      <section class="wallet-section">
        <div class="wallet-card">
          <div class="wallet-header">
            <div class="wallet-brand">
              <div class="wallet-icon">💳</div>
              <span class="wallet-brand-text">PLAYMATE PAY</span>
            </div>
            <button class="menu-btn">⋮</button>
          </div>
          
          <div class="balance-amount" @click="toggleBalanceVisibility">
            <span class="currency">Rp</span>
            <span class="amount">{{ isBalanceVisible ? formatPrice(userBalance) : '••••••' }}</span>
            <span class="toggle-icon">{{ isBalanceVisible ? '👁️' : '👁️‍🗨️' }}</span>
          </div>

          <div class="wallet-actions">
            <button class="action-btn" @click="openTopUp">
              <div class="action-icon scan">📱</div>
              <span>Scan</span>
            </button>
            <button class="action-btn" @click="openTopUp">
              <div class="action-icon topup">💰</div>
              <span>Top Up</span>
            </button>
            <button class="action-btn" @click="openHistory">
              <div class="action-icon history">📊</div>
              <span>Riwayat</span>
            </button>
          </div>

          <div class="premium-badge">
            <span class="premium-icon">⭐</span>
            <span>Premium</span>
            <span class="premium-arrow">→</span>
          </div>
        </div>
      </section>

      <!-- Sports Section -->
      <section class="sports-section">
        <div class="section-header">
          <h2 class="section-title">Pilih Olahraga</h2>
        </div>

        <div class="sports-grid">
          <div
            v-for="sport in sports"
            :key="sport.id"
            class="sport-item"
            @click="goToSport(sport.id)"
          >
            <div class="sport-icon-circle">
              <span class="sport-emoji">{{ icon(sport.name) }}</span>
            </div>
            <span class="sport-label">{{ sport.name }}</span>
          </div>
        </div>
      </section>

      <!-- Menu Features Section -->
      <section class="features-section">
        <div class="features-grid">
          <div class="feature-item" @click="goToLeaderboard">
            <div class="feature-icon-circle leaderboard">
              <span class="feature-emoji">🏆</span>
            </div>
            <span class="feature-label">Leaderboard</span>
          </div>

          <div class="feature-item" @click="goToEvent">
            <div class="feature-icon-circle event">
              <span class="feature-emoji">📅</span>
            </div>
            <span class="feature-label">Event</span>
          </div>

        <div class="feature-item" @click="goToPertandingan">
            <div class="feature-icon-circle event">
              <span class="feature-emoji">📅</span>
            </div>
            <span class="feature-label">Pertandingan</span>
          </div>

            <div class="feature-item" @click="goToShop">
            <div class="feature-icon-circle event">
              <span class="feature-emoji">📅</span>
            </div>
            <span class="feature-label">Shop</span>
          </div>

          <div class="feature-item" @click="goToTournament">
            <div class="feature-icon-circle tournament">
              <span class="feature-emoji">⚔️</span>
            </div>
            <span class="feature-label">Tournament</span>
          </div>

          <div class="feature-item" @click="goToLainnya">
            <div class="feature-icon-circle event">
              <span class="feature-emoji">📅</span>
            </div>
            <span class="feature-label">Lainnya</span>
          </div>


          
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "Home",
  data() {
    return {
      sports: [],
      userBalance: 0,
      isBalanceVisible: true
    };
  },
  computed: {
    isLoggedIn() {
      return !!localStorage.getItem("user");
    },
    userName() {
      const user = localStorage.getItem("user");
      if (!user) return "";
      return JSON.parse(user).name || "User";
    }
  },
  async mounted() {
    try {
      const res = await api.get("/sports");
      this.sports = res.data;
    } catch (err) {
      console.error("Gagal ambil data sports:", err);
    }
  },
  methods: {
    goToSport(id) {
      this.$router.push(`/sport/${id}`);
    },
    icon(name) {
      const map = {
        Badminton: "🏸",
        Paddle: "🎾",
        "Futsal": "⚽",
        Billiard: "🎱",
        Tenis: "🎾"
      };
      return map[name] || "🏆";
    },
    formatPrice(price) {
      return price.toLocaleString('id-ID');
    },
    toggleBalanceVisibility() {
      this.isBalanceVisible = !this.isBalanceVisible;
    },
    openTopUp() {
      alert("Fitur Top Up akan segera hadir!");
    },
    openHistory() {
      alert("Fitur Riwayat akan segera hadir!");
    },
    goToLeaderboard() {
    this.$router.push('/leaderboard');
  },
    goToEvent() {
      this.$router.push('/event');
    },
    goToPertandingan() {
      this.$router.push('/pertandingan');
    },
    goToShop() {
      this.$router.push('/shop');
    },
    goToTournament() {
      this.$router.push('/tournament');
    },
    gotoLainnya() {
      alert("akan segera hadir!");
    },
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

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
  max-width: 480px;
  margin: 0 auto;
  padding: 24px 20px;
}

/* Hero Section */
.hero-section {
  margin-bottom: 16px;
  animation: fadeInUp 0.8s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hero-content {
  text-align: center;
}

.brand-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1;
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

.welcome-text {
  font-size: 14px;
  color: #e0e0e0;
  animation: fadeIn 1s ease 0.3s both;
}

.wave-emoji {
  display: inline-block;
  animation: wave 2s ease infinite;
  margin-right: 4px;
}

@keyframes wave {
  0%, 100% { transform: rotate(0deg); }
  10%, 30% { transform: rotate(14deg); }
  20%, 40% { transform: rotate(-8deg); }
  50% { transform: rotate(14deg); }
  60% { transform: rotate(0deg); }
}

.user-highlight {
  color: #4ecdc4;
  font-weight: 600;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Wallet Section */
.wallet-section {
  margin-bottom: 24px;
  animation: fadeInUp 1s ease 0.3s both;
}

.wallet-card {
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.12) 0%, rgba(78, 205, 196, 0.12) 100%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 14px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.wallet-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.wallet-brand {
  display: flex;
  align-items: center;
  gap: 6px;
}

.wallet-icon {
  font-size: 16px;
}

.wallet-brand-text {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 12px;
  color: #fff;
  letter-spacing: 0.5px;
}

.menu-btn {
  background: transparent;
  border: none;
  color: #fff;
  font-size: 18px;
  cursor: pointer;
  padding: 2px;
}

.balance-amount {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  user-select: none;
  margin-bottom: 12px;
}

.currency {
  font-size: 14px;
  color: #999;
  font-weight: 500;
}

.amount {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  letter-spacing: -0.02em;
}

.toggle-icon {
  font-size: 14px;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.balance-amount:hover .toggle-icon {
  opacity: 1;
}

.wallet-actions {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}

.action-btn {
  flex: 1;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 10px 6px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #fff;
  font-size: 11px;
  font-weight: 500;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  transform: translateY(-2px);
}

.action-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.action-icon.scan {
  background: rgba(78, 205, 196, 0.2);
}

.action-icon.topup {
  background: rgba(255, 107, 107, 0.2);
}

.action-icon.history {
  background: rgba(255, 195, 113, 0.2);
}

.premium-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: linear-gradient(90deg, rgba(255, 215, 0, 0.12) 0%, rgba(255, 195, 113, 0.12) 100%);
  border: 1px solid rgba(255, 215, 0, 0.25);
  border-radius: 8px;
  color: #ffd700;
  font-weight: 600;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.premium-badge:hover {
  background: linear-gradient(90deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 195, 113, 0.2) 100%);
  transform: translateX(2px);
}

.premium-icon {
  font-size: 14px;
}

.premium-arrow {
  margin-left: auto;
  font-size: 14px;
}

/* Sports Section */
.sports-section {
  animation: fadeInUp 1s ease 0.5s both;
  margin-bottom: 24px;
}

.section-header {
  margin-bottom: 20px;
}

.section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #fff;
}

/* Sports Grid */
.sports-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.sport-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.sport-item:hover {
  transform: translateY(-4px);
}

.sport-icon-circle {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(78, 205, 196, 0.2) 100%);
  border: 2px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.sport-item:hover .sport-icon-circle {
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.3) 0%, rgba(78, 205, 196, 0.3) 100%);
  border-color: rgba(255, 107, 107, 0.5);
  box-shadow: 0 8px 24px rgba(255, 107, 107, 0.3);
}

.sport-emoji {
  font-size: 32px;
  transition: transform 0.3s ease;
}

.sport-item:hover .sport-emoji {
  transform: scale(1.15) rotate(5deg);
}

.sport-label {
  font-size: 12px;
  color: #e0e0e0;
  font-weight: 500;
  text-align: center;
  line-height: 1.3;
}

/* Features Section */
.features-section {
  animation: fadeInUp 1s ease 0.7s both;
  margin-top: 30px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: transform 0.3s ease;
  padding: 10px 8px;
  background: rgba(255, 255, 255, 0.01);
  border: 1px solid rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.feature-item:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.03);
  border-color: rgba(255, 255, 255, 0.08);
}

.feature-icon-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.feature-icon-circle.leaderboard {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.15) 0%, rgba(255, 195, 113, 0.15) 100%);
}

.feature-icon-circle.event {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(167, 139, 250, 0.15) 100%);
}

.feature-icon-circle.tournament {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(248, 113, 113, 0.15) 100%);
}
.feature-icon-circle.Pertandingan {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.15) 0%, rgba(248, 113, 113, 0.15) 100%);
}

.feature-item:hover .feature-icon-circle.leaderboard {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.25) 0%, rgba(255, 195, 113, 0.25) 100%);
  border-color: rgba(255, 215, 0, 0.3);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.2);
}

.feature-item:hover .feature-icon-circle.event {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.25) 0%, rgba(167, 139, 250, 0.25) 100%);
  border-color: rgba(139, 92, 246, 0.3);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}

.feature-item:hover .feature-icon-circle.tournament {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.25) 0%, rgba(248, 113, 113, 0.25) 100%);
  border-color: rgba(239, 68, 68, 0.3);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}
.feature-item:hover .feature-icon-circle.pertandingan {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.25) 0%, rgba(248, 113, 113, 0.25) 100%);
  border-color: rgba(239, 68, 68, 0.3);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}
.feature-item:hover .feature-icon-circle.shop {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.25) 0%, rgba(167, 139, 250, 0.25) 100%);
  border-color: rgba(139, 92, 246, 0.3);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}
.feature-item:hover .feature-icon-circle.lainyya {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.25) 0%, rgba(167, 139, 250, 0.25) 100%);
  border-color: rgba(139, 92, 246, 0.3);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.2);
}


.feature-emoji {
  font-size: 24px;
  transition: transform 0.3s ease;
}

.feature-item:hover .feature-emoji {
  transform: scale(1.1);
}

.feature-label {
  font-size: 11px;
  color: #999;
  font-weight: 500;
  text-align: center;
  line-height: 1.3;
}

/* ========================================
   RESPONSIVE DESIGN - TABLET & DESKTOP
   ======================================== */

/* Tablet (Portrait) - 768px */
@media (min-width: 768px) {
  .content-wrapper {
    max-width: 500px;
    padding: 32px 24px;
  }

  .brand-title {
    font-size: 36px;
  }

  .wallet-card {
    padding: 18px;
  }

  .amount {
    font-size: 28px;
  }

  .wallet-actions {
    gap: 12px;
  }

  .action-btn {
    padding: 12px 8px;
    font-size: 12px;
  }

  .action-icon {
    width: 40px;
    height: 40px;
    font-size: 20px;
  }

  .section-title {
    font-size: 24px;
  }

  .sports-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
  }

  .sport-icon-circle {
    width: 80px;
    height: 80px;
  }

  .sport-emoji {
    font-size: 36px;
  }

  .sport-label {
    font-size: 13px;
  }

  .features-grid {
    gap: 12px;
  }

  .feature-item {
    padding: 14px 10px;
  }

  .feature-icon-circle {
    width: 60px;
    height: 60px;
  }

  .feature-emoji {
    font-size: 28px;
  }

  .feature-label {
    font-size: 12px;
  }
}

/* Desktop - 1024px and above */
@media (min-width: 1024px) {
  .content-wrapper {
    max-width: 520px;
    padding: 40px 28px;
  }

  .brand-title {
    font-size: 40px;
  }

  .welcome-text {
    font-size: 15px;
  }

  .wallet-card {
    padding: 20px;
  }

  .wallet-brand-text {
    font-size: 13px;
  }

  .amount {
    font-size: 30px;
  }

  .wallet-actions {
    gap: 14px;
  }

  .action-btn {
    padding: 14px 10px;
    font-size: 13px;
    border-radius: 12px;
  }

  .action-icon {
    width: 44px;
    height: 44px;
    font-size: 22px;
  }

  .premium-badge {
    padding: 10px 14px;
    font-size: 13px;
  }

  .section-title {
    font-size: 26px;
    margin-bottom: 4px;
  }

  .sports-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
  }

  .sport-icon-circle {
    width: 85px;
    height: 85px;
  }

  .sport-emoji {
    font-size: 38px;
  }

  .sport-label {
    font-size: 14px;
  }

  .features-section {
    margin-top: 36px;
  }

  .features-grid {
    gap: 14px;
  }

  .feature-item {
    padding: 16px 12px;
  }

  .feature-icon-circle {
    width: 64px;
    height: 64px;
  }

  .feature-emoji {
    font-size: 30px;
  }

  .feature-label {
    font-size: 13px;
  }
}

/* Large Desktop - 1440px */
@media (min-width: 1440px) {
  .content-wrapper {
    max-width: 540px;
  }
}

/* Mobile Responsive */
@media (max-width: 480px) {
  .content-wrapper {
    padding: 20px 16px;
  }

  .brand-title {
    font-size: 28px;
  }

  .wallet-card {
    padding: 12px;
  }

  .amount {
    font-size: 20px;
  }

  .sports-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }

  .sport-icon-circle {
    width: 65px;
    height: 65px;
  }

  .sport-emoji {
    font-size: 28px;
  }

  .features-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
  }

  .feature-item {
    padding: 8px 6px;
  }

  .feature-icon-circle {
    width: 45px;
    height: 45px;
  }

  .feature-emoji {
    font-size: 20px;
  }

  .feature-label {
    font-size: 10px;
  }
}

@media (max-width: 360px) {
  .sports-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }

  .sport-icon-circle {
    width: 60px;
    height: 60px;
  }

  .features-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
  }

  .feature-item {
    padding: 6px 4px;
  }

  .feature-icon-circle {
    width: 40px;
    height: 40px;
  }

  .feature-emoji {
    font-size: 18px;
  }

  .feature-label {
    font-size: 9px;
  }
}
</style>