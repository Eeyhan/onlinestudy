<template>
  <div class="shopping-cart-wrap">
    <h3 class="shopping-cart-tit">
      我的订单 &nbsp;
    </h3>
    <div class="row">
      <el-table
        ref="multipleTable"
        :data="PaymentOrder"
        tooltip-effect="dark"
        style="width: 100%"
        
      >
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column label="商品" width="200">
          <template >
            <template slot-scope="scope">
              {{scope.row}}
              <img :src="scope.row.course_img" alt>
              <a href="javascript:void(0);">{{ products.title}}</a>
            </template>
            <img :src="products.course_img" alt>
            <a href="javascript:void(0);">{{ products.title}}</a>
          </template>
        </el-table-column>
        
        <el-table-column prop="money" label="交易金额" show-overflow-tooltip width="130">
          <template >¥{{products.price}}</template>
        </el-table-column>
        <el-table-column prop="valid" label="有效期" show-overflow-tooltip width="130">
          <template >{{products.valid_period_display}}</template>
        </el-table-column>

        <el-table-column prop="name" label="提交订单时间" width="130">
          <template slot-scope="scope">
            {{scope.row.pay_success_time|formatTime}}         
          </template>
        </el-table-column>
        <el-table-column prop="date" label="交易时间" width="130">
          <template slot-scope="scope">
            {{scope.row.order_date|formatTime}}           
          </template>
        </el-table-column>
        

        <el-table-column prop="order" label="订单号" width="130">
          <template slot-scope="scope">
            {{scope.row.transaction_number}}          
          </template>
        </el-table-column>

        <el-table-column prop="name" label="收货地址" width="130">
          <template slot-scope="scope">
            {{scope.row.user_address}}          
          </template>
        </el-table-column>

        <el-table-column fixed="right" label="操作" width="130">
          <template slot-scope="scope">
            <el-button
              @click.native.prevent="deleteRow(scope.$index, PaymentOrder)"
              type="text"
              size="small"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-pagination background layout="prev, pager, next" :total="80"></el-pagination>
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
      products:[]
    };
  },
  // computed: {
  //   totalPrice() {
  //     let total = 0;
  //     this.multipleSelection.forEach((item, index) => {
  //       total += parseFloat(item.price);
  //     });
  //     console.log(total);
  //     return total.toFixed(2);
  //   }
  // },
  methods: {
    // 删除账单
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
        this.$http.delPayment(params).then(res => {
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

    
    
    // 获取账单列表
    getPaymentList() {
      this.$http
        .PaymentList()
        .then(res => {
          if (!res.error) {
            if(res.data !== 0){              
              this.PaymentOrder =  Object.values(res.data);
              this.PaymentOrder.forEach((items,index)=>{

                Object.values(items).forEach((item,i)=>{
                  if(typeof item == 'object'){
                    this.products = item
                  }
                })
                
              })
            }            
          }
        })
        .catch(err => {
          console.log(err);
        });
    },

  },

  filters:{
    formatTime(value){
      return value.replace("T",' ').split('.')[0]
    }
  },
  created() {
    this.getPaymentList();
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
