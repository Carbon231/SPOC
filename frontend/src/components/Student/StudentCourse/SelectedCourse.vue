<template>
  <div>
    <el-container>
      <el-aside class="aside" width="show?'64px':'400px'">
        <StudentNav></StudentNav>
      </el-aside>
      <el-container class="main">
        <el-header>
          <StudentHeading></StudentHeading>
        </el-header>
        <el-main style="padding-right: 10%; padding-left: 10%">
          <el-row>
            <el-col :span="22">
              <el-input placeholder="查找您的相关课程" prefix-icon="el-icon-search" v-model="inputSearch"
                style="margin-bottom: 5%"></el-input>
            </el-col>
            <el-col :span="2">
              <el-button type="primary" icon="el-icon-search" style="float: right" @click="searchCourse(inputSearch)"
                circle></el-button>
            </el-col>
          </el-row>
          <el-card v-for="(course, index) in showCourseList" :key="index" v-loading="loading" shadow="hover"
            style="margin-bottom: 2%;">
            <el-row>
              <el-col :offset="2" :span="2">
                <el-image :src="courseImg" lazy></el-image>
              </el-col>
              <el-col :offset="2" :span="14">
                <el-row style="margin-bottom: 3%">
                  <el-link type="primary" v-on:click="getCourseInfo(index)">
                    <span style="font-size: 16px"><strong>{{ course.c_name }}</strong></span>
                  </el-link>
                </el-row>
                <el-row>
                  <el-tag type="primary" style="margin-right: 10px;">授课教师<span>&nbsp;&nbsp;{{ course.t_name
                      }}</span></el-tag>
                  <el-tag type="success">开课院系<span>&nbsp;&nbsp;{{ course.d_name }}</span></el-tag>
                </el-row>
              </el-col>
              <el-col :span="2">
                <span style="color: gray">{{ course.selectedNum }} / {{ course.capacity }}</span>
              </el-col>
              <el-col :span="2">
                <el-button-group style="margin-top: 2%">
                  <el-button v-if="course.isSelect === 1" v-on:click="dropCourse(index)" type="danger">退课</el-button>
                  <el-button v-else-if="course.isSelect === 2 && course.hasScore" type="primary"
                    @click="viewScore(index)">查看成绩</el-button>
                  <el-button v-else type="info" disabled>查看成绩</el-button>
                </el-button-group>
              </el-col>
            </el-row>
          </el-card>
          <el-dialog title="课程成绩" :visible.sync="gradesDialogVisible" width="30%">
            <div v-if="currentCourseScore">
              <p>成绩：{{ currentCourseScore }}</p>
            </div>
            <div v-else>
              <p>该课程暂无成绩信息。</p>
            </div>
            <div slot="footer" class="dialog-footer">
              <el-button @click="gradesDialogVisible = false">确 定</el-button>
            </div>
          </el-dialog>
          <el-dialog :visible.sync="courseInfoVisible">
            <el-descriptions class="margin-top" border>
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-s-management"></i>
                  课程名称
                </template>
                {{ courseInfo.c_name }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-sunny"></i>
                  课程编号
                </template>
                {{ courseInfo.c_id }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-s-home"></i>
                  开课院系
                </template>
                {{ courseInfo.d_name }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-s-custom"></i>
                  授课教师
                </template>
                {{ courseInfo.t_name }}
              </el-descriptions-item>
              <el-descriptions-item>
                <template slot="label">
                  <i class="el-icon-info"></i>
                  课程简介
                </template>
                <span v-html="courseInfo.intro"></span>
              </el-descriptions-item>
            </el-descriptions>
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
  name: 'StudentCourse',
  components: { StudentNav, StudentHeading },
  data: function () {
    return {
      courseInfoVisible: false,
      courseInfo: {
        c_id: '',
        c_name: '',
        d_name: '',
        t_name: '',
        isSelect: 1,
        avgDegree: 0,
        capacity: 0,
        selectedNum: 0,
        d_id: 0,
        isOpen: false,
        intro: '',
        hasScore: false
      },
      courseImg: CourseImg,
      loading: true,
      s_id: '',
      s_name: '',
      inputSearch: '',
      courseList: [{
        c_id: '1',
        c_name: '课程1',
        t_name: '教师1',
        avgDegree: 2.0,
        d_name: '院系1',
        intro: '',
        hasScore: false,
        isSelect: 1,
      }],
      showCourseList: this.courseList,
      gradesDialogVisible: false,
      currentCourseScore: null
    }
  },
  mounted: function () {
    this.s_id = this.cookie.getCookie('s_id')
    this.s_name = this.cookie.getCookie('s_name')
    this.getStudentCourseList()
  },
  methods: {
    getCourseInfo: function (index) {
      let that = this
      that.courseInfo = that.showCourseList[index]
      that.courseInfoVisible = true
    },
    getStudentCourseList: function () {
      let that = this
      that.loading = true
      this.$http.request({
        url: that.$url + 'GetStudentCourseList/',
        method: 'post',
        data: {
          s_id: that.s_id
        },
        headers: {
          'Content-Type': 'application/json'
        }
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
    dropCourse: function (index) {
      this.$confirm('此操作将退选该课程，是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        console.log(index)
        let that = this
        this.$http.request({
          url: that.$url + 'DropCourse/',
          method: 'post',
          data: {
            s_id: that.s_id,
            c_id: that.showCourseList[index].c_id
          }
        }).then(function (response) {
          console.log(response.data)
          if (response.data.code === 200) {
            that.$message.success(response.data.message)
          } else {
            that.$message.error('未知错误')
          }
          that.getStudentCourseList()
        }).catch(function (error) {
          console.log(error)
        })
      })
    },
    viewScore: function (index) {
      let that = this
      this.$http.request({
        url: that.$url + 'GetStudentCourseScore/',
        method: 'post',
        data: {
          s_id: that.s_id,
          c_id: that.showCourseList[index].c_id
        },
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        if (response.data.code === 200) {
          that.$message.success(response.data.message)
          that.gradesDialogVisible = true;
          that.currentCourseScore = response.data.data.score;
        } else {
          that.$message.error('未知错误')
        }
      }).catch(function (error) {
        console.log(error)
      })
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
