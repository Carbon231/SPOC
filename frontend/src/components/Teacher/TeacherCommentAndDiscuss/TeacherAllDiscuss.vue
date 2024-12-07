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
        <el-main style="padding-left: 10%; padding-right: 10%">
          <el-row>
            <el-col :span="14" class="left-information" style="width: 50%">
              <el-row>
                <el-col :span="22">
                  <el-input placeholder="查找相关帖子" prefix-icon="el-icon-search" v-model="inputSearch"
                    style="margin-bottom: 5%"></el-input>
                </el-col>
                <el-col :span="2">
                  <el-button type="primary" icon="el-icon-search" style="float: right"
                    @click="searchDiscuss(inputSearch)" circle></el-button>
                </el-col>
              </el-row>
              <el-card v-for="(postTheme, index) in showPostThemeList" :key="index" v-loading="loading" shadow="hover"
                style="margin-bottom: 2%">
                <div class="clearfix">
                  <span>{{ postTheme.title }}</span>
                  <el-button style="float: right; padding: 3px 0" type="text"
                    v-on:click="enterPostTheme(index)">进入帖子</el-button>
                </div>
                <div class="textitem" style="font-size: 10px; margin-top: 2%; margin-bottom: 2%">
                  <el-tag size="mini">
                    <span v-if="postTheme.isTeacher === 0">学生</span>
                    <span v-else-if="postTheme.isTeacher === 1">教师</span>
                    <span v-else-if="postTheme.isTeacher === 2">管理员</span>
                  </el-tag>
                </div>
                <div>
                  <span style="color: gray; font-size: 8px">发表于-{{ postTheme.time }}</span>
                </div>
              </el-card>
            </el-col>
            <el-col :span="8" :offset="2" class="right-information">
              <el-card shadow="hover" style="width: 100%">
                <el-row>
                  <el-col :span="11">
                    <el-image :src="teacherImg" lazy></el-image>
                  </el-col>
                  <el-col :span="12" :offset="1">
                    <el-descriptions :column="1">
                      <el-descriptions-item label="用户名">{{ t_name }}</el-descriptions-item>
                      <el-descriptions-item label="工号">{{ t_id }}</el-descriptions-item>
                    </el-descriptions>
                  </el-col>
                </el-row>
                <el-row>
                  <el-divider></el-divider>
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
// import { quillEditor } from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import TeacherImg from '../../../assets/img/teacher.png'

export default {
  name: 'TeacherAllDiscuss',
  components: { TeacherNav, TeacherHeading },
  data: function () {
    return {
      loading: true,
      t_id: '',
      t_name: '',
      inputSearch: '',
      input: {
        title: '',
        content: ''
      },
      teacherImg: TeacherImg,
      postThemeList: [],
      showPostThemeList: [],
      buildThemeVisible: false,
      time: ''
    }
  },
  mounted: function () {
    this.t_id = this.cookie.getCookie('t_id')
    this.t_name = this.cookie.getCookie('t_name')
    this.getPostThemeList()
    this.getTeacherDiscussNum()
  },
  methods: {
    getPostThemeList: function () {
      let that = this
      that.loading = true
      this.$http.request({
        url: that.$url + 'GetPostThemeList/',
        method: 'post'
      }).then(function (response) {
        console.log(response.data)
        that.loading = false
        if (response.data.code === 200) {
          that.postThemeList = response.data.data
          that.showPostThemeList = response.data.data
        } else {
          that.$message.error(response.data.message)
        }
      }).catch(function (error) {
        console.log(error)
        that.loading = false
      })
    },
    searchDiscuss: function (inputSearch) {
      this.showPostThemeList = this.postThemeList.filter(postTheme => postTheme.title.includes(inputSearch))
    },
    enterPostTheme: function (index) {
      this.$router.push({ name: 'TeacherDiscuss', params: { id: this.showPostThemeList[index].id } })
    },
    getTime: function () {
      let dt = new Date()
      let yyyy = dt.getFullYear()
      let MM = (dt.getMonth() + 1).toString().padStart(2, '0')
      let dd = dt.getDate().toString().padStart(2, '0')
      let h = dt.getHours().toString().padStart(2, '0')
      let m = dt.getMinutes().toString().padStart(2, '0')
      let s = dt.getSeconds().toString().padStart(2, '0')
      this.time = yyyy + '-' + MM + '-' + dd + ' ' + h + ':' + m + ':' + s
    }
  }
}
</script>

<style scoped>
@import "../../../assets/css/back.css";
</style>