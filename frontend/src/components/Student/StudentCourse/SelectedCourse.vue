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
          <el-card v-for="(course, index) in showMyCourseList" :key="index" shadow="hover" style="margin-bottom: 2%">
            <el-row v-loading="loading">
              <el-col :offset="2" :span="2">
                <el-image :src="courseImg" lazy></el-image>
              </el-col>
              <el-col :offset="2" :span="12">
                <el-row style="margin-bottom: 3%">
                  <el-link type="primary" v-on:click="getCourseInfo(index)">
                    <span style="font-size: 16px"><strong>{{ course.c_name }}</strong></span>
                  </el-link>
                </el-row>
                <el-row>
                  <el-tag type="info">课程编号<span>&nbsp;&nbsp;{{course.c_id}}</span></el-tag>
                </el-row>
              </el-col>
              <el-col :span="2">
                <el-button-group style="margin-top: 2%">
                  <el-button v-if="course.isSelect === 1" v-on:click="dropCourse(index)" type="danger" size="small">退课</el-button>
                  <el-button v-else-if="course.isSelect === 2" v-if="course.hasScore" type="primary" @click="viewScore(index)" size="small">查看成绩</el-button>
                  <el-button v-else type="info" disabled size="small">查看成绩</el-button>
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
          <el-dialog title="提示" :visible.sync="courseInfoVisible" width="40%">
            <el-descriptions class="info" direction="vertical">
              <el-descriptions-item label="课程名称(ID)">
                &nbsp;&nbsp;
                {{courseInfo.c_name}}({{courseInfo.c_id}})
              </el-descriptions-item>
              <el-descriptions-item label="课程介绍">&nbsp;&nbsp;
                <span v-html="courseInfo.intro "></span>
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
  name: 'StudentCourse',
  components: {StudentNav, StudentHeading},
  data: function () {
    return {
      courseInfoVisible: false,
      courseInfo: {
        c_id: '',
        c_name: '',
        t_name: '',
        intro: '',
        hasScore: false,
        isSelect: 1,
      },
      courseImg: CourseImg,
      loading: true,
      s_id: '',
      s_name: '',
      inputSearch: '',
      myCourseList: [{
        c_id: '1',
        c_name: '课程1',
        t_name: '教师1',
        avgDegree: 2.0,
        intro: '',
        hasScore: false,
        isSelect: 1,
      }],
      showMyCourseList: this.myCourseList,
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
      that.courseInfo = that.showMyCourseList[index]
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
        that.myCourseList = response.data.data
        that.showMyCourseList = response.data.data
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
            c_id: that.showMyCourseList[index].c_id
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
          c_id: that.showMyCourseList[index].c_id
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
      this.showMyCourseList = this.searchByIndexOf(inputSearch, this.myCourseList)
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
