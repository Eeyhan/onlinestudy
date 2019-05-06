<template>
  <div class="box">
    <div class="mydata">
      <img src="https:////s2.ax1x.com/2019/04/14/AOaUqs.jpg" alt>
    </div>
    <div class="data-box">
      <h3>作业内容：</h3>
      <div class="content">
        <pre>{{homeworkdata}}</pre>
      </div>

      <h3>提交作业：</h3>
      <el-upload
        class="upload-demo"
        drag
        :action="uploadTO"
        multiple
        :show-file-list="true"
        :before-upload="isLogin"
        :data="homeworkInfo"
        :headers="myHeader"
        :on-success="callbackinfo"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">
          将文件拖到此处，或
          <em>点击上传</em>
        </div>
        <input type="hidden" multiple :name="homeworkId">
        <div class="el-upload__tip" slot="tip">只能上传zip文件，且不超过10M</div>
      </el-upload>
      <h3>批改状态：{{status}}</h3>

      <h3>作业批语：</h3>
      <div class="content">
        <pre>{{critic}}</pre>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "homework",
  data() {
    return {
      homeworkdata: null,
      homeworkId: null,
      status: null,
      critic: null,
      chapterId: null,
      courseId: null,
      uploadTO: "http://127.0.0.1:8000/api/v1/homework"
    };
  },
  computed: {
    homeworkInfo() {
      return {
        homework: this.homeworkId
      };
    },
    myHeader() {
      return {
        Authorization: localStorage.getItem("access_token")
      };
    }
  },

  methods: {
    isLogin() {
      let access_token = localStorage.getItem("access_token");
      // 未登录，跳转到登录页面
      if (!access_token) {
        this.$router.push({
          name: "Login"
        });
      }
    },
    callbackinfo(res) {
      this.$message({
        message: res.data,
        type: "success",
        center: true
      });
    },
    homeworkList(courseId, chapterId) {
      this.$http.homework(courseId, chapterId).then(res => {
        this.homeworkId = res.id;
        this.status = res.status;
        this.critic = res.critic;
        this.homeworkdata = res.content;
      });
    }
  },

  created() {
    this.isLogin();
    this.chapterId = this.$route.query.chapterId;
    this.courseId = this.$route.query.courseId;
    this.homeworkList(this.courseId, this.chapterId);
  },

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
  margin-left: 144px;
  padding: 30px;
  min-width: 900px;
}

.data-box h3 {
  text-align: left;
  border-left: 4px solid #8ba5ee;
  padding: 6px;
  margin: 20px auto;
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

