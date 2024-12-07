<template>
  <div>
    <el-container class="background">
      <el-aside class="aside" width="show?'64px':'400px'">
        <StudentNav></StudentNav>
      </el-aside>
      <el-container class="main">
        <el-header>
          <StudentHeading></StudentHeading>
        </el-header>
        <el-main style="padding-left: 10%; padding-right: 10%">
          <el-page-header @back="returnStudentAllComment" :content="c_name" style="margin-bottom: 2%"></el-page-header>
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
                  text-color="#ff9900"></el-rate>
              </el-col>
              <el-col :offset="2" :span="17">
                <el-row>
                  <el-col :span="18">
                    <strong>{{c_name}}</strong>
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
              评分
            </div>
            <el-rate
              style="font-size: medium"
              v-model="myDegree"
              show-text>
            </el-rate>
          </el-row>
          <el-row>
            &nbsp;
          </el-row>
          <el-row>
            <el-col>
              <el-input class="input" v-model="contentInput" type="textarea" :rows="3" placeholder="对于课程内容、讲课质量、考核方式等的评价">
              </el-input>
            </el-col>
            <el-button v-on:click="commentCourse" type="primary" size="small" style="float: right">添加评价</el-button>
          </el-row>
          <el-divider></el-divider>
          <div v-for="(comment) in commentList" v-bind:key="comment">
            <el-row class="time" v-loading="loading">
              <el-col :span="1">
                <el-image :src="studentImg" fit="contain" lazy></el-image>
              </el-col>
              <el-col :span="3" :offset="1">
                <el-row class="s_id">
                  {{comment.s_name}}({{comment.s_id}}) :
                </el-row>
                <el-row>{{comment.time}}</el-row>
              </el-col>
              <el-col :span="19" class="content">
                <el-row class="content-of-comment" v-html="comment.content">
                </el-row>
                <el-row class="delete" :span="1" style="float: right">
                  <div v-if="comment.s_id === s_id">
                    <el-link type="danger" v-on:click="deleteComment(comment.cm_id)">删除</el-link>
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
  .s_id {
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
import StudentNav from '../StudentNav'
import StudentHeading from '../StudentHeading'
import CourseImg from '../../../assets/img/buaa_class_img.jpg'
import StudentImg from '../../../assets/img/student.png'
export default {
  name: 'StudentComment',
  components: {StudentNav, StudentHeading},
  data: function () {
    return {
      loading: true,
      s_id: '',
      s_name: '',
      c_id: '',
      c_name: '',
      t_name: '',
      courseIntroduction: '',
      courseAvgDegree: 3.0,
      myDegree: 5,
      contentInput: '',
      courseImg: CourseImg,
      studentImg: StudentImg,
      time: '',
      commentList: [{
        cm_id: 1,
        s_id: '',
        s_name: '',
        degree: 5,
        content: '',
        time: ''
      }
      ]
    }
  },
  mounted () {
    this.s_id = this.cookie.getCookie('s_id')
    this.s_name = this.cookie.getCookie('s_name')
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
        that.c_id = response.data.c_id
        that.c_name = response.data.c_name
        that.t_name = response.data.t_name
        that.courseIntroduction = response.data.intro
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
        that.commentList = response.data
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
        that.courseAvgDegree = response.data.avgDegree
        if (that.courseAvgDegree !== 5) {
          that.courseAvgDegree = Number(that.courseAvgDegree).toFixed(1)
        }
      })
    },
    commentCourse: function () {
      let that = this
      that.getTime()
      this.$http.request({
        url: that.$url + 'CommentCourse/',
        method: 'post',
        data: {
          c_id: that.c_id,
          s_id: that.s_id,
          s_name: that.s_name,
          content: that.contentInput,
          time: that.time,
          degree: that.myDegree
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        if (response.data.code === 200) {
          that.$message.success(response.data.message)
          that.getCommentList()
          that.getDegree()
          that.contentInput = ''
        } else {
          that.$message.error('未知错误')
        }
      }).catch(function (error) {
        console.log(error)
      })
    },
    deleteComment: function (cm_id) {
      this.$confirm('此操作将永久删除该评价，是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      }).then(() => {
        let that = this
        that.getTime()
        this.$http.request({
          url: that.$url + 'DeleteComment/',
          method: 'post',
          data: {
            s_id: that.s_id,
            cm_id: cm_id
          },
          headers: {
            'Content-Type': 'application/json'
          },
        }).then(function (response) {
          console.log(response.data)
          if (response.data.code === 200) {
            that.$message.success(response.data.message)
            that.getCommentList()
            that.getDegree()
          } else if (response.data.code === 401) {
            that.$message.error(response.data.message)
          } else {
            that.$message.error('未知错误')
          }
        }).catch(function (error) {
          console.log(error)
        })
      })
    },
    returnStudentAllComment: function () {
      let that = this
      that.$router.push({
        name: 'StudentAllComment'
      })
    },
    goToHelloWorld: function () {
      this.cookie.clearCookie('s_id')
      this.cookie.clearCookie('s_name')
      this.$router.replace('/')
    }
  }
}
</script>
