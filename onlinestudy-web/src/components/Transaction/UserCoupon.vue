<template>
  <div>
    <div class="row">
      <h3>我的可用优惠券(已过滤掉已使用和已过期的)</h3>
      <el-table ref="multipleTable" :data="usercoupons" tooltip-effect="dark" style="width: 100%">
        <el-table-column label="优惠券名" width="250">
          <template slot-scope="scope">
            <span>{{ scope.row.title}}</span>
          </template>
        </el-table-column>
        <el-table-column label="活动介绍" width="200">
          <template slot-scope="scope">
            <span>{{ scope.row.brief}}</span>
          </template>
        </el-table-column>

        <el-table-column prop="name" label="活动开始领取时间" width="212">
          <template slot-scope="scope">
            <span>{{scope.row.grant_begin_time}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="address" label="优惠券生效时间" show-overflow-tooltip>
          <template slot-scope="scope">{{scope.row.start_time}}</template>
        </el-table-column>

        <el-table-column prop="address" label="优惠券有效期" show-overflow-tooltip>
          <template slot-scope="scope">{{scope.row.period}}</template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
export default {
  name: "Coupon",
  data() {
    return {
      usercoupons: []
    };
  },
  methods: {
    getCouponList() {
      this.$http.userCouponList().then(res => {
        this.usercoupons = Object.values(res.data);
      });
    }
  },
  created() {
    this.getCouponList();
  }
};
</script>

<style lang="css" scoped>

.row {
  width: 1200px;
  margin: 40px auto;
}

.row h3 {
  margin-bottom: 20px;
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
  margin-bottom: 82px;
  /*justify-content:flex-end;*/
}



.el-input {
  width: 600px !important;
  margin: 22px auto;
}

.el-breadcrumb {
  margin-left: 40px;
}
</style>
