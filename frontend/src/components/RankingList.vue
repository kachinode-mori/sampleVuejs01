<template>
  <b-container>
    <div v-for="(want, index) in wants" v-bind:key="want.id">
      <div v-for="user in users" v-bind:key="user.id">
        <div v-if="user.id===want.user && index<=6">
          <b-card>
            <b-media>
              <v-gravatar slot="aside" v-bind:email="user.email" alt="Media Aside" :size="20" default-img="mm"/>
              <b-row>
                <b-col sm="10"><router-link :to="`/userwantlist/${ user.id }`">{{ user.nickname }}</router-link></b-col>
                <b-col sm="2"><i class="fa fa-thumbs-o-up"></i> {{ want.likeNum }}</b-col>
              </b-row>
              <div>{{ want.content }}</div>
            </b-media>
          </b-card>
        </div>
      </div>
    </div>
  </b-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RankingList',
  data () {
    return {
      wants: [],
      users: []
    }
  },
  methods: {
    fetchData () {
      // axios.get('http://127.0.0.1:8000/api/wants/').then(resw => {
      axios.get(`${process.env.API_ENDPOINT}wants/`).then(resw => {
        var wantranks = []
        wantranks = resw.data.results
        // likes1以上で公開されているlikesに絞り込む
        for (var i = 0; i < wantranks.length; i++) {
          if (wantranks[i].publishSet === true && wantranks[i].likeNum >= 1) {
            this.wants.push(wantranks[i])
          }
        }
        // likesのランキングソート
        this.wants.sort(function (a, b) {
          if (a.likeNum < b.likeNum) return 1
          if (a.likeNum > b.likeNum) return -1
          return 0
        })
        // axios.get('http://127.0.0.1:8000/api/users/').then(resu => {
        axios.get(`${process.env.API_ENDPOINT}users/`).then(resu => {
          this.users = resu.data.results
        })
      })
    }
  },
  mounted () {
    this.fetchData()
  }
}
</script>

<style scoped>
</style>
