<template>
  <div class="person-wrap">
    <img src="http://wx1.sinaimg.cn/mw690/b099ab84gy1g213rb2t15j21hc0u0qko.jpg" alt>
    <div class="person">
      <h3 style=" text-indent: 70px;">机会永远只留给有准备的人</h3>
      <br>
      <br>
      <el-form
        :model="ruleForm"
        status-icon
        :rules="rules"
        ref="ruleForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <el-form-item label="昵称" prop="name">
          <el-input type="text" v-model="ruleForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pass">
          <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input type="password" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="邀请码" prop="invitation">
          <el-input type="text" v-model="ruleForm.invitation" autocomplete="off" placeholder="选填"></el-input>
        </el-form-item>
        <el-form-item id="embed-captcha" style="margin-left: 100px;" prop="geetest"></el-form-item>
        <p id="wait" class="show" ref="wait">正在加载验证码......</p>
        <p id="notice" class="hide" ref="notice">请先拖动验证码到相应位置</p>
        <br>

        <el-form-item>
          <el-button type="primary" @click="submitForm('ruleForm')" ref="btn">点我注册</el-button>
          <el-button @click="toLogin">已有账号？</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>


<script>
export default {
  name: "Login_Register",
  data() {
    var checkName = (rule, value, callback) => {
      if (!value) {
        return callback(new Error("昵称不能为空"));
      }
    };
    var validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
      } else {
        if (this.ruleForm.checkPass !== "") {
          this.$refs.ruleForm.validateField("checkPass");
        }
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请再次输入密码"));
      } else if (value !== this.ruleForm.pass) {
        callback(new Error("两次输入密码不一致!"));
      } else {
        callback();
      }
    };
    return {
      validateResult: "",
      ruleForm: {
        name: "",
        pass: "",
        checkPass: "",
        invitation: ""
      },
      rules: {
        pass: [{ validator: validatePass, trigger: "blur" }],
        checkPass: [{ validator: validatePass2, trigger: "blur" }],
        name: [{ validator: checkName, trigger: "blur" }]
      }
    };
  },
  methods: {
    submitForm(formName) {
      let params = {
        username: this.name,
        passwd: this.pass,
        geetest_challenge: this.validateResult.geetest_challenge,
        geetest_validate: this.validateResult.geetest_validate,
        geetest_seccode: this.validateResult.geetest_seccode
      };
      this.$http
        .userLogin(params)
        .then(res => {
          console.log(res);
          if (res.error_no === 0) {
            this.$router.push({
              name: "Home"
            });
            localStorage.setItem("access_token", res.data.access_token);
            localStorage.setItem("username", res.data.username);
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
    toLogin() {
      this.$router.push({
        name: "Login"
      });
    },

    // 获取极验验证码
    geetest() {
      this.$http.geetest().then(data => {
        var that = this;
        console.log(data)
        initGeetest(
          {
            gt: data.gt,
            challenge: data.challenge,
            product: "embed", // 产品形式，包括：float，embed，popup。注意只对PC版验证码有效
            offline: !data.success // 表示用户后台检测极验服务器是否宕机，一般不需要关注
            // 更多配置参数请参见：http://www.geetest.com/install/sections/idx-client-sdk.html#config
          },
          function(captchaObj) {
            let validate = captchaObj.getValidate();
            if (!validate) {
              that.$refs.notice.className = "show";
              setTimeout(function() {
                that.$refs.notice.className = "hide";
              }, 2000);
              that.$refs.btn.preventDefault;
            }
            // 将验证码加到id为captcha的元素里，同时会有三个input的值：geetest_challenge, geetest_validate, geetest_seccode
            console.log(captchaObj);
            captchaObj.appendTo("#embed-captcha");
            captchaObj.onReady(function() {
              that.$refs.wait.className = "hide";
            });
            // 更多接口参考：http://www.geetest.com/install/sections/idx-client-sdk.html
          }
        );
      });
    }
  },

  mounted() {
    // 把顶部的导航栏去掉
    document
      .getElementsByClassName("el-container")[0]
      .setAttribute("style", "display:none");
  },
  created() {
    this.geetest();
  }
};
</script>

<style lang="css" scoped>
.person-wrap {
  position: relative;
}

.person-wrap img {
  width: 100%;
  position: absolute;
  left: 0;
}

.person {
  width: 400px;
  /* margin: 0 auto; */
  padding-top: 40px;
  background: white;
  opacity: 0.9;
  padding-right: 44px;
  position: absolute;
  left: 35%;
  /* top: 20%; */
  margin-top: 10%;
  border-radius: 4px;
}

.inp {
  border: 1px solid gray;
  padding: 0 10px;
  width: 200px;
  height: 30px;
  font-size: 18px;
}

.btn {
  border: 1px solid gray;
  width: 100px;
  height: 30px;
  font-size: 18px;
  cursor: pointer;
}

#embed-captcha {
  width: 300px;
  margin: 0 auto;
}

.show {
  display: block;
}

.hide {
  display: none;
}

#notice {
  color: red;
}

/* 可自行设计实现captcha的位置大小 */
.popup-mobile {
  position: relative;
}

#popup-captcha-mobile {
  position: fixed;
  display: none;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  -webkit-transform: translate(-50%, -50%);
  z-index: 9999;
}
</style>
