<template>
  <div class="sport-detail-container">
    <!-- Animated Background -->
    <div class="bg-gradient"></div>
    <div class="noise-overlay"></div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Header Section -->
      <header class="page-header">
        <button @click="$router.back()" class="back-button">
          <span class="back-icon">←</span>
          <span>Kembali</span>
        </button>

        <div class="header-content">
          <h1 class="page-title">Slot Jadwal</h1>
          <p class="page-subtitle">Pilih waktu terbaik untuk bermain</p>
        </div>
      </header>

      <!-- Slot Grid -->
      <div class="slot-grid">
        <div
          v-for="(slot, index) in slots"
          :key="slot.id"
          class="slot-card"
          :class="{ full: slot.booked >= slot.capacity }"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <!-- Image Section -->
          <div class="image-section">
            <img
              :src="getProperImage(slot)"
              class="field-image"
              :alt="slot.lapangan"
            />
            <div class="image-overlay"></div>

            <!-- Badges -->
            <div class="badges-container">
              <span class="badge level-badge">
                <span class="badge-icon">⚡</span>
                {{ slot.tingkat }}
              </span>

              <span
                class="badge status-badge"
                :class="slot.booked >= slot.capacity ? 'full' : 'available'"
              >
                <span class="status-dot"></span>
                {{ slot.booked >= slot.capacity ? 'Penuh' : 'Tersedia' }}
              </span>
            </div>
          </div>

          <!-- Card Body -->
          <div class="card-body">
            <!-- Field Name -->
            <h3 class="field-name">{{ slot.lapangan }}</h3>

            <!-- Day & Time -->
            <div class="time-info">
              <span class="time-icon">📅</span>
              <span class="time-text">{{ slot.day }}</span>
              <span class="separator">•</span>
              <span class="time-icon">⏰</span>
              <span class="time-text">{{ slot.time }}</span>
            </div>

            <!-- Capacity Section -->
            <div class="capacity-section">
              <div class="capacity-header">
                <span class="capacity-label">Kapasitas</span>
                <span class="capacity-count">
                  <span class="current">{{ slot.booked }}</span>
                  <span class="divider">/</span>
                  <span class="total">{{ slot.capacity }}</span>
                </span>
              </div>
              <div class="capacity-bar-wrapper">
                <div class="capacity-bar">
                  <div 
                    class="capacity-fill" 
                    :style="{ width: `${(slot.booked / slot.capacity) * 100}%` }"
                    :class="{ 
                      full: slot.booked >= slot.capacity,
                      high: slot.booked / slot.capacity > 0.7 && slot.booked < slot.capacity
                    }"
                  ></div>
                </div>
                <div class="capacity-percentage">
                  {{ Math.round((slot.booked / slot.capacity) * 100) }}%
                </div>
              </div>
            </div>

            <!-- Action Button -->
            <button
              class="booking-button"
              :disabled="slot.booked >= slot.capacity"
              @click="goBooking(slot.id)"
            >
              <span v-if="slot.booked >= slot.capacity">
                <span class="btn-icon">🔒</span>
                Slot Penuh
              </span>
              <span v-else>
                <span class="btn-icon">✓</span>
                Booking Sekarang
              </span>
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="slots.length === 0" class="empty-state">
        <div class="empty-icon">📅</div>
        <h3 class="empty-title">Tidak Ada Slot Tersedia</h3>
        <p class="empty-description">Slot untuk olahraga ini akan segera hadir</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api"

export default {
  name: "SportDetail",

  data() {
    return {
      slots: []
    }
  },

  async mounted() {
    try {
      const sportId = this.$route.params.id
      const res = await api.get(`/sports/${sportId}/slots`)
      this.slots = res.data
    } catch (err) {
      console.error("Gagal ambil slot:", err)
    }
  },

  methods: {
    goBooking(slotId) {
      this.$router.push(`/booking/${slotId}`)
    },
    
    getProperImage(slot) {
      // Mapping proper sports images from Unsplash
      const sportImages = {
        'badminton': 'https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=600&h=400&fit=crop',
        'tenis': 'https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=600&h=400&fit=crop',
        'futsal': 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=600&h=400&fit=crop',
        'basket': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=600&h=400&fit=crop',
        'paddle': 'https://images.unsplash.com/photo-1622163642998-1ea32b0bbc67?w=600&h=400&fit=crop',
        'voli': 'https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?w=600&h=400&fit=crop'
      };
      
      // Detect sport type from slot name or use default
      const sportType = Object.keys(sportImages).find(sport => 
        slot.lapangan.toLowerCase().includes(sport)
      );
      
      return sportImages[sportType] || 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=600&h=400&fit=crop';
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.sport-detail-container {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  font-family: 'DM Sans', sans-serif;
  background: #0a0a0a;
  padding-bottom: 60px;
}

/* Animated Background */
.bg-gradient {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 30%, rgba(255, 107, 107, 0.12) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(78, 205, 196, 0.12) 0%, transparent 50%),
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 20px;
}

/* Header */
.page-header {
  margin-bottom: 32px;
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

.back-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #e0e0e0;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 24px;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(78, 205, 196, 0.3);
  transform: translateX(-4px);
}

.back-icon {
  font-size: 18px;
  transition: transform 0.3s ease;
}

.back-button:hover .back-icon {
  transform: translateX(-4px);
}

.header-content {
  text-align: left;
}

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
  background: linear-gradient(135deg, #fff 0%, #4ecdc4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-subtitle {
  font-size: 15px;
  color: #999;
  margin: 0;
}

/* Slot Grid */
.slot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  animation: fadeInUp 0.8s ease 0.2s both;
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

/* Slot Card */
.slot-card {
  position: relative;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  overflow: hidden;
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

.slot-card:hover {
  transform: translateY(-6px);
  border-color: rgba(78, 205, 196, 0.3);
  box-shadow: 0 12px 40px rgba(78, 205, 196, 0.15);
}

.slot-card.full {
  opacity: 0.7;
}

.slot-card.full:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  border-color: rgba(255, 255, 255, 0.1);
}

/* Image Section */
.image-section {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.field-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.slot-card:hover .field-image {
  transform: scale(1.1);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(10,10,10,0.6) 100%);
  z-index: 1;
}

/* Badges */
.badges-container {
  position: absolute;
  top: 14px;
  left: 14px;
  right: 14px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  z-index: 2;
  gap: 8px;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  white-space: nowrap;
}

.badge-icon {
  font-size: 14px;
}

.level-badge {
  background: rgba(59, 130, 246, 0.85);
  color: white;
  border-color: rgba(59, 130, 246, 0.4);
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-badge.available {
  background: rgba(34, 197, 94, 0.85);
  color: white;
  border-color: rgba(34, 197, 94, 0.4);
}

.status-badge.full {
  background: rgba(239, 68, 68, 0.85);
  color: white;
  border-color: rgba(239, 68, 68, 0.4);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s ease infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}

/* Card Body */
.card-body {
  padding: 20px;
}

.field-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 12px;
  line-height: 1.3;
}

.time-info {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #999;
  font-size: 13px;
  margin-bottom: 18px;
  flex-wrap: wrap;
}

.time-icon {
  font-size: 14px;
}

.time-text {
  font-weight: 500;
}

.separator {
  color: #666;
  margin: 0 2px;
}

/* Capacity Section */
.capacity-section {
  margin-bottom: 18px;
}

.capacity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.capacity-label {
  font-size: 12px;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.capacity-count {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}

.capacity-count .current {
  color: #4ecdc4;
}

.capacity-count .divider {
  color: #666;
}

.capacity-count .total {
  color: #999;
}

.capacity-bar-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.capacity-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 999px;
  overflow: hidden;
}

.capacity-fill {
  height: 100%;
  background: linear-gradient(90deg, #4ecdc4 0%, #44a89e 100%);
  border-radius: 999px;
  transition: all 0.6s ease;
  position: relative;
}

.capacity-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.capacity-fill.high {
  background: linear-gradient(90deg, #fbbf24 0%, #f59e0b 100%);
}

.capacity-fill.full {
  background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
}

.capacity-percentage {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 12px;
  font-weight: 700;
  color: #666;
  min-width: 40px;
  text-align: right;
}

/* Booking Button */
.booking-button {
  width: 100%;
  padding: 14px 20px;
  border-radius: 12px;
  background: linear-gradient(135deg, #4ecdc4 0%, #44a89e 100%);
  color: white;
  border: none;
  font-size: 14px;
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
  box-shadow: 0 8px 24px rgba(78, 205, 196, 0.4);
}

.booking-button:active {
  transform: translateY(0);
}

.btn-icon {
  font-size: 16px;
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

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  animation: fadeInUp 0.8s ease;
}

.empty-icon {
  font-size: 72px;
  margin-bottom: 20px;
  opacity: 0.3;
}

.empty-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 10px;
}

.empty-description {
  color: #999;
  font-size: 15px;
}

/* Responsive */
@media (min-width: 768px) {
  .content-wrapper {
    padding: 32px 32px 60px;
  }

  .page-title {
    font-size: 38px;
  }

  .page-subtitle {
    font-size: 16px;
  }

  .slot-grid {
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 28px;
  }

  .image-section {
    height: 220px;
  }

  .card-body {
    padding: 24px;
  }

  .field-name {
    font-size: 22px;
  }
}

@media (min-width: 1024px) {
  .content-wrapper {
    max-width: 1400px;
    padding: 40px 48px 80px;
  }

  .page-title {
    font-size: 42px;
  }

  .slot-grid {
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 32px;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: 20px 16px 40px;
  }

  .page-title {
    font-size: 28px;
  }

  .page-subtitle {
    font-size: 14px;
  }

  .slot-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .image-section {
    height: 180px;
  }

  .card-body {
    padding: 18px;
  }

  .field-name {
    font-size: 18px;
  }

  .badges-container {
    flex-wrap: wrap;
  }

  .badge {
    font-size: 11px;
    padding: 5px 10px;
  }
}
</style>