<template>
  <div>
    <el-container class="background">
      <el-aside class="aside" width="show?'64px':'300px'">
        <StudentNav></StudentNav>
      </el-aside>
      <el-container class="main">
        <el-header>
          <StudentHeading></StudentHeading>
        </el-header>
        <el-main>
          <el-card class="box-card">
            <div slot="header" class="clearfix">
              <span>学生信息</span>
            </div>
            <div class="avatar-container">
              <el-image :src="cookieImg" lazy></el-image>
            </div>
            <el-form :model="student" label-width="100px">
              <el-form-item label="学号">
                <el-input v-model="student.s_id" :disabled="true"></el-input>
              </el-form-item>
              <el-form-item label="姓名">
                <el-input v-model="student.s_name" :disabled="true"></el-input>
              </el-form-item>
              <el-form-item label="学院">
                <el-select v-model="d_new_name" clearable placeholder="开课院系">
                  <el-option v-for="dep in departmentSelections" :key="dep.d_id" :value="dep.d_name">
                  </el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="邮箱">
                <el-input v-model="s_new_email"></el-input>
                <span v-if="!s_new_email">{{ student.s_email }}</span>
              </el-form-item>
              <el-form-item label="电话">
                <el-input v-model="s_new_phone"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveChanges">保存修改</el-button>
              </el-form-item>
            </el-form>

          </el-card>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import StudentNav from "@/components/Student/StudentNav.vue";
import StudentHeading from "@/components/Student/StudentHeading.vue";
import CookieImg from '../../../assets/img/cookiePic.png'

export default {
  name: 'StudentInfo',
  components: { StudentHeading, StudentNav },
  data() {
    return {
      s_id: '',
      student: {
        s_id: '',
        s_name: '',
        s_department: '',
        s_email: '',
        s_phone: '',
      },
      s_new_email: '',
      s_new_phone: '',
      d_new_name: '',
      cookieImg: CookieImg,
      departmentSelections: '',
      departmentSelect: '',
    };
  },
  methods: {
    saveChanges() {
      let that = this;
      this.$http.request({
        url: that.$url + 'StudentChangeInfo/',
        method: 'post',
        data: {
          s_id: that.s_id,
          d_name: that.d_new_name,
          s_email: that.s_new_email,
          s_phone: that.s_new_phone,
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        if (response.data.code === 200) {
          that.$message.success(response.data.message)
        } else {
          that.$message.error(response.data.message)
        }
      }).catch(function (error) {
        console.log(error)
      })
    },
    getStudentInfo: function () {
      let that = this;
      this.$http.request({
        url: that.$url + 'GetStudentInfo/',
        method: 'post',
        data: {
          s_id: that.s_id,
        },
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        that.status = response.data.code
        if (that.status === 200) {
          that.student = response.data.data
          that.d_new_name = response.data.data.s_department
          that.s_new_email = response.data.data.s_email
          that.s_new_phone = response.data.data.s_phone
          // that.$message.success(response.data.message)
        } else {
          that.$message.error(response.data.message)
        }
      }).catch(function (error) {
        console.log(error)
      })
    },
    getAllDepartments() {
      let that = this
      this.$http.request({
        url: that.$url + 'GetAllDepartments/',
        method: 'get',
        headers: {
          'Content-Type': 'application/json'
        },
      }).then(function (response) {
        console.log(response.data)
        that.departmentSelections = response.data.data
      }).catch(function (error) {
        console.log(error)
        that.loading = false
      })
    },
  },
  mounted: function () {
    this.s_id = this.cookie.getCookie('s_id')
    this.getStudentInfo()
    this.getAllDepartments()
  },
}
  ;
</script>

<style scoped>
.box-card {
  width: 480px;
  margin: 20px auto;
}

.avatar-container {
  position: relative;
  width: 50%;
  /* 设置宽度为表单项的一半 */
  margin: 0 auto;
  /* 居中 */
  padding-top: 50%;
  /* 创建一个正方形容器 */
  overflow: hidden;
  /* 隐藏溢出的内容 */
}

.avatar-container .el-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  /* 保持图片的纵横比 */
}
</style>
