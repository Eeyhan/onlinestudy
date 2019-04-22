<template>
  <div class="box">
    <div class="mydata">
      <img src="https:////s2.ax1x.com/2019/04/14/AOaUqs.jpg" alt>
    </div>
    <div class="data-box">
      <el-input type="textarea" :rows="10" placeholder="请输入您遇到的问题" v-model="textarea"></el-input>
    </div>
  </div>
</template>





<script>
export default {
  name: "solvequestion",
  data() {
    return {
      textarea: ""
    };
  },

  methods: {
    loginHandler() {}
  },

  created() {},

  mounted() {}
};
</script>

<style lang="css" scoped>
.box {
  position: relative;
  min-height: 1200px;
}
.mydata {
  position: absolute;
}

.mydata img {
  opacity: 0.8;
  width: 100%;
}
.data-box {
  margin-top: 200px;
  position: absolute;
  background: white;
  margin-left: 200px;
  padding: 30px;
  width: 800px;
}
.data-box img {
  width: 60px;
}

.el-form h3 {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>

