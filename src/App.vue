<template>
  <div>
    <div class="nav-container">
      <button 
        class="nav-btn" 
        @click="toDownloadHistory"
        :class="{ 'active': $route.path === '/downloadHistory' }"
      >
        下载历史
      </button>
      <button 
        class="nav-btn" 
        @click="toSearch"
        :class="{ 'active': $route.path === '/Search' }"
      >
        搜索
      </button>
    </div>
    <router-view></router-view>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import router from './router';

const route = useRoute();

const toDownloadHistory = () => {
  router.push('/downloadHistory');
};

const toSearch = () => {
  router.push('/Search');
};
</script>

<style scoped>
.nav-container {
  display: flex;
  justify-content: center;
  padding: 16px 0;
  background-color: #f4f5f6;
  border-bottom: 1px solid #e7e7e7;
}

.nav-btn {
  padding: 8px 16px;
  margin: 0 8px;
  border: none;
  border-radius: 4px;
  background-color: #fff;
  color: #212121;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s;
}

.nav-btn:hover {
  background-color: #f0f0f0;
}

.nav-btn.active {
  background-color: #00a1d6;
  color: #fff;
}
</style>