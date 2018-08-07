<template>
  <div class="principal">
    <!-- Header -->
    <header class="masthead" :class="{'masthead2': !isMobile}">
      <div class="container text-center h-100" :class="{'mt-3': isMobile}">
        <div class="row h-100 align-items-center">
          <div class="col-sm-12 my-auto">
            <h1>{{ $t('frontpage.h1', language) }}</h1>
            <hr class="mb-5">
            <div class="row">
              <div class="col-md-6 mb-3">
                <router-link to="/numbers_solver" title="Numbers" class="btn btn-outline-light style-button w-100">
                  {{ $t('frontpage.numbers', language) }}
                </router-link>
              </div>
              <div class="col-md-6">
                <a href="#" class="btn btn-outline-light style-button w-100 disabled">
                  {{ $t('frontpage.letters', language) }}
                  <div class="ribbon"><span>{{ $t('frontpage.soon', language) }}</span></div>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      <footer class="footer w-100 mt-5">
        <div class="container">
          <div class="row">
            <div class="col-sm-12 text-center credits">
              <span v-html="$t('frontpage.footer', language)"> </span>
            </div>
          </div>
        </div>
      </footer>
      <div class="language" @click="changelanguage(language === 'en' ? 'es' : 'en')">
        <span :title="$t('frontpage.lang_title', language)" class="flag-icon"
              :class="{'flag-icon-gb': language === 'en', 'flag-icon-es': language === 'es'}"></span>
      </div>
    </header>
  </div>
</template>

<script>
import store from '../store'
export default {
  data: function () {
    return {
      isMobile: /Mobile/.test(navigator.userAgent)
    }
  },
  methods: {
    changelanguage: function (lang) {
      store.commit('UPDATE_LANG', lang)
    }
  },
  computed: {
    language: function () {
      return store.state.lang
    }
  }
}
</script>

<style scoped>
  .language {
    position: absolute;
    top: 20px;
    right: 25px;
  }

  .language span {
    font-size: 1.2rem;
    background-position: center;
    padding: 0.2em 0.5em;
    cursor: pointer;
  }

  .credits >>> a {
    color: inherit;
  }

  @media (min-height: 600px) {
    .footer {
      position: absolute;
    }
  }

  .footer {
    border-top: thin solid gainsboro;
    /*position: absolute;*/
    bottom: 0;
    line-height: 45px;
    background-color: rgba(0, 0, 0, .4);
  }

  .credits >>> .love {
    animation: beat .55s infinite alternate;
    transform-origin: center;
  }

  @keyframes beat {
    to {
      transform: scale(1.1);
    }
  }

  hr {
    border: 2px solid white;
  }

  @media (min-width: 768px) {
    h1 {
      font-size: 8rem;
    }
  }

  @media (max-width: 768px) {
    h1 {
      font-size: 4.5rem;
    }
  }

  .style-button {
    padding: 15px 45px;
    -webkit-border-radius:;
    -moz-border-radius:;
    border-radius: 0;
    font-size: 25px;
  }

  .masthead2 {
    height: 100vh;
  }

  .btn {
    font-weight: bold;
  }

  .btn:hover {
    color: #46474a;
  }

  .ribbon {
    position: absolute;
    right: 6px;
    top: -5px;
    z-index: 1;
    overflow: hidden;
    width: 75px;
    height: 75px;
    text-align: right;
  }

  .ribbon span {
    font-size: 10px;
    font-weight: bold;
    color: #FFF;
    text-transform: uppercase;
    text-align: center;
    line-height: 20px;
    transform: rotate(45deg);
    -webkit-transform: rotate(45deg);
    width: 80px;
    display: block;
    background: #79A70A;
    background: linear-gradient(#F70505 0%, #8F0808 100%);
    box-shadow: 0 3px 10px -5px rgba(0, 0, 0, 1);
    position: absolute;
    top: 12px;
    right: -15px;
  }

  .ribbon span::before {
    content: "";
    position: absolute;
    left: 0px;
    top: 100%;
    z-index: -1;
    border-left: 3px solid #8F0808;
    border-right: 3px solid transparent;
    border-bottom: 3px solid transparent;
    border-top: 3px solid #8F0808;
  }

  .ribbon span::after {
    content: "";
    position: absolute;
    right: 0px;
    top: 100%;
    z-index: -1;
    border-left: 3px solid transparent;
    border-right: 3px solid #8F0808;
    border-bottom: 3px solid transparent;
    border-top: 3px solid #8F0808;
  }

</style>
