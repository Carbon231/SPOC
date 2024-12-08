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

                    <div class="st-table">
                        <el-table :data="students" border style="width: 100%">
                            <el-table-column prop="s_id" label="学号" width="180">
                                <template slot-scope="scope">
                                    <span>{{ scope.row.date }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="name" label="姓名" width="180">
                                <template slot-scope="scope">
                                    <span>{{ scope.row.name }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column prop="address" label="成绩">
                                <template slot-scope="scope">
                                    <input type="text" v-model="scope.row.address" v-show="scope.row.iseditor" />
                                    <span v-show="!scope.row.iseditor">{{ scope.row.address }}</span>
                                </template>
                            </el-table-column>
                            <el-table-column label="操作" width="180">
                                <template slot-scope="scope">
                                    <el-button type="warning" @click="edit(scope.row, scope)">编辑</el-button>
                                    <el-button type="danger" @click="save(scope.row)">保存</el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </div>
                </el-main>
            </el-container>
        </el-container>
    </div>

</template>
<script>
import TeacherNav from '../TeacherNav'
import TeacherHeading from '../TeacherHeading'

export default {
    name: 'TeacherGetStudentsInCourse',
    components: { TeacherNav, TeacherHeading },
    data() {
        return {
            tableData: [
                {
                    date: "2016-05-02",
                    name: "王小虎",
                    address: "上海市普陀区金沙江路 1518 弄",
                    iseditor: false
                },
                {
                    date: "2016-05-04",
                    name: "王小虎",
                    address: "上海市普陀区金沙江路 1517 弄",
                    iseditor: false
                },
                {
                    date: "2016-05-01",
                    name: "王小虎",
                    address: "上海市普陀区金沙江路 1519 弄",
                    iseditor: false
                },
                {
                    date: "2016-05-03",
                    name: "王小虎",
                    address: "上海市普陀区金沙江路 1516 弄",
                    iseditor: false
                }
            ]
        };
    },
    methods: {
        edit(row) {
            row.iseditor = true;
        },
        save(row) {
            row.iseditor = false;
        }
    }
};
</script>
<style lang="less" scoped>
.st-table {
    padding: 10px;
}
</style>