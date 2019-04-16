<template>
  <div class="shopping-cart-wrap">
    <h3 class="shopping-cart-tit">
      我的订单 &nbsp;
      <small>共{{this.settlementProduct.length}}门课程</small>
    </h3>
    <div class="row">
      <el-table
        ref="multipleTable"
        :data="settlementProduct"
        tooltip-effect="dark"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column label="课程" width="400">
          <template slot-scope="scope">
            <img :src="scope.row.course_img" alt>
            <a href="javascript:void(0);">{{ scope.row.title}}</a>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="有效期" width="240">
          <template slot-scope="scope">
            {{scope.row.valid_period_display}}(此处不能修改套餐)            
          </template>
        </el-table-column>
        <el-table-column prop="address" label="单价" show-overflow-tooltip width="120">
          <template slot-scope="scope">¥{{scope.row.price}}</template>
        </el-table-column>

        <el-table-column prop="name" label="订单号" width="120">
          <template slot-scope="scope">
            {{scope.row.valid_period_display}}          
          </template>
        </el-table-column>

        <el-table-column prop="name" label="收货地址" width="120">
          <template slot-scope="scope">
            {{scope.row.valid_period_display}}          
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="操作" width="120">
          <template slot-scope="scope">
            <el-button
              @click.native.prevent="deleteRow(scope.$index, settlementProduct)"
              type="text"
              size="small"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <div class="total">
      <el-button type="primary" @click="buy()">去支付</el-button>
      <h3>总计: ¥{{totalPrice}}</h3>
    </div>
  </div>
</template>

<script>
export default {
  name: "Payment",
  data() {
    return {
      multipleSelection: [], //存放选中的当前数据
      currentVal: "",
      PaymentOrder: [], // 结算中心订单
      global_coupon_dict:'',// 全局的优惠券
      course_coupon_dict:'',// 专项的优惠券
    };
  },
  computed: {
    totalPrice() {
      let total = 0;
      this.multipleSelection.forEach((item, index) => {
        total += parseFloat(item.price);
      });
      console.log(total);
      return total.toFixed(2);
    }
  },
  methods: {
    // 删除课程
    deleteRow(index, rows) {
      this.$confirm("你确定要删除该订单吗？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
        center: true
      }).then(() => {
        let params = {
          course: parseInt(rows[index].id)
        };
        this.$http.delShopping(params).then(res => {
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

    //买东西
    buy(price, index, shopCartList) {
      let courseIds = [];
      this.multipleSelection.forEach((item, index) => {
        courseIds.push(item.id);
      });

      let course_list = {
        course_list: courseIds
      };
      // 加入支付中心
      // this.$http.settlement(course_list).then(res => {
      //   if (!res.error) {
      //     // 获取支付中心未支付商品
      //     this.getSettlement()
      //   }
      // });
    },
    
    // 获取订单中心列表
    getsettlementList() {
      this.$http
        .settlementList()
        .then(res => {
          if (!res.error) {
            if(res.data !== 0){              
              this.settlementProduct = res.data.settlement_info;
              this.global_coupon_dict = res.data.global_coupon_dict
            }            
          }
        })
        .catch(err => {
          console.log(err);
        });
    },

    // 计算加入的购物车数据
    handleSelectionChange(val) {
      console.log(val);
      this.multipleSelection = val;
    }
  },
  created() {
    this.getsettlementList();
  }
};
</script>

<style lang="css" scoped>
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
}
</style>
