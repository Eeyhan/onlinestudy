<template>
  <div class="shopping-cart-wrap">
    <h3 class="shopping-cart-tit">学无止境&nbsp;</h3>
    <div class="row">
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
      isSHow: false
    };
  },
  methods: {
    tolearning(course_id) {
      this.$router.push({
        name: "learning",
        params: { courseId: course_id }
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
    leaveHandler(){
      this.currentIndex = 999
    }
  },
  created() {
    this.getCourseChapter();
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
  background: #e1dbdb;
  padding: 20px;
  padding-bottom: 30px;
}

.content {
  padding: 40px;
  position: relative;
  cursor: pointer;
  line-height: 18px;
}

.content.active {
  background: #a2c5e9;
  color: white
}

.player {
  position: absolute;
  right: 66px;
  top: 40px;
}
.content img {
  width: 20px;
}
</style>
