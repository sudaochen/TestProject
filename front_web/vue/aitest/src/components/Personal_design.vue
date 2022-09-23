<template>
    <div>
    <h1>自定义</h1>
    <template>
            <v-tabs :value="2" background-color="primary">
                <v-tab @click="$router.push({name:'controller_auto'})">自动化测试控制台</v-tab>
                <v-tab @click="$router.push({name:'data_collect'})">测试数据录入</v-tab>
                <v-tab @click="$router.push({name:'personal_design'})">自定义模块</v-tab>
            </v-tabs>
    </template>

    <v-dialog v-model="addDialog"
        max-width="500px">
    <v-card>
        <v-card-title>添加测试用例</v-card-title>
        <v-card-text>
            <v-container>
            <v-text-field label="id" v-model="newid"></v-text-field>
            <v-select :items="selectitem"  label="type"></v-select>
            <v-text-field label="case_step" v-model="newcasestep"></v-text-field>
            </v-container>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn  color="gprimary" @click="postnewcase()" >确定</v-btn>
                <v-btn color="red" @click="addDialog=false">取消</v-btn>
            </v-card-actions>
        </v-card-text>
    
    </v-card>
    
    </v-dialog>
    <v-btn color="primary" class="btn" @click="addDialog=true">增加测试数据</v-btn>


    </div>
    
</template>
<script>
export default {
    data(){
        return{
            addDialog:false,
            selectitem:["testadd","testdel"],
            newid:'',
            newcasestep:'',
        }
    },
    methods:{
        postnewcase(){
            let postdata={
                id:this.newid,
                case_step:this.newcasestep
            }
            this.$api.user.postcase(postdata).then((result) => {
                // alert(result['data'])
                console.log(result["data"])
                this.addDialog=false
                if (result['data']=="ok")
                {   
                    alert("添加成功")
                }else{
                    alert("添加失败")
                }
                
            }).catch((err) => {
                
            });
        }

    }
    
}
</script>
<style scoped>
    .btn{
        margin: 30px;
        
    }

</style>