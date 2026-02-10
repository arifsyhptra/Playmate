<template>
  <div class="admin-container">
    <!-- Animated Background -->
    <div class="bg-gradient"></div>
    <div class="noise-overlay"></div>
    
    <!-- Main Content -->
    <div class="dashboard-wrapper">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <div class="logo">
            <span class="logo-icon">🎮</span>
            <div class="logo-text">
              <h2><span class="text-gradient">Play</span><span class="text-teal">mate</span></h2>
              <p>Admin Dashboard</p>
            </div>
          </div>
        </div>

        <nav class="sidebar-nav">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            :class="['nav-item', { active: activeTab === tab.id }]"
            @click="switchTab(tab.id)"
          >
            <span class="nav-icon">{{ tab.icon }}</span>
            <span class="nav-label">{{ tab.label }}</span>
          </button>
        </nav>

        <div class="sidebar-footer">
          <div class="admin-info">
            <div class="admin-avatar">{{ adminInitials }}</div>
            <div class="admin-details">
              <p class="admin-name">{{ admin.name }}</p>
              <p class="admin-role">Administrator</p>
            </div>
          </div>
          <button class="logout-btn" @click="handleLogout">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
              <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4M16 17l5-5-5-5M21 12H9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
            <span>Logout</span>
          </button>
        </div>
      </aside>

      <!-- Main Content Area -->
      <main class="main-content">
        <!-- Dashboard Tab -->
        <div v-if="activeTab === 'dashboard'" class="tab-content">
          <header class="content-header">
            <div>
              <h1 class="content-title">Dashboard</h1>
              <p class="content-subtitle">Selamat datang kembali, {{ admin.name }}! 👋</p>
            </div>
            <button class="action-btn primary" @click="loadDashboard">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M1 4v6h6M23 20v-6h-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M20.49 9A9 9 0 005.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 013.51 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              Refresh
            </button>
          </header>

          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon" style="background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)">
                👥
              </div>
              <div class="stat-content">
                <p class="stat-label">Total Users</p>
                <h3 class="stat-value">{{ dashboardStats.total_users || 0 }}</h3>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon" style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%)">
                ⚽
              </div>
              <div class="stat-content">
                <p class="stat-label">Total Sports</p>
                <h3 class="stat-value">{{ dashboardStats.total_sports || 0 }}</h3>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon" style="background: linear-gradient(135deg, #a855f7 0%, #9333ea 100%)">
                📅
              </div>
              <div class="stat-content">
                <p class="stat-label">Total Slots</p>
                <h3 class="stat-value">{{ dashboardStats.total_slots || 0 }}</h3>
              </div>
            </div>

            <div class="stat-card">
              <div class="stat-icon" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%)">
                💰
              </div>
              <div class="stat-content">
                <p class="stat-label">Total Revenue</p>
                <h3 class="stat-value">Rp {{ formatNumber(dashboardStats.total_revenue || 0) }}</h3>
              </div>
            </div>
          </div>

          <div class="charts-row">
            <div class="chart-card">
              <h3 class="card-title">Booking Status</h3>
              <div class="status-list">
                <div v-for="status in dashboardStats.bookings_by_status" :key="status.status" class="status-item">
                  <div class="status-info">
                    <span :class="['status-dot', getStatusDotClass(status.status)]"></span>
                    <span class="status-name">{{ status.status }}</span>
                  </div>
                  <span class="status-count">{{ status.count }}</span>
                </div>
              </div>
            </div>

            <div class="chart-card">
              <h3 class="card-title">Olahraga Populer</h3>
              <div class="popular-list">
                <div v-for="(sport, index) in dashboardStats.popular_sports" :key="sport.name" class="popular-item">
                  <div class="popular-info">
                    <span class="popular-rank">{{ index + 1 }}</span>
                    <span class="popular-name">{{ sport.name }}</span>
                  </div>
                  <div class="popular-bar">
                    <div class="popular-fill" :style="{ width: sport.percentage + '%', background: getGradient(index) }"></div>
                  </div>
                  <span class="popular-count">{{ sport.percentage }}%</span>
                </div>
              </div>
            </div>
          </div>

          <div class="recent-card">
            <div class="card-header">
              <h3 class="card-title">Booking Terbaru</h3>
            </div>
            <div class="recent-list">
              <div v-for="booking in dashboardStats.recent_bookings" :key="booking.id" class="recent-item">
                <div class="recent-user">
                  <div class="recent-avatar">{{ getInitials(booking.user_name) }}</div>
                  <div class="recent-details">
                    <p class="recent-name">{{ booking.user_name }}</p>
                    <p class="recent-email">{{ booking.user_email }}</p>
                  </div>
                </div>
                <div class="recent-sport">
                  <p class="recent-sport-name">{{ booking.sport_name }}</p>
                  <p class="recent-time">{{ booking.day }}, {{ booking.time }}</p>
                </div>
                <span :class="['badge', getStatusClass(booking.status)]">{{ booking.status }}</span>
                <p class="recent-date">{{ formatDate(booking.created_at) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Users Tab -->
        <div v-if="activeTab === 'users'" class="tab-content">
          <header class="content-header">
            <div>
              <h1 class="content-title">Kelola User</h1>
              <p class="content-subtitle">Manajemen pengguna sistem</p>
            </div>
            <button class="action-btn primary" @click="loadUsers">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M1 4v6h6M23 20v-6h-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M20.49 9A9 9 0 005.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 013.51 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              Refresh
            </button>
          </header>

          <div class="table-card">
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nama</th>
                  <th>Email</th>
                  <th>Provider</th>
                  <th>Role</th>
                  <th>Bergabung</th>
                  <th>Aksi</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>#{{ user.id }}</td>
                  <td>
                    <div class="table-user">
                      <div class="table-avatar">{{ getInitials(user.name) }}</div>
                      <span>{{ user.name }}</span>
                    </div>
                  </td>
                  <td>{{ user.email }}</td>
                  <td><span :class="['badge', user.provider === 'google' ? 'badge-red' : 'badge-blue']">{{ user.provider }}</span></td>
                  <td><span :class="['badge', user.role === 'admin' ? 'badge-purple' : 'badge-gray']">{{ user.role || 'user' }}</span></td>
                  <td>{{ formatDate(user.created_at) }}</td>
                  <td>
                    <div class="action-buttons">
                      <button class="icon-btn delete" @click="deleteUser(user.id)" :disabled="user.role === 'admin'">🗑️</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Sports Tab -->
        <div v-if="activeTab === 'sports'" class="tab-content">
          <header class="content-header">
            <div>
              <h1 class="content-title">Kelola Olahraga</h1>
              <p class="content-subtitle">Manajemen jenis olahraga</p>
            </div>
            <button class="action-btn primary" @click="showAddSportModal = true">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              Tambah Olahraga
            </button>
          </header>

          <div class="sports-grid">
            <div v-for="sport in sports" :key="sport.id" class="sport-card">
              <div class="sport-header">
                <span class="sport-emoji">⚽</span>
                <button class="icon-btn delete" @click="deleteSport(sport.id)">🗑️</button>
              </div>
              <h3 class="sport-name">{{ sport.name }}</h3>
              <div class="sport-details">
                <div class="sport-detail-item">
                  <span class="detail-label">Harga</span>
                  <span class="detail-value">Rp {{ formatNumber(sport.price) }}</span>
                </div>
                <div class="sport-detail-item">
                  <span class="detail-label">Kapasitas</span>
                  <span class="detail-value">{{ sport.capacity }} orang</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Slots Tab -->
        <div v-if="activeTab === 'slots'" class="tab-content">
          <header class="content-header">
            <div>
              <h1 class="content-title">Kelola Slot</h1>
              <p class="content-subtitle">Manajemen jadwal slot booking</p>
            </div>
            <button class="action-btn primary" @click="openAddSlotModal">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              Tambah Slot
            </button>
          </header>

          <div class="table-card">
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Olahraga</th>
                  <th>Hari</th>
                  <th>Waktu</th>
                  <th>Lapangan</th>
                  <th>Tingkat</th>
                  <th>Terisi</th>
                  <th>Aksi</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="slot in slots" :key="slot.id">
                  <td>#{{ slot.id }}</td>
                  <td><span class="badge badge-blue">{{ slot.sport_name }}</span></td>
                  <td>{{ slot.day }}</td>
                  <td>{{ slot.time }}</td>
                  <td>{{ slot.lapangan }}</td>
                  <td>{{ slot.tingkat }}</td>
                  <td><span :class="['badge', slot.booked_count >= slot.capacity ? 'badge-red' : 'badge-green']">{{ slot.booked_count }}/{{ slot.capacity }}</span></td>
                  <td>
                    <div class="action-buttons">
                      <button class="icon-btn delete" @click="deleteSlot(slot.id)">🗑️</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Bookings Tab -->
        <div v-if="activeTab === 'bookings'" class="tab-content">
          <header class="content-header">
            <div>
              <h1 class="content-title">Kelola Booking</h1>
              <p class="content-subtitle">Manajemen pesanan pengguna</p>
            </div>
            <button class="action-btn primary" @click="loadBookings">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M1 4v6h6M23 20v-6h-6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <path d="M20.49 9A9 9 0 005.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 013.51 15" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              Refresh
            </button>
          </header>

          <div class="table-card">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Order ID</th>
                  <th>User</th>
                  <th>Olahraga</th>
                  <th>Jadwal</th>
                  <th>Nama Peserta</th>
                  <th>Status</th>
                  <th>Total</th>
                  <th>Aksi</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="booking in bookings" :key="booking.id">
                  <td class="mono-text">{{ booking.order_id }}</td>
                  <td>
                    <div class="table-user">
                      <div class="table-avatar">{{ getInitials(booking.user_name) }}</div>
                      <div>
                        <p class="user-name">{{ booking.user_name }}</p>
                        <p class="user-email">{{ booking.user_email }}</p>
                      </div>
                    </div>
                  </td>
                  <td><span class="badge badge-blue">{{ booking.sport_name }}</span></td>
                  <td>
                    <div class="schedule-info">
                      <p class="schedule-day">{{ booking.day }}, {{ booking.time }}</p>
                      <p class="schedule-court">{{ booking.lapangan }}</p>
                    </div>
                  </td>
                  <td>{{ booking.booking_name }}</td>
                  <td><span :class="['badge', getStatusClass(booking.status)]">{{ booking.status }}</span></td>
                  <td class="price-text">Rp {{ formatNumber(booking.price) }}</td>
                  <td>
                    <div class="action-buttons">
                      <button v-if="booking.status !== 'CANCELLED'" class="icon-btn cancel" @click="cancelBooking(booking.id)">❌</button>
                      <button class="icon-btn delete" @click="deleteBooking(booking.id)">🗑️</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>

    <!-- Add Sport Modal -->
    <div v-if="showAddSportModal" class="modal-overlay" @click.self="showAddSportModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <h3>Tambah Olahraga Baru</h3>
          <button class="close-btn" @click="showAddSportModal = false">✕</button>
        </div>
        <form @submit.prevent="addSport" class="modal-form">
          <div class="form-group">
            <label>Nama Olahraga</label>
            <input v-model="newSport.name" type="text" required class="form-input" />
          </div>
          <div class="form-group">
            <label>Harga</label>
            <input v-model.number="newSport.price" type="number" required class="form-input" />
          </div>
          <div class="form-group">
            <label>Kapasitas</label>
            <input v-model.number="newSport.capacity" type="number" required class="form-input" />
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="showAddSportModal = false">Batal</button>
            <button type="submit" class="btn-primary">Simpan</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Add Slot Modal -->
    <div v-if="showAddSlotModal" class="modal-overlay" @click.self="showAddSlotModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <h3>Tambah Slot Baru</h3>
          <button class="close-btn" @click="showAddSlotModal = false">✕</button>
        </div>
        <form @submit.prevent="addSlot" class="modal-form">
          <div class="form-group">
            <label>Olahraga</label>
            <select v-model.number="newSlot.sport_id" required class="form-input">
              <option value="">Pilih Olahraga</option>
              <option v-for="sport in sports" :key="sport.id" :value="sport.id">{{ sport.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>Hari</label>
            <select v-model="newSlot.day" required class="form-input">
              <option>Senin</option>
              <option>Selasa</option>
              <option>Rabu</option>
              <option>Kamis</option>
              <option>Jumat</option>
              <option>Sabtu</option>
              <option>Minggu</option>
            </select>
          </div>
          <div class="form-group">
            <label>Waktu</label>
            <input v-model="newSlot.time" type="text" required placeholder="08:00 - 10:00" class="form-input" />
          </div>
          <div class="form-group">
            <label>Lapangan</label>
            <input v-model="newSlot.lapangan" type="text" required placeholder="Lapangan A" class="form-input" />
          </div>
          <div class="form-group">
            <label>Tingkat</label>
            <select v-model="newSlot.tingkat" required class="form-input">
              <option>Pemula</option>
              <option>Menengah</option>
              <option>Lanjutan</option>
              <option>Semua Tingkat</option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="showAddSlotModal = false">Batal</button>
            <button type="submit" class="btn-primary">Simpan</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const API_URL = 'http://202.155.94.61:8000'

const admin = ref({
  name: '',
  email: '',
  role: ''
})

const activeTab = ref('dashboard')

const tabs = [
  { id: 'dashboard', label: 'Dashboard', icon: '📊' },
  { id: 'users', label: 'Kelola User', icon: '👥' },
  { id: 'sports', label: 'Kelola Olahraga', icon: '⚽' },
  { id: 'slots', label: 'Kelola Slot', icon: '📅' },
  { id: 'bookings', label: 'Kelola Booking', icon: '📋' }
]

// Data states
const dashboardStats = ref({
  total_users: 0,
  total_sports: 0,
  total_slots: 0,
  total_revenue: 0,
  bookings_by_status: [],
  popular_sports: [],
  recent_bookings: []
})

const users = ref([])
const sports = ref([])
const slots = ref([])
const bookings = ref([])

// Modal states
const showAddSportModal = ref(false)
const showAddSlotModal = ref(false)

const newSport = ref({
  name: '',
  price: 0,
  capacity: 0
})

const newSlot = ref({
  sport_id: '',
  day: '',
  time: '',
  lapangan: '',
  tingkat: ''
})

const adminInitials = computed(() => {
  return admin.value.name ? admin.value.name.substring(0, 2).toUpperCase() : 'AD'
})

onMounted(() => {
  const userStr = localStorage.getItem('user')
  
  if (!userStr) {
    router.push('/login')
    return
  }
  
  const user = JSON.parse(userStr)
  
  if (user.role !== 'admin') {
    router.push('/')
    return
  }
  
  admin.value = user
  loadDashboard()
})

function switchTab(tabId) {
  activeTab.value = tabId
  
  if (tabId === 'dashboard') loadDashboard()
  if (tabId === 'users') loadUsers()
  if (tabId === 'sports') loadSports()
  if (tabId === 'slots') loadSlots()
  if (tabId === 'bookings') loadBookings()
}

async function loadDashboard() {
  try {
    const { data } = await axios.get(`${API_URL}/admin/stats`)
    dashboardStats.value = data
  } catch (error) {
    console.error('Error loading dashboard:', error)
    alert('Gagal memuat dashboard')
  }
}

async function loadUsers() {
  try {
    const { data } = await axios.get(`${API_URL}/admin/users`)
    users.value = data
  } catch (error) {
    console.error('Error loading users:', error)
    alert('Gagal memuat data user')
  }
}

async function deleteUser(userId) {
  if (!confirm('Yakin ingin menghapus user ini?')) return
  
  try {
    await axios.delete(`${API_URL}/admin/users/${userId}`)
    alert('User berhasil dihapus')
    loadUsers()
  } catch (error) {
    console.error('Error deleting user:', error)
    alert('Gagal menghapus user')
  }
}

async function loadSports() {
  try {
    const { data } = await axios.get(`${API_URL}/sports`)
    sports.value = data
  } catch (error) {
    console.error('Error loading sports:', error)
    alert('Gagal memuat data olahraga')
  }
}

async function addSport() {
  try {
    await axios.post(`${API_URL}/admin/sports`, newSport.value)
    alert('Olahraga berhasil ditambahkan')
    showAddSportModal.value = false
    newSport.value = { name: '', price: 0, capacity: 0 }
    loadSports()
  } catch (error) {
    console.error('Error adding sport:', error)
    alert('Gagal menambahkan olahraga')
  }
}

async function deleteSport(sportId) {
  if (!confirm('Yakin ingin menghapus olahraga ini? Semua slot terkait akan ikut terhapus.')) return
  
  try {
    await axios.delete(`${API_URL}/admin/sports/${sportId}`)
    alert('Olahraga berhasil dihapus')
    loadSports()
  } catch (error) {
    console.error('Error deleting sport:', error)
    alert('Gagal menghapus olahraga')
  }
}

async function openAddSlotModal() {
  await loadSports()
  showAddSlotModal.value = true
}

async function loadSlots() {
  try {
    const { data } = await axios.get(`${API_URL}/admin/slots`)
    slots.value = data
  } catch (error) {
    console.error('Error loading slots:', error)
    alert('Gagal memuat data slot')
  }
}

async function addSlot() {
  try {
    await axios.post(`${API_URL}/admin/slots`, newSlot.value)
    alert('Slot berhasil ditambahkan')
    showAddSlotModal.value = false
    newSlot.value = { sport_id: '', day: '', time: '', lapangan: '', tingkat: '' }
    loadSlots()
  } catch (error) {
    console.error('Error adding slot:', error)
    alert('Gagal menambahkan slot')
  }
}

async function deleteSlot(slotId) {
  if (!confirm('Yakin ingin menghapus slot ini?')) return
  
  try {
    await axios.delete(`${API_URL}/admin/slots/${slotId}`)
    alert('Slot berhasil dihapus')
    loadSlots()
  } catch (error) {
    console.error('Error deleting slot:', error)
    alert('Gagal menghapus slot')
  }
}

async function loadBookings() {
  try {
    const { data } = await axios.get(`${API_URL}/admin/bookings`)
    bookings.value = data
  } catch (error) {
    console.error('Error loading bookings:', error)
    alert('Gagal memuat data booking')
  }
}

async function cancelBooking(bookingId) {
  if (!confirm('Yakin ingin membatalkan booking ini?')) return
  
  try {
    await axios.put(`${API_URL}/admin/bookings/${bookingId}/cancel`)
    alert('Booking berhasil dibatalkan')
    loadBookings()
  } catch (error) {
    console.error('Error cancelling booking:', error)
    alert('Gagal membatalkan booking')
  }
}

async function deleteBooking(bookingId) {
  if (!confirm('Yakin ingin menghapus booking ini?')) return
  
  try {
    await axios.delete(`${API_URL}/admin/bookings/${bookingId}`)
    alert('Booking berhasil dihapus')
    loadBookings()
  } catch (error) {
    console.error('Error deleting booking:', error)
    alert('Gagal menghapus booking')
  }
}

function handleLogout() {
  if (confirm('Yakin ingin logout?')) {
    localStorage.removeItem('user')
    router.push('/login')
  }
}

function formatNumber(num) {
  return new Intl.NumberFormat('id-ID').format(num)
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (hours < 1) return 'Baru saja'
  if (hours < 24) return `${hours} jam yang lalu`
  if (days < 7) return `${days} hari yang lalu`
  
  return date.toLocaleDateString('id-ID', { day: 'numeric', month: 'short', year: 'numeric' })
}

function getInitials(name) {
  if (!name) return '?'
  return name.substring(0, 2).toUpperCase()
}

function getStatusClass(status) {
  const classes = {
    'CONFIRMED': 'badge-green',
    'PENDING': 'badge-yellow',
    'CANCELLED': 'badge-red',
    'FAILED': 'badge-gray'
  }
  return classes[status] || 'badge-gray'
}

function getStatusDotClass(status) {
  const classes = {
    'CONFIRMED': 'confirmed',
    'PENDING': 'pending',
    'CANCELLED': 'cancelled',
    'FAILED': 'failed'
  }
  return classes[status] || 'failed'
}

function getGradient(index) {
  const gradients = [
    'linear-gradient(90deg, #3b82f6 0%, #2563eb 100%)',
    'linear-gradient(90deg, #22c55e 0%, #16a34a 100%)',
    'linear-gradient(90deg, #a855f7 0%, #9333ea 100%)',
    'linear-gradient(90deg, #f59e0b 0%, #d97706 100%)',
    'linear-gradient(90deg, #ef4444 0%, #dc2626 100%)'
  ]
  return gradients[index] || gradients[0]
}
</script>

<style scoped>
/* Gunakan CSS yang sama seperti sebelumnya */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.admin-container {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  font-family: 'DM Sans', sans-serif;
  background: #0a0a0a;
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
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
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

.dashboard-wrapper {
  position: relative;
  z-index: 2;
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: 280px;
  background: rgba(255, 255, 255, 0.02);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}

.sidebar-header {
  padding: 32px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.logo {
  display: flex;
  align-items: center;
  gap: 16px;
}

.logo-icon {
  font-size: 40px;
  animation: pulse 2s ease infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

.logo-text h2 {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 24px;
  font-weight: 700;
  margin: 0 0 4px 0;
}

.text-gradient {
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.text-teal {
  color: #4ecdc4;
}

.logo-text p {
  font-size: 12px;
  color: #666;
  margin: 0;
}

.sidebar-nav {
  flex: 1;
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 12px;
  color: #888;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.03);
  color: #e0e0e0;
}

.nav-item.active {
  background: rgba(78, 205, 196, 0.1);
  border-color: rgba(78, 205, 196, 0.3);
  color: #4ecdc4;
}

.nav-icon {
  font-size: 20px;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
}

.admin-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  margin-bottom: 12px;
}

.admin-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4ecdc4 0%, #44a399 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 14px;
}

.admin-details {
  flex: 1;
}

.admin-name {
  font-size: 14px;
  font-weight: 600;
  color: #e0e0e0;
  margin: 0 0 2px 0;
}

.admin-role {
  font-size: 12px;
  color: #666;
  margin: 0;
}

.logout-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px;
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid rgba(255, 107, 107, 0.2);
  border-radius: 10px;
  color: #ff6b6b;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(255, 107, 107, 0.15);
  border-color: rgba(255, 107, 107, 0.3);
  transform: translateY(-2px);
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 280px;
  padding: 40px;
}

.tab-content {
  animation: fadeInUp 0.6s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
  flex-wrap: wrap;
  gap: 16px;
}

.content-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 36px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px 0;
}

.content-subtitle {
  font-size: 15px;
  color: #888;
  margin: 0;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 10px;
  border: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.action-btn.primary {
  background: linear-gradient(135deg, #4ecdc4 0%, #44a399 100%);
  color: #fff;
}

.action-btn.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(78, 205, 196, 0.3);
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.12);
  transform: translateY(-4px);
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 13px;
  color: #888;
  margin: 0 0 8px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  margin: 0;
}

/* Charts Row */
.charts-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.chart-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 28px;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #fff;
  margin: 0 0 24px 0;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.status-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.status-dot.confirmed {
  background: #22c55e;
  box-shadow: 0 0 8px rgba(34, 197, 94, 0.5);
}

.status-dot.pending {
  background: #eab308;
  box-shadow: 0 0 8px rgba(234, 179, 8, 0.5);
}

.status-dot.cancelled {
  background: #ff6b6b;
  box-shadow: 0 0 8px rgba(255, 107, 107, 0.5);
}

.status-dot.failed {
  background: #6b7280;
}

.status-name {
  font-size: 15px;
  color: #e0e0e0;
  font-weight: 500;
}

.status-count {
  font-size: 20px;
  font-weight: 700;
  color: #4ecdc4;
}

.popular-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.popular-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.popular-info {
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 140px;
}

.popular-rank {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #4ecdc4;
  font-size: 14px;
}

.popular-name {
  font-size: 14px;
  font-weight: 500;
  color: #e0e0e0;
}

.popular-bar {
  flex: 1;
  height: 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
  overflow: hidden;
}

.popular-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.popular-count {
  font-size: 14px;
  font-weight: 600;
  color: #888;
  min-width: 40px;
  text-align: right;
}

/* Recent Card */
.recent-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 28px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.recent-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.recent-item {
  display: grid;
  grid-template-columns: 2fr 2fr auto auto;
  gap: 20px;
  align-items: center;
  padding: 20px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}

.recent-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.recent-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 14px;
}

.recent-details {
  flex: 1;
}

.recent-name {
  font-size: 14px;
  font-weight: 600;
  color: #e0e0e0;
  margin: 0 0 4px 0;
}

.recent-email {
  font-size: 12px;
  color: #666;
  margin: 0;
}

.recent-sport {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.recent-sport-name {
  font-size: 14px;
  font-weight: 600;
  color: #e0e0e0;
  margin: 0;
}

.recent-time {
  font-size: 12px;
  color: #666;
  margin: 0;
}

.recent-date {
  font-size: 12px;
  color: #666;
  margin: 0;
}

/* Table */
.table-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  overflow: hidden;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: rgba(255, 255, 255, 0.02);
}

.data-table th {
  padding: 16px 24px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.data-table td {
  padding: 16px 24px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  font-size: 14px;
  color: #e0e0e0;
}

.data-table tbody tr {
  transition: all 0.3s ease;
}

.data-table tbody tr:hover {
  background: rgba(255, 255, 255, 0.02);
}

.table-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.table-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-weight: 700;
  font-size: 12px;
  flex-shrink: 0;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
  color: #e0e0e0;
  margin: 0 0 2px 0;
}

.user-email {
  font-size: 12px;
  color: #666;
  margin: 0;
}

.schedule-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.schedule-day {
  font-size: 14px;
  color: #e0e0e0;
  margin: 0;
}

.schedule-court {
  font-size: 12px;
  color: #666;
  margin: 0;
}

.mono-text {
  font-family: 'Courier New', monospace;
  font-size: 13px;
  color: #888;
}

.price-text {
  font-weight: 600;
  color: #4ecdc4;
}

.badge {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.3px;
}

.badge-blue {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.badge-red {
  background: rgba(255, 107, 107, 0.15);
  color: #ff6b6b;
}

.badge-purple {
  background: rgba(168, 85, 247, 0.15);
  color: #a855f7;
}

.badge-gray {
  background: rgba(107, 114, 128, 0.15);
  color: #9ca3af;
}

.badge-green {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}

.badge-yellow {
  background: rgba(234, 179, 8, 0.15);
  color: #eab308;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.icon-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: none;
  background: rgba(255, 255, 255, 0.05);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 14px;
}

.icon-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.icon-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.icon-btn.delete:hover:not(:disabled) {
  background: rgba(255, 107, 107, 0.15);
}

.icon-btn.cancel:hover {
  background: rgba(245, 158, 11, 0.15);
}

/* Sports Grid */
.sports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
}

.sport-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s ease;
}

.sport-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.12);
  transform: translateY(-4px);
}

.sport-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.sport-emoji {
  font-size: 48px;
}

.sport-name {
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 20px 0;
}

.sport-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sport-detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
}

.detail-label {
  font-size: 13px;
  color: #888;
  font-weight: 500;
}

.detail-value {
  font-size: 14px;
  color: #e0e0e0;
  font-weight: 600;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-card {
  background: rgba(26, 26, 26, 0.98);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 32px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.modal-header h3 {
  font-size: 24px;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.05);
  color: #888;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  color: #e0e0e0;
  font-size: 14px;
  font-family: 'DM Sans', sans-serif;
  transition: all 0.3s ease;
}

.form-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.04);
  border-color: rgba(78, 205, 196, 0.3);
}

.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.btn-secondary,
.btn-primary {
  flex: 1;
  padding: 12px 24px;
  border-radius: 10px;
  border: none;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  color: #e0e0e0;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.08);
}

.btn-primary {
  background: linear-gradient(135deg, #4ecdc4 0%, #44a399 100%);
  color: #fff;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(78, 205, 196, 0.3);
}

/* Responsive */
@media (max-width: 1024px) {
  .sidebar {
    width: 240px;
  }

  .main-content {
    margin-left: 240px;
    padding: 32px 24px;
  }

  .recent-item {
    grid-template-columns: 1fr;
    gap: 12px;
  }
}

@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }

  .main-content {
    margin-left: 0;
    padding: 24px 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .charts-row {
    grid-template-columns: 1fr;
  }

  .sports-grid {
    grid-template-columns: 1fr;
  }

  .table-card {
    overflow-x: auto;
  }
}
</style>