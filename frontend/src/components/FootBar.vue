<template>
  <footer class="font-small pt-4 mt-4 mycolor1">
    <b-container class="text-left">
      <b-row>
        <b-col sm="4">
          <h5 class="title">100 Wants List</h5>
          <p>100 things you want to do in your life!!</p>
        </b-col>
        <b-col sm="4">
          <h6 class="title">Lists</h6>
            <p>
              <span><router-link to="/userlist">User List</router-link></span>
              <!-- <span> / <router-link to="/rankinglist">Ranking List</router-link></span> -->
            </p>
        </b-col>
        <b-col sm="4">
          <h6 class="title">About WebSite</h6>
          <p>
            <span><b-link v-b-modal.modal1>About</b-link></span>
            <span> / <a href="https://docs.google.com/forms/d/e/1FAIpQLSfAlVQk12HE25ogzrKtQEY-qZdHk3xqeH2Jg8esD5ybwjH3Ow/viewform?embedded=true" target="_blank">Contact</a></span>
            <span> / <a href="https://www.anothersky.jp/" target="_blank">Administrator WebSite <i class="fa fa-external-link"></i></a></span>
          </p>
        </b-col>
      </b-row>
    </b-container>
    <div class="footer-copyright text-center py-3 mycolor2">
      <b-container fluid>&copy; 2019 100 Wants List.</b-container>
    </div>

    <b-modal id="modal1" title="100 Wants List について">
      <p>「人生でやってみたい100のこと」を書き出してみよう！</p>
      <p>100個書くのは意外と大変ですが、いつでも追加・変更・削除・そしてダウンロード可能です。
        どんなに大きなことでも、どんなにちっぽけでもいいので、とにかく書き出してみると、
        <strong>「自分の人生における優先順位」・「自分の本当に好きなこと」・「これから自分はどんな人生を送りたいか」</strong>
        が見えてくると思います。前提条件はすべて取っ払い考えることがポイントです。</p>
      <p>リストは公開/非公開設定ができます。
        公開にすると、他の人にもwantsリストを公開できます(見せたくない場合は非公開にしてください)
        他の人のWantsリストも参照できるので(公開限定)、共感できるものは「いいね」しましょう！</p>
    </b-modal>

  </footer>
</template>

<script>

</script>

<style>
.mycolor1 {
  background-color: lightblue;
}
.mycolor2 {
  background-color: darkblue;
  color: white;
}
</style>
