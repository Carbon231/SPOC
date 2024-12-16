<template>
  <transition name="head-login-register">
    <div class="welcome">
    <div class="navigator">
      <div class="navigator-left">
        <i class="el-icon-s-platform"><span class="el-icon-s-platform-text">&nbsp;&nbsp;Sharing课程平台</span></i>
      </div>
      <div class="navigator-right">
        <span><el-button class="buttons" @click="goToStudentLogin">学生登录</el-button></span>
        <span>&nbsp;&nbsp;</span>
        <span><el-button class="buttons" @click="goToTeacherLogin">教师登录</el-button></span>
      </div>
  </div>
    <div class="introduction">
      <el-carousel height="400px">
        <el-carousel-item v-for="(item, index) in headImg" :key="index">
          <img :src="item.src" style="width: 100%; height: 100%;" alt="">
        </el-carousel-item>
      </el-carousel>
    </div>
    <div class="line_1">
      <div class="line-1-head"><span class="div-head">课程推荐</span></div>
      <br><br>
      <div class="line-1-content">
        <el-row class="this-el-row">
          <el-col :span="5" :offset="2" >
            <el-card >
              <img
                :src="cardImg_group.src"
                alt=""
                style="width: 100%; height: auto"/>
              <p>{{cardImg_group.title}}</p>
            </el-card>
          </el-col>
          <el-col :span="5" :offset="2" >
            <el-card >
              <img
                style="width: 100%; height: auto"
                :src="cardImg_book.src"
                alt=""/>
              <p>{{cardImg_book.title}}</p>
            </el-card>
          </el-col>
          <el-col :span="5" :offset="2" >
            <el-card >
              <img
                :src="cardImg_join.src"
                alt=""
                style="width: 100%; height: auto"/>
              <p>{{cardImg_join.title}}</p>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
  </transition>
</template>

<script>
import technology from '../assets/img/AI助手.png'
import book from '../assets/img/智学北航.png'
import Computer from '../assets/img/人才培养.png'
import cardBook from '../assets/img/300-240-book.jpg'
import cardJoin from '../assets/img/300-240-add.jpg'
import cardGroup from '../assets/img/300-240-group.png'

export default {
  data: function () {
    return {
      headImg: [
        {
          'src': technology
        },
        {
          'src': book
        },
        {
          'src': Computer
        }
      ],
      cardImg_group: {
        'id': 'group',
        'title': '计算机组成原理',
        'src': cardGroup
      },
      cardImg_join: {
        'id': 'join',
        'title': '编译原理',
        'src': cardJoin
      },
      cardImg_book: {
        'id': 'book',
        'title': '面向对象设计与构造',
        'src': cardBook
      },
      fullscreenLoading: false
    }
  },
  methods: {
    goToStudentLogin () {
      this.$router.push({
        name: 'StudentLogin'
      })
    },
    goToTeacherLogin () {
      this.$router.push({
        name: 'TeacherLogin'
      })
    },
    goToAdminLogin () {
      this.$router.push({
        name: 'AdminLogin'
      })
    }
  }
}
</script>

<style scoped>
  @import "../assets/css/HelloWorld/block1.css";
  @import "../assets/css/HelloWorld/block2.css";
  @import "../assets/css/HelloWorld/copyright.css";
  @import "../assets/css/HelloWorld/introduction.css";
  @import "../assets/css/HelloWorld/navigator.css";
  @import "../assets/css/Transition/head-login-register.css";
  .welcome {
    margin-left: 40px;
    margin-right: 40px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
  }

</style>
