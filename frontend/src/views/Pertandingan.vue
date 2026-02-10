<template>
  <div class="match-container">
    <!-- Animated Background -->
    <div class="bg-gradient"></div>
    <div class="noise-overlay"></div>
    
    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Header -->
      <header class="page-header">
        <button class="back-btn" @click="goBack">
          <span>←</span>
        </button>
        <div class="header-info">
          <h1 class="page-title">
            <span class="title-icon">🏸</span>
            Pertandingan
          </h1>
          <p class="page-subtitle">Badminton Ganda - Round Robin</p>
        </div>
        <div class="header-spacer"></div>
      </header>

      <!-- Team Selector -->
      <section class="team-selector">
        <div class="selector-label">Pilih Pasangan:</div>
        <div class="team-scroll">
          <button
            v-for="team in teams"
            :key="team.id"
            class="team-btn"
            :class="{ active: selectedTeam === team.id }"
            @click="selectTeam(team.id)"
          >
            <div class="team-avatars">
              <img :src="team.player1.avatar" :alt="team.player1.name" class="team-avatar">
              <img :src="team.player2.avatar" :alt="team.player2.name" class="team-avatar">
            </div>
            <div class="team-info">
              <div class="team-names">{{ team.player1.name }} & {{ team.player2.name }}</div>
              <div class="team-record">{{ team.wins }}W - {{ team.losses }}L</div>
            </div>
          </button>
        </div>
      </section>

      <!-- Match Statistics -->
      <section class="stats-section">
        <div class="stat-card wins">
          <div class="stat-icon">🏆</div>
          <div class="stat-info">
            <div class="stat-value">{{ currentTeam.wins }}</div>
            <div class="stat-label">Menang</div>
          </div>
        </div>
        <div class="stat-card losses">
          <div class="stat-icon">❌</div>
          <div class="stat-info">
            <div class="stat-value">{{ currentTeam.losses }}</div>
            <div class="stat-label">Kalah</div>
          </div>
        </div>
        <div class="stat-card points">
          <div class="stat-icon">⚡</div>
          <div class="stat-info">
            <div class="stat-value">{{ currentTeam.totalPoints }}</div>
            <div class="stat-label">Total Poin</div>
          </div>
        </div>
      </section>

      <!-- Matches List -->
      <section class="matches-section">
        <div class="section-header">
          <h2 class="section-title">Jadwal Pertandingan (4 Match)</h2>
        </div>

        <div
          v-for="(match, index) in currentMatches"
          :key="index"
          class="match-card"
          :class="{ completed: match.status === 'completed', live: match.status === 'live', upcoming: match.status === 'upcoming' }"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <!-- Match Header -->
          <div class="match-header">
            <div class="match-number">Match {{ index + 1 }}</div>
            <div class="match-status" :class="match.status">
              {{ getStatusText(match.status) }}
            </div>
          </div>

          <!-- Match Info -->
          <div class="match-info">
            <div class="match-datetime">
              <span class="datetime-icon">📅</span>
              <span>{{ match.date }}</span>
              <span class="separator">•</span>
              <span class="datetime-icon">⏰</span>
              <span>{{ match.time }}</span>
            </div>
            <div class="match-court">
              <span class="court-icon">🏟️</span>
              <span>{{ match.court }}</span>
            </div>
          </div>

          <!-- Match Score -->
          <div class="match-score">
            <!-- Team 1 (Current Team) -->
            <div class="team-score" :class="{ winner: match.winner === 'team1' }">
              <div class="team-players">
                <div class="player-avatars">
                  <img :src="match.team1.player1.avatar" :alt="match.team1.player1.name" class="player-avatar">
                  <img :src="match.team1.player2.avatar" :alt="match.team1.player2.name" class="player-avatar">
                </div>
                <div class="player-names">
                  <div class="player-name">{{ match.team1.player1.name }}</div>
                  <div class="player-name">{{ match.team1.player2.name }}</div>
                </div>
              </div>
              <div class="score-sets">
                <div
                  v-for="(set, setIndex) in match.team1.sets"
                  :key="setIndex"
                  class="set-score"
                  :class="{ won: set > match.team2.sets[setIndex] }"
                >
                  {{ set }}
                </div>
              </div>
              <div v-if="match.status === 'completed'" class="winner-badge" v-show="match.winner === 'team1'">
                👑
              </div>
            </div>

            <!-- VS Divider -->
            <div class="vs-divider">
              <span>VS</span>
            </div>

            <!-- Team 2 (Opponent) -->
            <div class="team-score" :class="{ winner: match.winner === 'team2' }">
              <div class="team-players">
                <div class="player-avatars">
                  <img :src="match.team2.player1.avatar" :alt="match.team2.player1.name" class="player-avatar">
                  <img :src="match.team2.player2.avatar" :alt="match.team2.player2.name" class="player-avatar">
                </div>
                <div class="player-names">
                  <div class="player-name">{{ match.team2.player1.name }}</div>
                  <div class="player-name">{{ match.team2.player2.name }}</div>
                </div>
              </div>
              <div class="score-sets">
                <div
                  v-for="(set, setIndex) in match.team2.sets"
                  :key="setIndex"
                  class="set-score"
                  :class="{ won: set > match.team1.sets[setIndex] }"
                >
                  {{ set }}
                </div>
              </div>
              <div v-if="match.status === 'completed'" class="winner-badge" v-show="match.winner === 'team2'">
                👑
              </div>
            </div>
          </div>

          <!-- Match Result Summary -->
          <div v-if="match.status === 'completed'" class="match-result">
            <div class="result-icon" :class="{ win: match.winner === 'team1', loss: match.winner === 'team2' }">
              {{ match.winner === 'team1' ? '✓ MENANG' : '✗ KALAH' }}
            </div>
            <div class="result-score">{{ match.team1.setsWon }} - {{ match.team2.setsWon }}</div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
export default {
  name: "Match",
  data() {
    return {
      selectedTeam: 1,
      teams: [
        {
          id: 1,
          player1: { name: 'Kevin', avatar: 'https://i.pravatar.cc/80?img=12' },
          player2: { name: 'Marcus', avatar: 'https://i.pravatar.cc/80?img=13' },
          wins: 3,
          losses: 1,
          totalPoints: 285
        },
        {
          id: 2,
          player1: { name: 'Greysia', avatar: 'https://i.pravatar.cc/80?img=5' },
          player2: { name: 'Apriyani', avatar: 'https://i.pravatar.cc/80?img=9' },
          wins: 2,
          losses: 2,
          totalPoints: 248
        },
        {
          id: 3,
          player1: { name: 'Fajar', avatar: 'https://i.pravatar.cc/80?img=33' },
          player2: { name: 'Rian', avatar: 'https://i.pravatar.cc/80?img=15' },
          wins: 4,
          losses: 0,
          totalPoints: 312
        },
        {
          id: 4,
          player1: { name: 'Siti', avatar: 'https://i.pravatar.cc/80?img=47' },
          player2: { name: 'Ribka', avatar: 'https://i.pravatar.cc/80?img=44' },
          wins: 1,
          losses: 3,
          totalPoints: 198
        }
      ],
      matches: {
        1: [ // Team 1 matches
          {
            date: '10 Feb 2026',
            time: '09:00 WIB',
            court: 'Court A',
            status: 'completed',
            team1: {
              player1: { name: 'Kevin', avatar: 'https://i.pravatar.cc/80?img=12' },
              player2: { name: 'Marcus', avatar: 'https://i.pravatar.cc/80?img=13' },
              sets: [21, 19, 21],
              setsWon: 2
            },
            team2: {
              player1: { name: 'Budi', avatar: 'https://i.pravatar.cc/80?img=51' },
              player2: { name: 'Andi', avatar: 'https://i.pravatar.cc/80?img=52' },
              sets: [18, 21, 15],
              setsWon: 1
            },
            winner: 'team1'
          },
          {
            date: '10 Feb 2026',
            time: '11:30 WIB',
            court: 'Court B',
            status: 'completed',
            team1: {
              player1: { name: 'Kevin', avatar: 'https://i.pravatar.cc/80?img=12' },
              player2: { name: 'Marcus', avatar: 'https://i.pravatar.cc/80?img=13' },
              sets: [21, 21],
              setsWon: 2
            },
            team2: {
              player1: { name: 'Doni', avatar: 'https://i.pravatar.cc/80?img=60' },
              player2: { name: 'Rudi', avatar: 'https://i.pravatar.cc/80?img=61' },
              sets: [15, 17],
              setsWon: 0
            },
            winner: 'team1'
          },
          {
            date: '10 Feb 2026',
            time: '14:00 WIB',
            court: 'Court A',
            status: 'live',
            team1: {
              player1: { name: 'Kevin', avatar: 'https://i.pravatar.cc/80?img=12' },
              player2: { name: 'Marcus', avatar: 'https://i.pravatar.cc/80?img=13' },
              sets: [21, 12],
              setsWon: 1
            },
            team2: {
              player1: { name: 'Fajar', avatar: 'https://i.pravatar.cc/80?img=33' },
              player2: { name: 'Rian', avatar: 'https://i.pravatar.cc/80?img=15' },
              sets: [19, 21],
              setsWon: 1
            },
            winner: null
          },
          {
            date: '10 Feb 2026',
            time: '16:30 WIB',
            court: 'Court C',
            status: 'upcoming',
            team1: {
              player1: { name: 'Kevin', avatar: 'https://i.pravatar.cc/80?img=12' },
              player2: { name: 'Marcus', avatar: 'https://i.pravatar.cc/80?img=13' },
              sets: [0, 0],
              setsWon: 0
            },
            team2: {
              player1: { name: 'Hendra', avatar: 'https://i.pravatar.cc/80?img=68' },
              player2: { name: 'Ahsan', avatar: 'https://i.pravatar.cc/80?img=69' },
              sets: [0, 0],
              setsWon: 0
            },
            winner: null
          }
        ],
        2: [ // Team 2 matches
          {
            date: '10 Feb 2026',
            time: '09:00 WIB',
            court: 'Court C',
            status: 'completed',
            team1: {
              player1: { name: 'Greysia', avatar: 'https://i.pravatar.cc/80?img=5' },
              player2: { name: 'Apriyani', avatar: 'https://i.pravatar.cc/80?img=9' },
              sets: [21, 18, 19],
              setsWon: 1
            },
            team2: {
              player1: { name: 'Siti', avatar: 'https://i.pravatar.cc/80?img=47' },
              player2: { name: 'Ribka', avatar: 'https://i.pravatar.cc/80?img=44' },
              sets: [19, 21, 21],
              setsWon: 2
            },
            winner: 'team2'
          },
          {
            date: '10 Feb 2026',
            time: '11:30 WIB',
            court: 'Court A',
            status: 'completed',
            team1: {
              player1: { name: 'Greysia', avatar: 'https://i.pravatar.cc/80?img=5' },
              player2: { name: 'Apriyani', avatar: 'https://i.pravatar.cc/80?img=9' },
              sets: [21, 21],
              setsWon: 2
            },
            team2: {
              player1: { name: 'Linda', avatar: 'https://i.pravatar.cc/80?img=25' },
              player2: { name: 'Maya', avatar: 'https://i.pravatar.cc/80?img=26' },
              sets: [16, 18],
              setsWon: 0
            },
            winner: 'team1'
          },
          {
            date: '10 Feb 2026',
            time: '14:00 WIB',
            court: 'Court B',
            status: 'completed',
            team1: {
              player1: { name: 'Greysia', avatar: 'https://i.pravatar.cc/80?img=5' },
              player2: { name: 'Apriyani', avatar: 'https://i.pravatar.cc/80?img=9' },
              sets: [18, 21, 15],
              setsWon: 1
            },
            team2: {
              player1: { name: 'Fajar', avatar: 'https://i.pravatar.cc/80?img=33' },
              player2: { name: 'Rian', avatar: 'https://i.pravatar.cc/80?img=15' },
              sets: [21, 19, 21],
              setsWon: 2
            },
            winner: 'team2'
          },
          {
            date: '10 Feb 2026',
            time: '16:30 WIB',
            court: 'Court A',
            status: 'upcoming',
            team1: {
              player1: { name: 'Greysia', avatar: 'https://i.pravatar.cc/80?img=5' },
              player2: { name: 'Apriyani', avatar: 'https://i.pravatar.cc/80?img=9' },
              sets: [0, 0],
              setsWon: 0
            },
            team2: {
              player1: { name: 'Kevin', avatar: 'https://i.pravatar.cc/80?img=12' },
              player2: { name: 'Marcus', avatar: 'https://i.pravatar.cc/80?img=13' },
              sets: [0, 0],
              setsWon: 0
            },
            winner: null
          }
        ],
        3: [ // Team 3 matches
          {
            date: '10 Feb 2026',
            time: '09:00 WIB',
            court: 'Court B',
            status: 'completed',
            team1: {
              player1: { name: 'Fajar', avatar: 'https://i.pravatar.cc/80?img=33' },
              player2: { name: 'Rian', avatar: 'https://i.pravatar.cc/80?img=15' },
              sets: [21, 21],
              setsWon: 2
            },
            team2: {
              player1: { name: 'Budi', avatar: 'https://i.pravatar.cc/80?img=51' },
              player2: { name: 'Andi', avatar: 'https://i.pravatar.cc/80?img=52' },
              sets: [14, 19],
              setsWon: 0
            },
            winner: 'team1'
          },
          {
            date: '10 Feb 2026',
            time: '11:30 WIB',
            court: 'Court C',
            status: 'completed',
            team1: {
              player1: { name: 'Fajar', avatar: 'https://i.pravatar.cc/80?img=33' },
              player2: { name: 'Rian', avatar: 'https://i.pravatar.cc/80?img=15' },
              sets: [21, 21],
              setsWon: 2
            },
            team2: {
              player1: { name: 'Hendra', avatar: 'https://i.pravatar.cc/80?img=68' },
              player2: { name: 'Ahsan', avatar: 'https://i.pravatar.cc/80?img=69' },
              sets: [18, 16],
              setsWon: 0
            },
            winner: 'team1'
          },
          {
            date: '10 Feb 2026',
            time: '14:00 WIB',
            court: 'Court A',
            status: 'live',
            team1: {
              player1: { name: 'Fajar', avatar: 'https://i.pravatar.cc/80?img=33' },
              player2: { name: 'Rian', avatar: 'https://i.pravatar.cc/80?img=15' },
              sets: [19, 21],
              setsWon: 1
            },
            team2: {
              player1: { name: 'Kevin', avatar: 'https://i.pravatar.cc/80?img=12' },
              player2: { name: 'Marcus', avatar: 'https://i.pravatar.cc/80?img=13' },
              sets: [21, 12],
              setsWon: 1
            },
            winner: null
          },
          {
            date: '10 Feb 2026',
            time: '16:30 WIB',
            court: 'Court B',
            status: 'upcoming',
            team1: {
              player1: { name: 'Fajar', avatar: 'https://i.pravatar.cc/80?img=33' },
              player2: { name: 'Rian', avatar: 'https://i.pravatar.cc/80?img=15' },
              sets: [0, 0],
              setsWon: 0
            },
            team2: {
              player1: { name: 'Siti', avatar: 'https://i.pravatar.cc/80?img=47' },
              player2: { name: 'Ribka', avatar: 'https://i.pravatar.cc/80?img=44' },
              sets: [0, 0],
              setsWon: 0
            },
            winner: null
          }
        ],
        4: [ // Team 4 matches
          {
            date: '10 Feb 2026',
            time: '09:00 WIB',
            court: 'Court C',
            status: 'completed',
            team1: {
              player1: { name: 'Siti', avatar: 'https://i.pravatar.cc/80?img=47' },
              player2: { name: 'Ribka', avatar: 'https://i.pravatar.cc/80?img=44' },
              sets: [19, 21, 21],
              setsWon: 2
            },
            team2: {
              player1: { name: 'Greysia', avatar: 'https://i.pravatar.cc/80?img=5' },
              player2: { name: 'Apriyani', avatar: 'https://i.pravatar.cc/80?img=9' },
              sets: [21, 18, 19],
              setsWon: 1
            },
            winner: 'team1'
          },
          {
            date: '10 Feb 2026',
            time: '11:30 WIB',
            court: 'Court C',
            status: 'completed',
            team1: {
              player1: { name: 'Siti', avatar: 'https://i.pravatar.cc/80?img=47' },
              player2: { name: 'Ribka', avatar: 'https://i.pravatar.cc/80?img=44' },
              sets: [18, 15],
              setsWon: 0
            },
            team2: {
              player1: { name: 'Linda', avatar: 'https://i.pravatar.cc/80?img=25' },
              player2: { name: 'Maya', avatar: 'https://i.pravatar.cc/80?img=26' },
              sets: [21, 21],
              setsWon: 2
            },
            winner: 'team2'
          },
          {
            date: '10 Feb 2026',
            time: '14:00 WIB',
            court: 'Court C',
            status: 'completed',
            team1: {
              player1: { name: 'Siti', avatar: 'https://i.pravatar.cc/80?img=47' },
              player2: { name: 'Ribka', avatar: 'https://i.pravatar.cc/80?img=44' },
              sets: [15, 17],
              setsWon: 0
            },
            team2: {
              player1: { name: 'Budi', avatar: 'https://i.pravatar.cc/80?img=51' },
              player2: { name: 'Andi', avatar: 'https://i.pravatar.cc/80?img=52' },
              sets: [21, 21],
              setsWon: 2
            },
            winner: 'team2'
          },
          {
            date: '10 Feb 2026',
            time: '16:30 WIB',
            court: 'Court B',
            status: 'upcoming',
            team1: {
              player1: { name: 'Siti', avatar: 'https://i.pravatar.cc/80?img=47' },
              player2: { name: 'Ribka', avatar: 'https://i.pravatar.cc/80?img=44' },
              sets: [0, 0],
              setsWon: 0
            },
            team2: {
              player1: { name: 'Fajar', avatar: 'https://i.pravatar.cc/80?img=33' },
              player2: { name: 'Rian', avatar: 'https://i.pravatar.cc/80?img=15' },
              sets: [0, 0],
              setsWon: 0
            },
            winner: null
          }
        ]
      }
    };
  },
  computed: {
    currentTeam() {
      return this.teams.find(t => t.id === this.selectedTeam) || this.teams[0];
    },
    currentMatches() {
      return this.matches[this.selectedTeam] || [];
    }
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    selectTeam(teamId) {
      this.selectedTeam = teamId;
    },
    getStatusText(status) {
      const statusMap = {
        completed: 'Selesai',
        live: 'Live',
        upcoming: 'Akan Datang'
      };
      return statusMap[status] || status;
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

.match-container {
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
    radial-gradient(circle at 20% 30%, rgba(78, 205, 196, 0.12) 0%, transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(255, 107, 107, 0.12) 0%, transparent 50%),
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
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
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
  flex-shrink: 0;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateX(-2px);
}

.header-info {
  flex: 1;
  text-align: center;
}

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 4px;
}

.title-icon {
  font-size: 26px;
}

.page-subtitle {
  font-size: 13px;
  color: #999;
  font-weight: 500;
}

.header-spacer {
  width: 44px;
  flex-shrink: 0;
}

/* Team Selector */
.team-selector {
  margin-bottom: 24px;
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

.selector-label {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 12px;
}

.team-scroll {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.team-btn {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.team-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(78, 205, 196, 0.3);
}

.team-btn.active {
  background: linear-gradient(135deg, rgba(78, 205, 196, 0.15) 0%, rgba(78, 205, 196, 0.08) 100%);
  border-color: rgba(78, 205, 196, 0.4);
}

.team-avatars {
  display: flex;
  margin-left: -8px;
}

.team-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid #0a0a0a;
  margin-left: -8px;
}

.team-avatar:first-child {
  margin-left: 0;
}

.team-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.team-names {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
}

.team-record {
  font-size: 12px;
  color: #4ecdc4;
  font-weight: 500;
}

/* Stats Section */
.stats-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 28px;
  animation: fadeInUp 0.8s ease 0.2s both;
}

.stat-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 14px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.05);
}

.stat-card.wins {
  border-color: rgba(34, 197, 94, 0.3);
}

.stat-card.losses {
  border-color: rgba(239, 68, 68, 0.3);
}

.stat-card.points {
  border-color: rgba(255, 215, 0, 0.3);
}

.stat-icon {
  font-size: 24px;
}

.stat-info {
  text-align: center;
}

.stat-value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 24px;
  font-weight: 700;
  color: #fff;
}

.stat-label {
  font-size: 11px;
  color: #999;
  font-weight: 500;
}

/* Matches Section */
.matches-section {
  animation: fadeInUp 0.8s ease 0.4s both;
}

.section-header {
  margin-bottom: 20px;
}

.section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: #fff;
}

.match-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 18px;
  margin-bottom: 16px;
  transition: all 0.3s ease;
  animation: fadeInUp 0.8s ease both;
}

.match-card:hover {
  background: rgba(255, 255, 255, 0.05);
  transform: translateY(-2px);
}

.match-card.live {
  border-color: rgba(239, 68, 68, 0.5);
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.2);
}

.match-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.match-number {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: #4ecdc4;
}

.match-status {
  padding: 4px 10px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.match-status.completed {
  background: rgba(100, 100, 100, 0.2);
  color: #999;
}

.match-status.live {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.match-status.upcoming {
  background: rgba(139, 92, 246, 0.2);
  color: #a78bfa;
}

.match-info {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.match-datetime,
.match-court {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #ccc;
}

.datetime-icon,
.court-icon {
  font-size: 14px;
}

.separator {
  color: #666;
  margin: 0 4px;
}

.match-score {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.team-score {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.05);
  position: relative;
  transition: all 0.3s ease;
}

.team-score.winner {
  background: rgba(34, 197, 94, 0.08);
  border-color: rgba(34, 197, 94, 0.3);
}

.team-players {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.player-avatars {
  display: flex;
  margin-left: -6px;
}

.player-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid #0a0a0a;
  margin-left: -6px;
}

.player-avatar:first-child {
  margin-left: 0;
}

.player-names {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.player-name {
  font-size: 13px;
  font-weight: 600;
  color: #fff;
}

.score-sets {
  display: flex;
  gap: 8px;
}

.set-score {
  min-width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: #999;
}

.set-score.won {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
}

.winner-badge {
  position: absolute;
  right: 10px;
  font-size: 20px;
  animation: float 2s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-4px); }
}

.vs-divider {
  text-align: center;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 12px;
  font-weight: 700;
  color: #666;
  padding: 4px 0;
}

.match-result {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.result-icon {
  font-size: 13px;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 8px;
}

.result-icon.win {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
}

.result-icon.loss {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
}

.result-score {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: #fff;
}

/* Responsive */
@media (min-width: 768px) {
  .content-wrapper {
    max-width: 680px;
    padding: 32px;
  }

  .page-title {
    font-size: 28px;
  }

  .title-icon {
    font-size: 30px;
  }

  .team-btn {
    padding: 16px;
  }

  .team-avatar {
    width: 48px;
    height: 48px;
  }

  .team-names {
    font-size: 16px;
  }

  .match-card {
    padding: 24px;
  }

  .player-avatar {
    width: 40px;
    height: 40px;
  }

  .player-name {
    font-size: 14px;
  }
}

@media (min-width: 1024px) {
  .content-wrapper {
    max-width: 800px;
  }

  .page-title {
    font-size: 32px;
  }
}
</style>