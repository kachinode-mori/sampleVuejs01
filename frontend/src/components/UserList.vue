<template>
  <b-container>
    <br>
    <h3>User List</h3>
    <div v-for="user in users" v-bind:key="user.id">
      <b-card v-if="user.isActive===true">
        <b-media>
          <!-- アバターの表示 -->
          <v-gravatar slot="aside" v-bind:email="user.email" alt="Media Aside" :size="40" default-img="mm"/>
          <!-- ユーザニックネームとtwitterアイコンの表示 -->
          <h5 class="mt-0">
            <router-link :to="`/userwantlist/${ user.id }`">{{ user.nickname }}</router-link>
            <span v-if="user.twitterUrl !==''">
              <a v-bind:href="'https://twitter.com/' + user.twitterUrl" target="_blank">
                <i class="fa fa-twitter fa-1x"></i>
              </a>
            </span>
          </h5>
          <!-- 自己紹介文の表示 -->
          <p v-if="isShow.userid==user.id && isShow.textshow==true">
            {{ user.introText }}
          </p>
          <p v-else-if="user.introText.length>=100">
            {{ user.introText | truncate(100) }} <span v-on:click="seemore(user.id)" id="seemore">see more</span>
          </p>
          <p v-else>
            {{ user.introText }}
          </p>
        </b-media>
      </b-card>
    </div>
    <br>
    <!-- <pre>{{ $data }}</pre> -->
  </b-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserList',
  data () {
    return {
      users: [],
      isShow: {
        userid: null,
        textshow: false
      }
    }
  },
  methods: {
    fetchData () {
      // axios.get('http://127.0.0.1:8000/api/users/').then(res => {
      axios.get(`${process.env.API_ENDPOINT}users/`).then(res => {
        this.users = res.data.results
      })
    },
    seemore (userid) {
      for (var i = 0; i < this.users.length; i++) {
        if (this.users[i].id === userid) {
          this.isShow.userid = userid
          this.isShow.textshow = true
        }
      }
    }
  },
  mounted () {
    this.fetchData()
  },
  filters: {
    truncate (value, n, o) {
      let len = +n
      let suffix = o ? o.toString() : '...'
      if (value.length <= len) return value
      return value.substring(0, len) + suffix
    }
  }
}
</script>

<style scoped>
  span {
    margin: 0 0 0 30px;
  }
  #seemore {
    color: blue;
    text-decoration: underline;
  }
</style>
