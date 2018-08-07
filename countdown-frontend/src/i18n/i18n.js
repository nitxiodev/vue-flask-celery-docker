import Vue from 'vue'
import VueI18n from 'vue-i18n'

Vue.use(VueI18n)

const messages = {
  'es': {
    frontpage: {
      h1: 'Cifras y Letras',
      numbers: 'Cifras',
      letters: 'Letras',
      soon: 'Prox',
      footer: 'Hecho con <i class="fas fa-heart love"></i> usando <a href="https://vuejs.org/" target="_blank">' +
      '<i class="fab fa-vuejs"></i></a> & <a href="https://www.python.org/" target="_blank">' +
      '<i class="fab fa-python"></i></a>',
      lang_title: 'Cambia al inglés'
    },
    numberspage: {
      controls: {
        random: 'Genera números aleatoriamente',
        clear: 'Reinicia la entrada de datos',
        send: 'Resolver'
      },
      rules: {
        h5: 'Reglas del juego',
        numbers: 'Números permitidos',
        target: 'Números objetivo permitidos'
      },
      network_error: {
        title: 'Error de red',
        body: 'Parece que el servidor no está respondiendo.'
      },
      solution: {
        title: 'Solución',
        time: 'Tiempo de ejecución',
        calls: 'Número de llamadas a la subrutina'
      }
    }
  },
  'en': {
    frontpage: {
      h1: 'Letters & Numbers',
      numbers: 'Numbers',
      letters: 'Letters',
      soon: 'Soon',
      footer: 'Made with <i class="fas fa-heart love"></i> using <a href="https://vuejs.org/" target="_blank">' +
      '<i class="fab fa-vuejs"></i></a> & <a href="https://www.python.org/" target="_blank">' +
      '<i class="fab fa-python"></i></a>',
      lang_title: 'Switch to Spanish'
    },
    numberspage: {
      controls: {
        random: 'Random numbers',
        clear: 'Clear inputs',
        send: 'Send to server'
      },
      rules: {
        h5: 'Game rules',
        numbers: 'Allowed numbers',
        target: 'Allowed targets'
      },
      network_error: {
        title: 'Network Error',
        body: 'Seems like remote API server is not responding.'
      },
      solution: {
        title: 'Solution',
        time: 'Execution time',
        calls: 'Number of calls to the subroutine'
      }
    }
  }
}

const i18n = new VueI18n({
  locale: 'en',
  messages
})

export default i18n
