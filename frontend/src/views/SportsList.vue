<script>
import axios from "axios"

export default {
  data() {
    return {
      sports: []
    }
  },
  mounted() {
    this.fetchSports()
  },
  methods: {
    async fetchSports() {
      try {
        const res = await axios.get("http://localhost:8000/api/sports")
        this.sports = res.data.map(s => ({
          name: s.name,
          icon: this.getIcon(s.name),
          route: `/admin/sport/${s.slug}`
        }))
      } catch (err) {
        console.error("Gagal ambil data sports", err)
      }
    },
    getIcon(name) {
      const icons = {
        "Padel": "🎾",
        "Badminton": "🏸",
        "Tenis": "🎾",
        "Tenis Meja": "🏓",
        "Mini Soccer": "⚽",
        "Biliard": "🎱"
      }
      return icons[name] || "🏟️"
    },
    goToSport(route) {
      this.$router.push(route)
    },
    logout() {
      localStorage.removeItem("role")
      this.$router.push("/admin-login")
    }
  }
}
</script>
