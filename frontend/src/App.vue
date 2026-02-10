<template>
  <div id="app">
    <!-- Navbar -->
    <nav class="navbar" v-if="shouldShowNavbar">
      <div class="nav-container">
        <div class="nav-brand">
          <router-link to="/" class="brand-link">
            <div class="brand-icon-small">
             
            </div>
            <span class="brand-text">
              <span class="brand-play">Play</span><span class="brand-mate">mate</span>
            </span>
          </router-link>
        </div>
        
        <ul class="nav-links">
          <li v-if="isLoggedIn">
            <router-link to="/" class="nav-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M3 9L12 2L21 9V20C21 20.5304 20.7893 21.0391 20.4142 21.4142C20.0391 21.7893 19.5304 22 19 22H5C4.46957 22 3.96086 21.7893 3.58579 21.4142C3.21071 21.0391 3 20.5304 3 20V9Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>Home</span>
            </router-link>
          </li>
          
          <li v-if="!isLoggedIn">
            <router-link to="/login" class="nav-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M15 3H19C19.5304 3 20.0391 3.21071 20.4142 3.58579C20.7893 3.96086 21 4.46957 21 5V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M10 17L15 12L10 7M15 12H3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              <span>Login</span>
            </router-link>
          </li>
          
          <li v-if="!isLoggedIn">
            <router-link to="/register" class="nav-link">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
                <path d="M16 21V19C16 17.9391 15.5786 16.9217 14.8284 16.1716C14.0783 15.4214 13.0609 15 12 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="8.5" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                <path d="M20 8V14M17 11H23" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              </svg>
              <span>Register</span>
            </router-link>
          </li>
          
          <!-- User Dropdown -->
          <li v-if="isLoggedIn" class="user-dropdown-wrapper">
            <button @click="toggleDropdown" class="user-dropdown-trigger">
              <div class="user-badge">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                </svg>
                <span class="user-name">{{ userName }}</span>
                <svg 
                  class="chevron-icon" 
                  :class="{ 'chevron-open': dropdownOpen }"
                  width="14" 
                  height="14" 
                  viewBox="0 0 24 24" 
                  fill="none"
                >
                  <path d="M6 9L12 15L18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
            </button>

            <!-- Dropdown Menu -->
            <transition name="dropdown-fade">
              <div v-if="dropdownOpen" class="dropdown-menu" @click.stop>
                <button @click="goToMyTicket" class="dropdown-item">
                  <span class="dropdown-icon">🎟</span>
                  <span>My Ticket</span>
                </button>
                <button @click="goToProfile" class="dropdown-item">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="12" cy="7" r="4" stroke="currentColor" stroke-width="2"/>
                  </svg>
                  <span>Profile</span>
                </button>
                <div class="dropdown-divider"></div>
                <button @click="handleLogout" class="dropdown-item danger">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M16 17L21 12L16 7M21 12H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  <span>Logout</span>
                </button>
              </div>
            </transition>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content" :class="{ 'no-navbar': !shouldShowNavbar }">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false,
      userName: '',
      dropdownOpen: false
    }
  },
  computed: {
    shouldShowNavbar() {
      // Hide navbar on login and register pages
      const hideNavbarRoutes = ['/login', '/register']
      return !hideNavbarRoutes.includes(this.$route.path)
    }
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen
    },
    closeDropdown() {
      this.dropdownOpen = false
    },
    goToMyTicket() {
      this.closeDropdown()
      this.$router.push('/myticket')
    },
    goToProfile() {
      this.closeDropdown()
      this.$router.push('/profile')
    },
    handleLogout() {
      this.isLoggedIn = false
      this.userName = ''
      this.dropdownOpen = false
      localStorage.removeItem('user')
      this.$router.push('/login')
    },
    checkAuth() {
      const user = localStorage.getItem('user')
      if (user) {
        this.isLoggedIn = true
        const parsed = JSON.parse(user)
        this.userName = parsed.name || 'User'
      } else {
        this.isLoggedIn = false
        this.userName = ''
      }
    },
    handleClickOutside(event) {
      const dropdown = this.$el?.querySelector('.user-dropdown-wrapper')
      if (dropdown && !dropdown.contains(event.target)) {
        this.closeDropdown()
      }
    }
  },
  mounted() {
    this.checkAuth()
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  },
  watch: {
    $route() {
      this.checkAuth()
      this.closeDropdown()
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'DM Sans', sans-serif;
  background: #0a0a0a;
  color: #e0e0e0;
  overflow-x: hidden;
}

#app {
  min-height: 100vh;
}

/* Navbar Styles */
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(10, 10, 10, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  padding: 16px 0;
  animation: slideDown 0.5s ease;
}

@keyframes slideDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand {
  display: flex;
  align-items: center;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 12px;
  text-decoration: none;
  transition: transform 0.3s ease;
}

.brand-link:hover {
  transform: translateY(-2px);
}

.brand-icon-small {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.brand-text {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.brand-play {
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.brand-mate {
  color: #4ecdc4;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 8px;
  align-items: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  color: #e0e0e0;
  text-decoration: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 10px;
  background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(78, 205, 196, 0.1) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.nav-link:hover::before {
  opacity: 1;
}

.nav-link:hover {
  color: #fff;
  transform: translateY(-2px);
}

.nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* User Dropdown */
.user-dropdown-wrapper {
  position: relative;
  margin-left: 8px;
}

.user-dropdown-trigger {
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  font-family: inherit;
}

.user-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: rgba(78, 205, 196, 0.1);
  border: 1px solid rgba(78, 205, 196, 0.2);
  border-radius: 10px;
  color: #4ecdc4;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.user-dropdown-trigger:hover .user-badge {
  background: rgba(78, 205, 196, 0.15);
  border-color: rgba(78, 205, 196, 0.3);
}

.user-name {
  max-width: 150px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.chevron-icon {
  transition: transform 0.3s ease;
}

.chevron-icon.chevron-open {
  transform: rotate(180deg);
}

/* Dropdown Menu */
.dropdown-menu {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  min-width: 200px;
  background: rgba(20, 20, 20, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  overflow: hidden;
  z-index: 1000;
}

.dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: none;
  border: none;
  color: #e0e0e0;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'DM Sans', sans-serif;
  text-align: left;
}

.dropdown-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: #fff;
}

.dropdown-item.danger {
  color: #ef4444;
}

.dropdown-item.danger:hover {
  background: rgba(239, 68, 68, 0.1);
}

.dropdown-icon {
  font-size: 16px;
}

.dropdown-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
  margin: 4px 0;
}

/* Dropdown Animation */
.dropdown-fade-enter-active,
.dropdown-fade-leave-active {
  transition: all 0.2s ease;
}

.dropdown-fade-enter-from,
.dropdown-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

/* Main Content */
.main-content {
  min-height: calc(100vh - 72px);
}

.main-content.no-navbar {
  min-height: 100vh;
}

/* Responsive */
@media (max-width: 968px) {
  .nav-container {
    padding: 0 20px;
  }

  .nav-links {
    gap: 4px;
  }

  .nav-link span {
    display: none;
  }

  .user-badge {
    padding: 10px;
  }

  .user-name {
    display: none;
  }

  .brand-text {
    font-size: 20px;
  }

  .brand-icon-small {
    width: 36px;
    height: 36px;
  }
}

@media (max-width: 640px) {
  .nav-container {
    padding: 0 16px;
  }

  .brand-link {
    gap: 8px;
  }

  .brand-text {
    font-size: 18px;
  }

  .brand-icon-small {
    width: 32px;
    height: 32px;
  }

  .nav-links {
    gap: 2px;
  }

  .nav-link {
    padding: 8px 12px;
  }

  .dropdown-menu {
    min-width: 180px;
  }
}
</style>