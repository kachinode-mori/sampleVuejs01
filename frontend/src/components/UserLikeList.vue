<template>
  <b-container>
    <br>
    <h3>Like List<span id="title">(これまでいいねしたユーザとWant)</span></h3>
    <div v-for="like in likes" v-bind:key="like.id">
      <div v-for="want in wants" v-bind:key="want.id">
        <div v-if="want.publishSet===true && like.want===want.id">
          <div v-for="user in users" v-bind:key="user.id">
            <div v-if="want.user===user.id">
              <b-card>
                <b-media>
                  <v-gravatar slot="aside" v-bind:email="user.email" alt="Media Aside" :size="30" default-img="mm"/>
                  <b-row>
                    <b-col><router-link :to="`/userwantlist/${ user.id }`">{{ user.nickname }}</router-link></b-col>
                    <b-col cols="8">{{ want.content }}</b-col>
                    <b-col><i class="fa fa-thumbs-o-up"></i> {{ want.likeNum }}</b-col>
                  </b-row>
                </b-media>
              </b-card>
            </div>
          </div>
        </div>
      </div>
    </div>
    <br>
  </b-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserLikeList',
  data () {
    return {
      likes: [],
      wants: [],
      users: []
    }
  },
  methods: {
    fetchData () {
      // 自分が押下したlikesを取得
      // axios.get('http://127.0.0.1:8000/api/userlikes/').then(res => {
      axios.get(`${process.env.API_ENDPOINT}userlikes/`).then(res => {
        this.likes = res.data.results
        // wants内容を取得
        // axios.get('http://127.0.0.1:8000/api/wants/').then(res => {
        axios.get(`${process.env.API_ENDPOINT}wants/`).then(res => {
          this.wants = res.data.results
          // users情報を取得
          // axios.get('http://127.0.0.1:8000/api/users/').then(res => {
          axios.get(`${process.env.API_ENDPOINT}users/`).then(res => {
            this.users = res.data.results
          })
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
  #title {
    font-size: 20px;
    margin: 0 0 0 30px;
  }
</style>
