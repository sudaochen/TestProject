import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Login from '../components/Login.vue'
import Mainpage from '../components/MainPage.vue'
import managelist from '../components/managelist.vue'
import testdata from '../components/testdata.vue'
import reportdata from '../components/reportdata.vue'
import settings from '../components/settings.vue'




Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'login',
    component: Login
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path:'/mainpage',
    name:'main',
    component:Mainpage,
    children:[{
      path:'testdata', //注意作为子路由的内容  不需要添加/  直接写名字即可
      name:'testdata',
      component:testdata
    },
      {
        path:'reportdata',
      name:'reportdata',
      component:reportdata
    },
    {
      path:"settings",
      name:"settings",
      component:settings
    }
  ],
    
  },

  {
    path:'/managelist',
    name:'manage',
    component:managelist

  }



]

const router = new VueRouter({
  routes
})

export default router
