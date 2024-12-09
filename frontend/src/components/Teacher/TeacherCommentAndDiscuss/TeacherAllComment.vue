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
        <el-main style="padding-right: 10%; padding-left: 10%">
          <el-row>
            <el-col :span="14" class="left-information" style="width: 50%">
              <el-row>
                <el-col :span="22">
                  <el-input placeholder="查找您的相关课程" prefix-icon="el-icon-search" v-model="inputSearch"
                    style="margin-bottom: 5%"></el-input>
                </el-col>
                <el-col :span="2">
                  <el-button type="primary" icon="el-icon-search" style="float: right"
                    @click="searchCourse(inputSearch)" circle></el-button>
                </el-col>
              </el-row>
              <el-card v-for="(course, index) in showCourseList" :key="index" v-loading="loading" shadow="hover"
                style="margin-bottom: 2%">
                <el-row>
                  <el-col :offset="1" :span="2">
                    <el-image :src="courseImg" lazy></el-image>
                  </el-col>
                  <el-col :offset="2" :span="14">
                    <el-row style="margin-bottom: 3%">
                      <el-link type="primary" v-on:click="commentCourse(index)">
                        <span style="font-size: 16px"><strong>{{ course.c_name }}</strong></span>
                      </el-link>
                    </el-row>
                    <el-row>
                      <el-tag type="info">课程编号<span>&nbsp;&nbsp;{{ course.c_id }}</span></el-tag>
                    </el-row>
                  </el-col>
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
import TeacherNav from '../TeacherNav'
import TeacherHeading from '../TeacherHeading'
import CourseImg from '../../../assets/img/buaa_class_img.jpg'

export default {
  name: 'TeacherAllComment',
  components: { TeacherNav, TeacherHeading },
  data: function () {
    return {
      loading: true,
      courseImg: CourseImg,
      t_id: '',
      courseList: [],
      showCourseList: [],
      inputSearch: ''
    }
  },
  mounted: function () {
    this.t_id = this.cookie.getCookie('t_id')
  },
  methods: {
    searchCourse: function (query) {
      this.showCourseList = this.courseList.filter(course => course.c_name.includes(query))
    },
    commentCourse: function (index) {
      this.$router.push({ name: 'TeacherComment', params: { id: this.showCourseList[index].c_id } })
    }
  }
}
</script>

<style scoped>
@import "../../../assets/css/back.css";
</style>