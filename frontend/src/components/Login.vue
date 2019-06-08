<template>
  <!-- <b-container> -->
  <div class="container">
    <br>
    <div class="mx-auto w-50 p-3">
      <div v-if="nonFieldErrors.length" class="alert alert-danger" role="alert">
        <div v-for="error in nonFieldErrors" :key="error">{{ error }}</div>
      </div>
      <h3>LOG IN</h3>
      <br>
      <b-form v-on:submit="onSubmit">
        <b-form-group label="メールアドレス:">
          <b-form-input type="email" v-model="form.email" required></b-form-input>
        </b-form-group>
        <b-form-group label="パスワード:">
          <b-form-input type="password" v-model="form.password" required></b-form-input>
        </b-form-group>
        <br>
        <b-button type="submit" variant="primary" class="btn-block">Log In</b-button>
      </b-form>
    </div>
    <br>
  </div>
  <!-- </b-container> -->
</template>

<script>
// import axios from 'axios'
import {mapActions} from 'vuex'

export default {
  name: 'Login',
  data () {
    return {
      form: {
        email: null,
        password: null
      },
      nonFieldErrors: []
    }
  },
  methods: {
    ...mapActions(['login']),
    onSubmit () {
      this.nonFieldErrors = []
      // axios.post('http://127.0.0.1:8000/api/auth/', {
      //   email: this.email,
      //   password: this.password
      // }).then(res => {
      //   // console.log(res.data)
      //   axios.defaults.headers.common['Authorization'] = `JWT ${res.data.token}`
      //   this.$router.push('/')
      // }, err => {
      //   // this.nonFieldErrors = err.response.data.nonFieldErrors
      //   console.log(err.response)
      // })
      this.login([this.form.email, this.form.password]).then(res => {
        this.$router.push('/')
      }, err => {
        this.nonFieldErrors = err.response.data.nonFieldErrors
      })
    }
  }
}
</script>

<style scoped>
h3 {
  text-align: center;
}
</style>
