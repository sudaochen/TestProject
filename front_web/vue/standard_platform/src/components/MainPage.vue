<template>
<div>

<v-app>

<v-navigation-drawer app clipped>

    <managelist />  
    <!-- 此方法直接将希望添加到本页面的组件注册显示到mainpage的指定位置中 -->

</v-navigation-drawer>


<router-view />        
<!-- 用于在本页面的指定位置显示mainpage的子路由  不需要单独注册  直接通过子路由地址即可   -->
<!-- 与上面直接注册展示的方法的区别在于，此处是通过路由灵活访问，注册显示的是固定内容  -->



</v-app>


</div>
    
</template>
<script>
    import managelist from "./managelist.vue"
    
export default {

        components:{
            managelist,
        
        }
    }
</script>

<style scoped>

</style>