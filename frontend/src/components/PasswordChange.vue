<template>
  <b-container>
    <br>
    <!-- エラーが発生した場合のメッセージ表示 -->
    <div v-if="responseErrors.length" class="alert alert-danger" role="alert">
      <div>{{ responseErrors }}</div>
    </div>
    <h4>パスワード変更</h4>
    <b-form v-on:submit="onSubmit(form.id)">
      <b-form-group label="元のパスワード:">
        <b-form-input type="password" v-model="form.password" required></b-form-input>
      </b-form-group>
      <b-form-group label="新しいパスワード:">
        <b-form-input type="password" v-model="form.newpassword1" required></b-form-input>
      </b-form-group>
      <b-form-group label="新しいパスワード(確認用):">
        <b-form-input type="password" v-model="form.newpassword2" required></b-form-input>
      </b-form-group>
      <li>あなたの他の個人情報と似ているパスワードにはできません。</li>
      <li>パスワードは最低 8 文字以上必要です</li>
      <li>よく使われるパスワードにはできません。</li>
      <li>数字だけのパスワードにはできません。</li>
      <br>
      <b-button type="submit" variant="primary">Change Password</b-button>
    </b-form>
    <!-- <pre>{{ $data }}</pre> -->
  </b-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'PasswordChange',
  data () {
    return {
      form: {
        id: null,
        password: null,
        newpassword1: null,
        newpassword2: null
      },
      responseErrors: []
    }
  },
  methods: {
    fetchData () {
      // axios.get(`http://127.0.0.1:8000/api/userinfo/`).then(res => {
      axios.get(`${process.env.API_ENDPOINT}userinfo/`).then(res => {
        this.form.id = res.data.results[0].id
      })
    },
    onSubmit (userid) {
      // Newpasswordが整合しているかを確認
      var input1 = this.form.newpassword1
      var input2 = this.form.newpassword2
      if (input1 !== input2) {
        alert('新しいパスワードの入力値が一致しません')
      } else {
        // パスワードの確認がOKであった場合
        // axios.post(`http://127.0.0.1:8000/api/users/${userid}/set_password/`, {
        axios.post(`${process.env.API_ENDPOINT}users/${userid}/set_password/`, {
          old_password: this.form.password,
          new_password: this.form.newpassword1
        }).then(res => {
          alert('パスワードを更新しました')
          this.$router.push('/')
        }, err => {
          this.responseErrors = err.request.response
        })
      }
    }
  },
  mounted () {
    this.fetchData()
  }
}
</script>
