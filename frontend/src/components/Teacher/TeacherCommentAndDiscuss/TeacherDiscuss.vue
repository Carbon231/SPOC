<template>
  <div>
    <el-container class="background">
      <el-aside class="aside" width="show?'64px':'300px'">
        <TeacherNav></TeacherNav>
      </el-aside>
      <el-container class="main">
        <el-header>
          <TeacherHeading></TeacherHeading>
        </el-header>
        <el-main style="padding-left: 10%; padding-right: 10%">
          <el-page-header @back="returnTeacherAllDiscuss" :content="postTheme.title" style="margin-bottom: 2%">
          </el-page-header>
          <el-row class="buttons">
          </el-row>
          <el-divider>楼主</el-divider>
          <el-card shadow="hover" style="margin-bottom: 2%">
            <el-row>
              <el-col :offset="2" :span="2">
                <el-row class="time">
                  {{ postTheme.time }}
                </el-row>
                <el-row class="s_id">
                  <el-col v-if="postTheme.isExcellent === 1">
                    {{ postTheme.s_name }}({{ postTheme.s_id }}) (教师)
                  </el-col>
                  <el-col v-else-if="postTheme.isExcellent === 2">
                    {{ postTheme.s_name }}({{ postTheme.s_id }}) (管理员)
                  </el-col>
                  <el-col v-else>
                    {{ postTheme.s_name }}({{ postTheme.s_id }})
                  </el-col>
                </el-row>
              </el-col>
              <el-col offset="2" :span="18">
                <el-row class="content" v-html="postTheme.content">
                </el-row>
                <el-col class="delete" :span="1" style="float: right">
                  <div>
                    <el-link type="danger" v-on:click="deletePostTheme">删除</el-link>
                  </div>
                </el-col>
              </el-col>
            </el-row>
          </el-card>
          <el-divider>跟贴</el-divider>
          <div v-for="(post, index) in postList" v-bind:key="index">
            <el-row v-loading="loading">
              <el-col :span="1" :offset="1">
                <el-image v-if="post.isExcellent === 1" :src="teacherImg" lazy></el-image>
                <el-image v-else-if="post.isExcellent === 2" :src="adminImg" lazy></el-image>
                <el-image v-else :src="studentImg" lazy></el-image>
              </el-col>
              <el-col :span="3">
                <el-row class="time">
                  {{ post.time }}
                </el-row>
                <el-row class="s_id">
                  <div v-if="post.isExcellent === 1">
                    {{ post.s_name }}({{ post.s_id }}) (教师) :
                  </div>
                  <div v-else-if="post.isExcellent === 2">
                    {{ post.s_name }}({{ post.s_id }}) (管理员) :
                  </div>
                  <div v-else>
                    {{ post.s_name }}({{ post.s_id }}) :
                  </div>
                </el-row>
              </el-col>
              <el-col class="content" :span="18" v-html="post.content">
              </el-col>
              <el-col class="delete" :span="1" style="float: right">
                <div>
                  <el-link type="danger" v-on:click="deletePost(post.p_id)">删除</el-link>
                </div>
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
  font-size: large;
}

.time {
  font-size: small;
  color: #e2e2e2;
}

.t_id {
  font-size: small;
  color: #66b1ff;
}

.content {
  font-size: medium;
  word-break: break-all;
}
</style>

<script>
import TeacherNav from '../TeacherNav'
import TeacherHeading from '../TeacherHeading'
import StudentImg from '../../../assets/img/student.png'
import TeacherImg from '../../../assets/img/teacher.png'
import AdminImg from '../../../assets/img/admin.jpg'

export default {
  name: 'TeacherDiscuss',
  components: { TeacherNav, TeacherHeading },
  data: function () {
    return {
      loading: true,
      t_id: '',
      t_name: '',
      dialogFormVisible: false,
      studentImg: StudentImg,
      teacherImg: TeacherImg,
      adminImg: AdminImg,
      p_id: 0,
      postTheme: {
        pt_id: '',
        s_id: '',
        s_name: '',
        title: '',
        content: '',
        time: '',
        isExcellent: 0
      },
      input: {
        content: ''
      },
      postList: [{
        p_id: '',
        s_id: '',
        s_name: '',
        content: '',
        time: '',
        isExcellent: 0
      }],
      time: ''
    }
  },
  mounted() {
    this.t_id = this.cookie.getCookie('t_id')
    this.t_name = this.cookie.getCookie('t_name')
    this.pt_id = this.$route.query.pt_id
    console.log(this.pt_id)
    this.getPostTheme()
    this.getPostList()
    console.log('Checking...')
    console.log(this.postTheme)
  },
  methods: {
    getPostTheme: function () {
      let that = this
      this.$http.request({
        url: that.$url + 'GetPostTheme/',
        method: 'post',
        data: {
          pt_id: that.pt_id
        },
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        that.postTheme = response.data.data
      }).catch(function (error) {
        console.log(error)
      })
    },
    getTime: function () {
      let that = this
      let dt = new Date()
      let yyyy = dt.getFullYear()
      let MM = (dt.getMonth() + 1).toString().padStart(2, '0')
      let dd = dt.getDate().toString().padStart(2, '0')
      let h = dt.getHours().toString().padStart(2, '0')
      let m = dt.getMinutes().toString().padStart(2, '0')
      let s = dt.getSeconds().toString().padStart(2, '0')
      that.time = yyyy + '-' + MM + '-' + dd + ' ' + h + ':' + m + ':' + s
    },
    deletePostTheme: function () {
      this.$confirm('此操作将永久删除该主题贴及其跟贴，是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let that = this
        that.getTime()
        this.$http.request({
          url: that.$url + 'DeletePostTheme/',
          method: 'post',
          data: {
            pt_id: that.pt_id
          },
          headers: {
            'Content-Type': 'application/json'
          }
        }).then(function (response) {
          console.log(response.data)
          if (response.data === 0) {
            that.$message.success(response.data.message)
            that.returnTeacherAllDiscuss()
          } else {
            that.$message.error('未知错误')
          }
        }).catch(function (error) {
          console.log(error)
        })
      })
    },
    getPostList: function () {
      let that = this
      that.loading = true
      this.$http.request({
        url: that.$url + 'GetPostList/',
        method: 'post',
        data: {
          pt_id: that.pt_id
        },
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(function (response) {
        console.log(response.data)
        that.loading = false
        that.postList = response.data.data
      }).catch(function (error) {
        console.log(error)
        that.loading = false
      })
    },
    deletePost: function (p_id) {
      this.$confirm('此操作将永久删除该跟贴，是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let that = this
        that.getTime()
        this.$http.request({
          url: that.$url + 'DeletePost/',
          method: 'post',
          data: {
            p_id: p_id
          },
          headers: {
            'Content-Type': 'application/json'
          }
        }).then(function (response) {
          console.log(response.data)
          if (response.data.code === 200) {
            that.$message.success(response.data.message)
            that.getPostList()
          } else {
            that.$message.error('未知错误')
          }
        }).catch(function (error) {
          console.log(error)
        })
      })
    },
    returnTeacherAllDiscuss: function () {
      let that = this
      that.$router.push({
        name: 'TeacherAllDiscuss'
      })
    },
    goToHelloWorld: function () {
      this.cookie.clearCookie('t_id')
      this.cookie.clearCookie('t_name')
      this.$router.replace('/')
    }
  }
}
</script>
