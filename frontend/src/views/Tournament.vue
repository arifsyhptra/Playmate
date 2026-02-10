<template>
  <div class="tournament-container">
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
          <span class="title-icon">⚔️</span>
          Tournament
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

      <!-- Tournament List -->
      <section class="tournament-section">
        <div
          v-for="(tournament, index) in currentTournaments"
          :key="index"
          class="tournament-card"
          :style="{ animationDelay: `${index * 0.1}s` }"
          @click="viewTournamentDetail(tournament)"
        >
          <div class="tournament-banner" :style="{ backgroundImage: `url(${tournament.banner})` }">
            <div class="banner-overlay"></div>
            <div class="tournament-badge" :class="tournament.status">
              {{ tournament.statusText }}
            </div>
          </div>

          <div class="tournament-content">
            <div class="tournament-header">
              <div class="tournament-sport-icon">
                {{ getSportIcon(selectedSport) }}
              </div>
              <div class="tournament-prize">
                <div class="prize-icon">🏆</div>
                <div class="prize-info">
                  <div class="prize-label">Total Hadiah</div>
                  <div class="prize-amount">Rp {{ formatPrice(tournament.prize) }}</div>
                </div>
              </div>
            </div>

            <h3 class="tournament-title">{{ tournament.title }}</h3>
            <p class="tournament-description">{{ tournament.description }}</p>

            <div class="tournament-details">
              <div class="detail-item">
                <span class="detail-icon">📍</span>
                <span class="detail-text">{{ tournament.location }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-icon">📅</span>
                <span class="detail-text">{{ tournament.date }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-icon">👥</span>
                <span class="detail-text">{{ tournament.teams }}/{{ tournament.maxTeams }} Tim</span>
              </div>
            </div>

            <div class="tournament-footer">
              <div class="registration-info">
                <span class="reg-label">Pendaftaran:</span>
                <span class="reg-price">Rp {{ formatPrice(tournament.registrationFee) }}</span>
              </div>
              <button class="register-btn" :class="{ registered: tournament.registered, full: tournament.teams >= tournament.maxTeams }">
                {{ getButtonText(tournament) }}
              </button>
            </div>
          </div>
        </div>

        <div v-if="currentTournaments.length === 0" class="empty-state">
          <div class="empty-icon">🏆</div>
          <div class="empty-title">Belum Ada Tournament</div>
          <div class="empty-description">Tournament untuk olahraga ini akan segera hadir!</div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: "Tournament",
  data() {
    return {
      selectedSport: 'tenis',
      sports: [
        { id: 'tenis', name: 'Tenis', icon: '🎾' },
        { id: 'badminton', name: 'Badminton', icon: '🏸' },
        { id: 'futsal', name: 'Futsal', icon: '⚽' },
        { id: 'basket', name: 'Basket', icon: '🏀' },
        { id: 'paddle', name: 'Paddle', icon: '🎾' }
      ],
      tournaments: {
        tenis: [
          {
            title: 'Tournament Tenis Mendha Berkah',
            description: 'Turnamen tenis open kategori junior dan senior. Sistem double elimination.',
            location: 'Lapangan Tenis Setia Budi',
            date: '15-17 Februari 2026',
            prize: 15000000,
            registrationFee: 350000,
            teams: 24,
            maxTeams: 32,
            status: 'open',
            statusText: 'Pendaftaran Dibuka',
            registered: false,
            banner: 'https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=800&h=400&fit=crop'
          },
          {
            title: 'Medan Tennis Championship 2026',
            description: 'Kejuaraan tenis tingkat kota dengan hadiah total jutaan rupiah. All level welcome!',
            location: 'GOR Medan Tennis Center',
            date: '1-3 Maret 2026',
            prize: 25000000,
            registrationFee: 500000,
            teams: 18,
            maxTeams: 32,
            status: 'open',
            statusText: 'Pendaftaran Dibuka',
            registered: true,
            banner: 'https://images.unsplash.com/photo-1622163642998-1ea32b0bbc67?w=800&h=400&fit=crop'
          },
          {
            title: 'Sumut Open Tennis Tournament',
            description: 'Tournament tenis terbesar di Sumatera Utara. Kategori U-15, U-18, dan Open.',
            location: 'Kompleks Olahraga Sumut',
            date: '20-25 Maret 2026',
            prize: 50000000,
            registrationFee: 750000,
            teams: 28,
            maxTeams: 48,
            status: 'open',
            statusText: 'Pendaftaran Dibuka',
            registered: false,
            banner: 'https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?w=800&h=400&fit=crop'
          }
        ],
        badminton: [
          {
            title: 'Medan Badminton League 2026',
            description: 'Liga badminton bulanan dengan sistem round-robin. Kategori tunggal dan ganda.',
            location: 'GOR Badminton Arena Medan',
            date: '12-14 Februari 2026',
            prize: 12000000,
            registrationFee: 300000,
            teams: 30,
            maxTeams: 40,
            status: 'open',
            statusText: 'Pendaftaran Dibuka',
            registered: false,
            banner: 'https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=800&h=400&fit=crop'
          },
          {
            title: 'Shuttlecock Smash Championship',
            description: 'Turnamen badminton bergengsi dengan peserta dari seluruh Sumut.',
            location: 'Istora Badminton Medan',
            date: '5-7 Maret 2026',
            prize: 30000000,
            registrationFee: 450000,
            teams: 32,
            maxTeams: 32,
            status: 'full',
            statusText: 'Penuh',
            registered: false,
            banner: 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=800&h=400&fit=crop'
          }
        ],
        futsal: [
          {
            title: 'Futsal Fiesta Medan 2026',
            description: 'Turnamen futsal antar klub se-Medan. Format 5v5 dengan hadiah menarik!',
            location: 'Arena Futsal Cemara Asri',
            date: '18-20 Februari 2026',
            prize: 20000000,
            registrationFee: 1500000,
            teams: 14,
            maxTeams: 16,
            status: 'open',
            statusText: 'Pendaftaran Dibuka',
            registered: true,
            banner: 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=800&h=400&fit=crop'
          },
          {
            title: 'Sumut Futsal Cup',
            description: 'Piala futsal terbesar di Sumatera Utara dengan total hadiah puluhan juta!',
            location: 'GOR Futsal Sumut',
            date: '10-15 Maret 2026',
            prize: 45000000,
            registrationFee: 2000000,
            teams: 20,
            maxTeams: 24,
            status: 'open',
            statusText: 'Pendaftaran Dibuka',
            registered: false,
            banner: 'https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800&h=400&fit=crop'
          }
        ],
        basket: [
          {
            title: 'Medan Basketball Tournament',
            description: 'Turnamen basket 3x3 untuk umum. Terbuka untuk semua tingkat kemampuan.',
            location: 'Lapangan Basket Taman Cadika',
            date: '22-24 Februari 2026',
            prize: 18000000,
            registrationFee: 800000,
            teams: 10,
            maxTeams: 16,
            status: 'open',
            statusText: 'Pendaftaran Dibuka',
            registered: false,
            banner: 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800&h=400&fit=crop'
          }
        ],
        paddle: [
          {
            title: 'Medan Paddle Open 2026',
            description: 'Tournament paddle tennis pertama di Medan. Kategori pemula hingga profesional.',
            location: 'Medan Paddle Club',
            date: '8-10 Maret 2026',
            prize: 10000000,
            registrationFee: 400000,
            teams: 12,
            maxTeams: 24,
            status: 'open',
            statusText: 'Pendaftaran Dibuka',
            registered: false,
            banner: 'https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=800&h=400&fit=crop'
          }
        ]
      }
    };
  },
  computed: {
    currentTournaments() {
      return this.tournaments[this.selectedSport] || [];
    }
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    selectSport(sportId) {
      this.selectedSport = sportId;
    },
    getSportIcon(sportId) {
      const sport = this.sports.find(s => s.id === sportId);
      return sport ? sport.icon : '🏆';
    },
    formatPrice(price) {
      return price.toLocaleString('id-ID');
    },
    getButtonText(tournament) {
      if (tournament.registered) return '✓ Terdaftar';
      if (tournament.teams >= tournament.maxTeams) return 'Penuh';
      return 'Daftar';
    },
    viewTournamentDetail(tournament) {
      console.log('View tournament:', tournament);
      alert(`Detail tournament: ${tournament.title}\n\nFitur detail akan segera hadir!`);
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

.tournament-container {
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
    radial-gradient(circle at 20% 30%, rgba(239, 68, 68, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(255, 215, 0, 0.1) 0%, transparent 50%),
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
  margin-bottom: 28px;
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
  border-color: rgba(239, 68, 68, 0.3);
}

.filter-btn.active {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(248, 113, 113, 0.2) 100%);
  border-color: rgba(239, 68, 68, 0.5);
  color: #f87171;
}

.filter-emoji {
  font-size: 18px;
}

.tournament-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.tournament-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  animation: fadeInUp 0.8s ease both;
}

.tournament-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(239, 68, 68, 0.3);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(239, 68, 68, 0.15);
}

.tournament-banner {
  position: relative;
  width: 100%;
  height: 160px;
  background-size: cover;
  background-position: center;
}

.banner-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(10, 10, 10, 0.8) 100%);
}

.tournament-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 6px 14px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  backdrop-filter: blur(10px);
}

.tournament-badge.open {
  background: rgba(34, 197, 94, 0.3);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.5);
}

.tournament-badge.full {
  background: rgba(239, 68, 68, 0.3);
  color: #f87171;
  border: 1px solid rgba(239, 68, 68, 0.5);
}

.tournament-content {
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.tournament-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.tournament-sport-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
  border: 1px solid rgba(239, 68, 68, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
}

.tournament-prize {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.15) 0%, rgba(255, 195, 113, 0.15) 100%);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: 10px;
}

.prize-icon {
  font-size: 20px;
}

.prize-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.prize-label {
  font-size: 10px;
  color: #999;
  font-weight: 500;
}

.prize-amount {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: #ffd700;
}

.tournament-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  line-height: 1.3;
}

.tournament-description {
  font-size: 14px;
  color: #999;
  line-height: 1.5;
}

.tournament-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #ccc;
}

.detail-icon {
  font-size: 16px;
  width: 20px;
  text-align: center;
}

.detail-text {
  font-weight: 500;
}

.tournament-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 14px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.registration-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.reg-label {
  font-size: 11px;
  color: #666;
  font-weight: 500;
}

.reg-price {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #4ecdc4;
}

.register-btn {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
  border: 1px solid rgba(239, 68, 68, 0.4);
  border-radius: 10px;
  padding: 10px 24px;
  color: #f87171;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.register-btn:hover {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(239, 68, 68, 0.2) 100%);
  transform: translateY(-2px);
}

.register-btn.registered {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%);
  border-color: rgba(34, 197, 94, 0.4);
  color: #4ade80;
}

.register-btn.full {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.1);
  color: #666;
  cursor: not-allowed;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  text-align: center;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 16px;
  opacity: 0.3;
}

.empty-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
}

.empty-description {
  font-size: 14px;
  color: #666;
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

  .tournament-banner {
    height: 200px;
  }

  .tournament-content {
    padding: 24px;
  }

  .tournament-title {
    font-size: 22px;
  }

  .tournament-description {
    font-size: 15px;
  }
}

@media (min-width: 1024px) {
  .content-wrapper {
    max-width: 800px;
  }

  .page-title {
    font-size: 36px;
  }

  .tournament-banner {
    height: 240px;
  }

  .tournament-title {
    font-size: 24px;
  }
}
</style>