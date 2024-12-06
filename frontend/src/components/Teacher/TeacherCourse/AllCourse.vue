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
          <el-main style="padding-left: 10%; padding-right: 10%">
          <el-row>
            <el-col :span="23">
              <el-input
                placeholder="查找您的相关课程"
                prefix-icon="el-icon-search" v-model="inputSearch"
                style="margin-bottom: 5%"></el-input>
            </el-col>
            <el-col :span="1">
              <el-button
                type="primary"
                icon="el-icon-search"
                style="float: right"
                @click="searchCourse(inputSearch)"
                circle></el-button>
            </el-col>
          </el-row>
          <el-card v-for="(course, index) in showCourseList" :key="index"
                   v-loading="loading"
                   shadow="hover"
                   style="margin-bottom: 2%">
            <el-row>
              <el-col :offset="1" :span="2">
                <el-image :src="courseImg" lazy></el-image>
              </el-col>
              <el-col :offset="2" :span="16">
                <el-row style="margin-bottom: 3%">
                  <el-link type="primary" v-on:click="getCourseInfo(index)">
                      <span style="font-size: 16px"><strong>{{ course.c_name }}</strong></span>
                  </el-link>
                </el-row>
                <el-row>
                    <el-tag type="info">课程编号<span>&nbsp;&nbsp;{{course.c_id}}</span></el-tag>
                </el-row>
              </el-col>
            </el-row>
          </el-card>
            <el-dialog title="课程详情" :visible.sync="courseInfoVisible" width="40%">
            <el-descriptions class="info">
              <el-descriptions-item label="课程名称(ID)">
                &nbsp;&nbsp;
                  {{courseInfo.c_name}}({{courseInfo.c_id}})
              </el-descriptions-item>
                <el-descriptions-item label="课程介绍">&nbsp;&nbsp;
                <span v-html="courseInfo.introduction"></span>
              </el-descriptions-item>
            </el-descriptions>
            <div slot="footer" class="dialog-footer">
              <el-button type="primary" @click="courseInfoVisible = false">确 定</el-button>
            </div>
          </el-dialog>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import TeacherNav from '../TeacherNav'
import TeacherHeading from '../TeacherHeading'
import CourseImg from '../../../assets/img/buaa_class_img.jpg'
export default {
  /* eslint-disable */
  name: 'AllCourse',
  components: {TeacherNav, TeacherHeading},
  data: function () {
    return {
      courseInfoVisible: false,
      courseImg: CourseImg,
      courseInfo: {
          c_id: '',
          c_name: '',
        introduction: ''
      },
      loading: true,
      t_name: '',
      t_id: '',
        courseList: [],
        showCourseList: [],
      inputSearch: ''
    }
  },
  mounted: function () {
    this.t_name = this.cookie.getCookie('t_name')
    this.t_id = this.cookie.getCookie('t_id')
    this.getAllCourses()
  },
  methods: {
    getCourseInfo: function (index) {
      let that = this
      that.courseInfo = that.showCourseList[index]
      that.courseInfoVisible = true
    },
    getCourseList: function () {
      let that = this
      that.loading = true
      this.$http.request({
        url: that.$url + 'GetCourseList/',
        method: 'get'
      }).then(function (response) {
        console.log(response.data)
        that.loading = false
          if (response.data.code === 200) {
            that.courseList = response.data.data
            that.showCourseList = response.data.data
          } else {
            that.$message.error(response.data.message)
          }
      }).catch(function (error) {
        console.log(error)
        that.loading = false
      })
    },
      searchCourse: function (query) {
        this.showCourseList = this.courseList.filter(course => course.c_name.includes(query))
    }
  }
}
</script>

<style scoped>
@import "../../../assets/css/nav.css";
@import "../../../assets/css/back.css";
</style>