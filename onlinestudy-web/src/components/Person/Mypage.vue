<template>
  <div class="box">
    <div class="mydata">
      <img src="https:////s2.ax1x.com/2019/04/14/AOaUqs.jpg" alt>
    </div>
    <div class="data-box">
      <el-form ref="form" :model="form" label-width="80px" v-model="labelPosition">
        <h3>我的资料</h3>
        <el-form-item label="姓名">
          <span>{{userInfo.username}}</span>
        </el-form-item>
        <el-form-item label="头像">
          <img :src="userInfo.avatar">
        </el-form-item>
        <el-form-item label="账户余额">
          <span>￥{{userInfo.balance}}</span>
        </el-form-item>
        <el-form-item label="学历">
          <el-select v-model="form.region" placeholder="请选择活动区域">
            <el-option label="大专" value="dazhuan"></el-option>
            <el-option label="本科" value="benke"></el-option>
            <el-option label="研究生" value="yanjiu"></el-option>
            <el-option label="博士" value="boshi"></el-option>
            <el-option label="硕士" value="shuoshi "></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="年龄">
          <el-input type="age" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="出生日期">
          <el-col :span="11">
            <el-date-picker
              type="date"
              placeholder="选择日期"
              v-model="form.date1"
              style="width: 100%;"
            ></el-date-picker>
          </el-col>
          <el-col class="line" :span="2">-</el-col>
          <el-col :span="11">
            <el-time-picker
              type="fixed-time"
              placeholder="选择时间"
              v-model="form.date2"
              style="width: 100%;"
            ></el-time-picker>
          </el-col>
        </el-form-item>
        <el-form-item label="立即学习">
          <el-switch v-model="form.delivery"></el-switch>
        </el-form-item>

        <el-form-item label="悉知平台">
          <el-checkbox-group v-model="form.type">
            <el-checkbox label="百度等搜索引擎" name="type"></el-checkbox>
            <el-checkbox label="新闻" name="type"></el-checkbox>
            <el-checkbox label="朋友介绍" name="type"></el-checkbox>
            <el-checkbox label="其他" name="type"></el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="教学形式">
          <el-radio-group v-model="form.resource">
            <el-radio label="线上,我自学能力很强"></el-radio>
            <el-radio label="线下,我需要学习氛围"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="自我介绍">
          <el-input type="textarea" v-model="form.desc"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="onSubmit">点我</el-button>
          <el-button>取消</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>





<script>
export default {
  name: "Mypage",
  data() {
    return {
      form: {
        name: "",
        region: "",
        date1: "",
        date2: "",
        delivery: false,
        type: [],
        resource: "",
        desc: ""
      },
      
      labelPosition: "right",
    };
  },

  methods: {
    loginHandler() {},
    onSubmit() {
      console.log("submit!");
    }
  },
  computed: {
    userInfo() {
      return this.$store.state.userInfo;
    }
  },
  created() {},

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
  margin-top: 200px;
  position: absolute;
  background: white;
  margin-left: 350px;
  padding: 30px;
}
.data-box img {
  width: 60px;
}

.el-form h3 {
  margin-top: 20px;
  margin-bottom: 20px;
}
</style>

