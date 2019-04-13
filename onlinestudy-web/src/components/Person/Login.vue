<template>
  <div class="box">
    <img src="http://wx1.sinaimg.cn/mw690/b099ab84gy1g213rb2t15j21hc0u0qko.jpg" alt>
    <div class="login">
      <div class="login-title">
        <p>机会永远只留给有准备的人</p>
        <br>
        <br>
      </div>
      <div class="login_box">
        <div class="title">
          <span>密码登录</span>
          <span>短信登录</span>
        </div>
        <div class="inp">
          <input v-model="username" type="text" placeholder="用户名 / 手机号码" class="user">
          <input v-model="password" type="password" name class="pwd" placeholder="密码">
          <div id="geetest"></div>
          <div class="rember">
            <p>
              <input type="checkbox" class="no" name="a">
              <el-checkbox v-model="checked">记住密码</el-checkbox>
            </p>
            <p>忘记密码</p>
          </div>
          <button class="login_btn" @click="loginHandler">登录</button>
          <p class="go_login">
            没有账号?
            <span @click="toRegister">立即注册</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      username: "",
      password: "",

      checked:'',
      validateResult: {} //验证成功之后返回的结果，它用于服务端sdk的二次验证
    };
  },

  methods: {
    loginHandler() {
      let params = {
        username: this.username,
        passwd: this.password,
        geetest_challenge: this.validateResult.geetest_challenge,
        geetest_validate: this.validateResult.geetest_validate,
        geetest_seccode: this.validateResult.geetest_seccode
      };
      this.$http
        .login(params)
        .then(res => {
          console.log(res);
          if (!res.error) {
            this.$router.push({
              name: "Home"
            });
            localStorage.setItem("access_token", res.data.data);
            localStorage.setItem("username", this.username);
            localStorage.setItem("avatar", res.data.avatar);
            localStorage.setItem("shop_cart_num", res.data.shop_cart_num);

            // dispacth action的行为
            this.$store.dispatch("getUserInfo", res.data);
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    getGeetest() {
      this.$http
        .geetest()
        .then(res => {
          console.log(res);
          let data = res
          var _this = this;
          //请检测data的数据结构， 保证data.gt, data.challenge, data.success有值
          initGeetest(
            {
              // 以下配置参数来自服务端 SDK
              gt: data.gt,
              challenge: data.challenge,
              offline: !data.success,
              new_captcha: true,
              product: "popup",
              width: "100%"
            },
            captchaObj => {
              // 这里可以调用验证实例 captchaObj 的实例方法
              captchaObj.appendTo("#geetest"); //将验证按钮插入到宿主页面中captchaBox元素内
              captchaObj
                .onReady(() => {
                  //your code
                })
                .onSuccess(() => {
                  var result = captchaObj.getValidate();
                  this.validateResult = result;
                  console.log(this);
                })
                .onError(() => {});
            }
          );
        })
        .catch(err => {
          console.log(err);
        });
    },
    toRegister(){
      this.$router.push({
        name:'Register'
      })
    }
  },
  created() {
    this.getGeetest();
  },
  mounted() {
    // 把顶部的导航栏去掉
    document
      .getElementsByClassName("el-container")[0]
      .setAttribute("style", "display:none");
  },
};
</script>

<style lang="css" scoped>
.box {
  width: 100%;
  position: relative;
}
.box img {
  width: 100%;
}
.box .login {
  position: absolute;
  width: 500px;
  height: 400px;
  top: 50%;
  left: 50%;
  margin-left: -250px;
  margin-top: -300px;  
  opacity: 0.9;
}
.login .login-title {
  width: 100%;
  text-align: center;
}
.login-title img {
  width: 190px;
  height: auto;
}
.login-title p {
  font-family: PingFangSC-Regular;
  font-size: 18px;
  color: #fff;
  letter-spacing: 0.29px;
  padding-top: 10px;
}
.login_box {
  width: 400px;
  height: auto;
  background: #fff;
  box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.5);
  border-radius: 4px;
  margin: 0 auto;
  padding-bottom: 40px;
}
.login_box .title {
  font-size: 20px;
  color: #9b9b9b;
  letter-spacing: 0.32px;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-around;
  padding: 50px 60px 0 60px;
  margin-bottom: 20px;
  cursor: pointer;
}
.login_box .title span:nth-of-type(1) {
  color: #4a4a4a;
  border-bottom: 2px solid #00b4e4;
}

.inp {
  width: 350px;
  margin: 0 auto;
}
.inp input {
  border: 0;
  outline: 0;
  width: 100%;
  height: 45px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  text-indent: 20px;
  font-size: 14px;
  background: #fff !important;
}
.inp input.user {
  margin-bottom: 16px;
}
.inp .rember {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  margin-top: 10px;
}
.inp .rember p:first-of-type {
  font-size: 12px;
  color: #4a4a4a;
  letter-spacing: 0.19px;
  margin-left: 22px;
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  /*position: relative;*/
}
.inp .rember p:nth-of-type(2) {
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: 0.19px;
  cursor: pointer;
}



.inp .rember p span {
  display: inline-block;
  font-size: 12px;
  width: 100px;
  /*position: absolute;*/
  /*left: 20px;*/
}
#geetest {
  margin-top: 20px;
}
.login_btn {
  width: 100%;
  height: 45px;
  background: #00b4e4;
  border-radius: 5px;
  font-size: 16px;
  color: #fff;
  letter-spacing: 0.26px;
  margin-top: 30px;
}
.inp .go_login {
  text-align: center;
  font-size: 14px;
  color: #9b9b9b;
  letter-spacing: 0.26px;
  padding-top: 20px;
}
.inp .go_login span {
  color: #00b4e4;
  cursor: pointer;
}
</style>
