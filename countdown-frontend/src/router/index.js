import Vue from 'vue'
import Router from 'vue-router'
import VueSocketio from 'vue-socket.io'
import NumbersPage from '@/components/NumbersPage'
import FrontPage from '@/components/FrontPage'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'FrontPage',
      component: FrontPage
    },
    {
      path: '/numbers_solver',
      component: NumbersPage,
      name: 'Numbers',
      beforeEnter: function (to, from, next) {
        console.log('BEFOREENTER', Vue.prototype.$config_json)
        if (!Vue.prototype.$socket) {
          Vue.use(VueSocketio, Vue.prototype.$config_json.socketio_url)
        }
        next()
      }
    },
    {path: '*', redirect: '/'}
  ]
})
