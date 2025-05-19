import { defineStore } from "pinia";
import { watch } from "vue";
import { ref } from "vue";

const useVideoStore = defineStore('video', () => {
  const videoMap = ref<Map<string, string>>(new Map());
  // 从localStorage初始化数据
  try {
    const storedData = localStorage.getItem('videoMap');
    if (storedData) {
      const entries = JSON.parse(storedData);
      videoMap.value = new Map(entries);
    }
  } catch (error) {
    console.error('加载localStorage数据失败:', error);
    videoMap.value = new Map();
  }

  // 数据变化时保存到localStorage
  watch(videoMap, (newMap) => {
    try {
      const entries = Array.from(newMap.entries());
      localStorage.setItem('videoMap', JSON.stringify(entries));
    } catch (error) {
      console.error('保存到localStorage失败:', error);
    }
  }, { deep: true });

  return {
    videoMap: videoMap
  };
});
export default useVideoStore;