
<template>
    <v-data-table
            :headers="headers"
            :items="desserts"
            :items-per-page="5"
            class="elevation-1"
        ></v-data-table>
</template>


<script>
  export default {
    data () {
      return {
        headers: [
          {
            text: 'Type',
            align: 'start',
            sortable: false,
            value: 'name',
          },
          { text: 'case_id', value: 'id' },
          
          { text: 'case_step', value: 'case_step' },
          
      
        ],
        desserts: [],
      }
    },
    methods:{
      initialize(){
        this.$api.user.initial_all_case().then((result) => {
          console.log(result.data)
          this.desserts=result.data
        }).catch((err) => {
          
        });
      }
    },
    created(){
      this.initialize();
    }

  }
</script>
