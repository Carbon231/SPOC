<template>
  <transition name="head-login-register">
    <div class="background">
      <br>
      <div class="register_block">
        <div class="register_head">
          <p>教师登录</p>
        </div>
        <el-form>
          <div id="register-name">
            <el-form-item>
              <el-input class="inputs" type="text" placeholder="请输入工号" v-model="t_id" clearable></el-input>
            </el-form-item>
          </div>
          <div id="register-password">
            <el-form-item>
              <el-input class="inputs" type="text" placeholder="请输入密码" v-model="t_pwd" show-password
                clearable></el-input>
            </el-form-item>
          </div>
          <div class="confirm-button">
            <el-button id="button_in" type="primary" size="small" v-on:click="goToTeacherHead">
              确认
            </el-button>
          </div>
          <div class="register-button">
            <el-button id="button_re" type="primary" :plain="true" size="small" v-on:click="goToTeacherRegister">
              注册
            </el-button>
          </div>
          <div class="return-text">
            <el-link href="#/" style="font-size: 8px; color: white">返回</el-link>
          </div>
        </el-form>
      </div>
    </div>
  </transition>
</template>

<script>
/* eslint-disable */
export default {
  name: 'TeacherLogin',
  data() {
    return {
      t_id: '',
      t_name: '',
      t_pwd: '',
      status: -1
    };
  },
  methods: {
    goToTeacherHead: function () {
      let that = this

      this.$http.request({
        url: that.$url + 'TeacherLogin/',
        method: 'post',
        data: {
          t_id: that.t_id,
          t_pwd: that.t_pwd
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        that.status = response.data.code;
        if (that.status === 200) {
          that.$message.success(response.data.message);
          let loginInfo = { "t_id": that.t_id, "t_name": response.data.t_name }
          that.cookie.setCookie(loginInfo)
          that.$router.push({
            name: 'TeacherHead'
          });
        } else if (that.status === 401) {
          that.$message.error(response.data.error);
        }
      }).catch(function (error) {
        console.log(error)
      })
    },
    goToTeacherRegister: function () {
      this.$router.push({
        name: 'TeacherRegister'
      });
    },
    keydown(e) {
      if (e.keyCode === 13) {
        this.goToTeacherHead()
      }
    }
  },
  mounted() {
    window.addEventListener('keydown', this.keydown)
  },
  destroyed() {
    window.removeEventListener('keydown', this.keydown, false)
  }
}
</script>

<style scoped>
@import "../../assets/css/login.css";
@import "../../assets/css/Transition/head-login-register.css";
</style>
