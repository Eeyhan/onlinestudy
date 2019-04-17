<template>
  <div id="app">
    <BaseHeader />
    <router-view/>
    <BaseFooter/>
  </div>
</template>

<script>
import BaseHeader from "@/components/common/BaseHeader"; //  导航栏
import BaseFooter from "@/components/common/BaseFooter"; //  底部栏
export default {
  name: "App",
  components: {
    BaseHeader,
    BaseFooter
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
