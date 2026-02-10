<template>
  <div class="shop-container">
    <!-- Animated Background -->
    <div class="bg-gradient"></div>
    <div class="noise-overlay"></div>
    
    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Header -->
      <header class="page-header">
        <div class="header-top">
          <button class="back-btn" @click="goBack">
            <span>←</span>
          </button>
          <h1 class="page-title">
            <span class="title-icon">🛒</span>
            Playmate Shop
          </h1>
          <button class="sell-btn" @click="openSellModal">
            <span class="sell-icon">+</span>
            <span>Jual</span>
          </button>
        </div>
        <p class="page-subtitle">Jual beli peralatan olahraga antar sesama pemain</p>
      </header>

      <!-- Filter Section -->
      <section class="filter-section">
        <div class="filter-scroll">
          <button
            v-for="category in categories"
            :key="category.id"
            class="filter-btn"
            :class="{ active: selectedCategory === category.id }"
            @click="selectCategory(category.id)"
          >
            <span class="filter-emoji">{{ category.icon }}</span>
            <span class="filter-label">{{ category.name }}</span>
          </button>
        </div>

        <!-- Sort & Condition Filter -->
        <div class="sub-filters">
          <select v-model="selectedCondition" class="condition-filter">
            <option value="all">Semua Kondisi</option>
            <option value="new">Baru</option>
            <option value="used">Bekas</option>
          </select>
          <select v-model="sortBy" class="sort-filter">
            <option value="newest">Terbaru</option>
            <option value="price_low">Harga Terendah</option>
            <option value="price_high">Harga Tertinggi</option>
          </select>
        </div>
      </section>

      <!-- Products Grid -->
      <section class="products-section">
        <div class="products-grid">
          <div
            v-for="(product, index) in filteredProducts"
            :key="product.id"
            class="product-card"
            :style="{ animationDelay: `${index * 0.05}s` }"
            @click="viewProduct(product)"
          >
            <!-- Product Image -->
            <div class="product-image-wrapper">
              <img :src="product.image" :alt="product.name" class="product-image">
              <div class="image-overlay"></div>
              
              <!-- Badges -->
              <div class="product-badges">
                <span class="badge condition-badge" :class="product.condition">
                  {{ product.condition === 'new' ? '✨ Baru' : '♻️ Bekas' }}
                </span>
              </div>

              <!-- Favorite Button -->
              <button class="favorite-btn" @click.stop="toggleFavorite(product.id)">
                <span v-if="product.isFavorite">❤️</span>
                <span v-else>🤍</span>
              </button>
            </div>

            <!-- Product Info -->
            <div class="product-info">
              <h3 class="product-name">{{ product.name }}</h3>
              
              <!-- Price -->
              <div class="product-price">
                <span class="price-current">Rp {{ formatPrice(product.price) }}</span>
                <span v-if="product.originalPrice" class="price-original">
                  Rp {{ formatPrice(product.originalPrice) }}
                </span>
              </div>

              <!-- Seller Info -->
              <div class="seller-info">
                <img :src="product.seller.avatar" :alt="product.seller.name" class="seller-avatar">
                <div class="seller-details">
                  <span class="seller-name">{{ product.seller.name }}</span>
                  <div class="seller-meta">
                    <span class="seller-rating">
                      <span class="rating-icon">⭐</span>
                      {{ product.seller.rating }}
                    </span>
                    <span class="separator">•</span>
                    <span class="seller-location">{{ product.seller.location }}</span>
                  </div>
                </div>
              </div>

              <!-- Product Footer -->
              <div class="product-footer">
                <div class="product-meta">
                  <span class="meta-item">
                    <span class="meta-icon">👁️</span>
                    {{ product.views }}
                  </span>
                  <span class="meta-item">
                    <span class="meta-icon">⏰</span>
                    {{ product.postedTime }}
                  </span>
                </div>
                <button class="chat-btn" @click.stop="chatSeller(product.seller)">
                  <span class="chat-icon">💬</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredProducts.length === 0" class="empty-state">
          <div class="empty-icon">📦</div>
          <h3 class="empty-title">Tidak Ada Produk</h3>
          <p class="empty-description">Belum ada produk di kategori ini</p>
        </div>
      </section>
    </div>

    <!-- Floating Action Button -->
    <button class="fab" @click="openSellModal">
      <span class="fab-icon">+</span>
    </button>
  </div>
</template>

<script>
export default {
  name: "Shop",
  data() {
    return {
      selectedCategory: 'all',
      selectedCondition: 'all',
      sortBy: 'newest',
      categories: [
        { id: 'all', name: 'Semua', icon: '🏪' },
        { id: 'racket', name: 'Raket', icon: '🎾' },
        { id: 'shoes', name: 'Sepatu', icon: '👟' },
        { id: 'apparel', name: 'Pakaian', icon: '👕' },
        { id: 'ball', name: 'Bola', icon: '⚽' },
        { id: 'accessories', name: 'Aksesoris', icon: '🎒' }
      ],
      products: [
        {
          id: 1,
          name: 'Raket Badminton Yonex Astrox 99',
          price: 2500000,
          originalPrice: 3200000,
          condition: 'used',
          category: 'racket',
          image: 'https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=400&h=400&fit=crop',
          seller: {
            name: 'Budi Santoso',
            avatar: 'https://i.pravatar.cc/80?img=12',
            rating: 4.8,
            location: 'Medan Selatan'
          },
          views: 245,
          postedTime: '2 jam lalu',
          isFavorite: false
        },
        {
          id: 2,
          name: 'Sepatu Futsal Nike Mercurial',
          price: 850000,
          originalPrice: null,
          condition: 'new',
          category: 'shoes',
          image: 'https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=400&h=400&fit=crop',
          seller: {
            name: 'Andi Wijaya',
            avatar: 'https://i.pravatar.cc/80?img=33',
            rating: 4.9,
            location: 'Medan Utara'
          },
          views: 128,
          postedTime: '5 jam lalu',
          isFavorite: false
        },
        {
          id: 3,
          name: 'Jersey Basket NBA Original',
          price: 450000,
          originalPrice: 600000,
          condition: 'used',
          category: 'apparel',
          image: 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=400&h=400&fit=crop',
          seller: {
            name: 'Dewi Lestari',
            avatar: 'https://i.pravatar.cc/80?img=5',
            rating: 4.7,
            location: 'Medan Barat'
          },
          views: 89,
          postedTime: '1 hari lalu',
          isFavorite: true
        },
        {
          id: 4,
          name: 'Bola Futsal Mikasa Original',
          price: 350000,
          originalPrice: null,
          condition: 'new',
          category: 'ball',
          image: 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=400&h=400&fit=crop',
          seller: {
            name: 'Rudi Hartono',
            avatar: 'https://i.pravatar.cc/80?img=51',
            rating: 4.6,
            location: 'Medan Timur'
          },
          views: 156,
          postedTime: '3 jam lalu',
          isFavorite: false
        },
        {
          id: 5,
          name: 'Raket Tenis Wilson Pro Staff',
          price: 1800000,
          originalPrice: 2500000,
          condition: 'used',
          category: 'racket',
          image: 'https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=400&h=400&fit=crop',
          seller: {
            name: 'Siti Nurhaliza',
            avatar: 'https://i.pravatar.cc/80?img=47',
            rating: 4.9,
            location: 'Medan Selatan'
          },
          views: 203,
          postedTime: '6 jam lalu',
          isFavorite: false
        },
        {
          id: 6,
          name: 'Tas Olahraga Adidas',
          price: 280000,
          originalPrice: null,
          condition: 'new',
          category: 'accessories',
          image: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=400&fit=crop',
          seller: {
            name: 'Ahmad Yani',
            avatar: 'https://i.pravatar.cc/80?img=68',
            rating: 4.5,
            location: 'Medan Utara'
          },
          views: 67,
          postedTime: '4 jam lalu',
          isFavorite: false
        },
        {
          id: 7,
          name: 'Sepatu Badminton Li-Ning',
          price: 650000,
          originalPrice: 900000,
          condition: 'used',
          category: 'shoes',
          image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop',
          seller: {
            name: 'Maya Sari',
            avatar: 'https://i.pravatar.cc/80?img=9',
            rating: 4.8,
            location: 'Medan Barat'
          },
          views: 142,
          postedTime: '1 hari lalu',
          isFavorite: false
        },
        {
          id: 8,
          name: 'Kaos Olahraga Under Armour',
          price: 180000,
          originalPrice: null,
          condition: 'new',
          category: 'apparel',
          image: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&h=400&fit=crop',
          seller: {
            name: 'Eko Prasetyo',
            avatar: 'https://i.pravatar.cc/80?img=15',
            rating: 4.7,
            location: 'Medan Timur'
          },
          views: 98,
          postedTime: '8 jam lalu',
          isFavorite: true
        }
      ]
    };
  },
  computed: {
    filteredProducts() {
      let filtered = [...this.products];

      // Filter by category
      if (this.selectedCategory !== 'all') {
        filtered = filtered.filter(p => p.category === this.selectedCategory);
      }

      // Filter by condition
      if (this.selectedCondition !== 'all') {
        filtered = filtered.filter(p => p.condition === this.selectedCondition);
      }

      // Sort
      if (this.sortBy === 'price_low') {
        filtered.sort((a, b) => a.price - b.price);
      } else if (this.sortBy === 'price_high') {
        filtered.sort((a, b) => b.price - a.price);
      }

      return filtered;
    }
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    selectCategory(categoryId) {
      this.selectedCategory = categoryId;
    },
    formatPrice(price) {
      return price.toLocaleString('id-ID');
    },
    toggleFavorite(productId) {
      const product = this.products.find(p => p.id === productId);
      if (product) {
        product.isFavorite = !product.isFavorite;
      }
    },
    viewProduct(product) {
      console.log('View product:', product);
      alert(`Detail produk: ${product.name}\n\nFitur detail produk akan segera hadir!`);
    },
    chatSeller(seller) {
      console.log('Chat with:', seller);
      alert(`Chat dengan ${seller.name}\n\nFitur chat akan segera hadir!`);
    },
    openSellModal() {
      alert('Fitur jual produk akan segera hadir!\n\nAnda bisa:\n- Upload foto produk\n- Tentukan harga\n- Pilih kondisi (Baru/Bekas)\n- Tambahkan deskripsi');
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.shop-container {
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
  font-family: 'DM Sans', sans-serif;
  background: #0a0a0a;
  padding-bottom: 40px;
}

.bg-gradient {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 30%, rgba(255, 195, 113, 0.12) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(78, 205, 196, 0.12) 0%, transparent 50%),
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

.content-wrapper {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* Header */
.page-header {
  margin-bottom: 28px;
  animation: fadeInDown 0.6s ease;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.back-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #fff;
  font-size: 20px;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(-2px);
}

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 26px;
  font-weight: 700;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  font-size: 28px;
}

.sell-btn {
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  border: none;
  border-radius: 12px;
  padding: 10px 18px;
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
}

.sell-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(255, 107, 107, 0.4);
}

.sell-icon {
  font-size: 18px;
  font-weight: 700;
}

.page-subtitle {
  font-size: 14px;
  color: #999;
  text-align: center;
}

/* Filter Section */
.filter-section {
  margin-bottom: 28px;
  animation: fadeInUp 0.8s ease;
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

.filter-scroll {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  padding-bottom: 8px;
  margin-bottom: 12px;
  scrollbar-width: none;
}

.filter-scroll::-webkit-scrollbar {
  display: none;
}

.filter-btn {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 10px 18px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #999;
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
}

.filter-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 195, 113, 0.3);
}

.filter-btn.active {
  background: linear-gradient(135deg, rgba(255, 195, 113, 0.2) 0%, rgba(255, 195, 113, 0.1) 100%);
  border-color: rgba(255, 195, 113, 0.5);
  color: #ffc371;
}

.filter-emoji {
  font-size: 18px;
}

/* Sub Filters */
.sub-filters {
  display: flex;
  gap: 10px;
}

.condition-filter,
.sort-filter {
  flex: 1;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 10px;
  padding: 10px 14px;
  color: #fff;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.condition-filter:hover,
.sort-filter:hover {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.15);
}

.condition-filter option,
.sort-filter option {
  background: #1a1a1a;
  color: #fff;
}

/* Products Grid */
.products-section {
  animation: fadeInUp 0.8s ease 0.2s both;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 20px;
}

/* Product Card */
.product-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  animation: fadeInScale 0.6s ease both;
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.product-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255, 195, 113, 0.3);
  box-shadow: 0 12px 32px rgba(255, 195, 113, 0.15);
}

/* Product Image */
.product-image-wrapper {
  position: relative;
  height: 220px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}

.product-card:hover .product-image {
  transform: scale(1.1);
}

.image-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(10,10,10,0.4) 100%);
  z-index: 1;
}

/* Product Badges */
.product-badges {
  position: absolute;
  top: 12px;
  left: 12px;
  z-index: 2;
}

.condition-badge {
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.condition-badge.new {
  background: rgba(34, 197, 94, 0.85);
  color: white;
  border-color: rgba(34, 197, 94, 0.4);
}

.condition-badge.used {
  background: rgba(59, 130, 246, 0.85);
  color: white;
  border-color: rgba(59, 130, 246, 0.4);
}

/* Favorite Button */
.favorite-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 2;
  font-size: 18px;
}

.favorite-btn:hover {
  transform: scale(1.1);
  background: rgba(0, 0, 0, 0.8);
}

/* Product Info */
.product-info {
  padding: 16px;
}

.product-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 10px;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Price */
.product-price {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 14px;
}

.price-current {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: #ffc371;
}

.price-original {
  font-size: 13px;
  color: #666;
  text-decoration: line-through;
}

/* Seller Info */
.seller-info {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.seller-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.seller-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.seller-name {
  font-size: 13px;
  font-weight: 600;
  color: #fff;
}

.seller-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  color: #999;
}

.seller-rating {
  display: flex;
  align-items: center;
  gap: 3px;
  color: #ffc371;
}

.rating-icon {
  font-size: 12px;
}

.separator {
  color: #666;
}

.seller-location {
  font-weight: 500;
}

/* Product Footer */
.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.product-meta {
  display: flex;
  gap: 12px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #999;
  font-weight: 500;
}

.meta-icon {
  font-size: 13px;
}

.chat-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(78, 205, 196, 0.2) 0%, rgba(78, 205, 196, 0.1) 100%);
  border: 1px solid rgba(78, 205, 196, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.chat-btn:hover {
  transform: scale(1.1);
  background: linear-gradient(135deg, rgba(78, 205, 196, 0.3) 0%, rgba(78, 205, 196, 0.2) 100%);
}

.chat-icon {
  font-size: 16px;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  animation: fadeInUp 0.8s ease;
}

.empty-icon {
  font-size: 72px;
  margin-bottom: 20px;
  opacity: 0.3;
}

.empty-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #fff;
  margin-bottom: 8px;
}

.empty-description {
  font-size: 14px;
  color: #666;
}

/* Floating Action Button */
.fab {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #ff6b6b 0%, #ff8e53 100%);
  border: none;
  box-shadow: 0 8px 24px rgba(255, 107, 107, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fab:hover {
  transform: scale(1.1) rotate(90deg);
  box-shadow: 0 12px 32px rgba(255, 107, 107, 0.5);
}

.fab-icon {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
}

/* Responsive */
@media (min-width: 768px) {
  .content-wrapper {
    padding: 32px;
  }

  .page-title {
    font-size: 32px;
  }

  .title-icon {
    font-size: 34px;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 24px;
  }

  .product-image-wrapper {
    height: 240px;
  }

  .fab {
    display: none;
  }
}

@media (min-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  }

  .page-title {
    font-size: 36px;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: 16px;
  }

  .page-title {
    font-size: 22px;
  }

  .title-icon {
    font-size: 24px;
  }

  .sell-btn {
    padding: 8px 14px;
    font-size: 13px;
  }

  .products-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .product-image-wrapper {
    height: 160px;
  }

  .product-info {
    padding: 12px;
  }

  .product-name {
    font-size: 14px;
  }

  .price-current {
    font-size: 16px;
  }

  .sub-filters {
    flex-direction: column;
  }
}
</style>