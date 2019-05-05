<template>
  <div class="shopping-cart-wrap">
    <h3 class="shopping-cart-tit">学无止境&nbsp;</h3>
    <div class="row">
      <div class="course-left">
        <div @click="tohomework" class="comment">
          <el-button type="success" round size="mini" class="common">作业/提交</el-button>
        </div>
        <div @click="toquestion" class="comment">
          <el-button type="danger" round size="mini" class="common">问题求救</el-button>
        </div>

        <div style="margin-top:50px">
          <div class="block comment">
            <span class="demonstration">课程评价</span>
            <br>
            <br>
            <el-input
              type="textarea"
              :rows="2"
              placeholder="请输入评价内容"
              v-model="assess"
              style="width:200px"
            ></el-input>
            <div class="comment-yan">
              <br>
              <el-rate v-model="value2" :colors="['#99A9BF', '#F7BA2A', '#FF9900']"></el-rate>
              <el-button type="primary" size="mini" @click="tocomment">提交</el-button>
            </div>
          </div>
        </div>
      </div>
      <div>
        <div class="course-item" v-for="(item,index) in courseChapter" :key="index">
          <div class="course-inner">
            <div class="course-info">
              <p>章节 {{index+1}}：{{item.title}}</p>
            </div>
            <div
              class="content"
              v-for="(lesson,index) in item.chapter_lesson"
              :key="index"
              :class="{active:currentIndex==index}"
              @mouseenter="enterHandler(index)"
              @mouseleave="leaveHandler"
              @click="tolearning(lesson.id)"
            >
              <p>课时 {{index+1}} - {{lesson.title}}</p>
              <span class="player">
                <img src="http://127.0.0.1:8000/media/player.png">
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-pagination background layout="prev, pager, next" :total="80"></el-pagination>
  </div>
</template>

<script>
// @click="toclearning(item.course_id)"
export default {
  name: "Courselesson",
  data() {
    return {
      courseChapter: "",
      currentIndex: 999,
      isSHow: false,
      assess: "", // 评价内容
      courseId: 0
    };
  },
  methods: {
    tolearning(lesson_id) {
      this.$router.push({
        name: "learning",
        params: { courseId: lesson_id }
      });
    },

    tocomment() {
      let params = {
        course: this.courseId,
        assess: this.assess
      };
      this.$http.PaymentAssess(params).then(res => {
        this.$message({
          type: "success",
          message: res.data,
          center: true
        });
        this.assess = ''
      });
    },
    tohomework() {
      this.$router.push({
        name: "homework",
        params: { courseId: this.$route.params.courseId }
      });
    },
    toquestion() {
      this.$router.push({
        name: "solvequestion",
        params: { courseId: this.$route.params.courseId }
      });
    },

    getCourseChapter() {
      let course_id = this.$route.params.courseId;
      this.$http.chapter(course_id).then(res => {
        if (!res.error) {
          this.courseChapter = res.data;
          console.log(this.courseChapter);
        }
      });
    },
    enterHandler(index) {
      this.currentIndex = index;
    },
    leaveHandler() {
      this.currentIndex = 999;
    }
  },
  created() {
    this.getCourseChapter();
    this.courseId = this.$route.params.courseId;
  }
};
</script>

<style scoped>
</style>



<style lang="css" scoped>
.shopping-cart-wrap {
  width: 100%;
  transition: all 0.3s ease;
}

.row {
  width: 1200px;
  margin: 0 auto;
  padding-top: 20px;
  padding-bottom: 20px;
  display: flex;
}

.course-left {
  margin-right: 100px;
}

.shopping-cart-wrap h3 {
  padding: 50px 0;
}

.course-item {
  width: 800px;
  border: 1px solid #dfe4f7;
  margin: 0 auto;
  padding-bottom: 30px;
  border-radius: 3px;
  margin-bottom: 20px;
}

.course-inner {
  text-align: left;
}
.course-info {
  background: #d7eef2;
  padding: 20px;
  border-left: 2px solid #8d03f6;
}

.content {
  padding: 20px;
  position: relative;
  cursor: pointer;
  line-height: 18px;
}

.content.active {
  background: #ffcd00;
  color: white;
  border-radius: 5px;
  font-size: 20px;
}

.player {
  position: absolute;
  right: 66px;
  top: 40px;
}
.content img {
  width: 35px;
  position: absolute;
  top: -27px;
}
.comment {
  margin-bottom: 20px;
}
.comment-yan {
  display: flex;
  margin-top: 10px;
  margin-left: 5px;
}
</style>
