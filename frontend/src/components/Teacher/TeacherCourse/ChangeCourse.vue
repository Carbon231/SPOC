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
        <!-- <el-page-header @back="returnManageCourse" :content="name" style="margin-bottom: 2%">
        </el-page-header> -->
        <el-form label-position="top" v-loading="loading">
          <el-form-item label="课程名称">
            <el-col :span="12">
              <el-input v-model="name"></el-input>
            </el-col>
          </el-form-item>
          <el-form-item label="课程介绍">
            <el-col :span="12">
                  <el-input type="textarea" v-model="introduction"></el-input>
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
// import {quillEditor} from 'vue-quill-editor'
// import 'quill/dist/quill.core.css'
// import 'quill/dist/quill.snow.css'
// import 'quill/dist/quill.bubble.css'
export default {
  /* eslint-disable */
  name: 'ChangeCourse',
    components: { TeacherNav, TeacherHeading },
  data: function () {
    return {
      loading: false,
      c_id: '',
      c_name: '',
      introduction: '',
      t_id: ''
    }
  },
    mounted: function () {
      this.id = this.$route.params.id
      this.name = this.$route.params.name
      this.introduction = this.$route.params.introduction
    this.t_id = this.cookie.getCookie('t_id')
  },
  methods: {
    returnManageCourse: function () {
        this.$router.push({ name: 'ManageCourse' })
    },
    changeCourse: function () {
      let that = this
      that.loading = true
      this.$http.request({
        url: that.$url + 'ChangeCourse/',
          method: 'post',
          data: {
            id: that.id,
            name: that.name,
            introduction: that.introduction,
            t_id: that.t_id
        }
      }).then(function (response) {
        console.log(response.data)
        that.loading = false
          if (response.data.code === 200) {
            that.$message.success(response.data.message)
            that.$router.push({ name: 'ManageCourse' })
          } else if (response.data.code === 400) {
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
