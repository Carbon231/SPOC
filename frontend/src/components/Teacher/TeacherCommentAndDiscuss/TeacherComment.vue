<template>
  <div>
    <el-container>
      <el-aside class="aside" width="show?'64px':'400px'">
        <TeacherNav></TeacherNav>
      </el-aside>
      <el-container class="main">
        <el-header>
          <TeacherHeading></TeacherHeading>
        </el-header>
        <el-main style="padding-left: 10%; padding-right: 10%">
          <el-page-header @back="returnTeacherAllComment" :content="c_name" style="margin-bottom: 2%"></el-page-header>
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
                <el-rate align="center" v-model="courseAvgDegree" disabled show-score text-color="#ff9900"></el-rate>
              </el-col>
              <el-col :offset="2" :span="17">
                <el-row>
                  <el-col :span="18">
                    <strong>{{ c_name }}</strong>
                  </el-col>
                </el-row>
                <el-row>
                  <el-divider>
                  </el-divider>
                </el-row>
                <el-row>
                  <div style="font-size: small">
                    <h3>课程介绍</h3>
                    <span v-html="courseIntroduction"></span>
                  </div>
                </el-row>
              </el-col>
            </el-row>
          </el-card>
          <el-row>
            <el-divider></el-divider>
          </el-row>
          <el-row>
            <div style="font-size: medium">
              评价
            </div>
          </el-row>

          <el-divider></el-divider>
          <div v-for="(comment, index) in commentList" v-bind:key="index">
            <el-row class="time" v-loading="loading">
              <el-col :span="1">
                <el-image :src="studentImg" fit="contain" lazy></el-image>
              </el-col>
              <el-col :span="3" :offset="1">
                <el-row class="userName">
                  {{ comment.s_name }}({{ comment.s_id }}) :
                </el-row>
                <el-row>{{ comment.time }}</el-row>
              </el-col>
              <el-col :span="19" class="content">
                <el-row class="content-of-comment" v-html="comment.content">
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

<style scoped>
@import "../../../assets/css/back.css";

.buttons {
  margin-bottom: 10px;
}

.input {
  font-size: medium;
}

.time {
  font-size: small;
  color: #e2e2e2;
}

.t_id {
  font-size: medium;
  color: #66b1ff;
}

.content {
  font-size: medium;
  word-break: break-all;
}

.content-of-comment {
  color: black;
}
</style>

<script>
import TeacherNav from '../TeacherNav'
import TeacherHeading from '../TeacherHeading'
import CourseImg from '../../../assets/img/buaa_class_img.jpg'
import StudentImg from '../../../assets/img/student.png'

export default {
  name: 'TeacherComment',
  components: { TeacherNav, TeacherHeading },
  data: function () {
    return {
      loading: true,
      t_id: '',
      t_name: '',
      c_id: '',
      c_name: '',
      courseIntroduction: '',
      courseAvgDegree: 3.0,
      myDegree: 5,
      contentInput: '',
      courseImg: CourseImg,
      studentImg: StudentImg,
      time: '',
      commentList: [{
        cm_id: 1,
        t_id: '',
        t_name: '',
        degree: 5,
        content: '',
        time: ''
      }
      ]
    }
  },
  mounted() {
    this.t_id = this.cookie.getCookie('t_id')
    this.t_name = this.cookie.getCookie('t_name')
    this.c_id = this.$route.query.c_id
    this.getCourseInfo()
    this.getDegree()
    this.getCommentList()
  },
  methods: {
    getTime: function () {
      let dt = new Date()
      let yyyy = dt.getFullYear()
      let MM = (dt.getMonth() + 1).toString().padStart(2, '0')
      let dd = dt.getDate().toString().padStart(2, '0')
      let h = dt.getHours().toString().padStart(2, '0')
      let m = dt.getMinutes().toString().padStart(2, '0')
      let s = dt.getSeconds().toString().padStart(2, '0')
      this.time = yyyy + '-' + MM + '-' + dd + ' ' + h + ':' + m + ':' + s
    },
    getCourseInfo: function () {
      let that = this
      this.$http.request({
        url: that.$url + 'GetCourseInfo/',
        method: 'post',
        data: {
          c_id: that.c_id
        }
      }).then(function (response) {
        console.log(response.data)
        that.c_id = response.data.data.c_id
        that.c_name = response.data.data.c_name
        that.t_name = response.data.data.t_name
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
          c_id: that.c_id
        },
        headers: {
          'Content-Type': 'application/json'
        },
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
          c_id: that.c_id
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        that.courseAvgDegree = response.data.data.avgDegree
      })
    },
    returnTeacherAllComment: function () {
      let that = this
      that.$router.push({
        name: 'TeacherAllComment'
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
