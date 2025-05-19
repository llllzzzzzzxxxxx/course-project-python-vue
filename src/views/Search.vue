<template>
    <div>
        <div class="search-container">
        <input 
          type="text" 
          v-model="keywords" 
          class="search-input" 
          placeholder="请输入关键词"
        >
        <button class="search-btn" @click="search(keywords,1)">
          <svg t="1747652624424" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4988" width="20" height="20"><path d="M446.112323 177.545051c137.567677 0.219798 252.612525 104.59798 266.162424 241.493333 13.562828 136.895354-78.778182 261.818182-213.617777 289.008485-134.852525 27.203232-268.386263-52.156768-308.945455-183.608889s25.018182-272.252121 151.738182-325.779394A267.235556 267.235556 0 0 1 446.112323 177.545051m0-62.060607c-182.794343 0-330.989899 148.195556-330.989899 330.989899s148.195556 330.989899 330.989899 330.989899 330.989899-148.195556 330.989899-330.989899-148.195556-330.989899-330.989899-330.989899z m431.321212 793.341415a30.849293 30.849293 0 0 1-21.94101-9.102223l-157.220202-157.220202c-11.752727-12.179394-11.584646-31.534545 0.37495-43.50707 11.972525-11.972525 31.327677-12.140606 43.494141-0.37495l157.220202 157.220202a31.036768 31.036768 0 0 1 6.723232 33.810101 31.004444 31.004444 0 0 1-28.651313 19.174142z m0 0" p-id="4989" fill="#ffffff"/></svg>
        </button>
      </div>
    </div>
    <div class="search-content" v-if="videos != null">
      <div v-if="isLoading" class="loading">加载中...</div>
      <div v-else class="video-list">
          <div v-for="video in videos" :key="video.bvid ">
            <Video :bvid="video.bvid"></Video>
          </div>
      </div>
      <div class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">上一页</button>
        <span class="pageNum">{{ currentPage }} / {{ totalPages }}</span>
        <button @click="nextPage" :disabled="currentPage === totalPages">下一页</button>
      </div>
    </div>
    <div v-else>
      <el-empty description="description" />
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";
import Video from '../components/video.vue';

let keywords = ref("");
const videos = ref([]);
const isLoading = ref(false); 

const currentPage = ref(1);
const totalPages = ref(0);
const search = async (keywords: string, page: number) => {
  isLoading.value = true;
  try {
    const response = await axios.get(
      `http://127.0.0.1:5000/api/search/${keywords}/${page}`
    );
    // console.log(response.data.data)
    if (response.data.code === 0) {
      const videoResult = response.data.data.result.find((item: { result_type: string; }) => item?.result_type === 'video');
      videos.value = videoResult ? videoResult.data.map((video: { bvid: any; }) => ({ bvid: video.bvid })) : [];
      console.log(videos.value)
      totalPages.value = response.data.data.result.length;
      currentPage.value = page;
    }
  } catch (error) {
    console.error('搜索失败:', error);
  } finally {
    isLoading.value = false;
  }
}
const prevPage = () => {
  if (currentPage.value > 1) {
    search(keywords.value, currentPage.value - 1);
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    search(keywords.value, currentPage.value + 1);
  }
}
</script>

<style scoped>
.search-container {
  display: flex;
    justify-content: center;
    align-items: center;
    margin: 16px 0; 
}
.search-input {
    padding: 8px 16px;
    border: 1px solid #ccc;
    border-radius: 20px 0 0 20px;
    outline: none;
    font-size: 14px;
    width: 300px;
  }
  .search-input:focus {
    border-color: #00a1d6;
  }
  .search-btn {
    background: #00a1d6;
    border: none;
    border-radius: 0 20px 20px 0;
    padding: 8px 16px;
    cursor: pointer;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .search-btn:hover {
    background: #00b5e5;
  }
  .search-icon {
    width: 16px;
    height: 16px;
  }
  
  .pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px 0;
    gap: 20px;
  }
  .pageNum {
    font-size: 14px;
    color: #333; 
  }
  .pagination button {
    padding: 8px 16px;
    border: 1px solid #00a1d6;
    background: rgb(246, 244, 244);
    color: #00a1d6;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .pagination button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
  .pagination button:hover:not(:disabled) {
    background: #00a1d6;
    color: white;
  }
  .logo {
    display: block;
    margin: 0 auto 2rem;
  }
  .search-content {
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
  }
  .video-list {
   display: inline-flex;
   flex-wrap: wrap;
   gap: 20px;
   margin: 20px 30px;
  }
</style>