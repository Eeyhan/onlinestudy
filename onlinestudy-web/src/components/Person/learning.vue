<template>
  <div id="player">
    
  </div>

</template>

<script>

export default {  
  name: "Mypage",
  
  data() {
    return {};
  },
  methods: {
    // 获取视频
    getvideo() {
      let videoId = this.$route.params.courseId; // 课程章节传来的课程id

      // 保利威试用时间已过，视频无法播放

      var player = polyvObject("#player").videoPlayer({
        wrap: "#player",
        width: 800,
        height: 533,
        forceH5: true,
        vid: "2f57a436189b03930638e752c9a3761e_2", // 这里就应该放课程章节传来的课程id,这里只是演示
        code: "myRandomCodeValue",
        playsafe: function(vid, next) {
          // 向后端发送请求获取加密的token
          console.log(vid);
          axios
            .request({
              url: "http://localhost:8000/blv/polyv",
              method: "POST",
              data: {
                vid: vid
              }
            })
            .then(function(data) {
              console.log(data);
              next(data.data.token);
            });
        }
      });
    }
  },
  
  mounted() {
    this.getvideo();
  }
};
</script>

<style scoped>
</style>
