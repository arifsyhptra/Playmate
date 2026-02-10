import { createRouter, createWebHistory } from "vue-router"

import Home from "@/views/Home.vue"
import SportDetail from "@/views/SportDetail.vue"
import Booking from "@/views/Booking.vue"
import Checkout from "@/views/Checkout.vue"
import AdminDashboard from "@/views/AdminDashboard.vue"
import Login from "@/views/Login.vue"
import UserProfile from "@/views/UserProfile.vue"
import Register from "@/views/Register.vue"
import MyTicket from "@/views/MyTicket.vue"
import Tiket from "@/views/Tiket.vue"
import Leaderboard from "@/views/Leaderboard.vue"
import Event from "@/views/Event.vue"
import Shop from "@/views/Shop.vue"
import Pertandingan from "@/views/Pertandingan.vue"
import Tournament from "@/views/Tournament.vue"

const routes = [
  { path: "/", name: "Home", component: Home },
  { path: "/register", name: "Register", component: Register },
  { path: "/login", name: "Login", component: Login },
  { path: "/profile", name: "Profile", component: UserProfile },
  { path: "/myticket", name: "MyTicket", component: MyTicket },
  { path: "/tiket", name: "Tiket", component: Tiket },
  { path: "/sport/:id", name: "SportDetail", component: SportDetail },
  { path: "/booking/:slotId", name: "Booking", component: Booking },
  { path: "/checkout", name: "Checkout", component: Checkout },
  { path: "/leaderboard", name: "Leaderboard", component: Leaderboard },
  { path: "/event", name: "Event", component: Event },
  { path: "/shop", name: "Event", component: Shop},
  { path: "/tournament", name: "Tournament", component: Tournament },
  { path: "/pertandingan", name: "Pertandingan", component: Pertandingan },
  { path: "/admindashboard", name: "admindashboard", component: AdminDashboard },

  

  // ADMIN
  {
    path: "/admin",
    name: "AdminDashboard",
    component: AdminDashboard,
    meta: { requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

/* =========================
   ROUTER GUARD - FIXED
   ========================= */
router.beforeEach((to, from, next) => {
  const userStr = localStorage.getItem("user")
  const user = userStr ? JSON.parse(userStr) : null

  // 1️⃣ Jika halaman memerlukan admin
  if (to.meta.requiresAdmin) {
    if (!user) {
      // Belum login → ke login
      return next("/login")
    }
    if (user.role !== "admin") {
      // Bukan admin → ke home
      return next("/")
    }
    // Admin → lanjut
    return next()
  }

  // 2️⃣ Jika user sudah login dan akses halaman login/register
  if (to.name === "Login" || to.name === "Register") {
    if (user) {
      // Sudah login
      if (user.role === "admin") {
        return next("/admin")
      }
      return next("/")
    }
  }

  // 3️⃣ Lanjutkan navigasi normal
  next()
})

export default router