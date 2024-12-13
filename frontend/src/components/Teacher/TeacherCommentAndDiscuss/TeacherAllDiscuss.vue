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



              <el-row>
                <el-col :span="8" style="margin-bottom: 5%;margin-right: 5%;">
                  <el-select v-model="departmentSelect" @change="filtrateDepartment" clearable placeholder="筛选">
                    <el-option>只看我赞过的</el-option>
                  </el-select>
                </el-col>
                <el-col :span="8">
                  <el-select v-model="chooseCourseStatus" @change="filtrateStatus" clearable placeholder="查看顺序">
                    <el-option v-for="s in courseStatusLists" :key="s.label" :value="s.value"></el-option>
                  </el-select>
                </el-col>
              </el-row>

              <el-card v-for="(postTheme, index) in showPostThemeList" :key="index" v-loading="loading" shadow="hover"
                style="margin-bottom: 2%">
                <div class="clearfix">
                  <span>{{ postTheme.title }}</span>
                  <el-button style="float: right; padding: 3px 0" type="text"
                    v-on:click="enterPostTheme(index)">进入帖子</el-button>
                  <el-button v-if="!postTheme.isLiked" icon="el-icon-thumb" @click="likedPostTheme(index)">{{
                    postTheme.likedNum }} 点赞</el-button>
                  <el-button v-if="postTheme.isLiked" icon="el-icon-thumb" @click="cancelLikedPostTheme(index)">{{
                    postTheme.likedNum }} 取消点赞</el-button>
                </div>
                <el-icon></el-icon>
                <div class="textitem" style="font-size: 10px; margin-top: 2%; margin-bottom: 2%">
                  <el-tag size="mini" type="success" v-if="postTheme.isExcellent === 1">
                    <span>经助教认证</span>
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
                      <el-descriptions-item label="姓名">{{ t_name }}</el-descriptions-item>
                      <el-descriptions-item label="工号">{{ t_id }}</el-descriptions-item>
                      <el-descriptions-item label="已发帖子">{{ discussNum }}</el-descriptions-item>
                    </el-descriptions>
                  </el-col>
                </el-row>
                <el-row>
                  <el-divider></el-divider>
                </el-row>
                <el-row>
                  <el-button @click="buildThemeVisible = true" style="width: 100%" type="primary">新建主题贴</el-button>
                  <el-dialog title="新建主题帖" :visible.sync="buildThemeVisible" width="70%">
                    <el-row style="margin-bottom: 10px">
                      <el-col>
                        <el-input v-model="input.title" placeholder="请输入标题"></el-input>
                      </el-col>
                    </el-row>
                    <el-row style="margin-bottom: 10px">
                      <el-col>
                        <quill-editor ref="text" v-model="input.content" style="height: 300px"></quill-editor>
                      </el-col>
                    </el-row>
                    <div slot="footer" class="dialog-footer" style="margin-top: 10%">
                      <el-button @click="buildThemeVisible = false">取消</el-button>
                      <el-button type="primary" @click="buildPostTheme">确定</el-button>
                    </div>
                  </el-dialog>
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
import { quillEditor } from 'vue-quill-editor'
import 'quill/dist/quill.core.css'
import 'quill/dist/quill.snow.css'
import 'quill/dist/quill.bubble.css'
import TeacherImg from '../../../assets/img/teacher.png'


export default {
  name: 'TeacherAllDiscuss',
  components: { TeacherNav, TeacherHeading, quillEditor },
  data: function () {
    return {
      loading: true,
      t_id: '',
      t_name: '',
      discussNum: '',
      teacherImg: TeacherImg,
      input: {
        title: '',
        content: ''
      },
      inputSearch: '',
      postThemeList: [{}],
      showPostThemeList: [{}],
      myLikedPostThemeList: [{}],
      buildThemeVisible: false,
      time: ''
    }
  },
  mounted: function () {
    this.t_id = this.cookie.getCookie('t_id')
    this.t_name = this.cookie.getCookie('t_name')
    this.getPostThemeList()
    this.getTeacherDiscussNum()
    this.getMyLikedPostThemeList()
  },
  methods: {
    likedPostTheme: function (index) {
      let that = this
      this.$http.request({
        url: that.$url + 'LikedPostTheme/',
        method: 'post',
        data: {
          u_id: that.t_id,
          pt_id: that.showPostThemeList[index].pt_id
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        if (response.data.code === 200) {
          that.$message.success('点赞成功')
          that.getMyLikedPostThemeList()
          that.$router.go(0)
        } else {
          that.$message.error('未知错误')
        }
      }).catch(function (error) {
        console.log(error)
      })
    },
    cancelLikedPostTheme: function (index) {
      let that = this
      this.$http.request({
        url: that.$url + 'CancelLikedPostTheme/',
        method: 'post',
        data: {
          u_id: that.t_id,
          pt_id: that.showPostThemeList[index].pt_id
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        if (response.data.code === 200) {
          that.$message.success('取消点赞成功')
          that.$router.go(0)
        } else {
          that.$message.error('未知错误')
        }
      }).catch(function (error) {
        console.log(error)
      })
    },
    getMyLikedPostThemeList: function () {
      let that = this
      this.$http.request({
        url: that.$url + 'GetLikedPostThemeList/',
        method: 'post',
        data: {
          u_id: that.t_id
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        that.myLikedPostThemeList = response.data.data
      }).catch(function (error) {
        console.log(error)
      })
    },
    getTeacherDiscussNum: function () {
      let that = this
      this.$http.request({
        url: that.$url + 'GetTeacherDiscussNum/',
        method: 'post',
        data: {
          t_id: that.t_id
        }
      }).then(function (response) {
        console.log(response.data)
        that.discussNum = response.data.data.discussNum
      }).catch(function (error) {
        console.log(error)
      })
    },
    getPostThemeList: function () {
      let that = this
      that.loading = true
      this.$http.request({
        url: that.$url + 'GetPostThemeList/',
        method: 'post',
        data: {
          u_id: that.t_id
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        that.loading = false
        that.postThemeList = response.data.data
        that.showPostThemeList = response.data.data
      }).catch(function (error) {
        console.log(error)
        that.loading = false
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
    buildPostTheme: function () {
      let that = this
      that.getTime()
      this.$http.request({
        url: that.$url + 'BuildPostTheme/',
        method: 'post',
        data: {
          u_id: that.t_id,
          title: that.input.title,
          content: that.input.content,
          time: that.time
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        if (response.data.code === 200) {
          that.$message.success('创建成功')
          that.buildThemeVisible = false
          that.getPostThemeList()
          that.getTeacherDiscussNum()
          that.input = {
            title: '',
            content: ''
          }
        } else {
          that.$message.error('未知错误')
        }
      }).catch(function (error) {
        console.log(error)
      })
    },
    enterPostTheme: function (index) {
      let that = this
      this.$router.push({
        name: 'TeacherDiscuss',
        query: {
          pt_id: that.showPostThemeList[index].pt_id,
        }
      })
    },
    goToHelloWorld: function () {
      this.cookie.clearCookie('t_id')
      this.cookie.clearCookie('t_name')
      this.$router.replace('/')
    },
    searchDiscuss: function (inputSearch) {
      this.showPostThemeList = this.searchByIndexOf(inputSearch, this.postThemeList)
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
        if (list[i].title.toString().includes(keyWord)) {
          arr.push(list[i])
        }
      }
      return arr
    }
  }
}
</script>

<style scoped>
@import "../../../assets/css/back.css";
</style>
