<template>
  <div id="app">
    <!--<nav-bar></nav-bar>-->
    <!--<front-page></front-page>-->
    <router-view></router-view>
  </div>
</template>

<script>
import 'jquery/dist/jquery.min'
import 'popper.js/dist/popper.min'
import 'bootstrap/dist/js/bootstrap.min'
import NumbersPage from './components/NumbersPage.vue'
import FrontPage from './components/FrontPage.vue'
import store from './store'

export default {
  name: 'App',
  components: {
    NumbersPage,
    FrontPage
  },
  mounted: function () {
    if (!store.state.lang) {
      store.commit('UPDATE_LANG', (navigator.userLanguage || navigator.language) !== 'es' ? 'en' : 'es')
    }
  }
}
</script>

<style>
  @import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
  @import url('https://fonts.googleapis.com/css?family=Special+Elite|Dancing+Script|Coming+Soon|Cabin+Sketch|Londrina+Sketch');
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  .masthead {
    min-height: 100vh;
    position: relative;
    width: 100%;
    font-family: 'Cabin Sketch', cursive;
    color: #fff;
    background: #7f8485; /* Old browsers */
    background: -moz-radial-gradient(center, ellipse cover, #423e44 1%, #171519 100%); /* FF3.6+ */
    background: -webkit-gradient(radial, center center, 0px, center center, 100%, color-stop(1%, #423e44), color-stop(100%, #171519)); /* Chrome,Safari4+ */
    background: -webkit-radial-gradient(center, ellipse cover, #423e44 1%, #171519 100%); /* Chrome10+,Safari5.1+ */
    background: -o-radial-gradient(center, ellipse cover, #423e44 1%, #171519 100%); /* Opera 12+ */
    background: -ms-radial-gradient(center, ellipse cover, #423e44 1%, #171519 100%); /* IE10+ */
    background: radial-gradient(ellipse at center, #423e44 1%, #171519 100%); /* W3C */
    border: 8px solid #966F33;
    border-top-color: #896431;
    border-bottom-color: #896431;
  }

  /*Disable input control in FF*/
  input[type=number]::-webkit-outer-spin-button,
  input[type=number]::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  input[type=number] {
    -moz-appearance:textfield;
  }
</style>
