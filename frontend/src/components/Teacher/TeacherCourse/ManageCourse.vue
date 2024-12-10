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
                <el-button-group>
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
        t_name: '',
        capacity: '',
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
    getScoreDistribution(index) {
      let that = this;
      let course = this.showMyCourseList[index];
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