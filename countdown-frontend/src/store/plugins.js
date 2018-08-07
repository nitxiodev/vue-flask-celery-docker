import {STORAGE_KEY} from './state'
const sessionStoragePlugin = store => {
  store.subscribe((mutation, state) => {
    if (mutation.type === 'UPDATE_LANG') {
      const nonsyncedData = {lang: state.lang}
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(nonsyncedData))

      if (mutation.type === 'CLEAR_ALL_DATA') {
        sessionStorage.removeItem(STORAGE_KEY)
      }
    }
  })
}
const memoryStoragePlugin = store => {
  store.subscribe((mutation, state) => {
    console.log('MUTATION ', mutation, state)
  })
}

export default [memoryStoragePlugin, sessionStoragePlugin]
