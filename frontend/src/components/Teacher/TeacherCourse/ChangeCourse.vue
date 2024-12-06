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
        <el-main style="padding-left: 30%; padding-right: 10%">
        <el-form label-position="top" v-loading="loading">
          <el-form-item label="课程名称">
            <el-col :span="12">
                  <el-input v-model="course.c_name"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="课程介绍">
            <el-col :span="12">
                  <el-input type="textarea" v-model="course.introduction"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item style="margin-top: 20%">
            <el-col :span="6">
              <el-button v-on:click="changeCourse" type="primary">确认</el-button>
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
  name: 'ChangeCourse',
    components: { TeacherNav, TeacherHeading },
  data: function () {
    return {
      loading: false,
        course: {
          c_id: '',
          c_name: '',
          introduction: ''
        },
      t_id: ''
    }
  },
    mounted: function () {
      this.course.c_id = this.$route.params.id
      this.t_id = this.cookie.getCookie('t_id')
      this.getCourseInfo()
  },
  methods: {
      getCourseInfo: function () {
        let that = this
        that.loading = true
        this.$http.request({
          url: that.$url + 'GetCourseInfo/',
          method: 'get',
          params: {
            c_id: that.course.c_id
          }
        }).then(function (response) {
          console.log(response.data)
          that.loading = false
          if (response.data.code === 200) {
            that.course.c_name = response.data.data.c_name
            that.course.introduction = response.data.data.introduction
          } else {
            that.$message.error(response.data.message)
          }
        }).catch(function (error) {
          console.log(error)
          that.loading = false
        })
    },
    changeCourse: function () {
      let that = this
      that.loading = true
      this.$http.request({
        url: that.$url + 'ChangeCourse/',
          method: 'post',
          data: {
            c_id: that.course.c_id,
            c_name: that.course.c_name,
            introduction: that.course.introduction,
            t_id: that.t_id
        }
      }).then(function (response) {
        console.log(response.data)
        that.loading = false
          if (response.data.code === 200) {
            that.$message.success(response.data.message)
            that.$router.push({ name: 'ManageCourse' })
          } else {
            that.$message.error(response.data.message)
        }
      }).catch(function (error) {
        console.log(error)
        that.loading = false
      })
    },
    goToHelloWorld: function () {
      this.cookie.clearCookie('t_id')
      this.cookie.clearCookie('t_name')
      this.$router.replace('/')
    }
  }
}
</script>

<style scoped>
 @import "../../../assets/css/nav.css";
 @import "../../../assets/css/back.css";
</style>