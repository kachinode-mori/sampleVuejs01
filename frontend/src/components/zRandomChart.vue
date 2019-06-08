<template>
  <div class="container">
    <br>
    <div class="card-group">
      <div class="card">
        <div class="card-body">
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">100 Wants List :
            <span class="badge badge-dark">XX</span>
          </h5>
          <div class="card-text"><small class="text-muted">未着手：XX</small></div>
          <div class="card-text"><small class="text-muted">実施中：XX</small></div>
          <div class="card-text"><small class="text-muted">達成：XX</small></div>
        </div>
      </div>
      <div class="card">
        <div class="card-body">
          <Chart :chart-data="datacollection" :height="200"></Chart>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from './Chart.js'

export default {
  components: {
    Chart
  },
  data () {
    return {
      datacollection: null
    }
  },
  mounted () {
    this.getChartData()
  },
  methods: {
    getChartData () {
      this.datacollection = {
        labels: ['未着手', '実施中', '達成'],
        datasets: [
          {
            data: [this.getNostart(), this.getDoing(), this.getDone()],
            backgroundColor: ['lightgreen', 'lightblue', 'lightgray']
          }
        ]
      }
    },
    getNostart () {
      return 10
    },
    getDoing () {
      return 15
    },
    getDone () {
      return 20
    }
  }
}
</script>
