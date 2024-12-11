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
        <el-main style="padding-right: 10%; padding-left: 10%">
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
          <el-card v-for="(course, index) in showCourseList" :key="index" v-loading="loading" shadow="hover"
            style="margin-bottom: 2%;">
            <el-row>
              <el-col :offset="1" :span="2">
                <el-image style="width:150px;height:90px" :src="courseImg" lazy></el-image>
              </el-col>
              <el-col :offset="2" :span="12">
                <el-row style="margin-bottom: 3%">
                  <el-link type="primary" v-on:click="getCourseInfo(index)">
                    <span style="font-size: 18px"><strong>{{ course.c_name }}</strong></span>
                  </el-link>
                </el-row>
                <el-row>
                  <el-tag style="font-size: 15px" type="info">课程编号<span>&nbsp;&nbsp;{{ course.c_id }}</span></el-tag>
                  <el-tag style="font-size: 15px; margin-left:2%" type="success">开课院系<span>&nbsp;&nbsp;{{ course.d_name
                      }}</span></el-tag>
                </el-row>
              </el-col>
              <el-col :span="2">
                <span style="color: gray">{{ course.selectedNum }} / {{ course.capacity }}</span>
              </el-col>
              <el-col :span="4">
                <el-button-group>
                  <el-button style="margin-right: 5px" type="primary" icon="el-icon-edit"
                    v-on:click="changeCourse(index)">编辑</el-button>
                  <el-button type="danger" icon="el-icon-delete" v-on:click="cancelCourse(index)">停课</el-button>
                </el-button-group>
                <el-button-group style="margin-top: 2%;margin-left:10px">
                  <el-button type="info" icon="el-icon-pie-chart"
                    v-on:click="getScoreDistribution(index)">查看分数分布</el-button>
                </el-button-group>
              </el-col>
            </el-row>
          </el-card>
          <el-dialog title="课程详情" :visible.sync="courseInfoVisible" width="60%">
            <el-descriptions class="info">
              <el-descriptions-item label="课程名称(ID)">
                {{ courseInfo.c_name }}({{ courseInfo.c_id }})
              </el-descriptions-item>
              <el-descriptions-item label="课程介绍">
                <span v-html="courseInfo.intro"></span>
              </el-descriptions-item>
              <el-descriptions-item label="课程容量">
                <span v-html="courseInfo.capacity"></span>
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
          <el-dialog title="分数分布" :visible.sync="scoreDistributionVisible">
            <div id="score-distribution-chart" style="width: 100%; height: 400px;"></div>
            <div slot="footer" class="dialog-footer">
              <el-button type="primary" @click="scoreDistributionVisible = false">确 定</el-button>
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
import * as echarts from 'echarts';
import TeacherNav from '../TeacherNav'
import TeacherHeading from '../TeacherHeading'
import CourseImg from '../../../assets/img/buaa_class_img.jpg'

export default {
  name: 'ManageCourse',
  components: { TeacherNav, TeacherHeading },
  data: function () {
    return {
      courseInfoVisible: false,
      scoreDistributionVisible: false,
      courseInfo: {
        c_id: '',
        c_name: '',
        d_name: '',
        t_name: '',
        capacity: '',
        intro: ''
      },
      courseImg: CourseImg,
      loading: false,
      t_id: '',
      t_name: '',
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
      that.courseInfo = that.courseList[index]
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
    changeCourse: function (index) {
      this.$router.push({ name: 'ChangeCourse', params: { id: this.showCourseList[index].c_id } })
    },
    cancelCourse: function (index) {
      this.$confirm('此操作将退选该课程，是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let that = this
        that.loading = true
        this.$http.request({
          url: that.$url + 'CancelCourse/',
          method: 'post',
          data: {
            c_id: that.showCourseList[index].c_id,
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
      })
    },
    goToHelloWorld: function () {
      this.cookie.clearCookie('t_id')
      this.cookie.clearCookie('t_name')
      this.$router.replace('/')
    },
    getScoreDistribution(index) {
      let that = this;
      let course = this.showCourseList[index];
      console.log(course);

      this.$http.request({
        url: that.$url + 'GetScoreDistribution/',
        method: 'post',
        data: {
          c_id: course.c_id
        }
      }).then(function (response) {
        if (response.data.code === 200) {
          that.scoreDistributionVisible = true;
          that.$nextTick(() => {
            that.drawScoreDistributionChart(response.data.data);
          });
        } else {
          that.$message.error(response.data.message);
        }
      }).catch(function (error) {
        console.error(error);
        that.$message.error('获取分数分布失败');
      });
    },
    drawScoreDistributionChart(data) {
      let chartDom = document.getElementById('score-distribution-chart');
      let myChart = echarts.init(chartDom);
      let option = {
        title: {
          text: '分数分布'
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['0-20', '20-40', '40-60', '60-80', '80-100']
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: [data['0-20'], data['20-40'], data['40-60'], data['60-80'], data['80-100']],
          type: 'bar'
        }]
      };
      option && myChart.setOption(option);
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
  }
}
</script>
