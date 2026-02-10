<template>
  <div class="playmate-container">
    <!-- Animated Background -->
    <div class="bg-gradient"></div>
    <div class="noise-overlay"></div>
    
    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Header Section -->
      <header class="page-header">
        <div class="header-content">
          <h1 class="page-title">
            <span class="title-icon">🎟</span>
            <span>Tiket Saya</span>
          </h1>
          <div class="title-underline"></div>
        </div>

        <!-- Filter Tabs -->
        <div class="filter-tabs">
          <button
            v-for="f in filters"
            :key="f"
            :class="['filter-btn', { active: activeFilter === f }]"
            @click="activeFilter = f"
          >
            {{ f }}
          </button>
        </div>
      </header>

      <!-- Loading State -->
      <div v-if="loading" class="state-message">
        <div class="loader"></div>
        <p>Memuat tiket...</p>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredBookings.length === 0" class="state-message">
        <div class="empty-icon">📭</div>
        <p class="empty-text">
          Tidak ada tiket {{ activeFilter !== 'ALL' ? activeFilter.toLowerCase() : '' }}
        </p>
      </div>

      <!-- Tickets Grid -->
      <div v-else class="tickets-grid">
        <div
          v-for="(b, index) in filteredBookings"
          :key="b.id"
          class="ticket-card"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="card-glow"></div>
          
          <!-- Card Header -->
          <div class="ticket-header">
            <div class="ticket-info">
              <h3 class="ticket-name">{{ b.booking_name }}</h3>
              <p class="order-id">{{ b.order_id }}</p>
            </div>
            
            <span class="status-badge" :class="getStatusClass(b.status)">
              {{ b.status }}
            </span>
          </div>

          <!-- Card Body -->
          <div class="ticket-body">
            <div class="detail-row">
              <span class="detail-icon">📅</span>
              <span class="detail-text">{{ formatDate(b.created_at) }}</span>
            </div>
          </div>

          <!-- Card Footer -->
          <div v-if="b.status === 'PENDING'" class="ticket-footer">
            <button class="cancel-btn" @click="cancelBooking(b.id)">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <span>Batalkan Booking</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import api from "@/services/api"

const bookings = ref([])
const loading = ref(true)

const filters = ["ALL", "CONFIRMED", "PENDING", "CANCELLED"]
const activeFilter = ref("ALL")

onMounted(fetchBookings)

async function fetchBookings() {
  const user = JSON.parse(localStorage.getItem("user"))
  const email = user?.email

  if (!email) {
    loading.value = false
    return
  }

  try {
    const res = await api.get("/bookings/by-email", {
      params: { email }
    })
    bookings.value = res.data
  } catch (err) {
    console.error("[MyTicket] error:", err)
  } finally {
    loading.value = false
  }
}

const filteredBookings = computed(() => {
  if (activeFilter.value === "ALL") {
    return bookings.value
  }
  return bookings.value.filter(
    b => b.status === activeFilter.value
  )
})

async function cancelBooking(id) {
  const ok = confirm("Yakin mau membatalkan booking ini?")
  if (!ok) return

  try {
    await api.post(`/bookings/${id}/cancel`)
    bookings.value = bookings.value.map(b =>
      b.id === id ? { ...b, status: "CANCELLED" } : b
    )
  } catch (err) {
    alert("Gagal membatalkan booking")
  }
}

function formatDate(date) {
  return new Date(date).toLocaleString("id-ID", {
    dateStyle: "medium",
    timeStyle: "short"
  })
}

function getStatusClass(status) {
  return status.toLowerCase()
}
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
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px;
}

/* Page Header */
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

.header-content {
  text-align: center;
  margin-bottom: 40px;
}

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: clamp(36px, 6vw, 56px);
  font-weight: 700;
  color: #fff;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.title-icon {
  font-size: clamp(40px, 6vw, 60px);
  display: inline-block;
  animation: bounce 2s ease infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
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

/* Filter Tabs */
.filter-tabs {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 12px 24px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.03);
  color: #999;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'DM Sans', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.2);
  color: #e0e0e0;
}

.filter-btn.active {
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  border-color: transparent;
  color: white;
  box-shadow: 0 4px 16px rgba(255, 107, 107, 0.3);
}

/* State Messages */
.state-message {
  text-align: center;
  padding: 80px 20px;
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
  border-top-color: #ff6b6b;
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

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
  opacity: 0.5;
}

.empty-text {
  color: #666;
  font-size: 18px;
}

/* Tickets Grid */
.tickets-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 24px;
  animation: fadeInUp 1s ease;
}

.ticket-card {
  position: relative;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 24px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
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
  background: radial-gradient(circle, rgba(78, 205, 196, 0.1) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
  pointer-events: none;
}

.ticket-card:hover {
  transform: translateY(-4px);
  border-color: rgba(78, 205, 196, 0.3);
  box-shadow: 
    0 12px 40px rgba(78, 205, 196, 0.15),
    0 0 0 1px rgba(78, 205, 196, 0.1) inset;
}

.ticket-card:hover .card-glow {
  opacity: 1;
}

/* Ticket Header */
.ticket-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  gap: 16px;
}

.ticket-info {
  flex: 1;
  min-width: 0;
}

.ticket-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.order-id {
  font-size: 13px;
  color: #666;
  font-family: 'Courier New', monospace;
  margin: 0;
}

.status-badge {
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.status-badge.confirmed,
.status-badge.paid {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-badge.pending {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.status-badge.cancelled,
.status-badge.failed {
  background: rgba(239, 68, 68, 0.15);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.3);
}

/* Ticket Body */
.ticket-body {
  margin-bottom: 20px;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 0;
  color: #999;
  font-size: 14px;
}

.detail-icon {
  font-size: 18px;
}

.detail-text {
  color: #ccc;
}

/* Ticket Footer */
.ticket-footer {
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.cancel-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 10px;
  border: 1px solid rgba(239, 68, 68, 0.3);
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'DM Sans', sans-serif;
}

.cancel-btn:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: rgba(239, 68, 68, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2);
}

/* Responsive */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 40px 20px;
  }

  .tickets-grid {
    grid-template-columns: 1fr;
  }

  .filter-tabs {
    gap: 8px;
  }

  .filter-btn {
    padding: 10px 16px;
    font-size: 13px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 32px;
  }

  .ticket-card {
    padding: 20px;
  }

  .ticket-name {
    font-size: 18px;
  }
}
</style>