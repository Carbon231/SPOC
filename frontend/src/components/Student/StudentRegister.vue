<template>
  <transition name="head-login-register">
    <div class="background">
    <br>
    <div class="register_block">
      <div class="register_head">
        <p>学生注册</p>
      </div>
      <el-form rules="rules">
        <div id="register-n">
          <el-form-item>
            <el-input class="inputs" type="text" placeholder="请输入学号" v-model="s_id" clearable></el-input>
          </el-form-item>
        </div>
        <div id="register-name">
          <el-form-item>
            <el-input class="inputs" type="text" placeholder="请输入姓名" v-model="s_name" clearable></el-input>
          </el-form-item>
        </div>
        <div id="register-password">
          <el-form-item>
            <el-input class="inputs" type="text" placeholder="请输入密码" v-model="s_pwd" show-password clearable></el-input>
          </el-form-item>
        </div>
        <div id="confirm-password">
          <el-form-item>
            <el-input class="inputs" type="text" placeholder="请确认密码" v-model="s_pwd_confirm" show-password clearable></el-input>
          </el-form-item>
        </div>
        <div class="confirm-button">
            <el-button id="button_in" type="primary" size="small" v-on:click="Register">
              确认
            </el-button>
        </div>
        <div class="return-button">
            <el-button id="button_re" type="primary" plain="true" size="small" v-on:click="goToStudentLogin">
              返回
            </el-button>
        </div>
      </el-form>
    </div>
  </div>
  </transition>
</template>

<script>
export default {
  name: 'StudentRegister',
  data() {
    return {
      status: -1,
      s_id: '',
      s_name: '',
      s_pwd: '',
      s_pwd_confirm: ''
    }
  },
  methods: {
    goToStudentLogin: function () {
      this.$router.push({
        name: 'StudentLogin'
      })
    },
    Register: function () {
      let that = this
      console.log(that.s_id, that.s_name, that.s_pwd, that.s_pwd_confirm)
      if (that.s_pwd === '') {
        that.$message.error('密码不能为空')
      } else if (that.s_name === '') {
        that.$message.error('用户名不能为空')
      } else if (that.s_id === '') {
        that.$message.error('学号不能为空')
      } else {
        this.$http.request({
          url: that.$url + 'StudentRegister/',
          method: 'post',
          data: {
            s_id: that.s_id,
            s_name: that.s_name,
            s_pwd: that.s_pwd,
            s_pwd_confirm: that.s_pwd_confirm
          },
          headers: {
            'Content-Type': 'application/json'
          }
        }).then(function (response) {
          console.log(response.data)
          that.status = response.data.code;
          if (that.status === 200) {
            that.$message.success(response.data.message)
            that.$router.push({
              name: 'StudentLogin',
              query: {
                s_id: that.s_id,
                s_pwd: that.s_pwd
              }
            })
          }
          else if (that.status === 400) {
            that.$message.error(response.data.error)
          }
        }).catch(function (error) {
          console.log(error)
        })
      }
    },
    keydown (e) {
      if (e.keyCode === 13) {
        this.Register()
      }
    }
  },
  mounted () {
    window.addEventListener('keydown', this.keydown)
  },
  destroyed () {
    window.removeEventListener('keydown', this.keydown, false)
  }
}
</script>

<style scoped>
  @import "../../assets/css/register.css";
  @import "../../assets/css/Transition/head-login-register.css";
</style>
