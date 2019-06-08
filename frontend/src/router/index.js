import Vue from 'vue'
import Router from 'vue-router'
import IndexHome from '@/components/IndexHome'
import WantList from '@/components/WantList'
import UserWantList from '@/components/UserWantList'
import Login from '@/components/Login'
import MyAccount from '@/components/MyAccount'
import UserList from '@/components/UserList'
import SingUp from '@/components/SingUp'
// import RankingList from '@/components/RankingList'
import UserLikeList from '@/components/UserLikeList'
import PasswordChange from '@/components/PasswordChange'
// import zDragTest from '@/components/zDragTest'
// import HelloWorld from '@/components/HelloWorld'

Vue.use(Router)

export default new Router({
  // mode: 'history',
  routes: [
    {
      path: '/',
      name: 'IndexHome',
      component: IndexHome,
      meta: {
        title: 'index home'
        // isPublic: true
      }
    },
    {
      path: '/wants',
      name: 'WantList',
      component: WantList,
      meta: {
        title: 'want list'
      }
    },
    {
      path: '/userwantlist/:id',
      name: 'UserWantList',
      component: UserWantList,
      props: route => ({ id: Number(route.params.id) }),
      meta: {
        title: 'userwantlist'
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
      meta: {
        title: 'login'
        // isPublic: true
      }
    },
    {
      path: '/singup',
      name: 'SingUp',
      component: SingUp,
      meta: {
        title: 'singup'
      }
    },
    {
      path: '/myaccount',
      name: 'MyAccount',
      component: MyAccount,
      meta: {
        title: 'myaccount'
      }
    },
    {
      path: '/userlist',
      name: 'UserList',
      component: UserList,
      meta: {
        title: 'userlist'
      }
    },
    // {
    //   path: '/rankinglist',
    //   name: 'RankingList',
    //   component: RankingList,
    //   meta: {
    //     title: 'rankinglist'
    //   }
    // },
    {
      path: '/userlikelist',
      name: 'UserLikeList',
      component: UserLikeList,
      meta: {
        title: 'userlikelist'
      }
    },
    {
      path: '/passwordchange',
      name: 'PasswordChange',
      component: PasswordChange,
      meta: {
        title: 'passwordchange'
      }
    }
    // {
    //   path: '/zdragtest',
    //   name: 'zDragTest',
    //   component: zDragTest,
    //   meta: {
    //     title: 'zdragtest'
    //   }
    // }
  ]
})
