<template>
  <div class="container clearfix">
    <!-- 课程分类标签 热度 -->
    <div class="main">
      

      <!-- 课程 -->
      <div class="course-list">
        <dl v-for="course in courses" :key="course.id">
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
            <div class="price">
              <span class="discount" v-if="course.price==0">限时免费</span>
              <span class="discount" v-else>限时折扣</span>
              <span class="present-price">￥ {{course.price}}</span>
              <span class="discount-pay">立即购买</span>
            </div>
          </dd>
        </dl>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Course",
  data() {
    return {
      categorys: "",
      courses: "",
      
    };
  },
  filters: {
    filterImg(value) {
      return `https://${value}`;
    }
  },
  methods: {
    
  },
  created() {
    

    // 默认选中全部
    this.$http
      .get("/degree")
      .then(res => {
        this.courses = res.data;
      })
      .catch(error => {
        console.log(error.data);
      });
  }
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

.category {
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
  border:1px solid #00b4e4
}

.condition {
  display: flex;
  align-items: center;
  font-size: 16px;
  color: #888;
  letter-spacing: 0.36px;
  margin-top: 20px;
}

.condition ul li {
  list-style: none;
  float: left;
  line-height: 16px;
  margin-left: 14px;
  position: relative;
  transition: all 0.3s ease;
  cursor: pointer;
  padding: 6px 7px;
}
.condition ul li.active {
  color: #00b4e4;
  border-radius: 30px;
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
}
.discount {
  padding: 6px 10px;
  font-size: 16px;
  color: #fff;
  text-align: center;
  margin-right: 8px;
  background: #fa6240;
  border: 1px solid #fa6240;
  border-radius: 10px 0 10px 0;
  font-family: PingFangSC-Regular;
}
.present-price {
  font-size: 24px;
  color: #fa6240;
  text-align: center;
  line-height: 33px;
  width: 250px;
}
.discount-pay {
  right: 20px;
  padding: 6px 10px;
  font-size: 16px;
  color: #f50b0b;
  text-align: center;
  border: 1px solid #fa6240;
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
