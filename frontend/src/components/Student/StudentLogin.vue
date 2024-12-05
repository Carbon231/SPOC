<template>
  <transition name="head-login-register">
    <div class="background">
    <br>
    <div class="register_block">
      <div class="register_head">
        <p>学生登录</p>
      </div>
      <el-form>
        <div id="register-name">
          <el-form-item>
            <el-input class="inputs" type="text" placeholder="请输入学号" v-model="s_id" clearable></el-input>
          </el-form-item>
        </div>
        <div id="register-password">
          <el-form-item>
            <el-input class="inputs" type="text" placeholder="请输入密码" v-model="s_pwd" show-password clearable></el-input>
          </el-form-item>
        </div>
        <div class="confirm-button">
            <el-button id="button_in" type="primary" size="small" v-on:click="goToStudentHead">
              确认
            </el-button>
        </div>
        <div class="register-button">
            <el-button id="button_re" type="primary" :plain="true" size="small" v-on:click="goToStudentRegister">
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
  name: 'StudentLogin',
  data() {
    return {
      s_id: '',
      s_pwd: '',
      status: -1
    };
  },
  methods: {
    goToStudentHead: function () {
      let that = this

      this.$http.request({
        url: that.$url + 'StudentLogin/',
        method: 'post',
        data: {
          s_id: that.s_id,
          s_pwd: that.s_pwd
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        that.status = response.data.code;
        if (that.status === 200) {
          that.$message.success(response.data.message);
          let loginInfo = {"s_id": that.s_id, "s_name": response.data.s_name}
          that.cookie.setCookie(loginInfo)
          that.$router.push({
            name: 'StudentHead'
          });
        } else if (that.status === 401) {
          that.$message.error(response.data.error);
        }
      }).catch(function (error) {
        console.log(error)
      })
    },
    goToStudentRegister: function () {
      this.$router.push({
        name: 'StudentRegister'
      });
    },
    keydown(e) {
      if (e.keyCode === 13) {
        this.goToStudentHead()
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
