<template>
  <div class="shopping-cart-wrap">
    <h3 class="shopping-cart-tit">我的订单 &nbsp;</h3>
    <div class="row">
      <el-table ref="multipleTable" :data="product" tooltip-effect="dark" style="width: 100%">
        <el-table-column label="课程" width="950">
          <template slot-scope="scope">
            <img :src="scope.row.course_img" alt>
            <a href="javascript:void(0);">{{ scope.row.title}}</a> --
            <span>有效期：{{scope.row.valid_period_display}} - 价格：￥{{scope.row.price}} - 实付费：￥{{scope.row.real_price}}</span>
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="操作" width="150">
          <template slot-scope="scope">
            <el-button
              @click.native.prevent="Assess(scope.$index, product)"
              type="text"
              size="small"
            >评价</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-pagination background layout="prev, pager, next" :total="80"></el-pagination>
  </div>
</template>

<script>
export default {
  name: "OrderDetail",
  data() {
    return {
      multipleSelection: [], //存放选中的当前数据
      currentVal: "",
      PaymentOrder: [], // 结算中心订单
      product: [],
      orderId: 0,
      value: ""
    };
  },

  methods: {
    Assess(index, row) {
      let course = row[index].id;
      this.$prompt("请输入评价", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消"
      })
        .then(({ value }) => {
          this.value = value;

          let inner = {
            course: course,
            assess: this.value
          };
          let params = {};
          params[this.orderId] = inner;

          this.$http.PaymentAssess(params).then(res => {
            this.$message({
              type: "success",
              message: res.data,
              center: true
            });
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "取消输入",
            center: true
          });
        });
    },
    getData() {
      let datas = this.$route.params.params;
      this.orderId = this.$route.params.orderId;
      for (let key in datas) {
        this.product = Object.values(datas[key]);
      }
    }
  },

  created() {
    this.getData();
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
