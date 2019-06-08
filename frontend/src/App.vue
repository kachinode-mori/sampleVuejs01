<template>
  <div id="app">
    <nav-bar />
    <router-view/>
    <foot-bar />
  </div>
</template>

<script>
import navBar from '@/components/NavBar'
import footBar from '@/components/FootBar'

export default {
  name: 'App',
  components: {
    'navBar': navBar,
    'footBar': footBar
  }
}
</script>

<style>
html {
  height: 100%;
}
body {
  min-height: 100%;
  display: flex;
  flex-direction: column;
}
#app {
  flex: 1;
}
/* #app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
</style>
