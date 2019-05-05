<template>
  <div>
    <div class="box">
      <div class="mydata">
        <img src="https:////s2.ax1x.com/2019/04/14/AOaUqs.jpg" alt>
      </div>
      <div class="data-box">
        <h3>请输入您遇到的问题:</h3>
        <br>
        <el-input type="textarea" :rows="10" v-model="question"></el-input>
        <el-button
          type="primary"
          size="small"
          @click="quesitonHandler"
          style="float: right;margin-top: 5px;"
        >提交</el-button>
      </div>
      <div class="data-box answer">
        <h3>我提过的问题</h3>
        <br>
        <div v-for="(item,index) in answeredQuestion" :key="index" class="content">
          <p>Q：{{item.question}} -- {{item.question_date}}</p>

          <p v-if="item.answer">A：{{item.answer}}</p>
          <p v-else class='noanswer'>骚年，请等一等，导师正在马不停蹄的赶来！~</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "solvequestion",
  data() {
    return {
      question: "",
      answeredQuestion: ""
    };
  },

  methods: {
    quesitonHandler() {
      let params = {
        question: this.question
      };
      this.$http.question(params).then(res => {
        this.$message({
          type: "success",
          message: res.data,
          center: true
        });
        this.question = "";
      });
    },
    myQuestionList() {
      this.$http.questionList().then(res => {
        this.answeredQuestion = res;
      });
      console.log(this.answeredQuestion);
    }
  },

  created() {
    this.myQuestionList();
  },

  mounted() {}
};
</script>

<style lang="css" scoped>
.box {
  position: relative;
  min-height: 1000px;
}
.mydata {
  position: absolute;
}

.mydata img {
  opacity: 0.8;
  width: 100%;
}
.data-box {
  margin-top: 200px;
  position: absolute;
  background: white;
  margin-left: 200px;
  padding: 30px;
  width: 800px;
  box-shadow: 1px 2px 6px 1px #dfdcdc;
}

.data-box h3 {
  text-align: left;
}
.data-box img {
  width: 60px;
}

.el-form h3 {
  margin-top: 20px;
  margin-bottom: 20px;
}

.answer {
  margin-top: 600px;
  text-align: left;
}
.answer p {
  margin-bottom: 10px;
}

.content {
  border-bottom: 1px solid #f4f4f4;
  padding: 10px;
  background: #e9f0f4;
  border-radius: 6px;
  margin-bottom: 20px;
}
.noanswer{
  color: #a2a2a2;
  text-indent: 25px;
}
</style>

