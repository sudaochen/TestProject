import Vue from 'vue'
import VueRouter from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import Signin from '../components/SignIn.vue'
import TestHome from '../components/TestHome.vue'


Vue.use(VueRouter)

const routes = [
  // {
  //   path: '/',
  //   name: 'home',
  //   component: HomeView
  // },
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // }
  {
    path:'/',
    name:'Signin',
    component:Signin
  },
  {
    path:'/Testhome',
    name:'testhome',
    component:TestHome
  }
]

const router = new VueRouter({
  routes
})

export default router
