<template>
  <b-navbar toggleable="md" type="dark">
    <b-container>
      <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
      <router-link to="/"><b-navbar-brand>100 Wants List</b-navbar-brand></router-link>
      <b-collapse is-nav id="nav_collapse">
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right v-if="isLoggedIn">
            <template slot="button-content">
              <!-- <img src="https://s.gravatar.com/avatar/73cec8aaa85422460c83d17d4a1814a6?s=30" class="d-inline-block align-top" alt="BV"> -->
              <b-button size="sm" variant="primary">{{ nickName }}</b-button>
            </template>
            <b-dropdown-item><router-link to="/wants">My Wants List</router-link></b-dropdown-item>
            <b-dropdown-item><router-link to="/myaccount">アカウント設定</router-link></b-dropdown-item>
            <b-dropdown-item><router-link to="/passwordchange">パスワード変更</router-link></b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item v-on:click="submitlogout">ログアウト</b-dropdown-item>
          </b-nav-item-dropdown>
          <b-nav-form v-else>
            <router-link to="/login">
              <b-button size="sm" class="btn btn-info">ログイン</b-button>
            </router-link>
            <router-link to="/singup">
              <b-button size="sm" class="btn btn-info ml-2">新規ユーザ登録</b-button>
            </router-link>
          </b-nav-form>
        </b-navbar-nav>
      </b-collapse>
    </b-container>
  </b-navbar>
</template>

<script>
import {mapActions, mapGetters} from 'vuex'

export default {
  name: 'NavBar',
  computed: {
    ...mapGetters(['isLoggedIn', 'userId', 'nickName'])
  },
  created () {
    this.tryLoggedIn()
  },
  methods: {
    ...mapActions(['login', 'logout', 'tryLoggedIn']),
    submitlogout () {
      this.logout().then(res => {
        this.$router.push('/')
      })
    }
  }
}
</script>

<style>
.navbar-brand {
  font-family: 'Anton', sans-serif;
}
.navbar {
  background-color: darkblue;
}
</style>
