<template>
  <div class="container">
    <br>
    <div class="card-group">
      <div class="card">
        <div class="card-body">
          {{ userId }} {{ nickName }}
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">100 Wants List :
            <span class="badge badge-dark">XX</span>
            <small><button v-on:click="download(userId)" class="btn-sm btn-success">List Download</button></small>
          </h5>
          <div class="card-text"><small class="text-muted">未着手：XX</small></div>
          <div class="card-text"><small class="text-muted">実施中：XX</small></div>
          <div class="card-text"><small class="text-muted">達成：XX</small></div>
        </div>
      </div>
      <div class="card">
        <!-- <canvas id="myChart"></canvas> -->
      </div>
    </div>
    <!-- Want追加inputフィールド -->
    <br>
    <!-- <form v-if="isLoggedIn" v-on:submit.prevent> -->
    <form v-on:submit.prevent>
      <div class="form-row align-items-center">
        <div class="col-4">
          <label class="sr-only" for="inlineFormInput">Want</label>
          <input v-model="newWant" type="text" class="form-control mb-2" id="inlineFormInput" placeholder="Input Your Wants!">
        </div>
        <div class="col-auto">
          <div class="form-check mb-2">
            <input v-model="isOpen" class="form-check-input" type="checkbox" id="autoSizingCheck">
            <label class="form-check-label" for="autoSizingCheck">非公開</label>
          </div>
        </div>
        <div class="col-auto">
          <button v-on:click="addWant" class="btn btn-primary mb-2">追加</button>
        </div>
      </div>
    </form>
    <!-- 追加したwantを表示するテスト領域 -->
    <!-- <li v-for="wantlist in wantlists" v-bind:key="wantlist.want">
      <input type="text" v-model="wantlist.want">
      <select v-model="wantlist.isStatus">
        <option v-for="status in statuses" v-bind:value="status.value" v-bind:key="status.text">
          {{ status.text }}
        </option>
      </select>
      <select v-model="wantlist.isOpen">
        <option v-for="openset in opensets" v-bind:value="openset.name" v-bind:key="openset.name">
          {{ openset.name }}
        </option>
      </select>
    </li> -->
    <!-- wantテーブルの表示 -->
    <div class="col-xs-12">
      <table id="table1" class="table table-bordered">
        <thead>
          <tr class="table-primary" style="text-align:center;">
            <th>Status</th><th>No</th><th>Wants</th><th>Open</th><th>Target日付</th><th>達成入力</th><th>削除</th><th>Likes</th>
          </tr>
        </thead>
        <!-- <tbody v-for="(want, index) in wants" v-bind:key="want.id" v-if="want.user.id===userId"> -->
        <tbody v-for="(want, index) in wants" v-bind:key="want.id">
          <tr>
            <td v-if="want.status==='nostart'" style="background-color:lightgreen;">
              <select v-model="want.status" class="form-control" style="border:none; background-color:lightgreen;">
                <option value="nostart">未着手</option>
                <option value="doing">実施中</option>
                <option value="done">達成</option>
              </select>
            </td>
            <td v-else-if="want.status==='doing'" style="background-color:lightblue;">
              <select v-model="want.status" class="form-control" style="border:none; background-color:lightblue;">
                <option value="nostart">未着手</option>
                <option value="doing">実施中</option>
                <option value="done">達成</option>
              </select>
            </td>
            <td v-else style="background-color:lightgray;">
              <select v-model="want.status" class="form-control" style="border:none; background-color:lightgray;">
                <option value="nostart">未着手</option>
                <option value="doing">実施中</option>
                <option value="done">達成</option>
              </select>
            </td>
            <td style="text-align:center; vertical-align:middle;">
              {{ index + 1 }} {{ want.user.id }} {{ userId }}
            </td>
            <td>
              <input class="form-control" type="text" v-model="want.content" style="border:none;">
            </td>
            <td>
              <select v-model="want.publishSet" class="form-control" style="border:none;">
                <option value="true">公開</option>
                <option value="false">非公開</option>
              </select>
            </td>
            <td><input v-model="want.targetDate" type="date" max="9999-12-31" class="form-control" style="border:none;"></td>
            <td>
              <button class="btn btn-outline-info btn-sm">達成入力</button>
            </td>
            <td>
              <button class="btn btn-outline-danger btn-sm" v-on:click="wantdel(want.id)">削除</button>
            </td>
            <td>
              <i class="fa fa-thumbs-o-up"></i> {{ want.likeNum }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <br>
    <pre>{{ $data }}</pre>
  </div>
</template>

<script>
import axios from 'axios'
import moment from 'moment'
import {mapGetters} from 'vuex'

export default {
  name: 'WantsIndex',
  data () {
    return {
      wants: [],
      newWant: null,
      isOpen: null
      // wantlists: [],
      // statuses: [
      //   {text: 'nostart', value: '未着手'},
      //   {text: 'doing', value: '実施中'},
      //   {text: 'done', value: '達成'}
      // ],
      // opensets: [
      //   {name: '公開'},
      //   {name: '非公開'}
      // ]
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn', 'userId', 'nickName'])
  },
  methods: {
    // wantslistデータの取得
    fetchData () {
      axios.get('http://127.0.0.1:8000/api/wants/').then(res => {
        this.wants = res.data.results
      })
      // axios.get('http://127.0.0.1:8000/api/users/').then(resuser => {
      //   console.log(resuser)
      //   this.users = resuser.data.results
      // })
    },
    // wantslistデータの削除
    wantdel (wantid) {
      var result = window.confirm('本当に削除しますか？')
      if (result) {
        // yesの場合、delete処理後にデータ取得しリスト表示
        axios.delete(`http://127.0.0.1:8000/api/delete/${wantid}/`).then(res => {
          this.fetchData()
        })
      }
    },
    // download ボタンが押された場合
    download (userid) {
      axios.get(`http://127.0.0.1:8000/api/export/${userid}/`).then(res => {
        console.log(res)
        // alert('ダウンロードしました')
      })
    },
    // want追加ボタンが押された場合
    addWant () {
      // 追加内容が空だったら何もしない
      if (this.newWant === '') return
      // 公開か非公開を設定
      if (this.isOpen === null) {
        this.isOpen = true
      } else {
        this.isOpen = false
      }
      // ステータスのデフォルトは未着手
      var defaultstatus = 'nostart'

      axios.post(`http://127.0.0.1:8000/api/wants/create/`, {
        content: this.newWant,
        status: defaultstatus,
        publishSet: this.isOpen
      }).then(res => {
        this.fetchData()
      })
    }
    // // want追加ボタンが押された場合
    // addWant: function (event) {
    //   if (this.newWant === '') return
    //   if (this.isOpen === null) {
    //     this.isOpen = '公開'
    //   } else {
    //     this.isOpen = '非公開'
    //   }
    //   var want = {
    //     want: this.newWant,
    //     isStatus: '未着手',
    //     isOpen: this.isOpen
    //   }
    //   this.wantlists.push(want)
    //   this.newWant = ''
    //   this.isOpen = ''
    // }
  },
  mounted () {
    this.fetchData()
  },
  filters: {
    moment: function (date) {
      return moment(date).format('YYYY/MM/DD')
    }
  }
}
</script>
