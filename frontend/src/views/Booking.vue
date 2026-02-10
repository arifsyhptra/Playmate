<template>
  <div class="booking-container">
    <!-- Animated Background -->
    <div class="bg-gradient"></div>
    <div class="noise-overlay"></div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Header Section -->
      <header class="page-header">
        <button @click="$router.back()" class="back-button">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M16 10H4M4 10L9 5M4 10L9 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <span>Kembali</span>
        </button>

        <div class="header-content">
          <h1 class="page-title">Booking Slot</h1>
          <div class="title-underline"></div>
          <p class="page-subtitle">Pilih slot dan isi nama peserta untuk booking</p>
        </div>

        <!-- Capacity Info -->
        <div class="capacity-overview">
          <div class="overview-item">
            <span class="overview-number">{{ filledSlots }}</span>
            <span class="overview-label">Terisi</span>
          </div>
          <div class="overview-divider"></div>
          <div class="overview-item">
            <span class="overview-number">{{ availableSlots }}</span>
            <span class="overview-label">Tersedia</span>
          </div>
          <div class="overview-divider"></div>
          <div class="overview-item">
            <span class="overview-number">{{ capacity }}</span>
            <span class="overview-label">Total Slot</span>
          </div>
        </div>
      </header>

      <!-- Slots Grid -->
      <div class="slots-grid">
        <div
          v-for="i in capacity"
          :key="i"
          class="slot-card"
          :class="{ filled: getParticipant(i) }"
          :style="{ animationDelay: `${(i - 1) * 0.05}s` }"
        >
          <div class="card-glow"></div>

          <!-- Slot Header -->
          <div class="slot-header">
            <div class="slot-number-badge">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2"/>
                <path d="M9 3V21M15 3V21M3 9H21M3 15H21" stroke="currentColor" stroke-width="2"/>
              </svg>
              <span>Slot {{ i }}</span>
            </div>

            <!-- Status Badge -->
            <span
              v-if="getParticipant(i)"
              class="status-badge"
              :class="getParticipant(i).status === 'paid' ? 'paid' : 'unpaid'"
            >
              <span class="status-dot"></span>
              {{ getParticipant(i).status === 'paid' ? 'Sudah Bayar' : 'Belum Bayar' }}
            </span>
          </div>

          <!-- Slot Body -->
          <div class="slot-body">
            <!-- Filled Slot -->
            <template v-if="getParticipant(i)">
              <div class="participant-info">
                <div class="avatar-wrapper">
                  <img src="/animateduser.jpg" class="avatar" alt="User" />
                  <div class="avatar-ring"></div>
                </div>
                <div class="participant-details">
                  <span class="participant-name">{{ getParticipant(i).booking_name }}</span>
                  <span class="participant-status">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none">
                      <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Terbooking
                  </span>
                </div>
              </div>
            </template>

            <!-- Empty Slot -->
            <template v-else>
              <div class="empty-slot">
                <div class="input-group">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" class="input-icon">
                    <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <input
                    v-model="newNames[i - 1]"
                    placeholder="Masukkan nama peserta"
                    class="slot-input"
                  />
                </div>

                <button
                  @click="goCheckout(i - 1)"
                  :disabled="!newNames[i - 1]"
                  class="booking-button"
                >
                  <span v-if="!newNames[i - 1]">Isi Nama Dulu</span>
                  <span v-else>
                    Booking Slot
                    <svg width="18" height="18" viewBox="0 0 20 20" fill="none">
                      <path d="M4 10H16M16 10L11 5M16 10L11 15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </span>
                </button>
              </div>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api"

export default {
  name: "Booking",

  data() {
    return {
      participants: [],
      capacity: 0,
      newNames: {}
    }
  },

  computed: {
    filledSlots() {
      return this.participants.length
    },
    availableSlots() {
      return this.capacity - this.participants.length
    }
  },

  async mounted() {
    try {
      const slotId = Number(this.$route.params.slotId)

      // Ambil peserta
      const p = await api.get(`/slots/${slotId}/participants`)
      this.participants = p.data

      // Ambil kapasitas slot
      const s = await api.get(`/slots/${slotId}`)
      this.capacity = s.data.capacity
    } catch (err) {
      console.error("Gagal ambil data booking:", err)
    }
  },

  methods: {
    getParticipant(slotNumber) {
      return this.participants.find(
        p => p.slot_number === slotNumber
      )
    },

    goCheckout(index) {
      this.$router.push({
        name: "Checkout",
        query: {
          slot_id: this.$route.params.slotId,
          name: this.newNames[index]
        }
      })
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.booking-container {
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
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px;
}

/* Header */
.page-header {
  margin-bottom: 60px;
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

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #e0e0e0;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 30px;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 107, 107, 0.3);
  transform: translateX(-4px);
}

.header-content {
  text-align: left;
  margin-bottom: 30px;
}

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(36px, 5vw, 48px);
  font-weight: 700;
  color: #fff;
  margin-bottom: 12px;
  letter-spacing: -0.02em;
}

.title-underline {
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #ff6b6b 0%, #4ecdc4 100%);
  border-radius: 2px;
  margin-bottom: 16px;
}

.page-subtitle {
  font-size: 18px;
  color: #888;
  margin: 0;
}

/* Capacity Overview */
.capacity-overview {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  padding: 30px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.overview-item {
  text-align: center;
}

.overview-number {
  display: block;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 32px;
  font-weight: 700;
  background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
}

.overview-label {
  font-size: 14px;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.overview-divider {
  width: 1px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
}

/* Slots Grid */
.slots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  animation: fadeIn 1s ease 0.3s both;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

/* Slot Card */
.slot-card {
  position: relative;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 24px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  animation: cardFadeIn 0.6s ease both;
}

@keyframes cardFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-glow {
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(78, 205, 196, 0.15) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.slot-card:hover {
  transform: translateY(-4px);
  border-color: rgba(78, 205, 196, 0.2);
}

.slot-card:hover .card-glow {
  opacity: 1;
}

.slot-card.filled {
  background: rgba(78, 205, 196, 0.05);
  border-color: rgba(78, 205, 196, 0.15);
}

/* Slot Header */
.slot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.slot-number-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e0e0e0;
  font-weight: 600;
  font-size: 15px;
}

.slot-number-badge svg {
  color: #4ecdc4;
}

/* Status Badge */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.status-badge.paid {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-badge.unpaid {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s ease infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

/* Slot Body */
.slot-body {
  position: relative;
  z-index: 1;
}

/* Participant Info */
.participant-info {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 14px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.avatar-wrapper {
  position: relative;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #4ecdc4;
}

.avatar-ring {
  position: absolute;
  top: -4px;
  left: -4px;
  right: -4px;
  bottom: -4px;
  border-radius: 50%;
  border: 2px solid rgba(78, 205, 196, 0.3);
  animation: ringPulse 2s ease infinite;
}

@keyframes ringPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.5;
  }
}

.participant-details {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.participant-name {
  font-weight: 600;
  font-size: 16px;
  color: #fff;
}

.participant-status {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #10b981;
}

/* Empty Slot */
.empty-slot {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 14px;
  color: #666;
  pointer-events: none;
}

.slot-input {
  width: 100%;
  padding: 14px 14px 14px 44px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #e0e0e0;
  font-size: 15px;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.3s ease;
}

.slot-input::placeholder {
  color: #666;
}

.slot-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(78, 205, 196, 0.5);
}

/* Booking Button */
.booking-button {
  width: 100%;
  padding: 14px 20px;
  border-radius: 12px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  color: white;
  border: none;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  position: relative;
  overflow: hidden;
}

.booking-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.booking-button:hover::before {
  left: 100%;
}

.booking-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4);
}

.booking-button:active {
  transform: translateY(0);
}

.booking-button:disabled {
  background: rgba(255, 255, 255, 0.05);
  color: #666;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.booking-button:disabled::before {
  display: none;
}

/* Responsive */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 30px 20px;
  }

  .page-title {
    font-size: 32px;
  }

  .capacity-overview {
    flex-direction: column;
    gap: 20px;
  }

  .overview-divider {
    width: 40px;
    height: 1px;
  }

  .slots-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: 20px 16px;
  }

  .page-title {
    font-size: 28px;
  }
}
</style>