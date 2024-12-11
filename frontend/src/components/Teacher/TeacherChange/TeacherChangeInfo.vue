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
                <el-main style="padding-left: 30%; padding-right: 10%">
                    <el-form label-position="top" v-loading="loading">
                        <el-form-item label="部门">
                            <el-col :span="12">
                                <el-input v-model="teacher.d_id"></el-input>
                            </el-col>
                        </el-form-item> <el-form-item label="电子邮箱">
                            <el-col :span="12">
                                <el-input v-model="teacher.t_email"></el-input>
                            </el-col>
                        </el-form-item> <el-form-item label="电话">
                            <el-col :span="12">
                                <el-input v-model="teacher.t_phone"></el-input>
                            </el-col>
                        </el-form-item>
                        <el-form-item label="办公地址">
                            <el-col :span="12">
                                <el-input type="textarea" v-model="teacher.t_office"></el-input>
                            </el-col>
                        </el-form-item>
                        <el-form-item style="margin-top: 20%">
                            <el-col :span="6">
                                <el-button v-on:click="teacherChangeInfo" type="primary">确认</el-button>
                            </el-col>
                        </el-form-item>
                    </el-form>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script>
import TeacherNav from '../TeacherNav'
import TeacherHeading from '../TeacherHeading'

export default {
    name: 'teacherChangeInfo',
    components: { TeacherNav, TeacherHeading },
    data: function () {
        return {
            loading: false,
            t_id: '',
            t_name: '',
            teacher: {
                d_id: '',
                t_email: '',
                t_phone: '',
                t_office: ''
            },
        }
    },
    mounted: function () {
        this.t_id = this.cookie.getCookie('t_id')
        this.t_name = this.cookie.getCookie('t_name')
    },
    methods: {
        teacherChangeInfo: function () {
            let that = this
            that.loading = true
            this.$http.request({
                url: that.$url + 'TeacherChangeInfo/',
                method: 'post',
                data: {
                    t_id: that.t_id,
                    d_id: that.teacher.d_id,
                    t_email: that.teacher.t_email,
                    t_phone: that.teacher.t_phone,
                    t_office: that.teacher.t_office
                }
            }).then(function (response) {
                console.log(response.data)
                that.loading = false
                if (response.data.code === 200) {
                    that.$message.success(response.data.message)
                    that.teacher.d_id = ''
                    that.teacher.t_email = ''
                    that.teacher.t_phone = ''
                    that.teacher.t_office = ''

                    that.$router.push({ name: 'TeacherInfo' })
                } else {
                    that.$message.error(response.data.message)
                }
            }).catch(function (error) {
                console.error(error)
                that.loading = false
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

<style scoped>
@import "../../../assets/css/nav.css";
@import "../../../assets/css/back.css";
</style>