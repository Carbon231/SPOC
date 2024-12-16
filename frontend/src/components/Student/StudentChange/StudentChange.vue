<template>
  <div>
    <el-container>
      <el-aside class="aside" width="show?'64px':'300px'">
        <StudentNav></StudentNav>
      </el-aside>
      <el-container class="main">
        <el-header>
          <StudentHeading></StudentHeading>
        </el-header>
        <el-main>
          <el-row>{{s_name}} 密码修改 </el-row>
        <el-form label-width="100px">
          <el-form-item label="原密码">
            <el-col span="6">
              <el-input placeholder="请输入原密码" v-model="old_pwd" show-password></el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="新密码">
            <el-col span="6">
              <el-input placeholder="请输入新密码" v-model="new_pwd_1" show-password></el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="确认新密码">
            <el-col span="6">
              <el-input placeholder="请确认新密码" v-model="new_pwd_2" show-password></el-input>
            </el-col>
          </el-form-item>
          <el-form-item>
            <el-col span="6">
              <el-button v-on:click="changePassWord" type="primary" >确认</el-button>
            </el-col>
          </el-form-item>
        </el-form>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import StudentNav from '../StudentNav'
import StudentHeading from '../StudentHeading'

export default {
  name: 'StudentChangePassword',
  components: {StudentNav, StudentHeading},
  data: function () {
    return {
      s_id: '',
      s_name: '',
      old_pwd: '',
      new_pwd_1: '',
      new_pwd_2: ''
    }
  },
  mounted: function () {
    this.s_id = this.cookie.getCookie('s_id')
  },
  methods: {
    changePassWord: function () {
      let that = this
      if (that.new_pwd_1 === '') {
        that.$message.error('密码不能为空')
      } else {
        this.$http.request({
          url: that.$url + 'StudentChange/',
          method: 'post',
          data: {
            s_id: that.s_id,
            s_pwd: that.old_pwd,
            new_pwd_1: that.new_pwd_1,
            new_pwd_2: that.new_pwd_2
          },
          headers: {
            'Content-Type': 'application/json'
          },
        }).then(function (response) {
          console.log(response.data)
          that.status = response.data.code
          if (that.status === 200) {
            that.$message.success(response.data.message)
          } else if (that.status === 401) {
            that.$message.error(response.data.message)
          } else {
            that.$message.error('!')
          }
        }).catch(function (error) {
          console.log(error)
        })
      }
    },
    goToHelloWorld: function () {
      this.cookie.clearCookie('s_id')
      this.cookie.clearCookie('s_name')
      this.$router.replace('/')
    }
  }
}
</script>

<style scoped>
  @import "../../../assets/css/back.css";
</style>
