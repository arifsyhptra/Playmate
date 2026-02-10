<template>
  <div class="event-container">
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
          <span class="title-icon">📅</span>
          Event
        </h1>
        <div class="header-spacer"></div>
      </header>

      <!-- Event List -->
      <section class="event-section">
        <div
          v-for="(event, index) in events"
          :key="index"
          class="event-card"
          :style="{ animationDelay: `${index * 0.1}s` }"
          @click="viewEventDetail(event)"
        >
          <div class="event-header">
            <div class="event-icon" :class="event.type">
              <span>{{ event.emoji }}</span>
            </div>
            <div class="event-badge" :class="event.status">
              {{ event.statusText }}
            </div>
          </div>

          <div class="event-content">
            <h3 class="event-title">{{ event.title }}</h3>
            <p class="event-description">{{ event.description }}</p>

            <div class="event-details">
              <div class="detail-item">
                <span class="detail-icon">📍</span>
                <span class="detail-text">{{ event.location }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-icon">📅</span>
                <span class="detail-text">{{ event.date }}</span>
              </div>
              <div class="detail-item">
                <span class="detail-icon">⏰</span>
                <span class="detail-text">{{ event.time }}</span>
              </div>
            </div>

            <div class="event-footer">
              <div class="participants">
                <div class="participant-avatars">
                  <img
                    v-for="i in Math.min(event.participants, 3)"
                    :key="i"
                    :src="`https://i.pravatar.cc/40?img=${index * 3 + i}`"
                    :alt="`Participant ${i}`"
                    class="participant-avatar"
                  >
                  <div v-if="event.participants > 3" class="participant-more">
                    +{{ event.participants - 3 }}
                  </div>
                </div>
                <span class="participant-count">{{ event.participants }} peserta</span>
              </div>
              <button class="join-btn" :class="{ registered: event.registered }">
                {{ event.registered ? '✓ Terdaftar' : 'Daftar' }}
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: "Event",
  data() {
    return {
      events: [
        {
          title: 'Nobar Timnas Basket',
          description: 'Nonton bareng pertandingan Timnas Basket Indonesia vs Thailand di GOR. Gratis snack & minuman!',
          location: 'GOR Medan',
          date: 'Selasa, 6 Februari 2026',
          time: '19:00 - 22:00 WIB',
          emoji: '🏀',
          type: 'sport',
          status: 'upcoming',
          statusText: 'Segera',
          participants: 45,
          registered: false
        },
        {
          title: 'Punggahan Basket',
          description: 'Acara kumpul bareng pemain basket se-Medan. Ada games, doorprize, dan networking session.',
          location: 'Rumah Budi (Jl. Sudirman No. 123)',
          date: 'Kamis, 7 Februari 2026',
          time: '18:00 - 21:00 WIB',
          emoji: '🎉',
          type: 'social',
          status: 'upcoming',
          statusText: 'Segera',
          participants: 32,
          registered: true
        },
        {
          title: 'Acara Amal Fun Sport',
          description: 'Event olahraga untuk penggalangan dana pendidikan anak kurang mampu. Multi cabang olahraga!',
          location: 'Lapangan Terbuka Setia Budi',
          date: 'Minggu, 10 Februari 2026',
          time: '07:00 - 14:00 WIB',
          emoji: '❤️',
          type: 'charity',
          status: 'open',
          statusText: 'Buka',
          participants: 128,
          registered: false
        }
      ]
    };
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    viewEventDetail(event) {
      console.log('View event:', event);
      alert(`Detail event: ${event.title}\n\nFitur detail akan segera hadir!`);
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

.event-container {
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
    radial-gradient(circle at 20% 30%, rgba(139, 92, 246, 0.1) 0%, transparent 50%),
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
  margin-bottom: 28px;
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

.event-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.event-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 18px;
  padding: 18px;
  cursor: pointer;
  transition: all 0.3s ease;
  animation: fadeInUp 0.8s ease both;
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

.event-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(139, 92, 246, 0.3);
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(139, 92, 246, 0.15);
}

.event-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.event-icon {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
}

.event-icon.sport {
  background: linear-gradient(135deg, rgba(78, 205, 196, 0.2) 0%, rgba(78, 205, 196, 0.1) 100%);
  border: 1px solid rgba(78, 205, 196, 0.3);
}

.event-icon.social {
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(255, 107, 107, 0.1) 100%);
  border: 1px solid rgba(255, 107, 107, 0.3);
}

.event-icon.charity {
  background: linear-gradient(135deg, rgba(255, 195, 113, 0.2) 0%, rgba(255, 195, 113, 0.1) 100%);
  border: 1px solid rgba(255, 195, 113, 0.3);
}

.event-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.event-badge.upcoming {
  background: rgba(139, 92, 246, 0.2);
  color: #a78bfa;
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.event-badge.open {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.event-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.event-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  line-height: 1.3;
}

.event-description {
  font-size: 14px;
  color: #999;
  line-height: 1.5;
}

.event-details {
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

.event-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.participants {
  display: flex;
  align-items: center;
  gap: 10px;
}

.participant-avatars {
  display: flex;
  align-items: center;
}

.participant-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid #0a0a0a;
  margin-left: -8px;
  transition: all 0.3s ease;
}

.participant-avatar:first-child {
  margin-left: 0;
}

.participant-avatar:hover {
  transform: translateY(-2px);
  z-index: 10;
}

.participant-more {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid #0a0a0a;
  margin-left: -8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  color: #fff;
  font-weight: 600;
}

.participant-count {
  font-size: 12px;
  color: #999;
  font-weight: 500;
}

.join-btn {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(139, 92, 246, 0.1) 100%);
  border: 1px solid rgba(139, 92, 246, 0.4);
  border-radius: 10px;
  padding: 8px 20px;
  color: #a78bfa;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.join-btn:hover {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(139, 92, 246, 0.2) 100%);
  transform: translateY(-2px);
}

.join-btn.registered {
  background: linear-gradient(135deg, rgba(34, 197, 94, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%);
  border-color: rgba(34, 197, 94, 0.4);
  color: #4ade80;
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

  .event-card {
    padding: 24px;
  }

  .event-icon {
    width: 64px;
    height: 64px;
    font-size: 32px;
  }

  .event-title {
    font-size: 22px;
  }

  .event-description {
    font-size: 15px;
  }

  .detail-item {
    font-size: 14px;
  }
}

@media (min-width: 1024px) {
  .content-wrapper {
    max-width: 800px;
  }

  .page-title {
    font-size: 36px;
  }

  .event-title {
    font-size: 24px;
  }
}
</style>