import Vue from 'vue'
import Router from 'vue-router'
Vue.use(Router)

import StoreContent from '@/components/StoreContent'
import StoreList from '@/components/StoreList'
import layout from '@/components/layout.vue'
export default new Router({
  routes: [
    {
      path: '/',
      name: 'StoreList',
      component: StoreList
    },
    {
      path: '/store',
      name: 'StoreContent',
      component: StoreContent
    },
    
  ]
})
