<template>
  <div>
    <span class="toggle-btn" @click="toggleCollapse">
      <i class="el-icon-s-unfold" v-if="!show"></i>
      <i class="el-icon-s-fold" v-else></i>
    </span>
    <el-dropdown @command="handleCommand"  class="userInfo" >
      <span class="el-dropdown-link">
        <i class="el-icon-user"></i>
        {{t_name}}
        <i class="el-icon-arrow-down el-icon--right"></i>
      </span>
      <el-dropdown-menu>
        <el-dropdown-item command="goToHelloWorld">退出登录</el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </div>
</template>

<script>
import Utils from '../../assets/js/util.js'
// import TeacherNav from './TeacherNav'
export default {
  name: 'TeacherHeading',
  // components: {TeacherNav},
  data: function () {
    return {
      t_id: '',
      t_name: '',
      show: false
    }
  },
  mounted: function () {
    this.t_id = this.cookie.getCookie('t_id')
    this.t_name = this.cookie.getCookie('t_name')
  },
  methods: {
    goToHelloWorld: function () {
      this.cookie.clearCookie('t_id')
      this.cookie.clearCookie('t_name')
      this.$router.replace('/')
    },
    toggleCollapse: function () {
      this.show = !this.show
      Utils.$emit('toggleCollapseTeacher', 'call function toggleCollapse in TeacherNav')
    },
    handleCommand () {
      this.goToHelloWorld()
    },
    goToCommentPlatform () {
      let that = this
      let loginInfo =
        { t_id: that.t_id,
          t_name: that.t_name,
          userType: 'teacher'
        }
      that.cookie.setCookie(loginInfo)
      that.$router.push({
        name: 'CommentPlatForm'
      })
    }
  }
}
</script>

<style scoped>
  @import "../../assets/css/head.css";
</style>
