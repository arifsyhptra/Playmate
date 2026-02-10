<template>
  <div class="container">
    <h2>Isi Data Peserta</h2>

    <label>Jumlah Orang</label>
    <select v-model="count">
      <option v-for="n in 10" :key="n" :value="n">{{ n }}</option>
    </select>

    <div v-for="(p, i) in participants" :key="i" class="card">
      <input v-model="p.name" placeholder="Nama Peserta" />
      <input v-model="p.phone" placeholder="No WhatsApp" />
    </div>

    <button class="primary" @click="submit">
      Pesan
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      count: 1,
      participants: [{ name: "", phone: "" }]
    };
  },
  watch: {
    count(val) {
      this.participants = Array.from({ length: val }, () => ({
        name: "",
        phone: ""
      }));
    }
  },
  methods: {
    submit() {
      this.$router.push({
        path: "/order-detail",
        state: {
          slotId: this.$route.params.slotId,
          participants: this.participants
        }
      });
    }
  }
};
</script>
