<template>
  <div class="container clearfix">
    <!-- 课程分类标签 热度 -->
    <div class="main">
      <div class="category">
        <div class="item">
          课程分类：
          <ul>
            <li
              v-for="category in categorys"
              :key="category.id"
              :class="{active:category_id===category.id}"
            >
              <span @click="categoryTocourse(category.id)">{{category.title}}</span>
            </li>
          </ul>
        </div>
        <div class="condition">
          筛&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;选：
          <ul>
            <li v-for="con in conditon" :key="con.id" :class="{active:condition_id===con.id}">
              <span @click="conditoncourse(con.query,con.id)">{{con.title}}</span>
              <span v-if="con.query==='price'" class="condtion-span">
                <span class="condtion-i i-top" ref="spantop"></span>
                <span class="condtion-i i-buttom" ref="spanbuttom"></span>
              </span>
            </li>
          </ul>
        </div>
      </div>

      <!-- 课程 -->
      <div class="course-list">
        <!-- 这里绑定key为index时因为后端从不同表中传来多个相同的id值的数据，绑定id为有冲突 -->
        <dl v-for="(course,index) in courses" :key="index">
          <dt>
            <img :src="course.course_img|filterImg" class="image">
          </dt>
          <dd @click="coursedetail(course.id)">
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
      query: "", // 做上一次筛选条件存储
      query_isup: "-price",
      isActive: false,
      conditon: [
        { id: 0, title: "默认", query: "" },
        { id: 1, title: "热门", query: "hot" },
        { id: 2, title: "价格", query: "price" }
      ],
      category_id: 0,
      condition_id: 0
    };
  },
  filters: {
    filterImg(value) {
      // 拼接图片地址
      return `https://${value}`;
    }
  },
  methods: {
    categoryTocourse(id) {
      this.category_id = id;
      this.$http
        .get(`/course?cid=${id}&query=${this.query}`)
        .then(res => {
          this.courses = res.data;
        })
        .catch(error => {
          console.log(error.data);
        });
    },

    conditoncourse(query, id) {
      this.condition_id = id; // 修改当前的筛选条件id,选中条件高亮显示
      this.query = query; // 做上一次筛选条件存储，点击热门，切换课程分类时，筛选条件仍是热门

      // 清除条件为非价格时三角形图标样式
      this.$refs.spantop[0].className = "condtion-i i-top";
      this.$refs.spanbuttom[0].className = "condtion-i i-buttom";

      if (this.query_isup != query) {
        // 最开始 this.query_isup 为 -price  query 为 price
        this.query_isup = query; // 当筛选条件为hot或price时,赋值, this.query_isup已经为price
        // 价格升序
        if (query == "price") {
          // 当筛选条件为price时，
          this.$refs.spantop[0].className = "condtion-i i-top";
          this.$refs.spanbuttom[0].className = "condtion-i i-buttom active";
        }
      } else if (this.query_isup == query) {
        //this.query_isup = price  query = price
        if (query == "price") {  // 如果筛选条件为价格,做条件缓存
          // 价格降序
          this.query_isup = "-price"; // this.query_isup变为初始值

          // 修改三角形按钮样式
          this.$refs.spantop[0].className = "condtion-i i-top active";
          this.$refs.spanbuttom[0].className = "condtion-i i-buttom";
        } else {
          this.query_isup = query; // 如果筛选条件不为价格，为hot,做条件缓存
        }
      }

      this.$http
        .get(`/course?cid=${this.category_id}&query=${this.query_isup}`)
        .then(res => {
          this.courses = res.data;
        })
        .catch(error => {
          console.log(error.data);
        });
    },
    coursedetail(courseid) {
      console.log(courseid);
      this.$router.push({
        name: "CourseDetail",
        params: { detailId: courseid }
      });
    }
  },
  created() {
    this.$http
      .get("/category")
      .then(res => {
        this.categorys = res.data;
        this.categorys.unshift({ id: 0, title: "全部" });
      })
      .catch(error => {
        console.log(error.data);
      });

    // 默认选中全部
    this.$http
      .get("/course?cid=" + 0)
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
  border: 1px solid #00b4e4;
}

.condition {
  display: flex;
  align-items: center;
  font-size: 16px;
  color: #888;
  letter-spacing: 0.36px;
  margin-top: 20px;
}

.condition ul {
  margin-top: 14px;
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

.condtion-span .i-top {
  content: "test";
  width: 0;
  border: 5px solid transparent;
  border-top-color: #d8d8d8;
  position: absolute;
  right: 0;
  bottom: 20.5px;
}

.condtion-span .i-buttom {
  content: "test";
  width: 0;
  border: 5px solid transparent;
  border-bottom-color: #d8d8d8;
  position: absolute;
  right: 0;
  top: 2.5px;
}

.condtion-span .i-top.active {
  border-top-color: #00b4e4;
}
.condtion-span .i-buttom.active {
  border-bottom-color: #00b4e4;
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
