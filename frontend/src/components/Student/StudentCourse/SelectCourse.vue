<template>
  <div>
    <el-container class="background">
      <el-aside class="aside" width="show?'64px':'300px'">
        <StudentNav></StudentNav>
      </el-aside>
      <el-container class="main">
        <el-header>
          <StudentHeading></StudentHeading>
        </el-header>
        <el-main style="padding-right: 10%; padding-left: 10%">
          <el-row>
            <el-col :span="23">
              <el-input placeholder="查找您的相关课程(课程名或课程编号)" prefix-icon="el-icon-search" v-model="inputSearch"
                style="margin-bottom: 5%"></el-input>
            </el-col>
            <el-col :span="1">
              <el-button type="primary" icon="el-icon-search" style="float: right" @click="searchCourse(inputSearch)"
                circle></el-button>
            </el-col>
          </el-row>
          <el-card v-for="(course, index) in showCourseList" :key="index" v-loading="loading" shadow="hover"
            style="margin-bottom: 2%;">
            <el-row>
              <el-col :offset="1" :span="2">
                <el-image :src="courseImg" lazy></el-image>
              </el-col>
              <el-col :offset="2" :span="14">
                <el-row style="margin-bottom: 3%">
                  <el-link type="primary" v-on:click="getCourseInfo(index)">
                    <span style="font-size: 16px"><strong>{{ course.c_name }}</strong></span>
                  </el-link>
                </el-row>
                <el-row>
                  <el-tag type="info">课程编号<span>&nbsp;&nbsp;{{ course.c_id }}</span></el-tag>
                  <el-tag type="success">开课院系<span>&nbsp;&nbsp;{{ course.d_name }}</span></el-tag>
                </el-row>
              </el-col>
              <el-col :span="2">
                <span style="color: gray">{{course.selectedNum}} / {{course.capacity}}</span>
              </el-col>
              <el-col :span="2">
                <el-button-group style="margin-top: 2%">
                  <el-button v-if="!showCourseList[index].isSelect" v-on:click="selectCourse(index)" type="primary">选课</el-button>
                  <el-button v-else type="info" disabled>已选</el-button>
                </el-button-group>
              </el-col>
            </el-row>
          </el-card>
          <el-dialog title="提示" :visible.sync="courseInfoVisible" width="40%">
            <el-descriptions class="info">
              <el-descriptions-item label="课程名称(ID)">
                &nbsp;&nbsp;
                {{ courseInfo.c_name }}({{ courseInfo.c_id }})
              </el-descriptions-item>
              <el-descriptions-item label="院系名称">
                &nbsp;&nbsp;
                {{ courseInfo.d_name }}
              </el-descriptions-item>
              <el-descriptions-item label="课程介绍">&nbsp;&nbsp;
                <span v-html="courseInfo.intro"></span>
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

<style scoped>
@import "../../../assets/css/back.css";

.info {
  margin-bottom: 20px;
  word-break: break-all;
}
</style>

<script>
import StudentNav from '../StudentNav'
import StudentHeading from '../StudentHeading'
import CourseImg from '../../../assets/img/buaa_class_img.jpg'
export default {
  /* eslint-disable */
  name: 'SelectCourse',
  components: { StudentNav, StudentHeading },
  data: function () {
    return {
      courseInfoVisible: false,
      courseInfo: {
        c_id: '',
        c_name: '',
        d_name: '',
        t_name: '',
        intro: ''
      },
      courseImg: CourseImg,
      loading: false,
      s_id: '',
      s_name: '',
      courseList: [{
        c_id: '1',
        c_name: '课程1',
        t_name: '教师1',
        d_id: 0,
        d_name: '暂无',
        avgDegree: 2.0,
        intro: '',
        isSelect: false,
        capacity: 100,
        selectedNum: 0
      }],
      showCourseList: this.courseList,
      inputSearch: ''
    }
  },
  mounted: function () {
    this.s_id = this.cookie.getCookie('s_id')
    this.s_name = this.cookie.getCookie('s_name')
    this.getCourseList()
  },
  methods: {
    getCourseInfo: function (index) {
      let that = this
      that.courseInfo = that.courseList[index]
      that.courseInfoVisible = true
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
    selectCourse(index) {
      console.log(index)
      let that = this
      if (!that.courseList[index].isSelect) {
          this.$http.request({
          url: that.$url + 'SelectCourse/',
          method: 'post',
          data: {
            s_id: that.s_id,
            c_id: that.showCourseList[index].c_id
          }
        }).then(function (response) {
          console.log(response.data)
          var status = response.data.code
          if (status === 200) {
            that.$message.success(response.data.message)
            that.courseList[index].isSelect = true
            that.getCourseList()
          } else if (status === 401) {
            that.$message.info(response.data.message)
          } else {
            that.$message.error(response.data.message)
          }
        })
      }
      else {
        that.message({
          message: '您已选过该课程',
          type: 'warning'
        })
      }

    },
    goToHelloWorld: function () {
      this.cookie.clearCookie('s_id')
      this.cookie.clearCookie('s_name')
      this.$router.replace('/')
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
