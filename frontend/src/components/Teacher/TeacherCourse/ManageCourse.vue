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
              <el-input placeholder="查找您的相关课程" prefix-icon="el-icon-search" v-model="inputSearch"
                style="margin-bottom: 5%"></el-input>
            </el-col>
            <el-col :span="1">
              <el-button type="primary" icon="el-icon-search" style="float: right" @click="searchCourse(inputSearch)"
                circle></el-button>
            </el-col>
          </el-row>
          <el-card v-for="(course, index) in showMyCourseList" :key="index" v-loading="loading" shadow="hover"
            style="margin-bottom: 2%">
            <el-row>
              <el-col :offset="2" :span="2">
                <el-image :src="courseImg" lazy></el-image>
              </el-col>
              <el-col :offset="2" :span="16">
                <el-row style="margin-bottom: 3%">
                  <el-link type="primary" v-on:click="getCourseInfo(index)">
                    <span style="font-size: 16px"><strong>{{ course.c_name }}</strong></span>
                  </el-link>
                </el-row>
                <el-row>
                  <el-tag type="info">课程编号<span>&nbsp;&nbsp;{{ course.c_id }}</span></el-tag>
                </el-row>
              </el-col>
              <el-col :span="2">
                <el-button-group style="margin-bottom: 1%">
                  <el-button type="primary" icon="el-icon-edit" v-on:click="changeCourse(index)">编辑</el-button>
                </el-button-group>
                <el-button-group>
                  <el-button type="danger" icon="el-icon-delete" v-on:click="cancelCourse(index)">停课</el-button>
                </el-button-group>
              </el-col>
            </el-row>
          </el-card>
          <el-dialog title="课程详情" :visible.sync="courseInfoVisible" width="40%">
            <el-descriptions class="info">
              <el-descriptions-item label="课程名称(ID)">
                {{ courseInfo.c_name }}({{ courseInfo.c_id }})
              </el-descriptions-item>
              <el-descriptions-item label="课程介绍">
                <span v-html="courseInfo.intro"></span>
              </el-descriptions-item>
              <el-descriptions-item label="选课学生">
                <el-button-group style="margin-left: 20px;">
                  <el-button type="primary" icon="el-icon-edit"
                    v-on:click="teacherGetStudentInCourse">查看选课学生名单</el-button>
                </el-button-group>
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
  name: 'ManageCourse',
  components: { TeacherNav, TeacherHeading },
  data: function () {
    return {
      courseInfoVisible: false,
      courseInfo: {
        c_id: '',
        c_name: '',
        t_name: '',
        intro: ''
      },
      courseImg: CourseImg,
      loading: true,
      t_name: '',
      t_id: '',
      myCourseList: [],
      showMyCourseList: [],
      inputSearch: '',
    }
  },
  mounted: function () {
    this.t_name = this.cookie.getCookie('t_name')
    this.t_id = this.cookie.getCookie('t_id')
    this.getTeacherCourseList()
  },
  methods: {
    teacherGetStudentInCourse: function () {
      this.$router.push({ name: 'TeacherGetStudentInCourse', params: { c_id: this.courseInfo.c_id } })
    },
    getCourseInfo: function (index) {
      let that = this
      that.courseInfo = that.showMyCourseList[index]
      that.courseInfoVisible = true
    },
    getTeacherCourseList: function () {
      let that = this
      that.loading = true
      this.$http.request({
        url: that.$url + 'GetTeacherCourseList/',
        method: 'post',
        data: {
          t_id: that.t_id
        }
      }).then(function (response) {
        console.log(response.data)
        that.loading = false
        if (response.data.code === 200) {
          that.myCourseList = response.data.data
          that.showMyCourseList = response.data.data
        } else {
          that.$message.error(response.data.message)
        }
      }).catch(function (error) {
        console.log(error)
        that.loading = false
      })
    },
    changeCourse: function (index) {
      this.$router.push({ name: 'ChangeCourse', params: { id: this.showMyCourseList[index].c_id } })
    },
    cancelCourse: function (index) {
      let that = this
      that.loading = true
      this.$http.request({
        url: that.$url + 'CancelCourse/',
        method: 'post',
        data: {
          c_id: that.showMyCourseList[index].c_id,
          t_id: that.t_id
        }
      }).then(function (response) {
        console.log(response.data)
        that.loading = false
        if (response.data.code === 200) {
          that.$message.success(response.data.message)
          that.getTeacherCourseList()
        } else {
          that.$message.error(response.data.message)
        }
      }).catch(function (error) {
        console.log(error)
        that.loading = false
      })
    },
    searchCourse: function (query) {
      this.showMyCourseList = this.myCourseList.filter(course => course.c_name.includes(query))
    }
  }
}
</script>

<style scoped>
@import "../../../assets/css/nav.css";
@import "../../../assets/css/back.css";
</style>