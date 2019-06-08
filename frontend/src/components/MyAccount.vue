<template>
  <b-container>
    <br>
    <div v-if="errors.length" class="alert alert-danger" role="alert">
      <div>{{ errors }}</div>
    </div>
    <h4>ユーザアカウントの設定</h4>
    <br>
    <b-form v-on:submit="onSubmit(form.id)">
      <b-form-group label="Emailアドレス(必須):">
        <b-form-input type="email" v-model="form.email" disabled placeholder="Enter email"></b-form-input>
      </b-form-group>
      <b-form-group label="UserName(NickName)(必須):">
        <b-form-input type="text" v-model="form.nickname" required placeholder="Enter your nick name"></b-form-input>
      </b-form-group>
      <b-form-group label="Twitter URL(任意):">
        <b-input-group prepend="https://twitter.com/">
           <b-form-input type="text" v-model="form.twitterurl" required placeholder="Your Twitter ID"></b-form-input>
        </b-input-group>
      </b-form-group>
      <b-form-group label="自己紹介(任意):">
        <b-form-textarea :rows="4" type="text" v-model="form.introtext" required placeholder="自己紹介を入れて下さい"></b-form-textarea>
      </b-form-group>
      <br>
      <b-button type="submit" variant="primary">変更を保存</b-button>
    </b-form>
    <br>
    <hr>
    <br>
    <h4>アカウントの削除</h4>
    <p>一度アカウントを削除すると、二度と元に戻せません。十分ご注意ください。</p>
    <b-button type="submit" variant="danger" v-on:click="deluser">ユーザアカウントの削除</b-button>
    <br><br><br>
  </b-container>
</template>

<script>
import axios from 'axios'
import {mapActions} from 'vuex'

export default {
  name: 'MyAccount',
  data () {
    return {
      form: {
        id: '',
        email: '',
        nickname: '',
        twitterurl: '',
        introtext: ''
      },
      errors: []
    }
  },
  created () {
    this.tryLoggedIn()
  },
  methods: {
    ...mapActions(['logout', 'tryLoggedIn']),
    // ユーザ情報取得
    fetchData () {
      // axios.get(`http://127.0.0.1:8000/api/userinfo/`).then(res => {
      axios.get(`${process.env.API_ENDPOINT}userinfo/`).then(res => {
        this.form.id = res.data.results[0].id
        this.form.email = res.data.results[0].email
        this.form.nickname = res.data.results[0].nickname
        this.form.twitterurl = res.data.results[0].twitterUrl
        this.form.introtext = res.data.results[0].introText
      })
    },
    onSubmit (userid) {
      this.errors = []
      // axios.patch(`http://127.0.0.1:8000/api/users/${userid}/`, {
      axios.patch(`${process.env.API_ENDPOINT}users/${userid}/`, {
        // email: this.form.email,
        nickname: this.form.nickname,
        twitterUrl: this.form.twitterurl,
        introText: this.form.introtext
      }).then(res => {
        this.fetchData()
        alert('変更を保存しました')
      }, err => {
        // console.log(err.request.response)
        this.errors = err.request.response
      })
    },
    deluser (evt) {
      this.errors = []
      var result = window.confirm('本当に削除しますか？')
      if (result) {
        // axios.delete(`http://127.0.0.1:8000/api/userdelete/`).then(res => {
        axios.delete(`${process.env.API_ENDPOINT}userdelete/`).then(res => {
          alert('ユーザを削除しました')
          this.logout().then(res => {
            this.$router.push('/')
          })
        }, err => {
          // console.log(err.request.response)
          this.errors = err.request.response
        })
      }
    }
  },
  mounted () {
    this.fetchData()
  }
}
</script>
