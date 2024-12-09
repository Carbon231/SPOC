<template>
  <div>
    <span class="toggle-btn" @click="toggleCollapse">
      <i class="el-icon-s-unfold" v-if="!show"></i>
      <i class="el-icon-s-fold" v-else></i>
    </span>
    <el-dropdown @command="handleCommand"  class="userInfo" >
      <span class="el-dropdown-link">
        <i class="el-icon-user"></i>
        {{s_name}}
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
// import StudentNav from './StudentNav'
export default {
  name: 'StudentHeading',
  // components: {StudentNav},
  data: function () {
    return {
      s_id: '',
      s_name: '',
      show: false
    }
  },
  mounted: function () {
    this.s_id = this.cookie.getCookie('s_id')
    this.s_name = this.cookie.getCookie('s_name')
    this.checkIdent()
  },
  methods: {
    checkIdent: function() {
      if (this.s_id == null || this.s_name == null) {
        this.$router.push({
          name: 'StudentLogin'
        })
      }
    },
    goToHelloWorld: function () {
      this.cookie.clearCookie('s_id')
      this.cookie.clearCookie('s_name')
      this.cookie.clearCookie('accepted')
      this.$router.replace('/')
    },
    toggleCollapse: function () {
      this.show = !this.show
      Utils.$emit('toggleCollapse', 'call function toggleCollapse in StudentNav')
    },
    handleCommand () {
      this.goToHelloWorld()
    },
  }
}
</script>

<style scoped>
  @import "../../assets/css/head.css";
</style>
