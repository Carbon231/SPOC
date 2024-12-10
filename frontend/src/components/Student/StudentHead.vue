<template>
  <div>
    <el-container class="background">
      <el-aside class="aside" width="show?'64px':30%">
        <StudentNav></StudentNav>
      </el-aside>
      <el-container class="main">
        <el-header>
          <StudentHeading></StudentHeading>
        </el-header>
        <el-main style="padding-left: 10%; padding-right: 10%">
          <h1>FreeTalk课程平台</h1>
          <p>FreeTalk课程平台是一个基于Vue进行前端设计的平台，经历过多次更新。</p>
          <ul>
            <li>介绍</li>
            <li>项目地址</li>
          </ul>

          <h2>介绍</h2>
          <p>本次课程设计的FreeTalk课程平台是综合了选课系统、教材管理、课程评价和讨论，面向所有学生与老师的选课平台。</p>

          <h4>(1)综合需求</h4>
          <p>FreeTalk课程平台（FreeTalk1.0）初步实现了课程管理和评论区，通过对于以下单元进行操作完成您的需求：</p>
          <ul>
            <li>课程：根据您的需要进行选课</li>
            <li>资料：获取相应的学习资料</li>
            <li>留言：分享您的看法</li>
          </ul>

          <h4>(2)使用说明</h4>
          <p>左侧栏中进行如下操作：</p>
          <ul>
            <li>点击课程信息——进行选课退课</li>
            <li>点击留言板——进行讨论交流，查看您的课程</li>
            <li>点击课程管理——管理您的课程（教师端）</li>
          </ul>
          <h4>讨论区</h4>
          <p>在讨论区中进行问题交流，关注讨论区中的通知。您也可以向FreeTalk工作组进行反馈，我们会尽快解决您的问题。</p>

          <h2>项目地址</h2>
          <p>如果您的有更好的建议，欢迎通过以下方式联系我们：</p>
          <el-link href="https://github.com/fangzhou0216/buaa_db">fangzhou0216</el-link>
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
