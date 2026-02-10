<template>
  <div class="checkout-container">
    <!-- Animated Background -->
    <div class="bg-gradient"></div>
    <div class="noise-overlay"></div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <div class="checkout-card">
        <!-- Header -->
        <div class="checkout-header">
          <div class="header-icon">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
              <rect x="3" y="6" width="18" height="15" rx="2" stroke="currentColor" stroke-width="2"/>
              <path d="M3 10H21" stroke="currentColor" stroke-width="2"/>
              <path d="M7 15H7.01M11 15H13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </div>
          <h1 class="checkout-title">Checkout Booking</h1>
          <p class="checkout-subtitle">Konfirmasi detail pembayaran Anda</p>
        </div>

        <!-- User Info Section -->
        <div class="info-section">
          <div class="section-label">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
            </svg>
            <span>Informasi User</span>
          </div>

          <div class="info-grid">
            <div class="info-row">
              <span class="info-label">Nama User</span>
              <span class="info-value">{{ userName }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Email</span>
              <span class="info-value">{{ userEmail }}</span>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- Booking Info Section -->
        <div class="info-section">
          <div class="section-label">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <rect x="3" y="4" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2"/>
              <path d="M16 2V6M8 2V6M3 10H21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>Detail Booking</span>
          </div>

          <div class="info-grid">
            <div class="info-row">
              <span class="info-label">Nama Peserta</span>
              <span class="info-value highlight">{{ bookingName }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Olahraga</span>
              <span class="info-value">{{ sportName }}</span>
            </div>
            <div class="info-row">
              <span class="info-label">Harga</span>
              <span class="info-value price">Rp {{ price.toLocaleString("id-ID") }}</span>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- Total Section -->
        <div class="total-section">
          <div class="total-row">
            <span class="total-label">Total Pembayaran</span>
            <span class="total-amount">Rp {{ price.toLocaleString("id-ID") }}</span>
          </div>
        </div>

        <!-- Payment Button -->
        <button
          class="payment-button"
          :disabled="loading"
          @click="pay"
        >
          <span v-if="loading" class="loading-content">
            <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" opacity="0.25"/>
              <path d="M12 2C6.47715 2 2 6.47715 2 12" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>
            </svg>
            Memproses pembayaran...
          </span>
          <span v-else class="button-content">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M9 11L12 14L22 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M21 12V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Bayar & Booking Sekarang
          </span>
        </button>

        <!-- Payment Info -->
        <div class="payment-info">
          <div class="info-badge">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              <path d="M12 16V12M12 8H12.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>Pembayaran aman menggunakan QRIS (DOKU)</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import api from "@/services/api"

// =====================
// ROUTER
// =====================
const route = useRoute()
const router = useRouter()

// =====================
// USER LOGIN
// =====================
const userName = ref("-")
const userEmail = ref("-")

const user = localStorage.getItem("user")
if (!user) {
  router.push("/login")
} else {
  const parsed = JSON.parse(user)
  userName.value = parsed.name || "-"
  userEmail.value = parsed.email || "-"
}

// =====================
// QUERY PARAM
// =====================
const slotId = Number(route.query.slot_id)
const bookingName = route.query.name

if (!slotId || !bookingName) {
  alert("Data booking tidak valid")
  router.push("/")
}

// =====================
// STATE
// =====================
const sportName = ref("")
const price = ref(0)
const loading = ref(false)

// =====================
// LOAD DOKU SCRIPT
// =====================
function loadDokuCheckout() {
  return new Promise((resolve, reject) => {
    // Cek apakah sudah ada
    if (window.loadJokulCheckout) {
      return resolve()
    }

    const script = document.createElement("script")
    
    // ⚠️ PENTING: Ganti URL sesuai environment
    // SANDBOX (untuk testing):
    // script.src = "https://sandbox.doku.com/jokul-checkout-js/v1/jokul-checkout-1.0.0.js"
    
    // PRODUCTION (untuk live):
    script.src = "https://jokul.doku.com/jokul-checkout-js/v1/jokul-checkout-1.0.0.js"
    
    script.onload = () => {
      console.log("✅ DOKU Checkout loaded")
      resolve()
    }
    script.onerror = () => reject("Gagal load DOKU Checkout")
    document.head.appendChild(script)
  })
}

// =====================
// LOAD SLOT DATA
// =====================
onMounted(async () => {
  try {
    const res = await api.get(`/slots/${slotId}`)
    sportName.value = res.data.sport_name
    price.value = res.data.price
  } catch (err) {
    console.error(err)
    alert("Gagal mengambil data slot")
    router.push("/")
  }
})

// =====================
// PAY
// =====================
const pay = async () => {
  if (loading.value) return

  try {
    loading.value = true

    // 1️⃣ Load DOKU script
    await loadDokuCheckout()

    // 2️⃣ Create transaction
    const res = await api.post("/create-transaction", {
      slot_id: slotId,
      booking_name: bookingName,
      name: userName.value,
      email: userEmail.value
    })

    console.log("Response create transaction:", res.data)
    console.log("Payment URL:", res.data.payment_url)

    if (!res.data.payment_url) {
      alert("❌ Payment URL tidak ditemukan")
      return
    }

    // 3️⃣ Buka halaman checkout DOKU
    if (window.loadJokulCheckout) {
      window.loadJokulCheckout(res.data.payment_url)
      
      // Optional: Polling untuk cek status pembayaran
      const orderId = res.data.order_id
      const checkInterval = setInterval(async () => {
        try {
          const statusRes = await api.get(`/booking-status?order_id=${orderId}`)
          
          if (statusRes.data.status === "CONFIRMED") {
            clearInterval(checkInterval)
            alert("✅ Pembayaran berhasil")
            router.push("/my-ticket")
          } else if (statusRes.data.status === "FAILED") {
            clearInterval(checkInterval)
            alert("❌ Pembayaran gagal")
          }
        } catch (err) {
          console.error("Error checking status:", err)
        }
      }, 3000) // Cek setiap 3 detik

      // Stop polling setelah 5 menit
      setTimeout(() => {
        clearInterval(checkInterval)
      }, 300000)
      
    } else {
      // Fallback: buka di tab baru
      window.open(res.data.payment_url, '_blank')
      alert("Silakan selesaikan pembayaran di tab yang baru dibuka")
    }

  } catch (err) {
    console.error("PAY ERROR:", err)
    alert("Gagal memproses pembayaran: " + (err.response?.data?.detail || err.message))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

.checkout-container {
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
  max-width: 520px;
}

/* Checkout Card */
.checkout-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 40px;
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

/* Header */
.checkout-header {
  text-align: center;
  margin-bottom: 32px;
}

.header-icon {
  width: 64px;
  height: 64px;
  margin: 0 auto 20px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  animation: iconPulse 2s ease infinite;
}

@keyframes iconPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

.checkout-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.checkout-subtitle {
  font-size: 15px;
  color: #888;
  margin: 0;
}

/* Info Section */
.info-section {
  margin-bottom: 24px;
}

.section-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #4ecdc4;
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-grid {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 14px;
  padding: 20px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-label {
  font-size: 14px;
  color: #888;
}

.info-value {
  font-size: 15px;
  font-weight: 600;
  color: #e0e0e0;
  text-align: right;
}

.info-value.highlight {
  color: #4ecdc4;
}

.info-value.price {
  color: #ff6b6b;
  font-family: 'Space Grotesk', sans-serif;
}

/* Divider */
.divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  margin: 24px 0;
}

/* Total Section */
.total-section {
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(78, 205, 196, 0.1) 100%);
  border: 1px solid rgba(255, 107, 107, 0.2);
  border-radius: 14px;
  padding: 20px;
  margin-bottom: 24px;
}

.total-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-label {
  font-size: 15px;
  font-weight: 600;
  color: #e0e0e0;
}

.total-amount {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Payment Button */
.payment-button {
  width: 100%;
  padding: 18px 24px;
  border-radius: 14px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  color: white;
  border: none;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  position: relative;
  overflow: hidden;
  margin-bottom: 20px;
}

.payment-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.payment-button:hover::before {
  left: 100%;
}

.payment-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(255, 107, 107, 0.5);
}

.payment-button:active {
  transform: translateY(0);
}

.payment-button:disabled {
  background: rgba(255, 255, 255, 0.1);
  color: #666;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.payment-button:disabled::before {
  display: none;
}

.button-content,
.loading-content {
  display: flex;
  align-items: center;
  gap: 10px;
}

.spinner {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Payment Info */
.payment-info {
  display: flex;
  justify-content: center;
}

.info-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(78, 205, 196, 0.1);
  border: 1px solid rgba(78, 205, 196, 0.2);
  border-radius: 999px;
  color: #4ecdc4;
  font-size: 13px;
}

/* Responsive */
@media (max-width: 580px) {
  .checkout-card {
    padding: 32px 24px;
  }

  .checkout-title {
    font-size: 24px;
  }

  .total-amount {
    font-size: 20px;
  }

  .info-value {
    font-size: 14px;
  }
}

@media (max-width: 400px) {
  .checkout-card {
    padding: 24px 20px;
  }

  .info-row {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }

  .info-value {
    text-align: left;
  }
}
</style>