<template>
    <div>
    <h1>数据收集</h1>
    <template>
            <v-tabs :value="1" background-color="primary">    <!--:相当于<v-bind></v-bind>-->
                <v-tab @click="$router.push({name:'controller_auto'})">自动化测试控制台</v-tab>     <!-- 相当于v-on -->
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
            <template v-slot>
                <v-btn color="red">删除</v-btn>
                
            </template> 
            </v-data-table>

        
        </template>

        <template>
        
            <v-dialog
            v-model="dialog"
            width="500"
            >
            

            <v-card>
                <v-card-title class="text-h5 grey lighten-2">
                调试导入面板
                </v-card-title>

                <v-card-text>
                调试导入内容
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    color="primary"
                    text
                    @click="dialog = false"
                >
                    确认
                </v-btn>
                </v-card-actions>
            </v-card>
            
            </v-dialog>
            <v-btn color="primary" class="btn" @click="dialog=true">导入数据调试</v-btn>
        

        </template>
          <template>
        
            <v-dialog
            v-model="dialog2"
            width="500"
            >
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                color="blue lighten-2"
                dark
                v-bind="attrs"
                v-on="on"
                class="btn"
                >
                删除数据调试
                </v-btn>
            </template>
            

            <v-card>
                <v-card-title class="text-h5 grey lighten-2">
                调试删除面板
                </v-card-title>

                <v-card-text>
                调试删除内容
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                    color="primary"
                    text
                    @click="dialog2 = false"
                >
                    确认
                </v-btn>
                </v-card-actions>
            </v-card>
            
            </v-dialog>
        
        </template>

        
        <!-- <v-btn color="primary" class="btn">导入数据</v-btn>

        <v-btn color="red" class="btn">删除数据</v-btn> -->

        <v-text-field v-model="id"  label="输入要拉取的数据id" type="number" ></v-text-field>
        <v-btn  color="yellow" class="btn"  @click="getcase()">测试数据拉取接口</v-btn>

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
                {text:"id",
                value:"id"},
                {text:"case_step",
                value:"case_step"},
                {
                    text:"操作",
                    value:"operate"
                }
            ],
            desserts:[],
            id:0,
            dialog:false,
            dialog2:false,

        }
    },

    created(){
        this.$api.user.getcase({
            "id":0
        }).then((result) => {
                console.log(result)
                // alert(result["data"])
                this.desserts=result.data

            }).catch((err) => {
                
            });

    },
    methods:{
       
        getcase(){
             let get_data={
            "id":this.id
        }
        console.log(get_data,typeof(get_data))
            this.$api.user.getcase(get_data).then((result) => {
                console.log(result)
                alert(result["data"])
                this.desserts=result.data

            }).catch((err) => {
                
            });        }

    }
    
}
</script>
<style scoped>
    .btn{
        margin: 20px;
    }
</style>