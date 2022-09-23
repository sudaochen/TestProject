import Vue from 'vue'
import VueRouter from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import Signin from '../components/SignIn.vue'
import TestHome from '../components/TestHome.vue'
import Controller_auto from '../components/Controller_auto.vue'
import Data_collect from '../components/Data_collect.vue'
import Personal_design from '../components/Personal_design'


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
  },
  {
    path:'/Controller_auto',
    name:'controller_auto',
    component:Controller_auto
  },
  {
    path:'/Data_collect',
    name:'data_collect',
    component:Data_collect
  },
  {
    path:'/Personal_design',
    name:'personal_design',
    component:Personal_design
  }
]

const router = new VueRouter({
  routes
})
const originalPush = VueRouter.prototype.push

VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}


export default router
