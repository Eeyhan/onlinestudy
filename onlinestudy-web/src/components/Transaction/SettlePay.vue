<template>
  <div class="shopping-cart-wrap">
    <h3 class="shopping-cart-tit">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <router-link :to="{ path: '/ShopCart' }">我的购物车</router-link> > 
        <router-link :to="{ path: '/Coupon' }">领券中心</router-link> > 
        <router-link :to="{ path: '/SettlePay' }">结算中心</router-link>
      </el-breadcrumb>
      <p>您即将获得最好的服务，最好的教育方式</p>
    </h3>
    <div class="row">
      <el-table
        ref="multipleTable"
        :data="settlements"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column label="课程" width="555">
          <template slot-scope="scope">
            <img :src="scope.row.course_img" alt>
            <a href="javascript:void(0);">{{ scope.row.title}}</a>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="有效期" width="212">
          <template slot-scope="scope">{{scope.row.valid_period_display}}</template>
        </el-table-column>
        <el-table-column prop="address" label="单价" show-overflow-tooltip>
          <template slot-scope="scope">¥{{scope.row.price}}</template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="120">
          <template slot-scope="scope">
            <el-button
              @click.native.prevent="deleteRow(scope.$index, settlements)"
              type="text"
              size="small"
            >取消订单</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div style="text-align: right; margin-top: 30px">
      <div id="accordion">
        <div
          style="text-align: left; display: flex;padding-bottom: 22px;padding-left:30px;border-bottom: 1px solid #e8e8e8"
        >
          <div style="display: flex">
            <span class="select-coupon">使用优惠劵：</span>

            <img
              class="sign"
              src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAqCAMAAADCkShIAAAAflBMVEUAAABZV1ddW1u5uLje3d2BgIBbWVnf39/c29v+/v78/Pz39/ecm5t5d3daWFj7+/uioaFzcXFsa2tfXV3x8fHt7e3q6urX1tbKycnEw8PBwMC7urqnpqaZl5eTkpKRj4+NjIyKiYl/fX3R0dHPzs60s7OxsLCsq6uGhISEgoLZdRcuAAAAAXRSTlMAQObYZgAAAMRJREFUSMftldkKwjAQRXOqVrta7b641f3/f9AUKliKNgERH3qfsszJhJkLIww9hcJES4Y+4EM+VVTRZpgLRS1GYASUgcC1ujHWpvoAWC5s7dd4ewfue2B5APZLIboHdg/oPMjNeW6dO52UfUB+GahbwqkB1xqoUgB4UbOKPCAYLmsFrGIh4hVwVenDpSGSZA2c1Ro38WEt4/1StdOFiZSZq1sjM+RVpuOlUxge9cyXpv9i7xH4EuCDN1OUJ4EfTNGJnsoHRqYNbYhMgeoAAAAASUVORK5CYII="
              width="20"
              height="20"
              alt
              @click="isShowHander"
            >

            <span class="coupon-num" v-if="countCoupon != 0">对应商品有{{countCoupon}}张可用</span>
            <span class="coupon-num" v-else>对应商品有0张可用</span>
          </div>

          <p class="sum-price-wrap" style="margin-right: 45px">
            商品总金额：
            <span class="sum-price">{{totalPrice}}元</span>
          </p>
        </div>
      </div>

      <div
        v-if="isShow"
        style="text-align: left;"
        id="collapseOne"
        class="panel-collapse out collapse in"
        aria-expanded="true"
      >
        <ul class="coupon-list" style="display: none;"></ul>
        <div
          v-if="countCoupon == 0"
          style="text-align: center;width: 1200px;padding: 50px 0px;align-items: center;justify-content: center;border-bottom: 1px solid rgb(232, 232, 232);margin: 0 auto;"
        >
          <span style="font-size: 16px; color: #9b9b9b">暂无可用优惠券</span>
          <router-link :to="{name:'Coupon'}" style="font-size: 16px; ">领取优惠券</router-link>
        </div>
        <div v-else style="margin: 20px auto;width: 800px;text-align: center;">
          <!-- 优惠券逻辑 -->
          <el-table
            ref="multipleTable"
            :data="coupon"
            @selection-change="handleSelectionChange1"
            tooltip-effect="dark"
            style="width: 100%"
          >
            <el-table-column
              type="selection"
              width="55"
              @click.native.prevent="useRow(scope.$index, golbalCoupon)"
            ></el-table-column>
            <el-table-column label="专项优惠券名(优惠券请对应指定商品使用,不能叠加)" width="400">
              <template slot-scope="scope">
                <span>{{ scope.row.title}}</span>
              </template>
            </el-table-column>

            <!-- <el-table-column label width="200">
              <template slot-scope="scope">
                <span @click="userROw(scope.$index, coupon)">
                  <el-checkbox>选择</el-checkbox>
                </span>
              </template>
            </el-table-column>-->
          </el-table>

          <el-table
            ref="multipleTable"
            :data="golbalCoupon"
            tooltip-effect="dark"
            style="width: 100%"
            @selection-change="handleSelectionChange2"
          >
            <el-table-column
              type="selection"
              width="55"
              @click.native.prevent="useRow(scope.$index, golbalCoupon)"
            ></el-table-column>
            <el-table-column label="通用优惠券(可和专项优惠券叠加使用)" width="400">
              <template slot-scope="scope">
                <span>{{ scope.row.title}}</span>
              </template>
            </el-table-column>
            <!-- <el-table-column label width="200">
              <template slot-scope="scope">
                <span @click="userROw(scope.$index, golbalCoupon)">
                  <el-checkbox>选择</el-checkbox>
                </span>
              </template>
            </el-table-column>-->
          </el-table>
          <!-- 优惠券逻辑 -->
        </div>
      </div>
      <div
        style="height: 30px; margin-top: 40px; display: flex; align-items: center; justify-content: flex-end ;margin-right: 36px;"
      >
        <input type="checkbox" class="ok" id="color-input-red">
        <label for="color-input-red">
          <img
            src="data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iMTFweCIgaGVpZ2h0PSI5cHgiIHZpZXdCb3g9IjAgMCAxMSA5IiB2ZXJzaW9uPSIxLjEiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiPgogICAgPCEtLSBHZW5lcmF0b3I6IFNrZXRjaCA0OS4zICg1MTE2NykgLSBodHRwOi8vd3d3LmJvaGVtaWFuY29kaW5nLmNvbS9za2V0Y2ggLS0+CiAgICA8dGl0bGU+5Yu+6YCJPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGRlZnM+PC9kZWZzPgogICAgPGcgaWQ9IumAgumFjU3pobUyIiBzdHJva2U9Im5vbmUiIHN0cm9rZS13aWR0aD0iMSIgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj4KICAgICAgICA8ZyBpZD0i5o+Q5Lqk6K6i5Y2VIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMzM4LjAwMDAwMCwgLTQyMi4wMDAwMDApIiBmaWxsPSIjRkZGRkZGIj4KICAgICAgICAgICAgPGcgaWQ9IkNoZWNrYm94LUNvcHkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDMzMi4wMDAwMDAsIDQxNC4wMDAwMDApIj4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0xMC4wNzc0NjQ3LDEwLjgyMTM3MSBMMTUuMzYwNDQ5NCwxNi4xMDQzNTU3IEMxNS41NTU1OTAyLDE2LjI5OTQ5NjUgMTUuNTU2NDcwOCwxNi42MTUwMDE2IDE1LjM1NTgxMDIsMTYuODE1NjYyMSBMMTQuOTQwMzg1LDE3LjIzMTA4NzQgQzE0Ljc0MjY4MjEsMTcuNDI4NzkwMyAxNC40Mjg3Nzc4LDE3LjQzNTQyNTggMTQuMjI5MDc4NSwxNy4yMzU3MjY1IEw4LjE4NzExODU4LDExLjE5Mzc2NjYgQzguMDc5MzUwNDgsMTEuMDg1OTk4NSA4LjAzMDgyOTYyLDEwLjk0MTUyMDYgOC4wNDI3ODIzNCwxMC43OTk5NDk3IEM4LjA0MjQ1NjUsMTAuNjcyNTEyOSA4LjA4OTMwMDA2LDEwLjU0Njc5MzkgOC4xODE0NjU5OCwxMC40NTQ2MjggTDExLjI1MzU2ODcsNy4zODI1MjUzMyBDMTEuNDQ1NTg3Niw3LjE5MDUwNjM3IDExLjc1ODU2Miw3LjE5MjE1NjUyIDExLjk1OTIyMjYsNy4zOTI4MTcwNiBMMTIuMzc0NjQ3OCw3LjgwODI0MjI5IEMxMi41NzIzNTA3LDguMDA1OTQ1MjEgMTIuNTcwNzM3Myw4LjMyODA5ODM1IDEyLjM4NDkzOTUsOC41MTM4OTYxOCBMMTAuMDc3NDY0NywxMC44MjEzNzEgWiIgaWQ9IuWLvumAiSIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTEuNzczNzg0LCAxMi4zMTE0MjMpIHJvdGF0ZSgtOTAuMDAwMDAwKSB0cmFuc2xhdGUoLTExLjc3Mzc4NCwgLTEyLjMxMTQyMykgIj48L3BhdGg+CiAgICAgICAgICAgIDwvZz4KICAgICAgICA8L2c+CiAgICA8L2c+Cjwvc3ZnPgo="
            alt
          >
        </label>
        <p class="discount-num" style="color:#9B9B9B ">使用我的账户余额</p>
        <p class="discount-num" style="margin-right: 45px ">
          <span style="display: none;">可用0个已抵扣 ￥0</span>
        </p>
      </div>
      <p class="sun-coupon-num" style="margin-right: 45px;margin-bottom: 43px;margin-right: 79px;">
        优惠券抵扣：
        <span>0元</span>
      </p>
    </div>

    <div class="payinfo">
      <p style="margin-top: 20px;margin-left:28px">支付方式：</p>
      <div @click="checkedHander(imgIsShow1)">
        <img
          src="http://127.0.0.1:8000/media/check.png"
          style=" position: absolute; top: -12px; right: -10px; width: 25px;"
          v-if="imgIsShow1"
        >
        <img src="http://127.0.0.1:8000/media/alipay.png">
      </div>
      <div @click="checkedHander(imgIsShow2)">
        <img
          v-if="imgIsShow2"
          src="http://127.0.0.1:8000/media/check.png"
          style=" position: absolute; top: -12px; right: -10px; width: 25px;"
        >
        <img src="http://127.0.0.1:8000/media/wechat.png">
      </div>
    </div>

    <div class="total">
      <form method="post" action="http://127.0.0.1:8000/api/v1/pay/pay/">
      <!-- <el-button type="primary" @click="toPayment(totalPrice)">立即支付</el-button>

      <h3>总计: ¥{{totalPrice}}</h3>-->
      <label for="money">总计：￥</label>
      <el-input type="text" name="money" :value="totalPrice" id="money"></el-input>
      <el-button type="primary" native-type="submit" @click="onsumbit">立即支付</el-button>
      </form>
    </div>
    <router-view></router-view>

    <el-pagination background layout="prev, pager, next" :total="80"></el-pagination>
  </div>
</template>
<script>
export default {
  name: "SettlePay",
  data() {
    return {
      settlements: [], // 结算(订单)中心数据
      golbalCoupon: [], // 全局优惠券
      coupon: [], // 专项优惠券
      multipleSelection: [], //存放选中的当前商品数据
      multipleSelection1: [], // 存放选中的当前专项优惠券数据
      multipleSelection2: [], // 存放选中的当前通用优惠券数据
      isShow: false, // 优惠券区域展开标志位
      imgIsShow1: true, //支付方式的图标
      imgIsShow2: false,
      use_coupon_id: {}, // 用户选择的专项优惠券ID
      course_id: [] //课程id
    };
  },
  computed: {
    totalPrice() {
      let total = 0;
      this.multipleSelection1.forEach((item, index) => {
        this.multipleSelection.forEach((course_item, index) => {
          // 找到商品对应的优惠券
          if (course_item.id == item.object_id) {
            // 满减券
            if (item.coupon_type == 2) {
              total -= parseFloat(item.equal_money);
            } else if (item.coupon_type == 1) {
              // //折扣券
              total -= course_item.price * (1 - item.off_percent / 100);
            }
          }
        });
      });

      // 通用券
      this.multipleSelection2.forEach((item, index) => {
        total -= parseFloat(item.equal_money);
      });

      this.multipleSelection.forEach((item, index) => {
        total += parseFloat(item.price);
      });

      return total.toFixed(2);
    },

    countCoupon() {
      let total = 0;
      if (this.coupon != []) {
        total += this.coupon.length;
      }
      if (this.golbalCoupon != []) {
        total += this.golbalCoupon.length;
      }
      return total;
    }
  },
  methods: {
    // 获取订单中心数据
    getSettlement() {
      //
      // // 先获取用户的优惠券
      // this.getUserCoupon();
      this.$http.settlementList().then(res => {
        if (!res.error) {
          this.settlements = res.data.settlement_info;

          // // 全局的优惠券
          // let global_coupon_dict = Object.values(res.data.global_coupon_dict);
          // console.log(global_coupon_dict)
          // if (global_coupon_dict.length != 0) {
          //   this.golbalCoupon = global_coupon_dict;
          // }

          this.settlements.forEach((item, index) => {
            this.course_id.push(item.id);
          });

          //  当前用户获得的优惠券
          this.getUserCoupon();
        }
      });
    },

    deleteRow(index, rows) {
      console.log(index, rows);
      this.$confirm("你确定要取消订单吗？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        center: true
      }).then(() => {
        let params = {
          course: parseInt(rows[index].id)
        };
        this.$http.delSettlement(params).then(res => {
          if (!res.error) {
            this.$message({
              message: ` ${res.data}`,
              center: true
            });

            // 先删除后端的数据再删除前端数据
            rows.splice(index, 1);
          }
        });
      });
    },

    // 支付方式切换
    checkedHander(imgIsShow) {
      if (this.imgIsShow1 == imgIsShow) {
        this.imgIsShow1 = !this.imgIsShow1;
        this.imgIsShow2 = !this.imgIsShow2;
      } else if (this.imgIsShow2 == imgIsShow) {
        this.imgIsShow1 = !this.imgIsShow1;
        this.imgIsShow2 = !this.imgIsShow2;
      }
    },
    isShowHander() {
      this.isShow = !this.isShow;
    },

    // 计算加入的订单中心数据
    handleSelectionChange(val) {
      this.multipleSelection = val;
    },

    // 计算加入的订单中心数据
    handleSelectionChange1(val) {
      this.multipleSelection1 = val;
    },

    // 计算加入的订单中心数据
    handleSelectionChange2(val) {
      this.multipleSelection2 = val;
    },

    // 获取用户优惠券，并筛选出当前结算中心里的商品对应的优惠券
    getUserCoupon() {
      this.$http.userCouponList().then(res => {
        // console.log(res);
        this.course_id.forEach((id, index) => {
          for (let coupon in res.data) {
            if (res.data[coupon].object_id == id) {
              this.coupon.push(res.data[coupon]);
            }
          }
        });
        // 单独取全局优惠券，防止两层for循环出现重复数据
        for (let coupon in res.data) {
          if (res.data[coupon].object_id == null) {
            // 全局优惠券
            this.golbalCoupon.push(res.data[coupon]);
          }
        }
      });
    },

    // // 选择使用优惠券
    // userROw(index, rows) {
    //   console.log(index,rows)
    //   if (rows[index].object_id == null) {
    //     this.use_coupon_id["global_coupon"] = rows[index].id;
    //   } else {
    //     this.use_coupon_id[rows[index].object_id] = {
    //       course: rows[index].object_id,
    //       coupon: rows[index].id
    //     };
    //   }
    // },

    // 点击按钮时，一边页面跳转到支付宝支付页面，一边这里后台自动发出支付请求
    // 支付
    onsumbit(totalPrice) {
      // 支付之前，先更新后端的结算中心数据，提交优惠券数据
      // 选择优惠券有三个情况，第一个是当前用户没有选择优惠券，第二个情况是当前用已选择优惠券，第三个情况是更改优惠券

      // 专项优惠券
      if (this.multipleSelection1.length !== 0) {
        this.multipleSelection1.forEach((item1, index) => {
          // 增删改查
          this.multipleSelection.forEach((item, index) => {
            // 最开始的从无到有的选择情况
            this.use_coupon_id[item1.object_id] = {
              course: item1.object_id,
              coupon: item1.id
            };
          });
        });
      } else {
        // 优惠券全部未选中，或全部去掉
        this.multipleSelection.forEach((item, index) => {
          delete this.use_coupon_id[item.id];
        });
      }

      // 全局，通用优惠券
      if (this.multipleSelection2.length !== 0) {
        this.multipleSelection2.forEach((item, index) => {
          this.use_coupon_id["global_coupon"] = item.id;
        });
      } else {
        this.multipleSelection.forEach((item, index) => {
          delete this.use_coupon_id["global_coupon"];
        });
      }
      let params = {
        balance: 0,
        price: this.totalPrice
      };
      console.log(this.use_coupon_id);
      if (JSON.stringify(this.use_coupon_id) !== "{}") {
        // 使用优惠券
        let settleparams = this.use_coupon_id;

        this.$http.Updatesettlement(settleparams).then(res => {
          console.log(res);
          if (!res.error) {
            // 支付
            this.$http.Payment(params).then(res => {
              console.log(res);
            });          
          }
        });
      } else {
        this.$http.Payment(params).then(res => {
          console.log(res);
        });
      }
    }
  },

  created() {
    this.getSettlement();
  }
};
</script>

<style scoped>
.shopping-cart-wrap {
  width: 100%;
}
.shopping-cart-wrap h3,
.row {
  width: 1200px;
  margin: 0 auto;
}
.shopping-cart-wrap h3 {
  padding: 50px 0;
}
.el-table .warning-row {
  background: #22c8c5;
}
.cell img {
  vertical-align: middle;
  width: 170px;
}
.cell a {
  color: #000;
  margin-left: 30px;
}
select {
  border: 0;
  outline: none;
  font-size: 12px;
  color: #666;
  line-height: 18px;
  width: 117px;
  height: 28px;
  padding-left: 16px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
}
.total {
  width: 1200px;
  margin: 0 auto;
  margin-bottom: 100px;
  /*display: flex;*/
  /*justify-content:flex-end;*/
}
.shopping-cart-wrap .total button {
  float: right;
  margin-top: 20px;
}

.shopping-cart-wrap .total h3 {
  padding: 0;
  float: right;
  width: 100px;
  height: 30px;
  margin-top: 30px;
  color: red;
}

.coupon-num {
  height: 22px;
  line-height: 22px;
  padding: 0 5px;
  text-align: center;
  margin-left: 14px;
  font-family: PingFangSC-Regular;
  font-size: 12px;
  color: #fff;
  letter-spacing: 0.27px;
  display: inline-block;
  background: #fa6240;
  border-radius: 2px;
  margin-left: 20px;
}

.select-coupon {
  color: #666;
  font-size: 16px;
}
.sum-price-wrap {
  display: inline-block;
  margin-left: auto;
  font-size: 16px;
  color: #4a4a4a;
}
#accordion {
  width: 1200px;
  margin: 0 auto;
}
.payinfo {
  display: flex;
  margin: 0 auto;
  width: 1200px;
}

.payinfo img {
  width: 40px;
}

.payinfo div {
  border: 1px solid #3a8ee6;
  text-align: center;
  margin-left: 20px;
  width: 63px;
  border-radius: 13px;
  padding: 3px;
  position: relative;
}

.el-breadcrumb {
  margin-left: 40px;
  width: 222px;
  color: #22c8c5;
}

.el-breadcrumb a {
  color: #409eff;
}

form {
  width: 1200px;
  margin: 0 auto;
  position: relative;
}

form label {
  position: absolute;
  margin-left: 350px;
  margin-top: 31px;
}
.el-input {
  margin-left: 391px;
  min-width: 96px;
  position: absolute;
  margin-top: 20px;
  font-size: 19px;
  max-width: 100px;
}

.el-input input {
  color: red;
}
</style>

