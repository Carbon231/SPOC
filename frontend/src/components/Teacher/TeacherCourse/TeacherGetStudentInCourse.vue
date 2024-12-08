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
                    <el-table :data="students" style="width: 100%">
                        <el-table-column prop="s_id" label="学生学号" width="180"></el-table-column>
                        <el-table-column prop="s_name" label="学生姓名" width="180"></el-table-column>
                        <el-table-column label="成绩" width="180">
                            <template slot-scope="scope">
                                <el-input v-if="scope.row.editing" v-model="scope.row.score" size="small" />
                                <span v-else>{{ scope.row.score }}</span>
                            </template>
                        </el-table-column>
                        <el-table-column label="操作" width="180">
                            <template slot-scope="scope">
                                <el-button type="warning" @click="editScore(scope.row)"
                                    v-if="!scope.row.editing">编辑</el-button>
                                <el-button type="danger" @click="saveScore(scope.row)" v-else>保存</el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </el-main>
            </el-container>
        </el-container>
    </div>
</template>

<script>
import TeacherNav from '../TeacherNav'
import TeacherHeading from '../TeacherHeading'

export default {
    name: 'TeacherGetStudentInCourse',
    components: { TeacherNav, TeacherHeading },
    data() {
        return {
            loading: false,
            c_id: '',
            students: [
                // { s_id: '20180001', s_name: '张三', score: 90 },
                // { s_id: '20180002', s_name: '李四', score: 85 },
                // { s_id: '20180003', s_name: '王五', score: 88 }
            ]
        };
    },
    mounted() {
        this.c_id = this.$route.params.c_id || localStorage.getItem('c_id');
        if (this.c_id) {
            // 将 c_id 存储到 localStorage 中
            localStorage.setItem('c_id', this.c_id);
            this.getStudentsInCourse();
        } else {
            this.$message.error('课程ID未定义');
        }
        this.getStudentsInCourse();
    },
    methods: {
        getStudentsInCourse() {
            let that = this;
            that.loading = true;
            this.$http.request({
                url: that.$url + 'TeacherGetStudentInCourse/',
                method: 'post',
                data: {
                    c_id: that.c_id
                }
            }).then(function (response) {
                that.loading = false;
                if (response.data.code === 200) {
                    that.students = response.data.data.map(student => {
                        student.editing = false; // 添加编辑状态
                        return student;
                    });
                    that.$message.success(response.data.message);
                } else {
                    that.$message.error(response.data.message);
                }
            }).catch(function (error) {
                console.error(error);
                that.loading = false;
            });
        },
        editScore(student) {
            student.editing = true;
        },
        saveScore(student) {
            student.editing = false;
            this.$http.request({
                url: this.$url + 'SetStudentCourseScore/',
                method: 'post',
                data: {
                    s_id: student.s_id,
                    c_id: this.c_id,
                    score: student.score
                }
            }).then((response) => {
                if (response.data.code === 200) {
                    this.$message.success(response.data.message);
                } else {
                    this.$message.error(response.data.message);
                }
            }).catch((error) => {
                console.error(error);
            });
            console.log('Saving score for student:', student);
        }
    }
}
</script>

<style scoped>
.st-table {
    padding: 10px;
}
</style>