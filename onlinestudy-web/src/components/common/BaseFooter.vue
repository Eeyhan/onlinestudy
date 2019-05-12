<template>
  <div class="footer" id="footer">
    <div class="w1200 w1000">
      <p>
        <a
          href="#"
          target="_blank"
        >沪网文［2019］xxx-xxx号</a>&nbsp;&nbsp;沪ICP备xxxx号-x&nbsp;&nbsp;
        <a
          href="#"
          target="_blank"
        >增值电信业务经营许可证沪B2-20xxxx8</a>&nbsp;&nbsp;
        <a
          href="#"
          target="_blank"
        >新出网证（沪）字xxx号</a>&nbsp;&nbsp;
        <a href="#" target="_blank">xxxx</a>&nbsp;&nbsp;
        <a href="#" target="_blank" title="xxxx">xxxx</a>&nbsp;&nbsp;
        <a
          href="#"
          target="_blank"
          title="自律公约"
        >自律公约</a>
        <br>XXX教育&nbsp;&nbsp;&nbsp;&nbsp;
        <a class="yellow" href="#" target="_blank">xxxx</a>&nbsp;&nbsp;&nbsp;&nbsp;
        <a class="yellow" href="#" target="_blank">xxxx</a>&nbsp;&nbsp;&nbsp;&nbsp;
        <a class="yellow" href="#" target="_blank">xxxx</a>&nbsp;&nbsp;&nbsp;&nbsp;
        <a class="yellow" href="#" target="_blank">xxxx</a>
      </p>
      <p>客服电话：0xx-xxx、xxxxx</p>
      <p>
        <img src="#" alt>
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "BaseFooter",
  data() {
    return {};
  },
  created() {
    // console.log(localStorage);
  }
};
</script>

<style lang="css" scoped>
.footer {
  width: 100%;
  height: 120px;
  padding: 35px 0;
  background: #2e3137;
}

.w1200 {
  margin: 0 auto;
  width: 1200px;
  overflow: hidden;
  position: relative;
}
a{
  color: #409eff
}

.footer p {
  color: #999;
  text-align: center;
  line-height: 24px;
}

.footer img {
  width: auto;
  height: auto;
  vertical-align: middle;
}

img {
  width: 100%;
  height: 100%;
}
</style>
