<template>
  <div>
    <!-- HEADER -->
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <h2>Pilih Mobil</h2>

      <!-- LOGOUT JANGAN HILANG -->
      <button @click="logout">Logout</button>
    </div>

    <table border="1" style="margin-top:20px; width:100%;">
      <thead>
        <tr>
          <th>Chassis</th>
          <th>Model</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="row in mobilUnik"
          :key="row.chassis"
          @click="goDetail(row.chassis)"
          style="cursor:pointer"
        >
          <td>{{ row.chassis }}</td>
          <td>{{ row.mod_id }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue"
import { useRouter } from "vue-router"

const wo = ref([])
const router = useRouter()

onMounted(async () => {
  const cus_name = localStorage.getItem("cus_name")

  // 🔐 proteksi halaman
  if (!cus_name) {
    router.push("/login")
    return
  }

  const res = await fetch(
    `http://127.0.0.1:8000/wo/customer/${cus_name}`
  )
  wo.value = await res.json()
})

// 🔥 ambil 1 baris per chassis
const mobilUnik = computed(() => {
  const map = {}
  wo.value.forEach(w => {
    if (!map[w.chassis]) {
      map[w.chassis] = w
    }
  })
  return Object.values(map)
})

const goDetail = (chassis) => {
  router.push(`/bengkel/${chassis}`)
}

// 🚪 LOGOUT
const logout = () => {
  localStorage.removeItem("cus_name")
  localStorage.removeItem("role")
  router.push("/login")
}
</script>
