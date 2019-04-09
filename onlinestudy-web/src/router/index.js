import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home/Home'
import Course from '@/components/Course/Course'
import CourseDetail from '@/components/Course/CourseDetail'
import LightCourse from '@/components/LightCourse/LightCourse'
import Degree from '@/components/Degree/Degree'
import ShopCart from '@/components/ShopCart/ShopCart'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect:Home
    },
    {
      path:'/Home',
      name:'Home',
      component:Home
    },
    {
      path:'/Course',
      name:'Course',
      component:Course
    },
    {
      path:'/Course/detail/:detailId',
      name:'CourseDetail',
      component:CourseDetail
    },
    {
      path:'/LightCourse',
      name:'LightCourse',
      component:LightCourse
    },
    {
      path:'/Degree',
      name:'Degree',
      component:Degree
    },
    {
      path:'/ShopCart',
      name:'ShopCart',
      component:ShopCart
    },

  ]
})
