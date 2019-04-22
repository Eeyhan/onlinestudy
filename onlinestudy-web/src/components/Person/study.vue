<template>
  <div class="container clearfix">
    <!-- 课程分类标签 热度 -->
    <div class="main">
      <!-- <div class="uptoquestion">
        <div class="item"></div>
      </div>-->

      <!-- 课程 -->
      <div class="course-list" v-loading="loading">
        <dl
          v-for="(course,index) in courses"
          :key="index"
          @click="tocourselesson(course.course_id)"
        >
          <dt>
            <img :src="course.course_img|filterImg" class="image">
          </dt>
          <dd>
            <!-- 课程名 -->
            <div class="name">
              <p>{{course.title}}</p>&nbsp;&nbsp;&nbsp;&nbsp;
              <p>
                <span>{{course.status}}</span>
              </p>
            </div>

            <div class="teacher">
              <p v-for="teacher in course.teacher" :key="teacher.id">
                {{teacher.username}}
                {{teacher.title}}
              </p>
              <p>
                <span>总课时:{{course.lesson}}&nbsp;学习人数:{{course.study_number}}</span>
              </p>
            </div>
            <div>
              <ul>
                <li v-for="(free,index) in course.free_course" :key="free.id">
                  <p>
                    课时{{index+1}}:
                    <i class="el-icon-service"></i>
                    {{free.title}}
                  </p>
                  <span>免费</span>
                </li>
              </ul>
            </div>
            <span></span>
            <div></div>
            
          </dd>
        </dl>
      </div>
    </div>
    <el-pagination background layout="prev, pager, next" :total="80"></el-pagination>
  </div>
</template>

<script>
export default {
  name: "Course",
  data() {
    return {
      courses: [],
      loading: true
    };
  },
  filters: {
    filterImg(value) {
      // 拼接图片地址
      return `https://${value}`;
    }
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
    },
    
  },

  created() {
    this.getPaymentList();
    if (this.courses) {
      this.loading = false;
    }
  },
  mounted() {}
};
</script>

<style lang="css" scoped>
.main {
  width: 960px;
  height: auto;
  margin: 0 auto;
  padding-top: 35px;
}

span {
  margin-left: 2px;
  cursor: pointer;
  transition: all 0.3s ease;
}

span.active {
  color: #00b4e4;
}

.uptoquestion {
  width: 910px;
  margin: 0 auto;
  padding-top: 20px;
  height: auto;
  margin-bottom: 35px;
  padding: 25px 30px 25px 20px;
  background: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 4px 0 #f0f0f0;
}

.item {
  display: flex;
  align-items: center;
  font-size: 16px;
  color: #888;
  letter-spacing: 0.36px;
  display: flex;
}

.item ul li {
  list-style: none;
  float: left;
  line-height: 16px;
  margin-left: 14px;
  position: relative;
  transition: all 0.3s ease;
  cursor: pointer;
  padding: 6px 7px;
}
.item ul li.active {
  color: #00b4e4;
  border-radius: 30px;
  border: 1px solid #00b4e4;
}

.course-list {
  width: 960px;
  margin: 0 auto;
}

.course-list .image {
  width: 423px;
  height: 210px;
}
.course-list dl {
  height: auto;
  background: #fff;
  padding: 20px 30px 20px 20px;
  display: -ms-flexbox;
  display: flex;
  margin: 35px auto;
  border-radius: 2px;
  cursor: pointer;
  box-shadow: 2px 3px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
  position: relative;
}

.course-list dl dt {
  width: 423px;
  height: 210px;
  margin-right: 30px;
}

.course-list ul {
  display: flex;
  -ms-flex-wrap: wrap;
  flex-wrap: wrap;
  -ms-flex-align: center;
  align-items: center;
  -ms-flex-pack: justify;
  justify-content: space-between;
}

.course-list ul li {
  width: 48%;
  display: -ms-flexbox;
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
  cursor: pointer;
}
.course-list ul li p {
  max-width: 227px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  font-family: PingFangSC-Regular;
}

.course-list ul li span {
  color: #ffc210;
  border: 1px solid #ffc210;
}

.name {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 8px;
  width: 480px;
}

.name > p {
  font-size: 19px;
  color: #070505;
  font-weight: bold;
}

.name p span {
  font-size: 15px;
  color: rgb(249, 29, 29);
  margin-right: 8px;
}

.teacher {
  display: -ms-flexbox;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  font-size: 14px;
  color: #9b9b9b;
  margin-bottom: 14px;
  padding-bottom: 14px;
  font-family: PingFangSC-Light;
  border-bottom: 1px solid #333;
  border-bottom-color: rgba(51, 51, 51, 0.05);
}

.teacher p span {
  font-size: 15px;
  color: rgb(239, 189, 77);
  font-weight: bolder;
  margin-right: 8px;
}

.price {
  display: flex;
  padding-top: 40px;
}
.discount {
  padding: 6px 10px;
  font-size: 16px;
  color: #fff;
  text-align: center;
  margin-right: 8px;
  background: #409eff;
  border: 1px solid #409eff;
  border-radius: 10px 0 10px 0;
  font-family: PingFangSC-Regular;
}
.present-price {
  font-size: 24px;
  color: #409eff;
  text-align: center;
  line-height: 33px;
  width: 250px;
}
.discount-pay {
  right: 20px;
  padding: 6px 10px;
  font-size: 16px;
  color: #409eff;
  text-align: center;
  border: 1px solid #6ab2fa;
  border-radius: 3px;
  font-family: PingFangSC-Regular;
  width: 90px;
}

.discount-pay:hover {
  background: #fa6240;
  color: white;
}
.course-list dl dd .price button:hover {
  color: #fff;
  background: #ffc210;
  border: 1px solid #ffc210;
}

</style>
