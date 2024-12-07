<template>
  <div>
    <el-container class="background">
      <el-aside class="aside" width="show?'64px':'400px'">
        <TeacherNav></TeacherNav>
      </el-aside>
      <el-container class="main">
        <el-header>
          <TeacherHeading></TeacherHeading>
        </el-header>
        <el-main style="padding-left: 10%; padding-right: 10%">
            <el-page-header @back="returnTeacherAllComment" :content="courseName" style="margin-bottom: 2%">
          </el-page-header>
          <el-card shadow="hover" style="margin-bottom: 1%">
            <el-row>
              <el-col :offset="1" :span="3">
                <el-image :src="courseImg" lazy></el-image>
                <el-row>
                  &nbsp;
                </el-row>
                <el-row style="text-align: center; font-size: medium">
                  课程评分
                </el-row>
                <el-rate
                  align="center"
                  v-model="courseAvgDegree"
                  disabled
                  show-score
                    text-color="#ff9900"
                    score-template="{value}">
                  </el-rate>
                  </el-col>
                <el-col :offset="2" :span="18">
                <el-row>
                    <span style="font-size: 16px"><strong>{{ courseName }}</strong></span>
                </el-row>
                <el-row>
                    <span style="font-size: 14px; color: gray">{{ courseIntroduction }}</span>
                </el-row>
              </el-col>
            </el-row>
          </el-card>
          <el-row>
            <el-divider></el-divider>
          </el-row>

            <div v-for="(comment, index) in commentList" :key="index">
            <el-row class="time">
              <el-col :span="1">
                <el-avatar :src="studentImg">
                </el-avatar>
              </el-col>
              <el-col :span="3">
                <el-row class="userName">
                    {{comment.s_name}}({{comment.s_id}}) :
                </el-row>
                <el-row>{{comment.time}}</el-row>
              </el-col>
              <el-col :span="20" class="content">
                <el-row class="content-of-comment" style="color: black">
                  <span v-html="comment.content"></span>
                </el-row>
                <el-row class="delete">
                    <div v-if="comment.s_id === s_id">
                      <el-link type="danger" @click="deleteComment(comment.cm_id)">删除</el-link>
                  </div>
                </el-row>
              </el-col>
            </el-row>
            <el-divider></el-divider>
          </div>
      </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import TeacherNav from '../TeacherNav'
import TeacherHeading from '../TeacherHeading'
// import CourseImg from '../../../assets/img/buaa_class_img.jpg'
import StudentImg from '../../../assets/img/student.png'
  
export default {
  name: 'TeacherComment',
    components: { TeacherNav, TeacherHeading },
  data: function () {
    return {
      loading: true,
        s_id: '',
        s_name: '',
      courseId: '',
      courseName: '',
      courseIntroduction: '',
        courseAvgDegree: 0,
        commentList: [],
        studentImg: StudentImg
      }
    },
    mounted: function () {
      this.s_id = this.cookie.getCookie('s_id')
      this.s_name = this.cookie.getCookie('s_name')
      this.courseId = this.$route.params.id
      this.getCourseInfo()
      this.getCommentList()
      this.getDegree()
  },
  methods: {
    getCourseInfo: function () {
      let that = this
      this.$http.request({
        url: that.$url + 'GetCourseInfo/',
          method: 'post',
          data: {
            c_id: that.courseId
        }
      }).then(function (response) {
        console.log(response.data)
          that.courseName = response.data.data.c_name
          that.courseIntroduction = response.data.data.intro
      }).catch(function (error) {
        console.log(error)
      })
    },
    getCommentList: function () {
      let that = this
      that.loading = true
      this.$http.request({
        url: that.$url + 'GetCommentList/',
          method: 'post',
          data: {
            c_id: that.courseId
        }
      }).then(function (response) {
        console.log(response.data)
        that.loading = false
          that.commentList = response.data.data
      }).catch(function (error) {
        console.log(error)
        that.loading = false
      })
    },
    getDegree: function () {
      let that = this
      this.$http.request({
        url: that.$url + 'GetDegree/',
          method: 'post',
          data: {
            c_id: that.courseId
        }
      }).then(function (response) {
        console.log(response.data)
          that.courseAvgDegree = response.data.data.avgDegree
        if (that.courseAvgDegree !== 5) {
          that.courseAvgDegree = Number(that.courseAvgDegree).toFixed(1)
        }
        }).catch(function (error) {
          console.log(error)
      })
    },
      deleteComment: function (cm_id) {
      let that = this
        this.$http.request({
          url: that.$url + 'DeleteComment/',
          method: 'post',
          data: {
            cm_id: cm_id
          }
        }).then(function (response) {
          console.log(response.data)
          if (response.data.code === 200) {
            that.$message.success('删除成功')
            that.getCommentList()
          } else {
            that.$message.error('未知错误')
          }
        }).catch(function (error) {
          console.log(error)
        })
      },
      returnTeacherAllComment: function () {
        this.$router.push({ name: 'TeacherAllComment' })
    }
  }
}
</script>

  <style scoped>
  @import "../../../assets/css/back.css";
  </style>