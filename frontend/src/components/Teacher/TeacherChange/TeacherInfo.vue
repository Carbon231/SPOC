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
                <el-main>
                    <el-card class="box-card">
                        <div slot="header" class="clearfix">
                            <span>教师信息</span>
                        </div>
                        <div class="avatar-container">
                            <el-image :src="cookieImg" lazy></el-image>
                        </div>
                        <el-form :model="teacher" label-width="100px">
                            <el-form-item label="工号">
                                <el-input v-model="teacher.t_id" :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="姓名">
                                <el-input v-model="teacher.t_name" :disabled="true"></el-input>
                            </el-form-item>
                            <el-form-item label="学院">
                                <el-select v-model="d_new_name" clearable>
                                    <el-option v-for="dep in departmentSelections" :key="dep.d_id" :value="dep.d_name">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                            <el-form-item label="邮箱">
                                <el-input v-model="t_new_email"></el-input>
                                <span v-if="!t_new_email">{{ teacher.t_email }}</span>
                            </el-form-item>
                            <el-form-item label="电话">
                                <el-input v-model="t_new_phone"></el-input>
                            </el-form-item>
                            <el-form-item label="办公地址">
                                <el-input v-model="t_new_office"></el-input>
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
import TeacherNav from "@/components/Teacher/TeacherNav.vue";
import TeacherHeading from "@/components/Teacher/TeacherHeading.vue";
import CookieImg from '../../../assets/img/cookiePic.png'

export default {
    name: 'TeacherInfo',
    components: { TeacherHeading, TeacherNav },
    data() {
        return {
            t_id: '',
            teacher: {
                t_id: '',
                t_name: '',
                t_department: '',
                t_email: '',
                t_phone: '',
                t_office: '',
            },
            t_new_email: '',
            t_new_phone: '',
            t_new_office: '',
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
                url: that.$url + 'TeacherChangeInfo/',
                method: 'post',
                data: {
                    t_id: that.t_id,
                    d_name: that.d_new_name,
                    t_email: that.t_new_email,
                    t_phone: that.t_new_phone,
                    t_office: that.t_new_office,
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
        getTeacherInfo: function () {
            let that = this;
            this.$http.request({
                url: that.$url + 'GetTeacherInfo/',
                method: 'post',
                data: {
                    t_id: that.t_id,
                },
                headers: {
                    'Content-Type': 'application/json'
                },
            }).then(function (response) {
                that.status = response.data.code
                if (that.status === 200) {
                    that.teacher = response.data.data
                    console.log(that.teacher)
                    that.d_new_name = response.data.data.t_department
                    that.t_new_email = response.data.data.t_email
                    that.t_new_phone = response.data.data.t_phone
                    that.t_new_office = response.data.data.t_office
                    that.$message.success(response.data.message)
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
        this.t_id = this.cookie.getCookie('t_id')
        this.getTeacherInfo()
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