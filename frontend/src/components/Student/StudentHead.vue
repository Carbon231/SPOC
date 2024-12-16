<template>
  <div>
    <el-container>
      <el-aside class="aside" width="show?'64px':30%">
        <StudentNav></StudentNav>
      </el-aside>
      <el-container class="main">
        <el-header>
          <StudentHeading></StudentHeading>
        </el-header>
        <el-main style="padding-left: 10%; padding-right: 10%">
          <h1>Sharing课程平台</h1>
          <ul>
            <li>介绍</li>
            <li>项目地址</li>
          </ul>

          <h2>介绍</h2>
          <p>Sharing课程平台是一个创新的在线教育解决方案，旨在为学生和教师提供一个全面、互动和用户友好的选课、教学和学习环境。</p>

          <h4>(1)综合需求</h4>
          <p>Sharing课程平台通过整合以下核心功能，满足教育过程中的多样化需求：</p>
          <ul>
            <li>课程系统：根据您的需要进行开课、选课、退课，对课程进行评价</li>
            <li>成绩系统：获取课程成绩</li>
            <li>讨论系统：提供一个平台，让学生和教师可以就课程内容进行深入讨论</li>
          </ul>

          <h4>(2)使用说明</h4>
          <p>左侧栏中进行如下操作：</p>
          <ul>
            <li>点击课程信息——学生：进行选课和查看我的课程 教师：开设课程以及管理课程</li>
            <li>点击留言板——进行课程评价、自由讨论交流</li>
            <li>点击用户信息——查看个人信息、更改用户资料</li>
          </ul>
          <h4>讨论区</h4>
          <p>讨论区是Sharing课程平台的社交中心，学生和教师可以在这里交流思想，分享知识，提问和解答。请积极参与讨论，同时关注平台的通知和更新。如果您有任何问题或建议，欢迎向Sharing工作组反馈，我们将竭诚为您服务。</p>

        </el-main>
      </el-container>
    </el-container>
    <el-dialog
      title="Cookies通知"
      :visible.sync="dialogVisible"
      :modal="true"
      class="cookie-consent-dialog"
      >
      <div class="content">
        <el-image :src="cookieImg" lazy style="height: 30%; width: 30%"></el-image>
        <div class="test">
          <span>我们使用cookies来改善您的网站体验,<br>继续浏览网站表示您同意我们使用cookies。</span>
          <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">拒绝</el-button>
          <el-button type="primary" @click="acceptCookies">接受所有Cookies</el-button>
        </span>
        </div>
      </div>

    </el-dialog>
  </div>
</template>

<script>
import StudentNav from './StudentNav'
import StudentHeading from './StudentHeading'
import CookieImg from '../../assets/img/cookiePic.png'
export default {
  name: 'StudentHead',
  components: {StudentHeading, StudentNav},
  data(){
    return {
      dialogVisible: false,
      cookieImg: CookieImg
    };
  },
  mounted() {
    console.log(this.cookie.getCookie('accepted'))
    this.dialogVisible = this.cookie.getCookie('accepted') === 'false';
    console.log(this.dialogVisible)
  },
  methods: {
    acceptCookies() {
      this.cookie.setCookie({
        'accepted': 'true'
      });
      this.dialogVisible = false;
    },
  },
}
</script>

<style scoped>
  @import "../../assets/css/back.css";
  .cookie-consent-dialog {
    display: flex;
    align-items: center;
  }

  .content {
    display: flex;
    align-items: center;
    justify-content: space-around;
    font-size: 16px;
  }

  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    margin-top: 20px;
  }
</style>
