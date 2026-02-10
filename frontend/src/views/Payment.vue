<!-- frontend/src/views/Payment.vue -->
<template>
  <div class="container">
    <h1>💳 Payment</h1>

    <div class="card">
      <h3>Detail Booking</h3>
      <p><strong>Olahraga:</strong> {{ booking.sport }}</p>
      <p><strong>Hari:</strong> {{ booking.day }}</p>
      <p><strong>Jam:</strong> {{ booking.time }}</p>
      <p><strong>Harga:</strong> Rp {{ booking.price.toLocaleString() }}</p>
    </div>

    <div class="card">
      <h3>Metode Pembayaran</h3>
      <label>
        <input type="radio" value="transfer" v-model="method" />
        Transfer Bank
      </label>
      <label>
        <input type="radio" value="ewallet" v-model="method" />
        E-Wallet
      </label>
      <label>
        <input type="radio" value="qris" v-model="method" />
        QRIS
      </label>
    </div>

    <div class="card" v-if="method">
      <h3>Instruksi Pembayaran</h3>
      <p v-if="method === 'transfer'">
        Transfer ke <strong>BCA 1234567890</strong><br />
        a.n Komunitas Olahraga
      </p>
      <p v-if="method === 'ewallet'">
        Kirim ke <strong>OVO / DANA / GOPAY: 08123456789</strong>
      </p>
      <p v-if="method === 'qris'">
        Scan QRIS di tempat atau admin
      </p>
    </div>

    <button class="pay-btn" :disabled="!method" @click="confirmPayment">
      Saya Sudah Bayar
    </button>
  </div>
</template>

<script>
export default {
  name: "Payment",
  data() {
    return {
      method: "",
      booking: {
        sport: "Tennis",
        day: "Sabtu",
        time: "07:00 - 09:00",
        price: 75000
      }
    };
  },
  methods: {
    confirmPayment() {
      alert("Pembayaran dikonfirmasi. Menunggu verifikasi admin.");
      this.$router.push("/");
    }
  }
};
</script>

<style scoped>
.container {
  padding: 32px;
  max-width: 600px;
  margin: auto;
}

.card {
  border: 1px solid #ddd;
  padding: 16px;
  margin-bottom: 20px;
  border-radius: 8px;
}

label {
  display: block;
  margin-bottom: 8px;
}

.pay-btn {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  cursor: pointer;
}

.pay-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
