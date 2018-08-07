// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import axios from './vue-axios' // Axios plugin
import VeeValidate, {Validator} from 'vee-validate'
import es from 'vee-validate/dist/locale/es'
import en from 'vee-validate/dist/locale/en'
import VueScrollReveal from 'vue-scroll-reveal'
import i18n from './i18n/i18n'

// English and Spanish validation messages
Validator.localize('es', es)
Validator.localize('en', en)

Vue.config.productionTip = false
Vue.use(axios)
Vue.use(VeeValidate)
Vue.use(VueScrollReveal)

// Vue.prototype.$config_json = 1

// Vue.use(VueSocketio, 'http://localhost:8000')

async function configuration () {
  let config = await Vue.http.get('/static/config.json')
  console.log('CONFIG', config.data)
  Vue.http.defaults.baseURL = config.data.rest_url
  Vue.prototype.$config_json = config.data
  /* eslint-disable no-new */
  new Vue({
    el: '#app',
    i18n,
    router,
    components: {App},
    template: '<App/>'
  })
}

configuration()

/* eslint-disable no-new */
// new Vue({
//   el: '#app',
//   router,
//   components: { App },
//   template: '<App/>'
// })
