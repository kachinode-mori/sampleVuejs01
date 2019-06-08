<template>
  <div class="container">
    <br>
    <div class="card-group">
      <!-- カード1: ユーザの情報(e-mailアバター、ニックネーム、likes一覧、いいね数、twitterアイコンを表示) -->
      <div v-for="user in users" v-bind:key="user.id" class="card">
        <div class="card-body">
          <span><v-gravatar v-bind:email="user.email" :size="60" class="w-30 rounded" default-img="mm"/></span>
          <span style="margin: 0 0 0 15px;"><strong>{{ user.nickname }}</strong></span>
          <span style="margin: 0 0 0 15px;" v-if="user.twitterUrl !==''">
            <a v-bind:href="'https://twitter.com/' + user.twitterUrl" target="_blank">
              <i class="fa fa-twitter fa-1x"></i>
            </a>
          </span>
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
    <!-- wantテーブルの表示 -->
    <div class="col-xs-12">
      <table id="table1" class="table table-bordered">
        <thead>
          <tr class="table-warning" style="text-align:center;">
            <th>Status</th>
            <th>No</th>
            <th>Wants</th>
            <th>Open</th>
            <th>目標日付</th>
            <th>達成参考URL</th>
            <th>達成日</th>
            <th>Likes</th>
          </tr>
        </thead>
        <tbody v-for="(want, index) in wants" v-bind:key="want.id">
          <tr v-if="want.publishSet===true">
            <!-- ステータス -->
            <td class="position" v-if="want.status==='nostart'" style="background-color:lightgreen;">未着手</td>
            <td class="position" v-else-if="want.status==='doing'" style="background-color:lightblue;">実施中</td>
            <td class="position" v-else style="background-color:lightgray;">達成</td>
            <!-- No -->
            <td class="position">{{ index + 1 }}</td>
            <!-- want内容 -->
            <td>{{ want.content }}</td>
            <!-- 公開/非公開設定 -->
            <td class="position">公開</td>
            <!-- 目標日付 -->
            <td class="position">{{ want.targetDate }}</td>
            <!-- 参考URL -->
            <td class="position">{{ want.achieveUrl }}</td>
            <!-- 達成日 -->
            <td class="position">{{ want.achieveDate }}</td>
            <!-- いいねlikes -->
            <td class="position">
              <b-btn size="sm" variant="outline-primary" v-on:click="likepush(want.id)">
                Like! <i class="fa fa-thumbs-o-up" ></i> {{ want.likeNum }}
              </b-btn>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <br>
    <!-- <pre>{{ $data }}</pre> -->
  </div>
</template>

<script>
import axios from 'axios'
import Chart from './Chart.js'

export default {
  name: 'UserWantList',
  props: {
    id: Number
  },
  components: {
    Chart
  },
  data () {
    return {
      wants: [],
      users: [],
      count: null,
      datacollection: null
    }
  },
  methods: {
    // wantslistデータの取得
    fetchData () {
      // axios.get(`http://127.0.0.1:8000/api/wants/`).then(res => {
      axios.get(`${process.env.API_ENDPOINT}wants/`).then(res => {
        var userwantlist = []
        var countall = 0
        var wantresult = res.data.results
        for (var i = 0; i < wantresult.length; i++) {
          if (wantresult[i].user === this.id) {
            userwantlist.push(wantresult[i])
            countall++
          }
        }
        this.wants = userwantlist
        this.count = countall
        // axios.get(`http://127.0.0.1:8000/api/users/?id=${this.id}`).then(res => {
        axios.get(`${process.env.API_ENDPOINT}users/?id=${this.id}`).then(res => {
          this.users = res.data.results
        })
        this.getChartdata()
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
</style>
