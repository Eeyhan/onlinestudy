<template>
  <!-- element-ui -->
  <el-container>
    <el-header height="80px">
      <div class="header">
        <div class="nav-left">
          <img src="../../../static/images/student.png" alt>
        </div>
        <div class="nav-center">
          <ul>
            <li v-for="list in headerList" :key="list.id">
              <router-link :to="{name:list.name}">{{list.title}}</router-link>
            </li>
          </ul>
        </div>

        <!-- <el-dropdown> -->

        <div
          class="nav-right"
          v-if="userInfo.access_token"
          @mouseenter="enterHandler"
          @mouseleave="leaveHandler"
        >
          <!-- <span class="count" v-if="userInfo.shop_cart_num == 0">(0)</span>
          <span class="count" v-else>({{userInfo.shop_cart_num.length}})</span> -->
          <span class="count" @click="toShoppingCart"> <i class="el-icon-goods"></i> 购物车</span>
          <!-- <span class="el-dropdown-link">学习中心</span> -->
          <span class="user">{{userInfo.username}}</span>
          <img :src="userInfo.avatar" alt>
          <ul class="my_account" v-show="isShow">
            <li>
              我的账户
              <i>></i>
            </li>
            <li>
              我的优惠券
              <i>></i>
            </li>
            <li>
              我的消息
              <span class="msg">(40)</span>
              <i>></i>
            </li>
            <li @click="toOrder">
              我的账单
              
            </li>
            <li @click="logout">
              退出
              <i>></i>
            </li>
          </ul>
        </div>
        <!-- </el-dropdown> -->
        <div class="nav-right" v-else>
          <span @click="loginHander">登录</span>
          &nbsp;| &nbsp;
          <span @click="registerHander">注册</span>
        </div>
      </div>
    </el-header>
  </el-container>
</template>

<script>
export default {
  name: "BaseHeader",
  data() {
    return {
      headerList: [
        { id: "1", name: "Home", title: "首页" },
        { id: "2", name: "Course", title: "体验课程" },        
        { id: "3", name: "Degree", title: "学位课程" },
        { id: "4", name: "LightCourse", title: "线下面授" },
      ],
      isShow: false
    };
  },
  methods: {
    
    enterHandler() {
      this.isShow = true;
    },
    leaveHandler() {
      this.isShow = false;
    },
    loginHander() {
      this.$router.push({
        name: "Login"
      });
    },
    registerHander() {
      this.$router.push({
        name: "Register"
      });
    },

    toShoppingCart(){
      this.$router.push({
        name:'ShopCart'
      })
    },
  
    // 账单中心
    toOrder(){
      this.$router.push({
        name:'Order'
      })
    },

    // 退出
    logout() {
      this.$store.dispatch("deleteUserInfo");
      console.log(this.$store.state.isRemember);
      // 如果记住密码标志位为false就在退出的同时删除用户信息，否则就不删除
      if (!this.$store.state.isRemember) {
        localStorage.clear();
      }
    }
  },
  computed: {
    userInfo() {
      return this.$store.state.userInfo;
    }
  },

  watch: {
    $route(to, form) {
      // 从登录组件过来的，恢复导航栏显示
      if (form.path == "/Login") {
        document
          .getElementsByClassName("el-container")[0]
          .setAttribute("style", "");
      }
    }
  }

  // mounted() {
  //   console.log(document.getElementsByClassName("el-container")[0]);
  //   // 登录过来跳转的，把顶部的导航栏显示
  //   document
  //     .getElementsByClassName("el-container")[0]
  //     .setAttribute("style", "");
  // }
  
};
</script>

<style lang="css" scoped>
.el-header {
  border-bottom: #c9c9c9;
  box-shadow: 0 0.5px 0.5px 0 #e3e3e3;
}
.header {
  width: 1200px;
  height: 80px;
  line-height: 80px;
  margin: 0 auto;
}
.nav-left {
  float: left;
  margin-top: 10px;
}

.nav-left img {
  margin-top: 10px;
  width: 40px;
  height: 40px;
}
.nav-center {
  float: left;
  margin-left: 100px;
  width: "";
}
.nav-center ul {
  overflow: hidden;
}
.nav-center ul li {
  float: left;
  margin: 0 5px;
  /*width: 100px;*/
  padding: 0 20px;
  height: 80px;
  line-height: 80px;
  text-align: center;
}
.nav-center ul li a {
  color: #4a4a4a;
  width: 100%;
  height: 60px;
  display: inline-block;
}
.nav-center ul li a:hover {
  color: #b3b3b3;
}
.nav-center ul li a.is-active {
  color: #4a4a4a;
  border-bottom: 4px solid #409eff;
}
.nav-right {
  float: right;
  position: relative;
  z-index: 100;
}
.nav-right span {
  cursor: pointer;
}
.nav-right .user {
  margin-left: 15px;
}
.nav-right img {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  display: inline-block;
  vertical-align: middle;
  margin-left: 15px;
}
.nav-right ul {
  position: absolute;
  width: 221px;
  z-index: 100;
  font-size: 12px;
  top: 80px;
  background: #fff;
  border-top: 2px solid #d0d0d0;
  box-shadow: 0 2px 4px 0 #e8e8e8;
}
.nav-right ul li {
  height: 40px;
  color: #4a4a4a;
  padding-left: 30px;
  padding-right: 20px;
  font-size: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  transition: all 0.2s linear;
}
.nav-right ul li span.msg {
  margin-left: -80px;
  color: red;
}
.nav-right ul li span.count {
  margin-left: -100px;
  color: red;
}
</style>
