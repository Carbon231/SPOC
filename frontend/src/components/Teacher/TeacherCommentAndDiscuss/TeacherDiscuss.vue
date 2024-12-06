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
          <el-divider>楼主</el-divider>
          <el-card shadow="hover" style="margin-bottom: 2%">
            <el-row v-loading="loading">
              <el-col :offset="2" :span="2">
                <el-row class="time">
                  {{postTheme.time}}
                </el-row>
                <el-row class="userName">
                  <el-col v-if="postTheme.isTeacher === 1">
                    {{postTheme.t_name}}({{postTheme.t_id}}) (教师)
                  </el-col>
                  <el-col v-else-if="postTheme.isTeacher === 2">
                    {{postTheme.t_name}}({{postTheme.t_id}}) (管理员)
                  </el-col>
                  <el-col v-else>
                    {{postTheme.s_name}}({{postTheme.s_id}})
                  </el-col>
                </el-row>
              </el-col>
              <el-col :offset="2" :span="16">
                <el-row class="content" v-html="postTheme.content">
                </el-row>
                <el-row class="delete" :span="1" style="float: right">
                  <div v-if="postTheme.t_id === t_id">
                    <el-link type="danger" @click="deletePostTheme">删除</el-link>
                  </div>
                </el-row>
              </el-col>
            </el-row>
          </el-card>
          <el-divider>跟帖</el-divider>
          <div v-for="(post, index) in postList" :key="index">
            <el-row>
              <el-col :span="1">
                <el-avatar v-if="post.isTeacher === 1" :src="teacherImg"></el-avatar>
                <el-avatar v-else-if="post.isTeacher === 2" :src="adminImg"></el-avatar>
                <el-avatar v-else :src="studentImg"></el-avatar>
              </el-col>
              <el-col :span="3">
                <el-row class="time">
                  {{post.time}}
                </el-row>
                <el-row class="userName">
                  <div v-if="post.isTeacher === 1">
                    {{post.t_name}}({{post.t_id}}) (教师) :
                  </div>
                  <div v-else-if="post.isTeacher === 2">
                    {{post.t_name}}({{post.t_id}}) (管理员) :
                  </div>
                  <div v-else>
                    {{post.s_name}}({{post.s_id}}) :
                  </div>
                </el-row>
              </el-col>
              <el-col class="content" :span="19" v-html="post.content">
              </el-col>
              <el-col class="delete" :span="1" style="float: right">
                <div v-if="post.t_id === t_id">
                  <el-link type="danger" @click="deletePost(post.id)">删除</el-link>
                </div>
              </el-col>
            </el-row>
            <el-divider></el-divider>
          </div>
          <el-dialog :visible.sync="dialogFormVisible">
            <el-input class="input" v-model="input.content" type="textarea" :rows="4" placeholder="与主题相关的讨论">
            </el-input>
            <div slot="footer" class="dialog-footer">
              <el-button @click="dialogFormVisible = false">取消</el-button>
              <el-button type="primary" @click="buildPost">确定</el-button>
            </div>
          </el-dialog>
          <el-button v-on:click="dialogFormVisible = true" type="primary" size="small">跟帖</el-button>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import TeacherNav from '../TeacherNav'
import TeacherHeading from '../TeacherHeading'
import TeacherImg from '../../../assets/img/teacher.png'
import StudentImg from '../../../assets/img/student.png'
import AdminImg from '../../../assets/img/admin.jpg'

export default {
  name: 'TeacherDiscuss',
  components: { TeacherNav, TeacherHeading },
  data: function () {
    return {
      loading: true,
      dialogFormVisible: false,
      t_id: '',
      studentImg: StudentImg,
      teacherImg: TeacherImg,
      adminImg: AdminImg,
      postThemeId: 0,
      postTheme: {
        id: '',
        t_id: '',
        t_name: '',
        s_id: '',
        s_name: '',
        title: '',
        content: '',
        time: '',
        isTeacher: 1
      },
      input: {
        content: ''
      },
      postList: [],
      time: ''
    }
  },
  mounted: function () {
    this.t_id = this.cookie.getCookie('t_id')
    this.postThemeId = this.$route.params.id
    this.getPostTheme()
    this.getPostList()
  },
  methods: {
    getPostTheme: function () {
      let that = this
      this.$http.request({
        url: that.$url + 'GetPostTheme/',
        method: 'post',
        data: {
          pt_id: that.postThemeId
        }
      }).then(function (response) {
        console.log(response.data)
        that.postTheme = response.data.data
      }).catch(function (error) {
        console.log(error)
      })
    },
    getPostList: function () {
      let that = this
      this.$http.request({
        url: that.$url + 'GetPostList/',
        method: 'post',
        data: {
          pt_id: that.postThemeId
        }
      }).then(function (response) {
        console.log(response.data)
        that.postList = response.data.data
      }).catch(function (error) {
        console.log(error)
      })
    },
    buildPost: function () {
      this.dialogFormVisible = false
      let that = this
      that.getTime()
      this.$http.request({
        url: that.$url + 'BuildPost/',
        method: 'post',
        data: {
          pt_id: that.postThemeId,
          t_id: that.t_id,
          content: that.input.content,
          time: that.time,
          isTeacher: 1
        }
      }).then(function (response) {
        console.log(response.data)
        if (response.data.code === 200) {
          that.$message.success('跟帖成功')
          that.getPostList()
          that.input.content = ''
        } else {
          that.$message.error('未知错误')
        }
      }).catch(function (error) {
        console.log(error)
      })
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
            pt_id: that.postThemeId
          }
        }).then(function (response) {
          console.log(response.data)
          if (response.data.code === 200) {
            that.$message.success('删除成功')
            that.returnTeacherAllDiscuss()
          } else {
            that.$message.error('未知错误')
          }
        }).catch(function (error) {
          console.log(error)
        })
      })
    },
    deletePost: function (postId) {
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
            p_id: postId
          }
        }).then(function (response) {
          console.log(response.data)
          if (response.data.code === 200) {
            that.$message.success('删除成功')
            that.getPostList()
          } else {
            that.$message.error('未知错误')
          }
        }).catch(function (error) {
          console.log(error)
        })
      })
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
    },
    returnTeacherAllDiscuss: function () {
      this.$router.push({ name: 'TeacherAllDiscuss' })
    }
  }
}
</script>

<style scoped>
@import "../../../assets/css/back.css";
</style>