<template>
  <div class="box">
    <div class="mydata">
      <img src="https:////s2.ax1x.com/2019/04/14/AOaUqs.jpg" alt>
    </div>
    <div class="data-box">
      <h3>作业内容：</h3>
      <div class="content">
        <p>1、熟练掌握计算机原理，熟悉Linux系统的使用</p>
        <p>2、熟练掌握Python函数/面向对象编程，可开发基于各种业务场景下的Python工具</p>
        <p>3、掌握Socket网络编程、线程、进程知识，可以开发C/S架构的高并发的FTP文件共享软件</p>
        <p>4、熟练掌握数据库常用操作，具备为复杂的项目（上百张表）设计合理、可扩展表结构的能力</p>
        <p>5、熟练掌握缓存、队列等中间件技术，为开发大并发、高性能应用打下基础</p>
        <p>6、熟练掌握前端HTML/CSS/JS/Jquery/Bootstrap知识，熟练掌握Django、Flask框架</p>
        <p>7、独立开发完成实战项目BBS论坛 、CRM软件</p>
        <p>8、掌握爬虫和基本数据分析知识</p>
      </div>

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
    return {};
  },

  methods: {
    loginHandler() {},
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

