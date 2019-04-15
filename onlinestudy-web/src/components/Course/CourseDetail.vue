<template>
  <div class="wrap">
    <div class="web-course-banner">
      <div class="container-coursedetail">
        <div class="course-top">
          <div class="title">
            <img :src="details.course_img">
            <video>
              <div class="video-icon"></div>
            </video>
          </div>
          <div class="course-detail-info">
            <p class="course-title">{{details.title}}</p>
            <div class="course-inner">
              <p class="course-slogin">{{details.slogan}}</p>
              <p>
                <span>{{details.study_number}}人在学</span>
                <span>课程总课时：{{details.lesson}}</span>
                <span>难度：{{details.difficult}}</span>
              </p>
              <div class="course-preferential">
                <p v-if="details.price === 0">限时免费</p>
                <p v-else>限时折扣</p>
                <span>距离活动结束：仅剩：15 天 12 小时 8 分 9秒</span>
              </div>
            </div>
            <p class="course-title"></p>
            <div class="course-buy">
              <p>
                <el-button type="danger" @click="toPrice">立即购买</el-button>
                <el-button type="primary" plain @click="toStudy">免费试学</el-button>
              </p>
              <p class="shopping">
                <i class="el-icon-goods"></i>
                <span>加入购物车</span>
              </p>
            </div>
          </div>
        </div>

        <div class="course-list">
          <ul>
            <li class="detail-item">难度：{{details.level}}</li>
            <li class="sep"></li>
            <li class="detail-item">时长：{{details.hours}}小时</li>
            <li class="sep"></li>
            <li class="detail-item">学习人数：{{details.study_number}}人</li>
            <li class="sep"></li>
            <li class="detail-item">评分 {{details.course_review}}</li>
          </ul>
        </div>
      </div>
    </div>
    <div class="course-review">
      <ul class="review-head-wrap">
        <li
          class="head-item"
          @click="getcourseInfo(item.field,item.id)"
          v-for="item in tab"
          :key="item.id"
          :class="{active:current_tab_id==item.id}"
        >{{item.title}}</li>
      </ul>
    </div>
    <!-- 课程详情 -->
    <div class="course-detail">
      <div class="container-coursedetail-buttom">
        <div class="coursedetail-left">
          <router-view></router-view>

          <div class="course-detail-text" v-show="isShow">
            <h3>课程背景</h3>
            <p>{{details.why_study}}</p>

            <h3>学前准备</h3>
            <p>{{details.prerequisite}}</p>

            <h3>课程概述</h3>
            <p>{{details.brief}}</p>

            <h3>适合人群</h3>
            <p>{{details.object_person}}</p>

            <h3>课程覆盖知识点</h3>
            <p>{{details.point}}</p>

            <h3>课程特点</h3>
            <p>{{details.feature}}</p>

            <h3>课程大纲</h3>
            <p v-for="(outline,index) in details.course_outline" :key="index">{{outline.content}}</p>

            <h3>学完收获</h3>
            <p>{{details.harvest}}</p>
          </div>
        </div>

        <div class="course-teacher-recommend">
          <div class="course-teacher">
            <h3
              style="border-left: 2px solid rgb(239, 53, 53); text-align: left; text-indent: 6px;"
            >授课讲师</h3>
            <div v-for="(teacher,index) in details.teacher" :key="index" class="teacher-info">
              <img :src="teacher.teacher_img">
              <p>{{teacher.username}}</p>
              <p>{{teacher.title}}</p>
              <p>{{teacher.brief}}</p>
            </div>
          </div>

          <div class="course-recommend">
            <h3
              style="border-left: 2px solid rgb(239, 53, 53); text-align: left; text-indent: 6px;"
            >课程推荐</h3>
            <div v-if="details.recommend_course !== null">
              <li
                v-for="(course,index) in details.recommend_course"
                :key="index"
                class="teacher-info"
              >
                <div class="recommend_course clearfix">
                  <img :src="course.course_img|filterImg">
                  <p>{{course.title}}</p>
                  <p>{{course.brief}}</p>
                </div>
              </li>
            </div>
            <div v-else>
              <p>暂无课程推荐</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="course-price" id="position-price">
      <div class="container">
        <span>根据您的学习情况购买适合您的学习套餐哦</span>
        <ul class="course-price-item">
          <li
            v-for="(item,index) in details.prices"
            :key="item.id"
            :class="{active:index===currentPriceIndex}"
            @click="priceClick(index)"
          >
            <p class="price" :class="{active:index===currentPriceIndex}">¥{{item.price}}</p>
            <p class="time" :class="{active:index===currentPriceIndex}">有效期{{item.valid_period}}</p>
          </li>
        </ul>
        <div class="course-action">
          <button class="left" @click="toBuy">购买</button>
          <button class="right" @click="addShopCart">加入购物车</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CourseDetail",
  data() {
    return {
      details: "", // 课程详情数据
      courseInfo: "", // 课程概述
      courseChapter: "", // 课程章节
      courseComment: "", // 课程评价
      CourseQuestion: "", // 课程常见问题
      isShow: true, // 默认课程概述部分显示标志位
      current_tab_id: 0, // 选项卡默认id
      tab: [
        // 中部选项卡
        { id: 0, title: "课程概述", field: "overview" },
        { id: 1, title: "课程章节", field: "chapter" },
        { id: 2, title: "学员评价", field: "comment" },
        { id: 3, title: "常见问题", field: "question" }
      ],
      currentPriceIndex: 0 // 课程套餐
    };
  },

  methods: {
    // 课程详情
    getcourseDetail() {
      this.$http
        .courseDetail(this.$route.params.detailId)
        .then(res => {
          if (!res.error) {
            this.details = res.data[0];
          }
        })
        .catch(error => {
          error.error;
        });
    },
    // 跳转到购买区域
    toPrice() {
      document.getElementById("position-price").scrollIntoView();
    },

    // 选项卡切换到章节
    toStudy() {
      this.current_tab_id = 1;
      this.getcourseInfo("chapter", this.current_tab_id);
    },

    // 切换页面中部选项卡
    getcourseInfo(field, id) {
      this.isShow = false;
      this.current_tab_id = id;
      this.$router.push({
        name: "CourseDetailTab",
        query: { sub: field }
      });
    },
    // 价格策略选择
    priceClick(index) {
      this.currentPriceIndex = index;
    },

    // 加入购物车
    addShopCart() {
      console.log(this.currentPriceIndex);
      if (this.details.prices[this.currentPriceIndex]) {
        let access_token = localStorage.getItem("access_token");
        if (access_token) {
          let product = {
            course: this.$route.params.detailId,
            price_policy: this.details.prices[this.currentPriceIndex].id,
            price:this.details.prices[this.currentPriceIndex].price
          };

          console.log(access_token);
          this.$http.shopping(product).then(res => {
            if (!res.error) {
              console.log(res);
              this.$message({
                message: this.details.title + ` 已加入购物车`,
                center: true
              });
            }
          });
        }
        // 未登录，跳转到登录页面
        else {
          this.$router.push({
            name: "Login"
          });
        }
      }
    },
    // 去购买页面
    toBuy() {
      console.log(this.currentPriceIndex);
      console.log(this.details.prices[this.currentPriceIndex]);
    }
  },
  created() {
    this.getcourseDetail();

    // course组件跳转过来会保持原来的滚动条位置，所以在创建时移动滚动条到根节点上
    document.getElementById("app").scrollIntoView();
  },
  mounted() {
    // 当刷新页面时，中部选项卡保持数据还在
    if (this.$route.query.sub) {
      this.tab.forEach((item, index) => {
        if (this.$route.query.sub == item.field) {
          this.current_tab_id = item.id;
        }
      });
      this.getcourseInfo(this.$route.query.sub, this.current_tab_id);
    }
  }
};
</script>

<style lang="css" scoped>
.wrap {
  width: 100%;
}

li {
  list-style-type: none;
}
.web-course-banner {
  width: 100%;
  height: 512px;
  background-size: 100% 100%;
  text-align: center;
  overflow: hidden;
}
.container-coursedetail {
  width: 1200px;
  margin: 12px auto;
  text-align: left;
}

/* .video-icon{
    background: url('../../../../static/images/video.png') no-repeat;
    background-size: contain;
    width: 64px;
    height: 64px;
} */

.course-top {
  display: flex;
}

.title {
  width: 720px;
}

.title img {
  width: 720px;
  height: 490px;
  padding: 6px 4px;
}

.container-coursedetail img {
  vertical-align: middle;
}
.container-coursedetail h1 {
  display: inline-block;
  font-size: 48px;
  color: #4a4a4a;
  letter-spacing: 0.37px;
  font-family: PingFangSC-Light;
  font-weight: 500;
  line-height: 1.1;
  position: relative;
  top: 10px;
}

.course-detail-info {
  position: relative;
  flex: 1;
  height: 420px;
  padding: 20px;
}

.course-slogin {
  margin-top: 12px;
  margin-bottom: 5px;
  font-size: 17px;
  color: #eb5089;
  font-weight: bold;
  border-top: 1px solid #bababa;
  line-height: 2em;
}
.course-title {
  font-size: 30px;
  margin-bottom: 4px;
}

.course-inner {
  color: #979797;
}

.course-preferential {
  width: 100%;
  height: auto;
  background: #fa6240;
  font-size: 14px;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 17px 5px;
  margin-top: 16px;
  border-left: 3px solid #7c0b8a;
}

.course-buy {
  display: flex;
  align-items: center;
  position: absolute;
  width: 100%;
  height: auto;
  bottom: 2px;
  flex: 1;
}

.course-buy .shopping {
  right: 40px;
  position: absolute;
  font-size: 14px;
  color: #ef58d5;
  text-align: center;
  font-weight: bold;
  border: 1px solid #e73767;
  padding: 8px;
  border-radius: 4px;
  cursor: pointer;
  box-shadow: 1px 0px 4px 0px #e73767;
}

.course-text {
  width: 464px;
  display: inline-block;
  font-size: 22px;
  color: #4a4a4a;
  letter-spacing: 0.17px;
  line-height: 36px;
  margin-top: 33px;
}

.course-teacher-recommend {
  position: absolute;
  right: 44px;
  top: 24px;
}

.container-coursedetail-buttom {
  position: relative;
  display: flex;
}

.coursedetail-left {
  margin-left: 35px;
  margin-top: 7px;
}

.teacher-info {
  margin-bottom: 10px;
  border-bottom: 1px inset #cdcdcd;
}

.teacher-info p {
  text-align: left;
  margin-left: 10px;
  margin-top: 20px;
  margin-bottom: 20px;
  width: 380px;
}

.course-list {
  width: 100%;
}
.course-list ul {
  margin-top: 63px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
.course-list ul li.detail-item {
  font-size: 18px;
  color: #4a4a4a;
  letter-spacing: 0.74px;
  height: 26px;
  padding: 0 20px;
}
.course-list ul li.sep {
  width: 2px;
  height: 14px;
  border-left: 1px solid #979797;
}
.course-review {
  width: 100%;
  height: 80px;
  border-top: 1px solid #e8e8e8;
  box-shadow: 0 1px 0 0 #e8e8e8;
}
.review-head-wrap {
  width: 590px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  margin-left: 100px;
}
.review-head-wrap .head-item {
  height: 80px;
  line-height: 80px;
  font-size: 16px;
  color: #555;
  cursor: pointer;
}

.review-head-wrap .head-item.active {
  color: #4a4a4a;
  border-bottom: 4px solid #409eff;
}

.course-detail {
  width: 100%;
  min-height: 350px;
}
.course-detail .container {
  width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
}
.course-detail-text {
  width: 650px;
  text-align: left;
}
.course-detail-text h3 {
  padding: 20px 0;
  border-left: 2px solid #904beb;
  text-indent: 4px;
  margin-bottom: 10px;
}
.course-detail-text p {
  width: 80%;
  font-size: 14px;
  color: #4a4a4a;
  letter-spacing: 1.83px;
  line-height: 30px;
  text-align: left;
  margin-bottom: 40px;
  text-indent: 10px;
  border-bottom: 1px inset #cdcdcd;
  padding: 20px;
  font-weight: bold;
}

.recommend_course {
  position: relative;
  width: 300px;
}
.clearfix {
  clear: both;
  content: "";
}
.recommend_course img {
  width: 100px;
  height: 50px;
  left: 2px;
  position: absolute;
}

.recommend_course p {
  margin-left: 120px;
}

.recommend_course p:last-child {
  font-size: 12px;
  color: #979797;
}

.course-price {
  width: 100%;
  background: #fafafa;
  border-top: 2px solid #e9e4eddd;
  padding-top: 20px;
}
.course-price .container {
  width: 1200px;
  margin: 0 auto;
  text-align: center;
}
.course-price span {
  color: #9b9b9b;
  letter-spacing: 1.57px;
  display: inline-block;
  margin-top: 102px;
  font-weight: bold;
}
.course-price ul {
  width: 1000px;
  margin: 50px auto;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.course-price ul li {
  width: 200px;
  height: 112px;
  border: 1px solid #979797;
  border-radius: 3px;
}
.course-price ul li.active {
  background: #409eff;
}
.course-price ul li p:first-child {
  font-size: 24px;
  letter-spacing: 1.92px;
  color: #333;
  margin-top: 17px;
}
.course-price ul li p:nth-child(2) {
  color: #9b9b9b;
  font-size: 20px;
  letter-spacing: 1.6px;
  margin-top: 9px;
}
.course-price ul li p.active {
  color: #fff;
}

.course-action {
  width: 1000px;
  margin: 0 auto;
  padding-bottom: 80px;
  display: flex;
  justify-content: center;
}
.course-action button {
  border: none;
  outline: none;
  cursor: pointer;
  display: inline-block;
  width: 181px;
  height: 51px;
  font-size: 14px;
  color: #fff;
  letter-spacing: 1.12px;
  text-align: center;
  background: #f5a623;
  border-radius: 82px;
}
.course-action button.left {
  background: #7ed321;
  box-shadow: 0 2px 4px 0 #e8e8e8;
  color: #fff;
  margin-right: 48px;
  padding: 0 20px;
}
.course-action button.right {
  background: #f5a623 url() no-repeat 125px 15px !important;
}
</style>
