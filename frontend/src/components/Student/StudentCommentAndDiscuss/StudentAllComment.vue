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
          <el-row>
            <el-col :span="14" class="left-information" style="width: 50%">
              <el-row>
                <el-col :span="22">
                  <el-input
                    placeholder="查找您的相关课程"
                    prefix-icon="el-icon-search" v-model="inputSearch"
                    style="margin-bottom: 5%"></el-input>
                </el-col>
                <el-col :span="2">
                  <el-button
                    type="primary"
                    icon="el-icon-search"
                    style="float: right"
                    @click="searchCourse(inputSearch)"
                    circle></el-button>
                </el-col>
              </el-row>
              <el-card
                v-for="(course, index) in showCourseList" :key="index"
                v-loading="loading"
                shadow="hover"
                style="font-size: small; margin-bottom: 2%;">
                <div slot="header" class="clearfix">
                  <el-col :span="2">
                    <el-image :src="courseImg" lazy></el-image>
                  </el-col>
                  {{ course.c_name }}
                  <el-button v-on:click="commentCourse(index)" type="text" style="font-size: smaller; float: right">
                    进入评价
                  </el-button>
                  <el-rate
                    v-model="course.avgDegree"
                    disabled
                    show-score
                    text-color="#ff9900">
                  </el-rate>
                </div>
                <div
                  style="font-size: x-small; text-overflow: ellipsis ;max-height: 50px; overflow: hidden; white-space: nowrap;">
                  <span v-html="course.introduction"></span>
                </div>
              </el-card>
            </el-col>
            <el-col :span="8" :offset="2" class="right-information">
              <el-card shadow="hover" style="width: 100%">
                <el-row>
                  <el-col :span="2" >
                    &nbsp;
                  </el-col>
                  <el-col :span="6">
                    <el-image :src="studentImg" lazy></el-image>
                  </el-col>
                  <el-col :span="2" >
                    &nbsp;
                  </el-col>
                  <el-col :span="12" :offset="1">
                    <el-descriptions :column="1">
                      <el-descriptions-item label="用户名">{{ s_name }}</el-descriptions-item>
                      <el-descriptions-item label="学号">{{ s_id }}</el-descriptions-item>
                      <el-descriptions-item label="已选课程">{{ courseNum }}</el-descriptions-item>
                      <el-descriptions-item label="参与评价">{{ commentNum }}</el-descriptions-item>
                    </el-descriptions>
                  </el-col>
                </el-row>
                <el-row>
                  <el-divider></el-divider>
                </el-row>
                <el-row>
                  <el-descriptions :column="1" v-if="showIt">
                    <el-descriptions-item label="用户名">{{ s_name }}</el-descriptions-item>
                    <el-descriptions-item label="学号">{{ s_id }}</el-descriptions-item>
                  </el-descriptions>
                </el-row>
                <el-row class="el-row-button-head">
<!--                  <el-button @click="changeShowIt" type="text" class="el-row-button">-->
<!--                    <i v-if="showIt" class="el-icon-caret-top">隐藏</i>-->
<!--                    <i v-else class="el-icon-caret-bottom">展开</i>-->
<!--                  </el-button>-->
                </el-row>
              </el-card>
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import StudentNav from '../StudentNav'
import StudentHeading from '../StudentHeading'
import StudentImg from '../../../assets/img/student.png'
import CourseImg from '../../../assets/img/buaa_class_img.jpg'
import {toNumber} from "vue/src/shared/util";

export default {
  name: 'StudentAllComment',
  components: {StudentNav, StudentHeading},
  data(){
    return {
      loading: true,
      s_id: '',
      s_name: '',
      commentNum: '',
      courseNum: '',
      courseImg: CourseImg,
      studentImg: StudentImg,
      inputSearch: '',
      showIt: false,
      courseList: [{
        c_id: '1',
        c_name: '课程1',
        t_name: '教师1',
        avgDegree: 2.0,
        intro: '',
        isSelect: false
      }],
      showCourseList: this.courseList
    }
  },
  mounted: function () {
    this.s_id = this.cookie.getCookie('s_id')
    this.s_name = this.cookie.getCookie('s_name')
    this.getCourseList()
    this.getStudentCommentNum()
    this.getStudentCourseNum()
    this.showCourseList = this.courseList
  },
  methods: {
    toNumber,
    getStudentCourseNum: function () {
      let that = this
      this.$http.request({
        url: that.$url + 'GetStudentCourseNum/',
        method: 'post',
        data: {
          s_id: that.s_id
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        that.courseNum = response.data.data.courseNum
      }).catch(function (error) {
        console.log(error)
      })
    },
    getStudentCommentNum: function () {
      let that = this
      this.$http.request({
        url: that.$url + 'GetStudentCommentNum/',
        method: 'post',
        data: {
          s_id: that.s_id
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        that.commentNum = response.data.data.commentNum
      }).catch(function (error) {
        console.log(error)
      })
    },
    getCourseList: function () {
      let that = this
      that.loading = true
      this.$http.request({
        url: that.$url + 'GetCourseList/',
        method: 'post',
        data: {
          s_id: that.s_id
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        that.loading = false
        that.courseList = response.data.data
        that.showCourseList = response.data.data
      }).catch(function (error) {
        console.log(error)
        that.loading = false
      })
    },
    commentCourse: function (index) {
      let that = this
      this.$router.push({
        path: '/StudentCommentAndDiscuss/StudentComment',
        query: {
          c_id: that.showCourseList[index].c_id
        }
      })
    },
    goToHelloWorld: function () {
      this.cookie.clearCookie('s_id')
      this.cookie.clearCookie('s_name')
      this.$router.replace('/')
    },
    changeShowIt: function () {
      this.showIt = !this.showIt
    },
    searchCourse: function (inputSearch) {
      this.showCourseList = this.searchByIndexOf(inputSearch, this.courseList)
    },
    searchByIndexOf: function (keyWord, list) {
      if (!(list instanceof Array)) {
        return
      } else if (keyWord === '') {
        return list
      }
      const len = list.length
      const arr = []
      for (let i = 0; i < len; i++) {
        // 如果字符串中不包含目标字符会返回-1
        if (list[i].c_name.toString().includes(keyWord) || list[i].c_id.toString().includes(keyWord)) {
          arr.push(list[i])
        }
      }
      return arr
    }
  }
}
</script>

<style scoped>
@import "../../../assets/css/back.css";

.el-row-button {
  width: 100% !important;
}

.el-row-button :hover {
  background-color: initial;
}

.el-row-button-head :hover {
  background-color: hsla(0, 0%, 74%, 0.2);
}
</style>
