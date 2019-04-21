import Axios from 'axios'
Axios.defaults.baseURL = 'http://127.0.0.1:8000/api/v1'



// 添加请求拦截器
Axios.interceptors.request.use(function (config) {
    // 在发送请求之前做些什么
    if (localStorage.getItem('access_token')) {
        // axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    	// Axios.defaults.headers.common['Authorization'] = localStorage.getItem('access_token');
    	// console.log(config.headers);
    	config.headers.Authorization = localStorage.getItem('access_token')
    }
    return config;
  }, function (error) {
    // 对请求错误做些什么
    return Promise.reject(error);
  });

// 课程分类
export const category = () => {
    return Axios.get("/category").then(res => res)
}

// 课程分类下对应的课程 categoryId为0时默认取全部课程
export const categoryTocourse = (categoryId, query) => {
    return Axios.get(`/course?cid=${categoryId}&query=${query}`).then(res => res)
}


// 筛选条件的课程
export const conditionCourse = (category_id, query_isup) => {
    return Axios.get(`/course?cid=${category_id}&query=${query_isup}`).then(res => res)
}


// 课程分类下对应的学位课程 categoryId为0时默认取全部课程
export const categoryToDegreecourse = (categoryId, query) => {
    return Axios.get(`/degree?cid=${categoryId}&query=${query}`).then(res => res)
}

// 筛选条件的学位课程
export const conditionDegreeCourse = (category_id, query_isup) => {
    return Axios.get(`/degree?cid=${category_id}&query=${query_isup}`).then(res => res)
}


// 课程详情

export const courseDetail = (courseId) => {
    return Axios.get(`/detail/${courseId}`).then(res => res)
}


// 课程章节
export const chapter = (courseId) => {
    return Axios.get(`/chapter/${courseId}`).then(res => res)
}


// 课程评论
export const comment = (courseId) => {
    return Axios.get(`/comment/${courseId}`).then(res => res)
}

// 课程常见问题
export const commonquestion = (courseId) => {
    return Axios.get(`/commonquestion/${courseId}`).then(res => res)
}

// 登录
export const login = (params) => {
    return Axios.post('/auth/login', params).then(res => res.data)
}

// 注册
export const register = (params) => {
    return Axios.post('/auth/register', params).then(res => res.data)
}

// 获取验证码
export const geetest = () => {
    return Axios.get("/auth/auth?t=" + (new Date()).getTime()).then(res => res.data) // 加随机数防止缓存
}


// 购物车列表数据
export const shoppingList = () => {
    return Axios.get(`/shopping`).then(res => res.data)
}
// 加入购物车
export const shopping = (params) =>{
    return Axios.post(`/shopping`,params).then(res=>res.data)
}

// 删除购物车
export const delShopping = (params) =>{
    return Axios.delete(`/shopping`,{data:params}).then(res=>res.data)
}

// 加入结算中心
export const settlement = (params) =>{
    return Axios.post('/settlement',params).then(res=>res)
}

// 结算中心列表数据
export const settlementList = () =>{
    return Axios.get('/settlement').then(res=>res.data)
}

// 更新结算中心数据,选择优惠券

export const Updatesettlement = (params) =>{
    return Axios.put('/settlement',params).then(res=>res.data)
}

// 删除结算中心订单

export const delSettlement = (params) =>{
    return Axios.delete('/settlement',{data:params}).then(res=>res.data)
}


// 获取全部优惠券

export const couponList = () =>{
    return Axios.get('/coupon').then(res=>res.data)
}

// 领取优惠券

export const coupon = (params) =>{
    return Axios.post('/coupon',params).then(res=>res.data)
}

// 获取用户优惠券

export const userCouponList = () =>{
    return Axios.get('/usercoupon').then(res=>res.data)
}


// 支付
export const Payment = (params) =>{
    return Axios.post('/payment',params).then(res=>res.data)
}

// 支付宝支付
export const Alipay = (params) =>{
    return Axios.post('/pay/pay/',params).then(res=>res)
}

// 微信支付 后续完善
// export const Wechat = (params) =>{
//     return Axios.post('',params).then(res=>res.data)
// }


// 获取账单

export const PaymentList = () =>{
    return Axios.get('/payment').then(res=>res.data)
}

// 删除账单
export const delPayment = (params) =>{
    return Axios.delete('/payment',{data:params}).then(res=>res.data)
}


// 用户已购买的课程、商品
export const userCourselist =()=>{
    return Axios.get('/usercourse').then(res=>res.data)
}
