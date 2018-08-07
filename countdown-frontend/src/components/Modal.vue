<template>
  <transition name="fade">
    <div class="modal modal-mask">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
              <slot name="header"></slot>
          </div>

          <div class="modal-body">
            <slot name="body"></slot>
          </div>

          <div class="modal-footer">
            <slot name="footer"></slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<style scoped>
  .modal-header > .row {
    padding-bottom: 25px;
  }
  .modal-header {
    border-bottom: thin solid #949ba2;
  }
  .modal-footer {
    border-top: thin solid #949ba2;
  }
  .modal-content {
    background-color: #2d3038;
  }
  .modal-title {
    color: orange;
  }
  .modal-mask {
    z-index: 9999;
    background-color: rgba(0, 0, 0, .5);
    display: block;
    transition: opacity .3s ease;
  }
  .fade-enter-active, .fade-leave-active {
    transition: opacity .3s ease;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
  }
</style>
