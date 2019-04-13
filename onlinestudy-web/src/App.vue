<template>
  <div id="app">
    <BaseHeader />
    <router-view/>
  </div>
</template>

<script>
import BaseHeader from "@/components/common/BaseHeader"; //  导航栏
export default {
  name: "App",
  components: {
    BaseHeader
  }
};
</script>

<style>
#app {
  font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
