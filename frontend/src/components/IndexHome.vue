<template>
  <div class="container">
    <!-- <h1 id="myfontset">100 wants list</h1> -->
    <div id="myfontset">
      <img src="../../static/homelogo.png" class="img-fluid rounded mx-auto d-block" style="max-height: 500px;">
    </div>
    <div class="row">
      <div class="col-md-12" id="myfontset1">
        <h5>人生でやりたいことリスト100 / 人生でやってみたい100のこと</h5>
      </div>
    </div>
    <div class="row">
      <div class="col-md-2">
        <p style="visibility: hidden;">space</p>
      </div>
      <div class="col-md-8">
        <p>人生でやってみたいことをリストにしてみよう！どんなに大きなことでも、どんなにちっぽけでもいいので書き出してみると、
          「自分の人生における優先順位」・「自分の本当に好きなこと」・「これから自分はどんな人生を送りたいか」 が見えてきます！</p>
      </div>
      <div class="col-md-2">
        <p style="visibility: hidden;">space</p>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12" id="myfontset2">
        <div v-if="isLoggedIn">
          <strong><p>ようこそ {{ nickName }} さん</p></strong>
          <router-link to="/wants" class="btn btn-info">My 100 Wants List</router-link>
        </div>
        <div v-else>
          <p>ログイン or 新規ユーザ作成で使ってみる！</p>
          <form class="form-inline ml-auto justify-content-center">
            <router-link to="/login"><button class="btn btn-info">ログイン</button></router-link>
            <br><br>
            <router-link to="/singup"><button class="btn btn-info ml-2">新規ユーザ登録</button></router-link>
          </form>
        </div>
      </div>
    </div>

    <br><hr><br>

    <div class="row">
      <div class="col-md-2">
        <p style="visibility: hidden;">space</p>
      </div>
      <div class="col-md-8 homeimg">
        <li>できること(Can)ではなく、とにかくやりたいこと(Want)を書き出そう！</li>
        <li>いつでも編集ダウンロード可能＆100個以上でもOKです</li>
        <li>公開設定をすると、他の人にもwantsリストを公開できます(見せたくない場合は非公開に)</li>
        <li>他の人のWantsリストも参照できます(公開限定)  共感できるものは、「いいね」しよう</li>
        <br>
        <img src="../../static/home.png" class="img-fluid rounded mx-auto d-block" style="max-height: 500px;">
      </div>
      <div class="col-md-2">
        <p style="visibility: hidden;">space</p>
      </div>
    </div>

    <br><hr><br>

    <div class="row">
      <div class="col-md-6 mybox">
        <h6 class="boxtitle">タイムライン：みんなのWants(公開のみ)</h6>
        <UserCreateList />
      </div>
      <div class="col-md-6 mybox">
        <h6 class="boxtitle">ランキング：いいね獲得ユーザ(公開のみ)</h6>
        <RankingList />
      </div>
    </div>
    <br>
    <!-- <pre>{{ $data }}</pre> -->
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
import RankingList from '@/components/RankingList'
import UserCreateList from '@/components/UserCreateList'

export default {
  name: 'IndexHome',
  components: {
    'RankingList': RankingList,
    'UserCreateList': UserCreateList
  },
  computed: {
    ...mapGetters(['isLoggedIn', 'userId', 'nickName'])
  }
}
</script>

<style scoped>
#myfontset {
  padding: 70px 0px 0px 0px;
}
#myfontset1 {
  text-align: center;
  font-size: 14px;
  padding: 70px 0px 40px 0px;
}
#myfontset2 {
  text-align: center;
  font-size: 16px;
  padding: 40px 0px 40px 0px;
  color: blue;
}
.homeimg {
  color: white;
  background: rgb(54, 73, 250);
  padding: 10px;
  border-radius: 10px;
}
.mybox {
  padding: 10px;
  border:1px solid lightgray;
}
.boxtitle {
  color: white;
  background: rgb(77, 1, 255);
  text-align: center;
  padding: 5px;
  border-radius: 5px;
}
</style>
