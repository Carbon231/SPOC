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
            <el-col :span="8">
              <el-select v-model="departmentSelect" @change="filtrate()" clearable placeholder="开课院系">
                <el-option v-for="dep in departmentSelections" :key="dep.d_id" :value="dep.d_name">
                </el-option>
              </el-select>
            </el-col>
            <el-col :span="8">
              <el-select v-model="chooseCourseStatus" @change="filtrate()" clearable placeholder="选课状态">
                <el-option v-for="s in courseStatusLists" :key="s.label" :value="s.value">
                </el-option>
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-input placeholder="课程名" prefix-icon="el-icon-search" v-model="inputSearch"
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
                  <!--                  <el-button v-if="!showCourseList[index].isSelect" v-on:click="selectCourse(index)" type="primary">选课</el-button>-->
                  <!--                  <el-button v-else type="info" disabled>已选</el-button>-->
                  <el-button v-if="showCourseList[index].isSelect !== 0" type="warning" disabled>已选</el-button>
                  <el-button v-else-if="showCourseList[index].isOpen" type="info" disabled>不可选</el-button>
                  <el-button v-else type="primary" @click="selectCourse(index)">选课</el-button>
                </el-button-group>
              </el-col>
            </el-row>
          </el-card>
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
        isSelect: 1,
        avgDegree: 0,
        capacity: 0,
        selectedNum: 0,
        d_id: 0,
        isOpen: false,
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
      inputSearch: '',
      tempCourseList: [],
      departmentSelections: '',
      departmentSelect: '',
      chooseCourseStatus: '',
      courseStatusLists: [{
        label: '0',
        value: '全部'
      }, {
        label: '1',
        value: '已选'
      }, {
        label: '2',
        value: '未选'
      }, {
        label: '3',
        value: '已开课'
      }
      ]
    }
  },
  mounted: function () {
    this.s_id = this.cookie.getCookie('s_id')
    this.s_name = this.cookie.getCookie('s_name')
    this.getCourseList()
    this.getAllDepartments()
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
    getAllDepartments() {
      let that = this
      this.$http.request({
        url: that.$url + 'GetAllDepartments/',
        method: 'get',
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        that.departmentSelections = response.data.data
        that.departmentSelections.unshift({ d_id: 0, d_name: '全部' })
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
        if (list[i].c_name.toString().includes(keyWord) || list[i].c_id.toString().includes(keyWord)) {
          arr.push(list[i])
        }
      }
      return arr
    },
    filtrate: function () {
      let that = this
      that.tempCourseList = that.courseList
      that.filtrateDepartment()
      that.filtrateStatus()
      that.showCourseList = that.tempCourseList
    },
    filtrateDepartment: function () {
      let that = this
      let newCourseList = []
      if (that.departmentSelect && that.departmentSelect !== '全部') {
        for (let i = 0; i < that.tempCourseList.length; i++) {
          if (that.departmentSelect === that.tempCourseList[i].d_name) {
            newCourseList.push(that.tempCourseList[i])
          }
        }
        that.tempCourseList = newCourseList
      }

    },
    filtrateStatus: function () {
      let that = this
      let newCourseList = []
      if (that.chooseCourseStatus && that.chooseCourseStatus !== '全部') {
        for (let i = 0; i < that.tempCourseList.length; i++) {
          if (that.chooseCourseStatus === '已选' && (that.tempCourseList[i].isSelect === 1 || that.tempCourseList[i].isSelect === 2 || that.tempCourseList[i].isSelect === 3)) {
            that.showCourseList.push(that.tempCourseList[i])
          } else if (that.chooseCourseStatus === '未选' && that.tempCourseList[i].isSelect === 0) {
            that.showCourseList.push(that.tempCourseList[i])
          } else if (that.chooseCourseStatus === '已开课' && that.tempCourseList[i].isOpen) {
            that.showCourseList.push(that.tempCourseList[i])
          }
        }
        that.tempCourseList = newCourseList
      }
    },
  }
}
</script>
