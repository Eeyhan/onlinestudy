<template>
  <div>
    <el-carousel indicator-position="outside" height="500px">
      <el-carousel-item v-for="item in lunboImgs" :key="item.id">
        <img :src="item.imgSrc" alt>
      </el-carousel-item>
    </el-carousel>
    <div style="    width: 1200px;    margin: 0 auto; margin-top:20px">
      <h3>我们的课程体系</h3>
      <el-steps :active="active" finish-status="success" align-center>
        <el-step title="步骤 1" description="学习"></el-step>
        <el-step title="步骤 2" description="做作业"></el-step>
        <el-step title="步骤 3" description="考试"></el-step>
        <el-step title="步骤 4" description="答疑"></el-step>
      </el-steps>

      <el-button style="margin-top: 12px;" @click="next">下一步</el-button>
      <div style="    width: 1200px;    margin: 0 auto; margin-top:20px">
        <h3>您将掌握的技能</h3>
        <el-progress type="circle" :percentage="0">计算机基础</el-progress>
        <el-progress type="circle" :percentage="25">Python</el-progress>
        <el-progress type="circle" :percentage="100" status="success">linux</el-progress>
        <el-progress type="circle" :percentage="50" status="exception">Go</el-progress>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      active: 0,
      lunboImgs: [
        {
          id: 1,
          imgSrc: "https://s2.ax1x.com/2019/04/17/Az0XCj.png"
        },
        {
          id: 2,
          imgSrc: "https://s2.ax1x.com/2019/04/17/Az0j8s.png"
        },
        {
          id: 3,
          imgSrc: "https://s2.ax1x.com/2019/04/17/AzDHhQ.jpg"
        },
        {
          id: 4,
          imgSrc: "https://i.niupic.com/images/2019/04/17/6eX4.jpg"
        },
        {
          id: 5,
          imgSrc: "https://s2.ax1x.com/2019/04/14/AOarGT.jpg"
        }
      ]
    };
  },
  created() {
    // console.log(localStorage);
  },
  methods: {
    next() {
      if (this.active++ > 2) this.active = 0;
    }
  },
  
};
</script>

<style lang="css" scoped>
img {
  width: 100%;
}
</style>
