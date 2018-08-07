<template>
  <div class="numbers">
    <div class="masthead">
      <div class="container-fluid h-100 mbcustom">
        <div class="row align-items-center mb-5 text-center">
          <div class="col-sm-6">
            <a href="/" id="home"><h1>Numbers <span class="solver">solver</span></h1></a>
          </div>
          <div class="col-sm-6">
            <div class="main-buttons mt-2">
              <button class="btn ml-1 custom-padding" @click="random()"
                      :title="$t('numberspage.controls.random', language)"><i class="fa fa-random"></i></button>
              <button class="btn ml-1 custom-padding" @click="clear_all()"
                      :title="$t('numberspage.controls.clear', language)"><i class="fa fa-trash-alt"></i></button>
              <button type="submit" form="solver_numbers" class="btn ml-1 custom-padding"
                      :title="$t('numberspage.controls.send', language)"
                      :disabled="!disable_send || !api_response.allow_send">
                <i class="fa fa-upload" v-show="api_response.allow_send"></i>
                <i class="fa fa-spinner fa-spin" v-show="!api_response.allow_send"></i>
              </button>
            </div>
          </div>
          <div class="col-sm-12">
            <hr class="myheader mb-0">
          </div>
        </div>

        <div class="row justify-content-center mb-5">
          <div class="col-sm-5">
            <div class="alert custom-alert" role="alert">
              <h5 class="text-center">{{ $t('numberspage.rules.h5', language) }}</h5>
              {{ $t('numberspage.rules.numbers', language) }}: {{numbers}}.
              <br>
              {{ $t('numberspage.rules.target', language) }}: [100, 999].
            </div>
          </div>
        </div>

        <div class="row">
          <div class="container">
            <div class="row">
              <div class="col-md-12">
                <form id="solver_numbers" class="form-row justify-content-center" @submit.prevent="submitForm">
                  <div class="col-sm-2 mb-3" v-for="n in 6" :key="n">
                    <input v-focus class="form-control custom-input" placeholder="1" type="number"
                           @keydown.enter.prevent=""
                           v-validate="'required|integer|included:1,2,3,4,5,6,7,8,9,10,25,50,75,100'" :name="n"
                           v-model.number="inputs.numbers[n-1]" :class="{'text-danger': errors.has(n.toString()) }">
                    <span v-show="errors.has(n.toString())"
                          class="help text-danger">{{ errors.first(n.toString()) }}</span>
                  </div>
                  <div class="col-sm-4 mb-3">
                    <input class="form-control custom-input" placeholder="100"
                           v-validate="'required|integer|min_value:100|max_value:999'" name="target"
                           v-model.number="inputs.target" type="number" @keydown.enter.prevent="">
                    <span v-show="errors.has('target')" class="help text-danger">{{ errors.first('target') }}</span>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>

        <modal class="modal" v-show="api_response.has_errors">
          <template slot="header">
            <h5 class="modal-title">{{ $t('numberspage.network_error.title', language) }}</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"
                    @click="api_response.has_errors = !api_response.has_errors">
              <span aria-hidden="true" class="modal-button">&times;</span>
            </button>
          </template>

          <template slot="body">
            {{ $t('numberspage.network_error.body', language) }} <i class="em em-disappointed"></i>
          </template>
        </modal>

        <div class="row mt-2 mb-5" v-if="this.numbers_solution.solution.length > 0">
          <div class="container">
            <div class="row align-items-center">
              <div class="col-sm-12"
                   v-scroll-reveal="{ duration: 1500, origin: 'bottom', distance:'100%', opacity: 0.3, scale: 1, mobile: false }">
                <div class="card">
                  <div class="card-header">
                    <span class="solution2">{{ $t('numberspage.solution.title', language) }}</span>
                    <div class="float-right">
                      <i class="fa fa-clock" :title="$t('numberspage.solution.time', language)">
                        {{numbers_solution.exec_time|two_decimals}}(s)</i>
                      <i class="fa fa-code ml-2" :title="$t('numberspage.solution.calls', language)">
                        {{numbers_solution.recursions}}</i>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-sm-12">
                <ul class="list-group">
                  <li class="list-group-item d-flex flex-row-reverse justify-content-between align-items-center"
                      v-for="(item, index) in numbers_solution.solution" :key="`item-${index}`"
                      v-scroll-reveal="{ duration: 1500 + (index * 200), delay: index+1, origin: 'left', distance:'100%', opacity: 1, scale: 1, mobile: false }">
                    {{item[0]}} {{item[1]}} {{item[2]}} = {{item[3]}}
                    <span class="badge badge-light badge-pill">{{index+1}}</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Modal from '@/components/Modal.vue'
import store from '../store'
export default {
  components: {
    Modal
  },
  directives: {
    focus: {
      inserted: function (el) {
        if (el.name === '1') { // Only on first input
          el.focus()
        }
      }
    }
  },
  mounted: function () {
    this.$validator.localize(store.state.lang)
  },
  data: function () {
    return {
      inputs: {
        numbers: ['', '', '', '', '', ''],
        target: ''
      },
      api_response: {
        has_errors: false,
        response: null,
        allow_send: true
      },
      manual_response: null,
      me: store.state.me,
      language: store.state.lang,
      numbers: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 25, 50, 75, 100],
      numbers_solution: {
        exec_time: 0,
        recursions: 0,
        solution: []
      }
    }
  },
  filters: {
    two_decimals: function (value) {
      return Number(value).toFixed(2)
    }
  },
  methods: {
    isNumber: function (value) {
      return Number.isInteger(value) && value > 0
    },
    clear_all: function () {
      this.clear_only_inputs()
      this.clear_only_solution()
      this.$validator.reset()
    },
    clear_only_inputs: function () {
      this.inputs = {
        numbers: ['', '', '', '', '', ''],
        target: ''
      }
    },
    clear_only_solution: function () {
      this.numbers_solution = {
        exec_time: 0,
        recursions: 0,
        solution: []
      }
    },
    random: function () {
      this.clear_all()
      for (let i = 0; i < 6; i++) {
        this.inputs.numbers[i] = (this.numbers[Math.floor(Math.random() * this.numbers.length)])
      }
      this.inputs.target = Math.floor(Math.random() * (999 - 100 + 1)) + 100
    },
    submitForm: function (e) {
      this.$validator.validateAll().then(response => {
        if (response && this.api_response.allow_send) {
          this.clear_only_solution()
          let data = {
            numbers: this.inputs.numbers,
            target: this.inputs.target,
            id: this.me
          }
          this.$http.post('/numbers_async', data).then((response) => {
            this.api_response.response = response.data
            this.api_response.allow_send = false
            if (this.numbers_solution.solution.length === 0 && !this.me) {
              this.manual_fetching_data() // only call if we don't have one solution yet
            }
          }).catch((error) => {
            console.log(error)
            this.api_response.has_errors = true
          })
        }
      })
    },
    manual_fetching_data: function () {
      this.manual_response = setTimeout(() => {
        this.$http.get('/progress/' + this.api_response.response).then((response) => {
          let data = response.data
          if (data.status === 'SUCCESS') {
            this.numbers_solution = data.msg
            this.api_response.allow_send = true
          }
        }).catch((error) => {
          console.log(error)
          this.api_response.allow_send = true
          this.api_response.has_errors = true
        })
      }, 5000)
    }
  },
  beforeDestroy: function () {
    clearTimeout(this.manual_response)
  },
  computed: {
    disable_send: function () {
      return this.inputs.numbers.every(this.isNumber) && this.isNumber(this.inputs.target) &&
        this.$validator.errors.count() === 0
    }
  },
  created: function () {
    this.$options.sockets.connect = () => {
      this.$socket.emit('my_id')
    }
    this.$options.sockets.disconnect = () => {
      store.commit('CLEAR_ALL_DATA')
      this.me = store.state.me
    }
    this.$options.sockets.connected = (e) => {
      store.commit('UPDATE_ME', e)
      this.me = store.state.me
    }
    this.$options.sockets.solution = (sol) => {
      this.numbers_solution = sol
      this.api_response.allow_send = true
      clearTimeout(this.manual_response)
    }
  }
}
</script>

<style scoped>
  #solver_numbers span {
    font-weight: bold;
  }

  .modal-button {
    color: white;
  }

  button.close:focus {
    border-color: white;
    outline: none;
  }

  .help {
    font-size: 1.2rem;
  }

  input[type=number]::-webkit-inner-spin-button,
  input[type=number]::-webkit-outer-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  .decorated {
    text-decoration: underline;
  }

  .navbar {
    min-height: 5rem;
  }

  .custom-input {
    font-family: 'Coming Soon', cursive;
    text-align: center;
    background: transparent;
    border: none;
    border-bottom: 1px solid gainsboro;
    border-radius: 0;
    font-size: 50px;
    color: white;
  }

  input:focus {
    outline: none !important;
    box-shadow: none;
    border-bottom-color: #00cd3e;
    /*box-shadow: 0 0 10px #cccace;*/
  }

  .custom-alert {
    background: inherit;
    border: thin solid gainsboro;
    -webkit-border-radius:;
    -moz-border-radius:;
    border-radius: 0;
  }

  .custom-padding {
    padding: .5rem 2rem;
  }

  h5.text-center {
    text-decoration: white underline solid;
  }

  .main-buttons > button {
    /*border: 1px solid gainsboro;*/
    /*cursor: pointer;*/
    background: inherit;
    border-radius: 0;
    border-color: #e8e8e8;
    color: white;
  }

  .main-buttons > button:hover:enabled {
    background-color: white;
    color: #171519;
  }

  .main-buttons > button:focus {
    box-shadow: 0 3px 4px 0 rgba(0, 0, 0, .14), 0 3px 3px -2px rgba(0, 0, 0, .2), 0 1px 8px 0 rgba(0, 0, 0, .12);
  }

  .solver {
    color: red;
    font-family: 'Dancing Script', cursive;
    font-size: 25px;
  }

  @media (min-width: 768px) {
    .solver {
      display: block;
      line-height: 1px;
      margin-left: 103px;
    }
  }

  .myheader {
    border: thin solid gainsboro;
  }

  li {
    background: inherit;
    border: none;
    border-bottom: thin solid gainsboro;
    font-family: 'Coming Soon', cursive;
    font-weight: bold;
    font-size: 18px;
    -webkit-border-radius:;
    -moz-border-radius:;
    border-radius: 0 !important;
  }

  .solution2 {
    font-family: Coming Soon, cursive;
    font-weight: bold;
    text-decoration: underline white;
  }

  .card {
    background: inherit;
  }

  .card-header {
    border-bottom-color: white;
    background-color: rgba(0, 0, 0, .5);
    -webkit-border-radius:;
    -moz-border-radius:;
    border-radius: 0;
  }

  #home {
    color: white;
  }

  #home:hover {
    text-decoration: none;
  }
</style>
