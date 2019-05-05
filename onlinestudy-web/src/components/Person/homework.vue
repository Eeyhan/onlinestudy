<template>
  <div class="box">
    <div class="mydata">
      <img src="https:////s2.ax1x.com/2019/04/14/AOaUqs.jpg" alt>
    </div>
    <div class="data-box">
      <h3>作业内容：</h3>
      <div class="content"> </div>

      <el-upload
        class="upload-demo"
        drag
        action="https://jsonplaceholder.typicode.com/posts/"
        multiple
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          将文件拖到此处，或
          <em>点击上传</em>
        </div>
        <div class="el-upload__tip" slot="tip">只能上传zip文件，且不超过10M</div>
      </el-upload>
    </div>
  </div>
</template>





<script>
export default {
  name: "homework",
  data() {
    return {
      homeworkdata:null
    };
  },

  methods: {
    loginHandler() {},
    homeworkList(){

    },
    onSubmit() {
      console.log("submit!");
    }
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
  margin-top: 100px;
  position: absolute;
  background: white;
  margin-left: 350px;
  padding: 30px;
}
.data-box img {
  width: 60px;
}

.el-form h3 {
  margin-top: 20px;
  margin-bottom: 20px;
}

.content {
  text-align: left;
  background: #e6e9ea;
  border-radius: 6px;
  padding: 20px;
}
</style>

