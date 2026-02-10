<script>
import axios from "axios";

export default {
  data() {
    return {
      order: {
        slotId: null,
        participants: []
      }
    };
  },

  computed: {
    total() {
      return this.order.participants.length * 50000;
    }
  },

  mounted() {
    const saved = sessionStorage.getItem("order");

    if (!saved) {
      alert("Data pesanan tidak ditemukan");
      this.$router.push("/");
      return;
    }

    this.order = JSON.parse(saved);
  },

  methods: {
    async checkout() {
      const res = await axios.post(
        "http://localhost:8000/create-transaction",
        {
          slot_id: this.order.slotId,
          participants: this.order.participants,
          amount: this.total
        }
      );

      window.location.href = res.data.redirect_url;
    }
  }
};
</script>
