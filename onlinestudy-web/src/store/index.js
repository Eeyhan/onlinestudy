import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex);

const store = new Vuex.Store({
    state:{
        userInfo:{},
        isRemember:false // 是否记住密码标志位
    },
    mutations:{
        // 设置记住用户信息
        getUserInfo(state,user){
            state.userInfo = user         
        },

        // 删除用户信息
        deleteUserInfo(state){
            state.userInfo = {}
        },
        // 记住用户密码
        rememberUserInfo(state){
            state.isRemember = true
        }
    },
    filters:{},
    actions:{
        getUserInfo({commit},user){
            commit('getUserInfo',user)
        },
        deleteUserInfo({commit}){
            commit('deleteUserInfo')
        },
        rememberUserInfo({commit}){
            commit('rememberUserInfo')
        }
    }
})
export default store;


