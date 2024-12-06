<template>
  <div>
    <el-container class="background">
      <el-aside class="aside" width="show?'64px':'250px'">
        <TeacherNav></TeacherNav>
      </el-aside>
      <el-container class="main">
        <el-header>
          <TeacherHeading></TeacherHeading>
        </el-header>
        <el-main>
        <el-form label-width="100px">
          <el-form-item label="原密码">
            <el-col span="6">
                  <el-input placeholder="请输入原密码" v-model="t_pwd" show-password></el-input>
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
                  <el-button type="primary" @click="changePassword">确认</el-button>
            </el-col>
          </el-form-item>
        </el-form>
      </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import TeacherNav from '../TeacherNav'
import TeacherHeading from '../TeacherHeading'
export default {
  name: 'TeacherChange',
    components: { TeacherNav, TeacherHeading },
  data: function () {
    return {
        t_pwd: '',
        new_pwd_1: '',
        new_pwd_2: '',
        t_id: ''
    }
  },
  mounted: function () {
      this.t_id = this.cookie.getCookie('t_id')
  },
  methods: {
      changePassword: function () {
        if (this.new_pwd_1 !== this.new_pwd_2) {
          this.$message.error('新密码不一致！')
          return
        }
      let that = this
        this.$http.request({
          url: that.$url + 'TeacherChange/',
          method: 'post',
          data: {
            t_id: that.t_id,
            t_pwd: that.t_pwd,
            new_pwd_1: that.new_pwd_1,
            new_pwd_2: that.new_pwd_2
          }
        }).then(function (response) {
          console.log(response.data)
          if (response.data.code === 200) {
            that.$message.success(response.data.message)
            that.t_pwd = ''
            that.new_pwd_1 = ''
            that.new_pwd_2 = ''
          } else {
            that.$message.error(response.data.message)
          }
        }).catch(function (error) {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped>
 @import "../../../assets/css/nav.css";
 @import "../../../assets/css/back.css";
</style>
