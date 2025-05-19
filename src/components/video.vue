<template>
    <div class="video-card" @click="openVideo">
        <div v-if="loading" class="loading">加载中...</div>
        <div v-else-if="error" class="error">获取数据失败：{{ error }}</div>
        <div v-else class="content">
            <transition name="fade">
                <div v-if="showToast" class="toast">{{ toastMessage }}</div>
            </transition>
            <img class="pic" :src="getProxiedImageUrl(videoInfo?.pic)" />
            <h3 class="title">{{ videoInfo?.title }}</h3>
            <div class="info">
                <span class="up-name">up: {{ videoInfo?.owner?.name }}</span>
                <span class="view-count">时长：{{ formatDuration(videoInfo?.duration) }}</span>
                <!-- <span v-if="localPath" class="local-path">存储路径：{{ localPath }}</span> -->
            </div>
        </div>
    </div>
    <loadingComponet v-if="isLoadingDownload"></loadingComponet>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import useVideoStore from "../stores/video";
import loadingComponet from "./loading.vue";
const props = defineProps<{ 
  bvid: string;
  localPath?: string;
}>();
const loading = ref(false);
const error = ref(null);
const videoInfo = ref();
const imageError = ref(false);

const videoStore = useVideoStore();
const isLoadingDownload = ref(false);
const formatDuration = (seconds: number) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  const parts = hours > 0 
    ? [hours, minutes, secs]
    : [minutes, secs];
  return parts
    .map(v => v.toString().padStart(2, '0'))
    .join(':');
};
const fetchVideoInfo = async () => {
    loading.value = true;
    error.value = null;
    try {
        const res = await axios.get('http://127.0.0.1:5000/api/info/'+props.bvid);
        if (res.data.code === 0) {
            videoInfo.value = res.data.data;
            console.log('获取到的视频图片URL:', videoInfo.value.pic);
        } else {
            error.value = res.data.message;
        }
    } catch (err) {
        alert('获取视频信息失败')
        console.error('获取视频信息失败:', err);
    } finally {
        loading.value = false;
    }
};
const getProxiedImageUrl = (url:string) => {
  return `http://localhost:5000/proxy-image?url=${encodeURIComponent(url)}` // 本地服务器地址
}

async function downloadVideo(bvid:string) {
    isLoadingDownload.value = true;
    console.log(bvid)
    try {
      // 1. 触发视频处理
      const response = await axios.post(
        'http://localhost:5000/api/video',
        { 
          bvid: bvid
         },
      );
      console.log(response)
      let local = response.data.download_url.replace(/\\/g, '/') // 将反斜杠替换为斜杠
      videoStore.videoMap.set(bvid, local);
      alert('下载成功')
      return response.data;
    } catch (error) {
      console.error('视频处理失败:', error);
      throw error;
    } finally {
      isLoadingDownload.value = false;
    }
  }
const showToast = ref(false);
const toastMessage = ref('');

const openVideo = async () => {
  if (props.localPath) {
    try {
      await navigator.clipboard.writeText(props.localPath);
      toastMessage.value = '文件路径已复制到剪贴板';
      showToast.value = true;
      setTimeout(() => showToast.value = false, 1500);
    } catch (err) {
      console.error('复制文件路径失败:', err);
      toastMessage.value = '复制文件路径失败';
      showToast.value = true;
      setTimeout(() => showToast.value = false, 1500);
    }
  }else{
    downloadVideo(props.bvid)
  }
};

onMounted(() => {
    if (props.bvid) fetchVideoInfo();
});

watch(() => props.bvid, (newBvid) => {
    if (newBvid) fetchVideoInfo();
});
</script>

<style scoped>
.video-card {
    width: 250px;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin: 16px;
    background: #fff;
    
}
.video-card:hover {
    transform: translateY(-2px);
    transition: all 0.3s ease;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15); 
}

.toast {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #00B034;
    color: white;
    padding: 10px 20px;
    border-radius: 4px;
    z-index: 1000;
}

.fade-enter-active, .fade-leave-active {
    transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
    opacity: 0;
}
.pic{
    width: 226px;
    height: 146px;
}
.loading,
.error {
    padding: 20px;
    text-align: center;
    color: #666;
}

.content {
    position: relative;
    padding: 12px;
}

.cover {
    width: 100%;
    height: 180px;
    object-fit: cover;
}

.title {
    font-size: 14px;
    margin: 8px 0;
    color: #222;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.info {
    font-size: 12px;
    color: #666;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>