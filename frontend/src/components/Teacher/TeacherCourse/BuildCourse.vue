<template>
  <div>
    <el-container>
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
                <el-input type="textarea" v-model="course.intro"></el-input>
              </el-col>
            </el-form-item>
            <el-form-item label="课程容量">
              <el-col :span="12">
                <el-input v-model="course.capacity"></el-input>
              </el-col>
            </el-form-item>
            <el-form-item style="margin-top: 20%">
              <el-col :span="6">
                <el-button v-on:click="buildCourse" type="primary">确认</el-button>
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
// import {quillEditor} from 'l-editor'
// import 'quill/dist/quill.core.css'
// import 'quill/dist/quill.snow.css'
// import 'quill/dist/quill.bubble.css'
export default {
  name: 'BuildCourse',
  components: { TeacherNav, TeacherHeading },
  data: function () {
    return {
      loading: false,
      t_name: '',
      t_id: '',
      course: {
        c_name: '',
        capacity: '',
        intro: ''
      }
    }
  },
  mounted: function () {
    this.t_name = this.cookie.getCookie('t_name')
    this.t_id = this.cookie.getCookie('t_id')
  },
  methods: {
    buildCourse: function () {
      let that = this
      that.loading = true
      this.$http.request({
        url: that.$url + 'BuildCourse/',
        method: 'post',
        data: {
          t_id: that.t_id,
          c_name: that.course.c_name,
          capacity: that.course.capacity,
          intro: that.course.intro
        }
      }).then(function (response) {
        console.log(response.data)
        that.loading = false
        if (response.data.code === 200) {
          that.$message.success(response.data.message)
          that.course = {
            c_name: '',
            capacity: '',
            intro: ''
          }
          // this.$router.push({ name: '' })
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
