import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex);

const store = new Vuex.Store({
    state:{
        userInfo:{}
    },
    mutations:{
        getUserInfo(state,user){
            state.userInfo = user
        }
    },
    filters:{},
    actions:{
        getUserInfo({commit},user){
            commit('getUserInfo',user)
        }
    }
})
export default store;


