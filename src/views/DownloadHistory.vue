<template>
    <div class="main">
      <!-- 输入bvid -->
      <div class="search-container">
        <input 
          type="text" 
          v-model="bvid" 
          class="search-input" 
          placeholder="输入视频BV号下载"
        >
        <button class="search-btn" @click="downloadVideo">
          <svg t="1747638731887" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="3107" width="20" height="20"><path d="M102.760931 509.188218c0-2.556166 0.511233-5.112332 1.533699-7.668498-0.511233 2.044933-1.022466 4.601098-1.533699 7.668498zM116.052993 482.604094l-1.5337 1.533699 1.5337-1.533699z" p-id="3108" fill="#ffffff"></path><path d="M511.236218 1.533699C229.035519 1.533699 0.003067 230.566151 0.003067 512.76685s229.032451 511.23315 511.233151 511.23315 511.23315-229.032451 511.23315-511.23315S793.436917 1.533699 511.236218 1.533699z m0 940.668997c-237.212182 0-429.435846-192.223665-429.435847-429.435846s192.223665-429.435846 429.435847-429.435847 429.435846 192.223665 429.435846 429.435847-192.223665 429.435846-429.435846 429.435846z" p-id="3109" fill="#ffffff"></path><path d="M655.403966 548.55317l-115.538692 115.538692c-1.022466 1.022466-2.044933 1.533699-3.067399 2.556166-1.022466 0.511233-1.533699 1.533699-2.556166 2.044933h-0.511233c-0.511233 0-0.511233 0.511233-1.022466 0.511233-0.511233 0.511233-1.533699 1.022466-2.556166 1.533699l-0.511233 0.511233c-1.022466 0.511233-2.044933 1.022466-3.578632 1.5337-1.022466 0.511233-2.044933 1.022466-3.067399 1.022466h-0.511233c-1.022466 0.511233-2.556166 0.511233-3.578632 1.022466-1.533699 0.511233-2.556166 0.511233-4.089865 0.511234h-8.179731c-1.533699 0-2.556166-0.511233-4.089865-0.511234s-2.556166-0.511233-3.578632-1.022466h-0.511233c-1.022466-0.511233-2.044933-1.022466-3.067399-1.022466-1.022466-0.511233-2.556166-1.022466-3.578632-1.5337 0 0-0.511233 0-0.511233-0.511233-1.022466-0.511233-1.533699-1.022466-2.556166-1.533699-0.511233 0-0.511233-0.511233-1.022466-0.511233h-0.511233c-1.022466-0.511233-1.533699-1.533699-2.556166-2.044933-1.022466-1.022466-2.044933-1.533699-3.067399-2.556166l-115.538692-115.538692c-15.848228-15.848228-15.848228-41.921118 0-57.769346 8.17973-8.17973 18.404393-11.758362 29.14029-11.758362 10.224663 0 20.960559 4.089865 29.140289 11.758362l46.010984 46.010984V267.374938c0-22.494259 18.404393-40.898652 40.898652-40.898652 11.247129 0 21.471792 4.601098 29.140289 11.758362 7.157264 7.668497 11.758362 17.89316 11.758363 29.14029V536.794808l46.010983-46.010984c15.848228-15.848228 41.921118-15.848228 57.769346 0 15.848228 15.848228 15.848228 41.921118-0.511233 57.769346z m19.42686 250.504244h-327.189216c-22.494259 0-40.898652-18.404393-40.898652-40.898652s18.404393-40.898652 40.898652-40.898652h327.189216c22.494259 0 40.898652 18.404393 40.898652 40.898652s-18.404393 40.898652-40.898652 40.898652z" p-id="3110" fill="#ffffff"></path></svg>
        </button>
      </div>
      <Loading v-if="isLoading" />
      <div v-if="videoStore.videoMap!=null" class="videoList">
        <div v-for="[bvid, path] in videoStore.videoMap.entries()" :key="bvid">
          <Video :bvid="bvid" :local-path="path"></Video>
        </div>
    </div>
    </div>
  </template>
  <script setup lang="ts">
  import { ref } from "vue";
  import axios from "axios";
  import Loading from '../components/loading.vue';
  import Video from '../components/video.vue';
  import useVideoStore from "../stores/video";
  const videoStore = useVideoStore();
  let bvid = ref(""); 
  let isLoading = ref(false); 
  async function downloadVideo() {
    isLoading.value = true;
    console.log(bvid.value)
    try {
      // 1. 触发视频处理
      const response = await axios.post(
        'http://localhost:5000/api/video',
        { 
          bvid: bvid.value
         },
      );
      console.log(response)
      let local = response.data.download_url.replace(/\\/g, '/') // 将反斜杠替换为斜杠
      videoStore.videoMap.set(bvid.value, local);
      bvid.value = "";
      return response.data;
    } catch (error) {
      console.error('视频处理失败:', error);
      throw error;
    } finally {
      isLoading.value = false;
    }
  }
  
  </script>
  <style scoped>
  .main {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  header {
    line-height: 1.5;
    max-height: 100vh;
  }
  .videoList{
    display: flex;
  }
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
  .logo {
    display: block;
    margin: 0 auto 2rem;
  }
  
  nav {
    width: 100%;
    font-size: 12px;
    text-align: center;
    margin-top: 2rem;
  }
  
  nav a.router-link-exact-active {
    color: var(--color-text);
  }
  
  nav a.router-link-exact-active:hover {
    background-color: transparent;
  }
  
  nav a {
    display: inline-block;
    padding: 0 1rem;
    border-left: 1px solid var(--color-border);
  }
  
  nav a:first-of-type {
    border: 0;
  }
  
  @media (min-width: 1024px) {
    header {
      display: flex;
      place-items: center;
      padding-right: calc(var(--section-gap) / 2);
    }
  
    .logo {
      margin: 0 2rem 0 0;
    }
  
    header .wrapper {
      display: flex;
      place-items: flex-start;
      flex-wrap: wrap;
    }
  
    nav {
      text-align: left;
      margin-left: -1rem;
      font-size: 1rem;
  
      padding: 1rem 0;
      margin-top: 1rem;
    }
  }
  </style>