<template>
  <div class="course-detail-text">
    <div v-if="courseinfo">
      <h3>课程背景</h3>
      <p>{{courseinfo.why_study}}</p>

      <h3>学前准备</h3>
      <p>{{courseinfo.prerequisite}}</p>

      <h3>课程概述</h3>
      <p>{{courseinfo.brief}}</p>

      <h3>适合人群</h3>
      <p>{{courseinfo.object_person}}</p>

      <h3>课程覆盖知识点</h3>
      <p>{{courseinfo.point}}</p>

      <h3>课程特点</h3>
      <p>{{courseinfo.feature}}</p>

      <h3>课程大纲</h3>
      <p v-for='(outline,index) in courseinfo.course_outline' :key='index'>
              {{outline.content}}</p>

      <h3>学完收获</h3>
      <p>{{courseinfo.harvest}}</p>
    </div>
    <div v-else></div>

    <div v-if="coursechapter">
      <ul v-for="chapter in coursechapter" :key="chapter.id">
        <h3>{{chapter.title}}</h3>
        <li v-for="(item,index) in chapter.chapter_lesson" :key="item.id">
          <p>
            第{{index+1}}节 - {{item.title}}
            <el-button size="mini" type="success" round v-if="item.free_trail">可试看</el-button>
          </p>
        </li>
      </ul>
    </div>
    <div v-else></div>

    <div v-if="coursecomment">
      <li v-for="item in coursecomment" :key="item.id">
        <h3>{{item.account}} - {{item.comment_date}}</h3>
        <p>{{item.content}}</p>
      </li>
    </div>
    <div v-else></div>

    <div v-if="Coursequestion">
      <li v-for="item in Coursequestion" :key="item.id">
        <h3>{{item.question}}</h3>
        <p>{{item.answer}}</p>
      </li>
    </div>
    <div v-else></div>
  </div>
</template>

<script>
export default {
  name: "CourseDetailTab",
  data() {
    return {
      msg: "",
      courseinfo: "",
      coursechapter: "",
      coursecomment: "",
      Coursequestion: ""
    };
  },
  created() {
    this.routerHander();
  },
  methods: {
    // 课程概述接口
    getcourseDetailInfo() {
      this.$http
        .courseDetail(this.$route.params.detailId)
        .then(res => {
          if (!res.error) {
            this.courseinfo = res.data[0];
            console.log(this.courseinfo);
          }
        })
        .catch(error => {
          error.error;
        });
    },
    // 课程章节接口
    getcourseDetailChapter() {
      this.$http
        .chapter(this.$route.params.detailId)
        .then(res => {
          if (!res.error) {
            this.coursechapter = res.data;
            console.log(this.coursechapter);
          }
        })
        .catch(error => {
          error.error;
        });
    },

    // 课程评论接口
    getcourseDetailComment() {
      this.$http
        .comment(this.$route.params.detailId)
        .then(res => {
          if (!res.error) {
            this.coursecomment = res.data;
            console.log(this.coursecomment);
          }
        })
        .catch(error => {
          error.error;
        });
    },
    // 课程常见问题接口
    getcourseDetailQuestion() {
      this.$http
        .commonquestion(this.$route.params.detailId)
        .then(res => {
          if (!res.error) {
            this.Coursequestion = res.data;
            console.log(this.Coursequestion);
          }
        })
        .catch(error => {
          error.error;
        });
    },
    routerHander() {
      if (this.$route.query.sub == "overview") {
        this.coursechapter = "";
        this.coursecomment = "";
        this.Coursequestion = "";
        this.getcourseDetailInfo();
        this.msg = "";

        //课程章节
      } else if (this.$route.query.sub == "chapter") {
        this.courseinfo = "";
        this.coursecomment = "";
        this.Coursequestion = "";
        this.getcourseDetailChapter();
        //课程评价
      } else if (this.$route.query.sub == "comment") {
        this.courseinfo = "";
        this.coursechapter = "";
        this.Coursequestion = "";
        this.getcourseDetailComment();
        //常见问题
      } else if (this.$route.query.sub == "question") {
        this.courseinfo = "";
        this.coursechapter = "";
        this.coursecomment = "";
        this.getcourseDetailQuestion();
      }
    }
  },

  watch: {
    $route(to, form) {
      // 课程概述
      console.log(to);
      console.log(form);
      this.routerHander();

      //   if (this.$route.query.sub === "overview") {
      //     this.msg = `<h3>课程背景</h3>
      // 			<p>{{details.why_study}}</p>

      // 			<h3>学前准备</h3>
      // 			<p>{{details.prerequisite}}</p>

      // 			<h3>课程概述</h3>
      // 			<p>{{details.brief}}</p>

      // 			<h3>适合人群</h3>
      // 			<p>{{details.object_person}}</p>

      // 			<h3>课程覆盖知识点</h3>
      // 			<p>{{details.point}}</p>

      // 			<h3>课程特点</h3>
      // 			<p>{{details.feature}}</p>

      // 			<h3>课程大纲</h3>
      // 			<p>{{details.course_outline}}</p>

      // 			<h3>学完收获</h3>
      // 			<p>{{details.harvest}}</p>`;
      //   }
    }
  }
};
</script>

<style lang="css" scoped>
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
li {
  list-style-type: none;
}
</style>
