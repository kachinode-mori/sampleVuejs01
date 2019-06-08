<template>
  <div>
    <draggable element="ul">
      <li v-for="item in items" v-bind:key="item.no">{{ item.name }}</li>
    </draggable>
  </div>
</template>

<script>
import draggable from 'vuedraggable'

export default {
  name: 'zDragTest',
  components: {
    draggable
  },
  data () {
    return {
      items: [
        {no: 1, name: 'キャベツ', categoryNo: '1'},
        {no: 2, name: 'ステーキ', categoryNo: '2'},
        {no: 3, name: 'リンゴ', categoryNo: '3'}
      ]
    }
  }
}
</script>
