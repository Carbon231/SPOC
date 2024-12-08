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
                <el-main>
                    <el-card shadow="hover" style="width: 100%">
                        <el-row>
                            <el-col :span="8">
                                <el-image :src="teacherImg" lazy class="teacher-img"></el-image>
                            </el-col>
                            <el-col :span="16">
                                <el-row class="form-title">教师信息
                                    <el-button-group style="margin-left: 20px;">
                                        <el-button type="primary" icon="el-icon-edit"
                                            v-on:click="teacherChangeInfo">编辑</el-button>
                                    </el-button-group>
                                </el-row>
                                <el-descriptions border :column="1" label-style="width: 30%;text-align: center;"
                                    content-style="text-align: center;">
                                    <el-descriptions-item label="姓名">{{ t_name }}</el-descriptions-item>
                                    <el-descriptions-item label="工号">{{ t_id }}</el-descriptions-item>
                                    <el-descriptions-item label="部门">{{ t_department }}</el-descriptions-item>
                                    <el-descriptions-item label="电子邮箱">{{ t_email }}</el-descriptions-item>
                                    <el-descriptions-item label="电话">{{ t_phone }}</el-descriptions-item>
                                    <el-descriptions-item label="办公地址">{{ t_office }}</el-descriptions-item>
                                </el-descriptions>
                            </el-col>
                        </el-row>
                        <el-row>
                            <el-divider></el-divider>
                        </el-row>
                    </el-card>


                </el-main>
            </el-container>
        </el-container>
    </div>
</template>


<script>
import TeacherNav from '../TeacherNav'
import TeacherHeading from '../TeacherHeading'
// import TeacherImg from '../../../assets/img/teacher.png'

export default {
    name: 'TeacherInfo',
    components: { TeacherNav, TeacherHeading },
    data: function () {
        return {
            teacherImg: require('../../../assets/img/teacher.png'),
            t_id: '',
            t_name: '',
            t_department: '',
            t_email: '',
            t_phone: '',
            t_office: ''
        }
    },
    mounted: function () {
        this.t_id = this.cookie.getCookie('t_id')
        this.t_name = this.cookie.getCookie('t_name')
        this.getTeacherInfo()
    },
    methods: {
        teacherChangeInfo: function () {
            this.$router.push({ name: 'TeacherChangeInfo', params: { id: this.t_id } })
        },

        getTeacherInfo: function () {
            let that = this
            this.loading = true

            this.$http.request({
                url: that.$url + 'GetTeacherInfo/',
                method: 'post',
                data: {
                    t_id: that.t_id
                }
            }).then(function (response) {
                console.log(response.data)
                that.loading = false
                if (response.data.code === 200) {
                    that.t_id = response.data.data.t_id
                    that.t_name = response.data.data.t_name
                    that.t_department = response.data.data.t_department
                    that.t_email = response.data.data.t_email
                    that.t_phone = response.data.data.t_phone
                    that.t_office = response.data.data.t_office
                } else {
                    that.$message.error(response.data.message)
                }
            }).catch(function (error) {
                console.log(error)
                that.loading = false
            })
        }

    }
}
</script>


<style scoped>
.form-title {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 20px;
}
</style>