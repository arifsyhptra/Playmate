<template>
  <div class="container">
    <h1>🏸 Badminton</h1>

    <table v-if="sport">
      <tr>
        <th>Harga</th>
        <td>Rp {{ sport.price }}</td>
      </tr>
      <tr>
        <th>Kapasitas</th>
        <td>{{ sport.capacity }} orang</td>
      </tr>
      <tr>
        <th>Aksi</th>
        <td>
          <button @click="book">Join</button>
        </td>
      </tr>
    </table>

    <p v-else>Loading...</p>
  </div>
</template>

<script>
export default {
  name: "Badminton",
  data() {
    return {
      sport: null,
      user_id: localStorage.getItem("user_id")
    };
  },
  mounted() {
    fetch("http://localhost:8000/sports/1")
      .then(res => res.json())
      .then(data => {
        this.sport = data;
      });
  },
  methods: {
    book() {
      if (!this.user_id) {
        alert("Silakan login dulu");
        this.$router.push("/login");
        return;
      }

      alert("Simulasi join badminton");
    }
  }
};
</script>
