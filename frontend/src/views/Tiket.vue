<template>
  <div class="page">
    <h1 class="title">🎟 Tiket Saya</h1>

    <div v-if="loading" class="info">
      Loading tiket...
    </div>

    <div v-else-if="tickets.length === 0" class="info">
      Kamu belum punya tiket
    </div>

    <div v-else class="list">
      <div
        class="card"
        v-for="t in tickets"
        :key="t.id"
      >
        <div class="row">
          <span class="label">Order ID</span>
          <span>{{ t.order_id }}</span>
        </div>

        <div class="row">
          <span class="label">Nama Booking</span>
          <span>{{ t.booking_name }}</span>
        </div>

        <div class="row">
          <span class="label">Status</span>
          <span
            class="status"
            :class="t.status.toLowerCase()"
          >
            {{ t.status }}
          </span>
        </div>

        <div class="row">
          <span class="label">Tanggal</span>
          <span>{{ formatDate(t.created_at) }}</span>
        </div>

        <button
          v-if="t.status === 'PENDING'"
          class="cancel-btn"
          @click="cancelBooking(t.id)"
        >
          Batalkan
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  name: "MyTicket",
  data() {
    return {
      tickets: [],
      loading: true
    };
  },
  computed: {
    userEmail() {
      const user = localStorage.getItem("user");
      if (!user) return "";
      return JSON.parse(user).email;
    }
  },
  methods: {
    async fetchTickets() {
      this.loading = true;
      try {
        const res = await api.get("/bookings/by-email", {
          params: {
            email: this.userEmail
          }
        });
        this.tickets = res.data;
      } catch (err) {
        console.error("Gagal ambil tiket:", err);
        alert("Gagal mengambil tiket");
      } finally {
        this.loading = false;
      }
    },

    async cancelBooking(id) {
      if (!confirm("Yakin ingin membatalkan tiket ini?")) return;

      try {
        await api.post(`/bookings/${id}/cancel`);
        alert("Tiket berhasil dibatalkan");
        this.fetchTickets();
      } catch (err) {
        alert(
          err.response?.data?.detail ||
          "Tiket tidak bisa dibatalkan"
        );
      }
    },

    formatDate(date) {
      return new Date(date).toLocaleString("id-ID");
    }
  },
  mounted() {
    if (!this.userEmail) {
      this.$router.push("/login");
      return;
    }
    this.fetchTickets();
  }
};
</script>

<style scoped>
.page {
  padding: 16px;
}

.title {
  font-size: 22px;
  margin-bottom: 16px;
}

.info {
  text-align: center;
  color: #777;
}

.list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 12px;
}

.row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.label {
  font-weight: 600;
}

.status.pending {
  color: orange;
}

.status.cancelled {
  color: red;
}

.status.confirmed {
  color: green;
}

.cancel-btn {
  margin-top: 10px;
  width: 100%;
  background: #ff4d4f;
  color: white;
  border: none;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
}
</style>
