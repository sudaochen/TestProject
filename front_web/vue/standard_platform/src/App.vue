<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
      clipped-left
    >
    <h1>Ziipin-Test-Platorm</h1>
      
    </v-app-bar>



    <v-main>
      <router-view/>  <!-- 通过这里控制在APP中展示其他各个路由的.vue -->
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
};
</script>
<style scoped>
 

</style>
