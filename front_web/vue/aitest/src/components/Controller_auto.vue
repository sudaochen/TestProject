<template>
    <div>
    <h1>自动测试控制</h1>
    <template>
            <v-tabs :value="0" background-color="primary">
                <v-tab @click="$router.push({name:'controller_auto'})">自动化测试控制台</v-tab>
                <v-tab @click="$router.push({name:'data_collect'})">测试数据录入</v-tab>
                <v-tab @click="$router.push({name:'personal_design'})">自定义模块</v-tab>
            </v-tabs>
    </template>

    <template>
        <v-data-table 
        v-model="selected"
        :headers="headers"
        :items="desserts"
        item-key="name"
        show-select
        class="elevation-1"
        >
        </v-data-table>
    </template>


    <v-btn class="btn" color="red lighten-5=" @click="doubleballs()">~看看今天的幸运值吧~</v-btn>


    </div>
     
    
</template>
<script>
export default {
    data(){
        return{
            selected:[],
            headers:[
                {text:"调试",
                value:""},
                {text:"模块",
                value:""},
                {text:"功能",
                value:""}
            ],
            desserts:[],
                }
        },
    methods:{
        doubleballs(){
            this.$api.user.doubleballs("11").then((result) => {
                console.log(result)
                alert("今天的幸运抽奖结果是:\n"+result["data"])
            }).catch((err) => {
                
            });
        }

    }
    
}
</script>
<style scoped>

</style>