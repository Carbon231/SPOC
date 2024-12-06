<template>
  <transition name="head-login-register">
    <div class="background">
    <br>
    <div class="register_block">
      <div class="register_head">
        <p>教师注册</p>
      </div>
      <el-form>
        <div id="register-n">
          <el-form-item>
            <el-input class="inputs" type="text" placeholder="请输入姓名" v-model="t_name" clearable></el-input>
          </el-form-item>
        </div>
        <div id="register-name">
          <el-form-item>
            <el-input class="inputs" type="text" placeholder="请输入工号" v-model="t_id" clearable></el-input>
          </el-form-item>
        </div>
        <div id="register-password">
          <el-form-item>
            <el-input class="inputs" type="text" placeholder="请输入密码" v-model="t_pwd" show-password clearable></el-input>
          </el-form-item>
        </div>
        <div id="confirm-password">
          <el-form-item>
            <el-input class="inputs" type="text" placeholder="请确认密码" v-model="t_pwd_confirm" show-password clearable></el-input>
          </el-form-item>
        </div>
        <div class="confirm-button">
            <el-button id="button_in" type="primary" size="small" v-on:click="Register">
              确认
            </el-button>
        </div>
        <div class="return-button">
            <el-button id="button_re" type="primary" plain="true" size="small" v-on:click="goToTeacherLogin">
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
  name: 'TeacherRegister',
  data() {
    return {
      status: -1,
      t_id: '',
      t_name: '',
      t_pwd: '',
      t_pwd_confirm: ''
    }
    },
  methods: {
    goToTeacherLogin: function () {
      this.$router.push({
        name: 'TeacherLogin'
      })
    },
    Register: function () {
      let that = this
      console.log(that.t_id, that.t_name, that.t_pwd, that.t_pwd_confirm)
      if (that.t_pwd === '') {
        that.$message.error('密码不能为空')
      } else if (that.t_name === '') {
        that.$message.error('用户名不能为空')
      } else if (that.t_id === '') {
        that.$message.error('学号不能为空')
      } else {
        this.$http.request({
          url: that.$url + 'TeacherRegister/',
          method: 'post',
          data: {
            t_id: that.t_id,
            t_name: that.t_name,
            t_pwd: that.t_pwd,
            t_pwd_confirm: that.t_pwd_confirm
          },
          headers: {
            'Content-Type': 'application/json'
          }
        }).then(function (response) {
          console.log(response.data)
          that.status = response.data.code;
          if (that.status === 201) {
            that.$message.success(response.data.message)
            that.$router.push({
              name: 'TeacherLogin',
              data: {
                t_id: that.t_id,
                t_pwd: that.t_pwd
              }
            })
          }
          else if (that.status === 400) {
            that.$message.error(response.data.message)
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
