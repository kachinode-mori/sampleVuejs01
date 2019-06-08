<template>
  <b-container>
    <br><br>
    <div class="mx-auto w-75 p-3">
      <!-- エラーが発生した場合のメッセージ表示 -->
      <div v-if="responseErrors.length" class="alert alert-danger" role="alert">
        <div>{{ responseErrors }}</div>
      </div>
      <!-- SingUP画面 -->
      <h3>新規ユーザ登録</h3>
      <br>
      <b-form v-on:submit="onSubmit">
        <b-form-group label="メールアドレス:">
          <b-form-input type="email" v-model="form.email" required placeholder="Enter email"></b-form-input>
        </b-form-group>
        <b-form-group label="ニックネーム:">
          <b-form-input type="text" v-model="form.nickname" required placeholder="Enter Your NickName"></b-form-input>
        </b-form-group>
        <b-form-group label="パスワード:">
          <b-form-input type="password" v-model="form.password1" required placeholder="Enter Your Password"></b-form-input>
        </b-form-group>
         <b-form-group label="パスワードの確認:">
          <b-form-input type="password" v-model="form.password2" required placeholder="Confirm Your Password" ></b-form-input>
        </b-form-group>
        <li>あなたの他の個人情報と似ているパスワードにはできません。</li>
        <li>パスワードは最低 8 文字以上必要です</li>
        <li>よく使われるパスワードにはできません。</li>
        <li>数字だけのパスワードにはできません。</li>
        <br>
        <b-button type="submit" variant="primary" class="btn-block">Create an account</b-button>
      </b-form>
    </div>
    <br><br>
    <!-- <pre>{{ $data }}</pre> -->
  </b-container>
</template>

<script>
import axios from 'axios'
import {mapActions} from 'vuex'

export default {
  name: 'SingUp',
  data () {
    return {
      form: {
        email: null,
        nickname: null,
        password1: null,
        password2: null
      },
      responseErrors: []
    }
  },
  methods: {
    ...mapActions(['login']),
    onSubmit () {
      this.responseErrors = []

      // パスワードが同じかを確認する
      var input1 = this.form.password1
      var input2 = this.form.password2
      if (input1 !== input2) {
        alert('パスワードの入力値が一致しません')
      } else {
        // パスワードの確認がOKであった場合
        // axios.post('http://127.0.0.1:8000/api/users/', {
        axios.post(`${process.env.API_ENDPOINT}users/`, {
          email: this.form.email,
          nickname: this.form.nickname,
          is_active: true,
          password: this.form.password1
        }).then(res => {
          this.login([this.form.email, this.form.password1]).then(res => {
            // alert('新規ユーザ登録をしました')
            this.$router.push('/')
          })
        }, err => {
          this.responseErrors = err.request.response
          console.log(this.responseErrors)
        })
      }
    }
  }
}
</script>

<style scoped>
h3 {
  text-align: center;
}
</style>
