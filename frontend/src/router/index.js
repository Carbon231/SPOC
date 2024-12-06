import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '../components/HelloWorld'
import StudentLogin from '../components/Student/StudentLogin'
import StudentRegister from '../components/Student/StudentRegister'
import StudentHead from '../components/Student/StudentHead'
import StudentCourse from '../components/Student/StudentCourse/StudentCourse'
import SelectCourse from '../components/Student/StudentCourse/SelectCourse'
import SelectedCourse from '../components/Student/StudentCourse/SelectedCourse'

import TeacherLogin from '../components/Teacher/TeacherLogin'
import TeacherRegister from '@/components/Teacher/TeacherRegister.vue'
import TeacherHead from '@/components/Teacher/TeacherHead.vue'
import TeacherCourse from '@/components/Teacher/TeacherCourse/TeacherCourse.vue'
import ChangeCourse from '@/components/Teacher/TeacherCourse/ChangeCourse.vue'
import BuildCourse from '@/components/Teacher/TeacherCourse/BuildCourse.vue'
import ManageCourse from '@/components/Teacher/TeacherCourse/ManageCourse.vue'
import AllCourse from '@/components/Teacher/TeacherCourse/AllCourse.vue'
import TeacherCommentAndDiscuss from '@/components/Teacher/TeacherCommentAndDiscuss/TeacherCommentAndDiscuss.vue'
import TeacherAllComment from '@/components/Teacher/TeacherCommentAndDiscuss/TeacherAllComment.vue'
import TeacherAllDiscuss from '@/components/Teacher/TeacherCommentAndDiscuss/TeacherAllDiscuss.vue'
import TeacherComment from '@/components/Teacher/TeacherCommentAndDiscuss/TeacherComment.vue'
import TeacherDiscuss from '@/components/Teacher/TeacherCommentAndDiscuss/TeacherDiscuss.vue'
import TeacherChange from '@/components/Teacher/TeacherChange/TeacherChange.vue'

// 解决ElementUI导航栏中的vue-router在3.0版本以上重复点菜单报错问题
const originalPush = Router.prototype.push
Router.prototype.push = function push(location) { return originalPush.call(this, location).catch(err => err) }

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/StudentLogin',
      name: 'StudentLogin',
      component: StudentLogin
    },
    {
      path: '/StudentRegister',
      name: 'StudentRegister',
      component: StudentRegister
    },
    {
      path: '/StudentHead',
      name: 'StudentHead',
      component: StudentHead
    },
    {
      path: '/StudentCourse',
      name: 'StudentCourse',
      component: StudentCourse,
      children: [
        {
          path: 'SelectCourse',
          name: 'SelectCourse',
          component: SelectCourse
        },
        {
          path: 'SelectedCourse',
          name: 'SelectedCourse',
          component: SelectedCourse
        }
      ]
    },
    {
      path: '/TeacherLogin',
      name: 'TeacherLogin',
      component: TeacherLogin
    },
    {
      path: '/TeacherRegister',
      name: 'TeacherRegister',
      component: TeacherRegister
    },
    {
      path: '/TeacherHead',
      name: 'TeacherHead',
      component: TeacherHead
    },
    {
      path: '/TeacherCourse',
      name: 'TeacherCourse',
      component: TeacherCourse,
      children: [
        {
          path: 'ChangeCourse',
          name: 'ChangeCourse',
          component: ChangeCourse
        },
        {
          path: 'BuildCourse',
          name: 'BuildCourse',
          component: BuildCourse
        },
        {
          path: 'ManageCourse',
          name: 'ManageCourse',
          component: ManageCourse
        },
        {
          path: 'AllCourse',
          name: 'AllCourse',
          component: AllCourse
        }
      ]
    },
    {
      path: '/TeacherCommentAndDiscuss',
      name: 'TeacherCommentAndDiscuss',
      component: TeacherCommentAndDiscuss,
      children: [
        {
          path: 'TeacherAllComment',
          name: 'TeacherAllComment',
          component: TeacherAllComment
        },
        {
          path: 'TeacherAllDiscuss',
          name: 'TeacherAllDiscuss',
          component: TeacherAllDiscuss
        },
        {
          path: 'TeacherComment',
          name: 'TeacherComment',
          component: TeacherComment
        },
        {
          path: 'TeacherDiscuss',
          name: 'TeacherDiscuss',
          component: TeacherDiscuss
        }
      ]
    },
    {
      path: '/TeacherChange',
      name: 'TeacherChange',
      component: TeacherChange
    }
  ]
})