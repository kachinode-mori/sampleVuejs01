import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

// debug
// const debug = process.env.NODE_ENV !== 'production'

// state
const state = {
  isLoggedIn: false,
  userId: null,
  nickName: null
}

// mutations
const mutations = {
  loggedIn (state, token) {
    state.isLoggedIn = true
    axios.defaults.headers.common['Authorization'] = `JWT ${token}`
    localStorage.setItem('token', token)
  },
  loggedOut (state) {
    state.isLoggedIn = false
    delete axios.defaults.headers.common['Authorization']
    localStorage.clear()
  },
  setuserid (state, userid) {
    state.userId = userid
    localStorage.setItem('userid', userid)
  },
  setnickname (state, nickname) {
    state.nickName = nickname
    localStorage.setItem('nickname', nickname)
  }
}

// actions
const actions = {
  login ({commit}, [email, password]) {
    // return axios.post('http://127.0.0.1:8000/api/auth/', {
    return axios.post(`${process.env.API_ENDPOINT}auth/`, {
      email: email,
      password: password
    }).then(res => {
      commit('loggedIn', res.data.token)
      // axios.get(`http://127.0.0.1:8000/api/users/?email=${email}`).then(res => {
      axios.get(`${process.env.API_ENDPOINT}users/?email=${email}`).then(res => {
        commit('setuserid', res.data.results[0].id)
        commit('setnickname', res.data.results[0].nickname)
      })
      return res
    })
  },
  tryLoggedIn ({commit}) {
    const token = localStorage.getItem('token')
    const userid = localStorage.getItem('userid')
    const nickname = localStorage.getItem('nickname')
    if (token) {
      axios.defaults.headers.common['Authorization'] = `JWT ${token}`
      // axios.post('http://127.0.0.1:8000/api/auth/verify/', {
      axios.post(`${process.env.API_ENDPOINT}auth/verify/`, {
        token: token
      }).then(() => {
        commit('loggedIn', token)
        commit('setuserid', userid)
        commit('setnickname', nickname)
      }, () => {
        // 不正なtoken
        localStorage.clear()
      })
    }
  },
  logout ({commit}) {
    commit('loggedOut')
  }
}

// getters
const getters = {
  isLoggedIn: state => state.isLoggedIn,
  userId: state => state.userId,
  nickName: state => state.nickName
}

export default new Vuex.Store({
  // strict: debug,
  actions,
  getters,
  mutations,
  state
})
