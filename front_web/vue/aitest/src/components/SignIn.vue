<template>
    <div class="sign-form"> 
        <h1>自动测试平台登录</h1>
        <v-text-field v-model="user"  label="用户名"></v-text-field>
        <v-text-field v-model="password"  label="密码" type="password"></v-text-field>
        <v-btn color="primary" @click="sign_in()">登录</v-btn>
        
    </div>
</template>
<script>
export default {

    data(){
        return{
            user:"",
            password:""
        }
        },
    methods:{
        sign_in(){
            let post_data={
                username:this.user,
                password:this.password
            }
            console.log(post_data,typeof(post_data))
            this.$api.user.signin(post_data).then((result) => {
                if(result["data"]=="ok"){
                this.$router.push({name:'testhome'})
                }else {
                    console.log("Retry")
                    alert("密码错误！")
                }
                
            }).catch((err) => {
                
            })
            
            
              }   

    }
    
}
</script>
<style scoped>
.sign-form{
    width: 500px;
    margin:0 auto ;
    text-align: center;
}

</style>