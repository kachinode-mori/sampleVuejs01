<template>
  <div class="container">
    <br>
    <div class="card-group">
      <!-- カード1: ユーザの情報(e-mailアバター、ニックネーム、likes一覧、いいね数、twitterアイコンを表示) -->
      <div v-for="user in users" v-bind:key="user.id" class="card">
        <div class="card-body">
          <span><v-gravatar v-bind:email="user.email" :size="60" class="w-30 rounded" default-img="mm"/>
            <strong>{{ user.nickname }}</strong>
          </span>
          <br><br>
          <small><router-link to="/userlikelist"><button class="btn-sm btn-warning">Likes一覧</button></router-link></small>
          <small><button v-on:click="download()" class="btn-sm btn-success">List Download</button></small>
        </div>
      </div>
      <!-- カード2: 100wantsの情報(総数、未着手、実施中、達成とダウンロードボタンの表示) -->
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">100 Wants List :
            <span class="badge badge-dark">{{ count }}</span>
          </h5>
          <div class="card-text"><small class="text-muted">未着手：{{ getStatus('nostart') }}</small></div>
          <div class="card-text"><small class="text-muted">実施中：{{ getStatus('doing') }}</small></div>
          <div class="card-text"><small class="text-muted">達成：{{ getStatus('done') }}</small></div>
        </div>
      </div>
      <!-- カード3: 100wantsのドーナツチャート -->
      <div class="card">
        <Chart :chart-data="datacollection" :height="200"></Chart>
      </div>
    </div>
    <br>
    <!-- Want追加inputフィールド -->
    <form v-if="isLoggedIn" v-on:submit.prevent>
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
    <!-- wantテーブルの表示 -->
    <div class="table-responsive">
      <table class="table table-bordered">
        <thead>
          <tr class="table-primary position">
            <th> - </th>
            <th>Status</th>
            <th>No</th>
            <th>Wants</th>
            <th>Open</th>
            <th>目標日付</th>
            <th>達成入力</th>
            <th>削除</th>
            <th>Likes</th>
          </tr>
        </thead>
        <draggable v-model="wants" :element="'tbody'" :options="{handle:'.handle', animation:150, delay:150}" v-on:end="onEnd">
        <!-- <tbody> -->
          <tr v-for="(want, index) in wants" v-bind:key="want.id">
            <!-- moveハンドル -->
            <td class="position handle"><i class="fa fa-bars myhandle"></i></td>
            <!-- ステータス -->
            <td v-if="want.status==='nostart'" style="background-color:lightgreen;">
              <select v-model="want.status" v-on:change="wantupdate(want.id)" class="form-control" style="border:none; background-color:lightgreen;">
                <option value="nostart">未着手</option>
                <option value="doing">実施中</option>
                <option value="done">達成</option>
              </select>
            </td>
            <td v-else-if="want.status==='doing'" style="background-color:lightblue;">
              <select v-model="want.status" v-on:change="wantupdate(want.id)" class="form-control" style="border:none; background-color:lightblue;">
                <option value="nostart">未着手</option>
                <option value="doing">実施中</option>
                <option value="done">達成</option>
              </select>
            </td>
            <td v-else style="background-color:lightgray;">
              <select v-model="want.status" v-on:change="wantupdate(want.id)" class="form-control" style="border:none; background-color:lightgray;">
                <option value="nostart">未着手</option>
                <option value="doing">実施中</option>
                <option value="done">達成</option>
              </select>
            </td>
            <!-- No -->
            <td class="position">
              {{ index + 1 }}
            </td>
            <!-- want内容 -->
            <td>
              <input v-model="want.content" v-on:change="wantupdate(want.id)" class="form-control" type="text" style="border:none;">
            </td>
            <!-- 公開/非公開設定 -->
            <td>
              <select v-model="want.publishSet" v-on:change="wantupdate(want.id)" class="form-control" style="border:none;">
                <option value="true">公開</option>
                <option value="false">非公開</option>
              </select>
            </td>
            <!-- 目標日付 -->
            <td>
              <input v-model="want.targetDate" v-on:change="wantupdate(want.id)" type="date" max="9999-12-31" class="form-control" style="border:none;">
            </td>
            <!-- 達成入力 -->
            <td class="position" v-if="want.status==='done'" >
              <b-btn v-on:click="showModal(want.id)" size="sm" variant="outline-success">達成入力</b-btn>
            <td class="position" v-else>
              <b-btn size="sm" disabled variant="outline-success">達成入力</b-btn>
            </td>
            <!-- 削除 -->
            <td class="position">
              <b-btn size="sm" variant="outline-danger" v-on:click="wantdel(want.id)">削除</b-btn>
            </td>
            <!-- いいねlikes -->
            <td class="position">
              <b-btn size="sm" disabled variant="outline-primary">
                <i class="fa fa-thumbs-o-up" ></i> {{ want.likeNum }}
              </b-btn>
            </td>
          </tr>
        <!-- </tbody> -->
        </draggable>
      </table>
    </div>
    <br>
    <b-modal ref="myModalRef" hide-footer title="達成入力">
      <div>
        <b-form v-on:submit="achieveSub(achieve.id)">
          <b-form-group label="達成日付：">
            <b-form-input v-model="achieve.date" type="date"></b-form-input>
          </b-form-group>
          <b-form-group label="参照URL：">
            <b-form-input v-model="achieve.url" type="url"></b-form-input>
          </b-form-group>
          <b-form-group label="達成コメント:">
            <b-form-textarea :rows="3" v-model="achieve.text" type="text"></b-form-textarea>
          </b-form-group>
          <b-btn type="submit" variant="primary" block>更新</b-btn>
        </b-form>
        <br>
        <b-btn variant="outline-danger" block v-on:click="hideModal">Close</b-btn>
      </div>
    </b-modal>
    <!-- <pre>{{ $data.wants }}</pre> -->
  </div>
</template>

<script>
import axios from 'axios'
import {mapActions, mapGetters} from 'vuex'
import Chart from './Chart.js'
import draggable from 'vuedraggable'

export default {
  name: 'WantsIndex',
  components: {
    Chart,
    draggable
  },
  data () {
    return {
      wants: [],
      users: [],
      count: null,
      newWant: null,
      isOpen: null,
      achieve: {
        id: null,
        date: null,
        url: null,
        text: null
      },
      datacollection: null,
      upwants: []
    }
  },
  computed: {
    ...mapGetters(['isLoggedIn', 'userId'])
  },
  created () {
    this.tryLoggedIn()
  },
  methods: {
    ...mapActions(['tryLoggedIn']),
    // wantslistデータの取得
    fetchData () {
      // axios.get('http://127.0.0.1:8000/api/userwants/').then(res => {
      axios.get(`${process.env.API_ENDPOINT}userwants/`).then(res => {
        this.wants = res.data.results
        this.count = res.data.count
        // axios.get(`http://127.0.0.1:8000/api/users/?id=${res.data.results[0].user}`).then(res => {
        axios.get(`${process.env.API_ENDPOINT}users/?id=${res.data.results[0].user}`).then(res => {
          this.users = res.data.results
        })
        this.getChartdata()
      }).catch(error => {
        console.log(error)
      })
    },
    // グラフデータの取得
    getChartdata () {
      this.datacollection = {
        labels: ['未着手', '実施中', '達成'],
        datasets: [
          {
            data: [this.getStatus('nostart'), this.getStatus('doing'), this.getStatus('done')],
            backgroundColor: ['lightgreen', 'lightblue', 'lightgray']
          }
        ]
      }
    },
    // Vue.Draggableの移動が終わったら処理を実施
    onEnd () {
      var num = 0
      // wantslistをループして、更新データを作成する
      for (var i = 0; i < this.wants.length; i++) {
        num += 1
        var addnum = {
          id: this.wants[i].id,
          displayOrder: num
        }
        this.upwants.push(addnum)
      }
      // 更新処理を実施
      axios.patch(`${process.env.API_ENDPOINT}wantsupdate/`, {
        upwants: this.upwants
      })
      // for (var i = 0; i < this.wants.length; i++) {
      //   num += 1
      //   this.wants[i].displayOrder = num
      //   axios.patch(`${process.env.API_ENDPOINT}wants/${this.wants[i].id}/`, {
      //     displayOrder: this.wants[i].displayOrder
      //   })
      // }
    },
    // want追加ボタンが押された場合
    addWant () {
      // 追加内容が空だったら何もしない
      if (this.newWant !== null) {
        // 公開か非公開を設定
        if (this.isOpen === null) {
          this.isOpen = true
        } else {
          this.isOpen = false
        }
        // ステータスのデフォルトは未着手
        var defaultstatus = 'nostart'
        // wantの新規追加処理
        // axios.put(`http://127.0.0.1:8000/api/wantscreate/`, {
        axios.put(`${process.env.API_ENDPOINT}wantscreate/`, {
          user: null,
          content: this.newWant,
          status: defaultstatus,
          publishSet: this.isOpen
        }).then(res => {
          this.fetchData()
          this.newWant = null
          this.isOpen = null
        }).catch(error => {
          console.log(error)
        })
      }
    },
    // データの更新
    wantupdate (wantid) {
      // wantsデータを回して、対象のwantidのデータを取得する
      for (var i = 0; i < this.wants.length; i++) {
        if (this.wants[i].id === wantid) {
          var content = this.wants[i].content
          var status = this.wants[i].status
          if (this.wants[i].targetDate === null) {
            var targetDate = null
          } else {
            targetDate = this.wants[i].targetDate + ' 09:00:00.000000'
          }
          var publishSet = this.wants[i].publishSet
        }
      }
      // axios.patchにて、対象のwantidにて対して更新処理
      // axios.patch(`http://127.0.0.1:8000/api/wants/${wantid}/`, {
      axios.patch(`${process.env.API_ENDPOINT}wants/${wantid}/`, {
        content: content,
        status: status,
        targetDate: targetDate,
        publishSet: publishSet
      }).then(res => {
        // console.log('更新しました')
        this.fetchData()
      }).catch(error => {
        console.log(error)
      })
    },
    // モーダルウィンドウの表示
    showModal (wantid) {
      // axios.get(`http://127.0.0.1:8000/api/wants/${wantid}/`).then(res => {
      axios.get(`${process.env.API_ENDPOINT}wants/${wantid}/`).then(res => {
        this.achieve.id = res.data.id
        this.achieve.date = res.data.achieveDate
        this.achieve.url = res.data.achieveUrl
        this.achieve.text = res.data.achieveText
      })
      this.$refs.myModalRef.show()
    },
    // キャンセルボタンが押下されたとき or 画面を閉じるとき
    hideModal () {
      this.achieve.id = null
      this.achieve.date = null
      this.achieve.url = null
      this.achieve.text = null
      this.$refs.myModalRef.hide()
    },
    // wants達成入力更新
    achieveSub (achieveid) {
      // 日付の調整
      if (this.achieve.date === '' || this.achieve.date === null) {
        var achievedate = null
      } else {
        achievedate = this.achieve.date + ' 09:00:00.000000'
      }
      // 更新処理
      // axios.patch(`http://127.0.0.1:8000/api/wants/${achieveid}/`, {
      axios.patch(`${process.env.API_ENDPOINT}wants/${achieveid}/`, {
        achieveDate: achievedate,
        achieveText: this.achieve.text,
        achieveUrl: this.achieve.url
      }).then(res => {
        // console.log('更新しました')
        this.achieve.id = null
        this.achieve.date = null
        this.achieve.url = null
        this.achieve.text = null
        this.$refs.myModalRef.hide()
      })
    },
    // wantslistデータの削除
    wantdel (wantid) {
      var result = window.confirm('本当に削除しますか？')
      if (result) {
        // yesの場合、delete処理後にデータ取得しリスト表示
        // axios.delete(`http://127.0.0.1:8000/api/delete/${wantid}/`).then(res => {
        axios.delete(`${process.env.API_ENDPOINT}delete/${wantid}/`).then(res => {
          this.fetchData()
        })
      }
    },
    // likesボタンの押下
    likepush (wantid) {
      // axios.put(`http://127.0.0.1:8000/api/likepush/${wantid}/`).then(res => {
      axios.put(`${process.env.API_ENDPOINT}likepush/${wantid}/`).then(res => {
        this.fetchData()
      }).catch(error => {
        console.log(error)
      })
    },
    // wantのステータスの状態をカウント
    getStatus (nowstatus) {
      var ncount = 0
      var wants = this.wants
      for (var i = 0; i < wants.length; i++) {
        if (wants[i].status === nowstatus) {
          ncount++
        }
      }
      return ncount
    },
    // download ボタンが押された場合
    download () {
      var csv = '\ufeff' + '内容,ステータス,目標日,公開設定,達成日,達成メモ,参考URL\n'
      this.wants.forEach(el => {
        var line = el['content'] + ',' + el['status'] + ',' + el['targetDate'] + ',' + el['publishSet'] + ',' + el['achieveDate'] + ',' + el['achieveText'] + ',' + el['achieveUrl'] + '\n'
        csv += line
      })
      let blob = new Blob([csv], { type: 'text/csv' })
      let link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = 'downwants.csv'
      link.click()
    }
  },
  mounted () {
    this.fetchData()
  }
}
</script>

<style scoped>
  .position {
    text-align: center;
    vertical-align: middle;
  }
  .myhandle {
    cursor: move;
    color: rgb(0, 174, 255);
  }
</style>
