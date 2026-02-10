<template>
  <div class="container">
    <div class="card">
      <!-- ICON SUKSES -->
      <div class="icon">
        ✅
      </div>

      <h2>Pembayaran Berhasil!</h2>

      <p class="message">
        Terima kasih, {{ booking.booking_name }}. Pembayaran Anda telah diterima.
      </p>

      <div class="details">
        <div>
          <strong>Order ID:</strong> {{ booking.order_id }}
        </div>
        <div>
          <strong>Lapangan:</strong> {{ booking.lapangan }}
        </div>
        <div>
          <strong>Hari & Jam:</strong> {{ booking.day }} • {{ booking.time }}
        </div>
        <div>
          <strong>Jumlah:</strong> Rp {{ formatCurrency(booking.amount) }}
        </div>
        <div>
          <strong>Status:</strong> {{ booking.status }}
        </div>
      </div>

      <button @click="goHome">Kembali ke Home</button>
    </div>
  </div>
</template>

<script>
import axios from "axios"

export default {
  name: "PaymentSuccess",
  data() {
    return {
      booking: {}
    }
  },
  async mounted() {
    try {
      const order_id = this.$route.query.order_id

      const res = await axios.get(
        `http://localhost:8000/booking-status?order_id=${order_id}`
      )

      this.booking = res.data
      // contoh data tambahan jika diperlukan
      this.booking.lapangan = this.$route.query.lapangan || "Lapangan"
      this.booking.day = this.$route.query.day || "Hari"
      this.booking.time = this.$route.query.time || "Jam"
      this.booking.amount = this.$route.query.amount || 0
      this.booking.booking_name = this.$route.query.name || "Peserta"
    } catch (err) {
      console.error("Gagal ambil booking:", err)
    }
  },
  methods: {
    goHome() {
      this.$router.push("/")
    },
    formatCurrency(value) {
      return Number(value).toLocaleString("id-ID")
    }
  }
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: 20px;
}

.card {
  max-width: 400px;
  background: #fff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
  text-align: center;
}

.icon {
  font-size: 48px;
  margin-bottom: 16px;
}

h2 {
  font-size: 24px;
  margin-bottom: 8px;
  color: #10b981;
}

.message {
  font-size: 16px;
  color: #555;
  margin-bottom: 16px;
}

.details {
  text-align: left;
  font-size: 14px;
  margin-bottom: 24px;
  line-height: 1.6;
}

button {
  padding: 12px 24px;
  border-radius: 12px;
  background: #111;
  color: #fff;
  border: none;
  cursor: pointer;
}

button:hover {
  background: #333;
}
</style>
