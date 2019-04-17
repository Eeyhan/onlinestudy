<template>
  <div class="footer">
    <h3>这是底部内容</h3>
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
  margin: 0 auto;
  /* background: #9a9d9a; */
  margin-top: 20px;
  min-height: 170px;
  padding-top: 20px
}
</style>
