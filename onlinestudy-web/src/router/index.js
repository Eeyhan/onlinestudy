import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home/Home'
import Course from '@/components/Course/Course'
import CourseDetail from '@/components/Course/CourseDetail'
import CourseDetailTab from '@/components/Course/CourseDetailTab'
import LightCourse from '@/components/LightCourse/LightCourse'
import Degree from '@/components/Degree/Degree'
import Login from  '@/components/Person/Login' 
import Register from  '@/components/Person/Register'
import ShopCart from '@/components/ShopCart/ShopCart'


Vue.use(Router)

export default new Router({
  linkActiveClass: 'is-active',
  mode: 'history',//改成history模式
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: "/home",
      name: 'Home',
      component: Home
    },
    {
      path: '/Course',
      name: 'Course',
      component: Course
    },
    {
      path: '/Course/detail/:detailId',
      name: 'CourseDetail',
      component: CourseDetail,
      children: [
        {
          path: '/',
          name: 'CourseDetailTab',
          component: CourseDetailTab
        },
        {
          path: '/Course/detail/:detailId',
          name: 'CourseDetailTab',
          component: CourseDetailTab
        }
      ]
    },
    {
      path: '/LightCourse',
      name: 'LightCourse',
      component: LightCourse
    },
    {
      path: '/Degree',
      name: 'Degree',
      component: Degree
    },
    {
      path: '/Register',
      name: 'Register',
      component: Register
    },   
    {
      path: '/Login',
      name: 'Login',
      component: Login
    }, 
    {
      path: '/ShopCart',
      name: 'ShopCart',
      component: ShopCart
    },

  ]
})
