<template>
  <div class="leaderboard-container">
    <!-- Animated Background -->
    <div class="bg-gradient"></div>
    <div class="noise-overlay"></div>
    
    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Header -->
      <header class="page-header">
        <button class="back-btn" @click="goBack">
          <span>←</span>
        </button>
        <h1 class="page-title">
          <span class="title-icon">🏆</span>
          Leaderboard
        </h1>
        <div class="header-spacer"></div>
      </header>

      <!-- Sport Filter -->
      <section class="filter-section">
        <div class="filter-scroll">
          <button
            v-for="sport in sports"
            :key="sport.id"
            class="filter-btn"
            :class="{ active: selectedSport === sport.id }"
            @click="selectSport(sport.id)"
          >
            <span class="filter-emoji">{{ sport.icon }}</span>
            <span class="filter-label">{{ sport.name }}</span>
          </button>
        </div>
      </section>

      <!-- Leaderboard List -->
      <section class="leaderboard-section">
        <div class="podium-section">
          <div class="podium-item second">
            <div class="podium-avatar">
              <img :src="getAvatarUrl(currentLeaderboard[1]?.name)" alt="2nd">
              <div class="podium-medal silver">2</div>
            </div>
            <div class="podium-name">{{ currentLeaderboard[1]?.name }}</div>
            <div class="podium-score">{{ currentLeaderboard[1]?.score }} pts</div>
          </div>

          <div class="podium-item first">
            <div class="podium-avatar champion">
              <img :src="getAvatarUrl(currentLeaderboard[0]?.name)" alt="1st">
              <div class="podium-medal gold">1</div>
              <div class="crown">👑</div>
            </div>
            <div class="podium-name">{{ currentLeaderboard[0]?.name }}</div>
            <div class="podium-score">{{ currentLeaderboard[0]?.score }} pts</div>
          </div>

          <div class="podium-item third">
            <div class="podium-avatar">
              <img :src="getAvatarUrl(currentLeaderboard[2]?.name)" alt="3rd">
              <div class="podium-medal bronze">3</div>
            </div>
            <div class="podium-name">{{ currentLeaderboard[2]?.name }}</div>
            <div class="podium-score">{{ currentLeaderboard[2]?.score }} pts</div>
          </div>
        </div>

        <div class="ranking-list">
          <div
            v-for="(player, index) in currentLeaderboard.slice(3)"
            :key="index"
            class="rank-item"
          >
            <div class="rank-number">{{ index + 4 }}</div>
            <div class="rank-avatar">
              <img :src="getAvatarUrl(player.name)" :alt="player.name">
            </div>
            <div class="rank-info">
              <div class="rank-name">{{ player.name }}</div>
              <div class="rank-stats">
                <span class="stat-item">🎯 {{ player.wins }}W</span>
                <span class="stat-item">❌ {{ player.losses }}L</span>
              </div>
            </div>
            <div class="rank-score">
              <div class="score-value">{{ player.score }}</div>
              <div class="score-label">pts</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: "Leaderboard",
  data() {
    return {
      selectedSport: 'paddle',
      sports: [
        { id: 'paddle', name: 'Paddle', icon: '🎾' },
        { id: 'tenis', name: 'Tenis', icon: '🎾' },
        { id: 'badminton', name: 'Badminton', icon: '🏸' },
        { id: 'basket', name: 'Basket', icon: '🏀' },
        { id: 'minisoccer', name: 'Mini Soccer', icon: '⚽' }
      ],
      leaderboards: {
        paddle: [
          { name: 'Budi Santoso', score: 2850, wins: 45, losses: 12 },
          { name: 'Andi Wijaya', score: 2720, wins: 42, losses: 15 },
          { name: 'Dewi Lestari', score: 2650, wins: 40, losses: 16 },
          { name: 'Rudi Hartono', score: 2520, wins: 38, losses: 18 },
          { name: 'Siti Nurhaliza', score: 2480, wins: 36, losses: 19 },
          { name: 'Ahmad Yani', score: 2420, wins: 35, losses: 20 },
          { name: 'Maya Sari', score: 2380, wins: 33, losses: 22 },
          { name: 'Eko Prasetyo', score: 2320, wins: 31, losses: 24 },
          { name: 'Rina Susanti', score: 2280, wins: 30, losses: 25 },
          { name: 'Doni Setiawan', score: 2240, wins: 28, losses: 27 }
        ],
        tenis: [
          { name: 'Agung Pratama', score: 3100, wins: 52, losses: 8 },
          { name: 'Linda Wijaya', score: 2980, wins: 49, losses: 11 },
          { name: 'Bambang Suryanto', score: 2850, wins: 46, losses: 14 },
          { name: 'Citra Dewi', score: 2720, wins: 43, losses: 17 },
          { name: 'Hendra Gunawan', score: 2650, wins: 41, losses: 19 },
          { name: 'Fitri Handayani', score: 2580, wins: 39, losses: 21 },
          { name: 'Yoga Prasetya', score: 2510, wins: 37, losses: 23 },
          { name: 'Dian Sastro', score: 2450, wins: 35, losses: 25 },
          { name: 'Irfan Bachdim', score: 2390, wins: 33, losses: 27 },
          { name: 'Tara Basro', score: 2330, wins: 31, losses: 29 }
        ],
        badminton: [
          { name: 'Kevin Sanjaya', score: 3250, wins: 58, losses: 5 },
          { name: 'Greysia Polii', score: 3120, wins: 55, losses: 8 },
          { name: 'Anthony Ginting', score: 2990, wins: 51, losses: 12 },
          { name: 'Apriyani Rahayu', score: 2880, wins: 48, losses: 15 },
          { name: 'Jonatan Christie', score: 2780, wins: 45, losses: 18 },
          { name: 'Putri Kusuma', score: 2690, wins: 42, losses: 21 },
          { name: 'Fajar Alfian', score: 2620, wins: 40, losses: 23 },
          { name: 'Siti Fadia', score: 2550, wins: 38, losses: 25 },
          { name: 'Bagas Maulana', score: 2480, wins: 36, losses: 27 },
          { name: 'Rizki Amelia', score: 2410, wins: 34, losses: 29 }
        ],
        basket: [
          { name: 'Michael Jordan Jr', score: 2950, wins: 48, losses: 10 },
          { name: 'Kobe Prasetyo', score: 2830, wins: 45, losses: 13 },
          { name: 'LeBron Wijaya', score: 2720, wins: 42, losses: 16 },
          { name: 'Curry Santoso', score: 2640, wins: 40, losses: 18 },
          { name: 'Durant Gunawan', score: 2560, wins: 38, losses: 20 },
          { name: 'Harden Kusuma', score: 2490, wins: 36, losses: 22 },
          { name: 'Giannis Pratama', score: 2420, wins: 34, losses: 24 },
          { name: 'Luka Setiawan', score: 2350, wins: 32, losses: 26 },
          { name: 'Tatum Wijaya', score: 2280, wins: 30, losses: 28 },
          { name: 'Booker Hartono', score: 2210, wins: 28, losses: 30 }
        ],
        minisoccer: [
          { name: 'Ronaldo Putra', score: 3050, wins: 50, losses: 9 },
          { name: 'Messi Pratama', score: 2940, wins: 47, losses: 12 },
          { name: 'Neymar Kusuma', score: 2820, wins: 44, losses: 15 },
          { name: 'Mbappe Santoso', score: 2730, wins: 41, losses: 18 },
          { name: 'Haaland Gunawan', score: 2650, wins: 39, losses: 20 },
          { name: 'Salah Prasetyo', score: 2570, wins: 37, losses: 22 },
          { name: 'Kane Wijaya', score: 2500, wins: 35, losses: 24 },
          { name: 'Benzema Hartono', score: 2430, wins: 33, losses: 26 },
          { name: 'Lewandowski Dwi', score: 2360, wins: 31, losses: 28 },
          { name: 'Suarez Budi', score: 2290, wins: 29, losses: 30 }
        ]
      }
    };
  },
  computed: {
    currentLeaderboard() {
      return this.leaderboards[this.selectedSport] || [];
    }
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    selectSport(sportId) {
      this.selectedSport = sportId;
    },
    getAvatarUrl(name) {
      return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=random&color=fff&size=128`;
    }
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

.leaderboard-container {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  font-family: 'DM Sans', sans-serif;
  background: #0a0a0a;
  padding-bottom: 40px;
}

.bg-gradient {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 30%, rgba(255, 215, 0, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(78, 205, 196, 0.1) 0%, transparent 50%),
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
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
  animation: fadeInDown 0.6s ease;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.back-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #fff;
  font-size: 20px;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(-2px);
}

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  font-size: 28px;
}

.header-spacer {
  width: 44px;
}

.filter-section {
  margin-bottom: 32px;
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

.filter-scroll {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 8px;
  scrollbar-width: none;
}

.filter-scroll::-webkit-scrollbar {
  display: none;
}

.filter-btn {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 10px 18px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #999;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 215, 0, 0.3);
}

.filter-btn.active {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 195, 113, 0.2) 100%);
  border-color: rgba(255, 215, 0, 0.5);
  color: #ffd700;
}

.filter-emoji {
  font-size: 18px;
}

.podium-section {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: 12px;
  margin-bottom: 32px;
  animation: fadeInUp 1s ease 0.2s both;
}

.podium-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  flex: 1;
  max-width: 120px;
}

.podium-item.first {
  order: 2;
}

.podium-item.second {
  order: 1;
}

.podium-item.third {
  order: 3;
}

.podium-avatar {
  position: relative;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  border: 3px solid rgba(255, 255, 255, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
}

.podium-avatar.champion {
  width: 96px;
  height: 96px;
  border-color: rgba(255, 215, 0, 0.5);
  box-shadow: 0 0 30px rgba(255, 215, 0, 0.3);
}

.podium-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.crown {
  position: absolute;
  top: -18px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 24px;
  animation: float 2s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50% { transform: translateX(-50%) translateY(-5px); }
}

.podium-medal {
  position: absolute;
  bottom: -4px;
  right: -4px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  border: 2px solid #0a0a0a;
}

.podium-medal.gold {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  color: #000;
}

.podium-medal.silver {
  background: linear-gradient(135deg, #c0c0c0 0%, #e8e8e8 100%);
  color: #000;
}

.podium-medal.bronze {
  background: linear-gradient(135deg, #cd7f32 0%, #e09850 100%);
  color: #fff;
}

.podium-name {
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  text-align: center;
  line-height: 1.2;
}

.podium-score {
  font-size: 12px;
  color: #ffd700;
  font-weight: 600;
}

.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.rank-item {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 14px;
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 14px;
  transition: all 0.3s ease;
  animation: fadeInUp 1s ease both;
}

.rank-item:nth-child(1) { animation-delay: 0.3s; }
.rank-item:nth-child(2) { animation-delay: 0.35s; }
.rank-item:nth-child(3) { animation-delay: 0.4s; }
.rank-item:nth-child(4) { animation-delay: 0.45s; }
.rank-item:nth-child(5) { animation-delay: 0.5s; }
.rank-item:nth-child(6) { animation-delay: 0.55s; }
.rank-item:nth-child(7) { animation-delay: 0.6s; }

.rank-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 215, 0, 0.2);
  transform: translateX(4px);
}

.rank-number {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: #666;
  min-width: 28px;
  text-align: center;
}

.rank-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.rank-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.rank-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.rank-name {
  font-size: 15px;
  font-weight: 600;
  color: #fff;
}

.rank-stats {
  display: flex;
  gap: 12px;
}

.stat-item {
  font-size: 11px;
  color: #999;
  font-weight: 500;
}

.rank-score {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
}

.score-value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: #4ecdc4;
}

.score-label {
  font-size: 10px;
  color: #666;
  font-weight: 500;
}

@media (min-width: 768px) {
  .content-wrapper {
    max-width: 680px;
    padding: 32px;
  }

  .page-title {
    font-size: 32px;
  }

  .title-icon {
    font-size: 34px;
  }

  .filter-btn {
    padding: 12px 22px;
    font-size: 15px;
  }

  .podium-avatar {
    width: 100px;
    height: 100px;
  }

  .podium-avatar.champion {
    width: 120px;
    height: 120px;
  }

  .podium-name {
    font-size: 15px;
  }

  .rank-item {
    padding: 18px;
  }

  .rank-avatar {
    width: 56px;
    height: 56px;
  }

  .rank-name {
    font-size: 16px;
  }
}

@media (min-width: 1024px) {
  .content-wrapper {
    max-width: 800px;
  }

  .page-title {
    font-size: 36px;
  }

  .podium-avatar.champion {
    width: 140px;
    height: 140px;
  }
}
</style>