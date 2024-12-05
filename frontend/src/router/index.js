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
  ]
})
