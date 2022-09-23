<template>
    <div>
        <h1><div class="mainpage">测试平台主页</div>
        <template>
            <v-tabs>
                <v-tab @click="$router.push({name:'controller_auto'})">自动化测试控制台</v-tab>
                <v-tab @click="$router.push({name:'data_collect'})">测试数据录入</v-tab>
                <v-tab @click="$router.push({name:'personal_design'})">自定义模块</v-tab>
            </v-tabs>
        </template> </h1>
    </div> 
    
</template>
<script>
export default {
    data(){
        return{

        }

    },
    methods:{

    }
    
}
</script>
<style scoped>
.mainpage{
    width: 2000px;
    text-align: center;
    margin: 0 auto;
}

</style>