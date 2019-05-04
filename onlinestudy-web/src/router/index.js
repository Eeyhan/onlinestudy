import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home/Home'
import Course from '@/components/Course/Course'
import CourseDetail from '@/components/Course/CourseDetail'
import CourseDetailTab from '@/components/Course/CourseDetailTab'
import LightCourse from '@/components/LightCourse/LightCourse'
import Degree from '@/components/Course/Degree'
import Login from '@/components/Person/Login'
import Register from '@/components/Person/Register'
import Mypage from '@/components/Person/Mypage'
import study from '@/components/Person/study'
import Courselesson from '@/components/Person/Courselesson'
import learning from '@/components/Person/learning'
import ShopCart from '@/components/Transaction/ShopCart'
import SettlePay from '@/components/Transaction/SettlePay'
import OrderDetail from '@/components/Transaction/OrderDetail'
import Order from '@/components/Transaction/Order'
import Coupon from '@/components/Transaction/Coupon'
import Usercoupon from '@/components/Transaction/UserCoupon'
import homework from '@/components/Person/homework'
import solvequestion from '@/components/Person/solvequestion'


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
          path: '',
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
      path: '/Mypage',
      name: 'Mypage',
      component: Mypage
    },  
    {
      path: '/study',
      name: 'study',
      component: study,
      
    },
    {
      path: '/study/:courseId',
      name: 'Courselesson',
      component: Courselesson,
      
    },
    {
      path:'/learning',
      name:'learning',
      component:learning
    },

    {
      path:'/homework',
      name:'homework',
      component:homework
    },
    {
      path:'/solvequestion',
      name:'solvequestion',
      component:solvequestion
    },   
    {
      path: '/ShopCart',
      name: 'ShopCart',
      component: ShopCart,

    },
    {
      path: '/SettlePay',
      name: 'SettlePay',
      component: SettlePay,
      
    },
    
    {
      path: '/Order',
      name: 'Order',
      component: Order
    },
    {
      path: '/Order/detail/:orderId',
      name: 'OrderDetail',
      component: OrderDetail
    },
    {
      path: '/coupon',
      name: 'Coupon',
      component: Coupon
    },
    {
      path: '/Usercoupon',
      name: 'Usercoupon',
      component: Usercoupon
    },
  ]
})
