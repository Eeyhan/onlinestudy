<template>
  <div class="shopping-cart-wrap">
    <h3 class="shopping-cart-tit">我的课程 &nbsp;</h3>
    <div class="row">
      <div
        class="course-item"
        v-for="(item,index) in courses"
        :key="index"
        @click="tocourselesson(item.course_id)"
      >
        <img :src="item.course_img">
        <div class="course-inner">
          <div>
            <h4>{{item.title}}</h4>
            <p>{{item.brief}}</p>
          </div>
          <div class="course-info">
            <p>难度：{{item.difficult}}</p>
            <p>课时：{{item.lesson}}</p>
          </div>
          <p>焦点：{{item.point}}</p>
          <p>特点：{{item.feature}}</p>
        </div>
      </div>
    </div>
    <el-pagination background layout="prev, pager, next" :total="80"></el-pagination>
  </div>
</template>

<script>
export default {
  name: "study",
  data() {
    return {
      courses: []
    };
  },

  methods: {
    // 获取已购买的商品的数据列表
    getPaymentList() {
      this.$http
        .userCourselist()
        .then(res => {
          if (!res.error) {
            this.courses = res.data;
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    tocourselesson(course_id) {
      this.$router.push({
        name: "Courselesson",
        params: { courseId: course_id }
      });
    }
  },

  created() {
    this.getPaymentList();
  }
};
</script>

<style lang="css" scoped>
.shopping-cart-wrap {
  width: 100%;
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
  width: 750px;
  height: 300px;
  box-shadow: 0px 2px 4px 2px #cdcdcd;
  margin: 0 auto;
  position: relative;
  cursor: pointer;
  margin-bottom: 20px;
}

.course-item img {
  width: 750px;
  height: 300px;
  position: absolute;
  left: 0;
  opacity: 0.2;
}
.course-inner {
  padding: 20px;
  padding-top: 62px;
}
.course-info {
  padding-top: 30px;
  display: flex;
  margin: 0 auto;
}
.course-info p {
  margin: 0 auto;
}
</style>
