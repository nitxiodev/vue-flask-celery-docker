export const UPDATE_ME = (state, me) => {
  state.me = me
}

export const UPDATE_LANG = (state, lang) => {
  state.lang = lang
}

/**
 * Clear each property, one by one, so reactivity still works.
 *
 * (ie. clear out state.auth.isLoggedIn so Navbar component automatically reacts to logged out state,
 * and the Navbar menu adjusts accordingly)
 *
 * TODO: use a common import of default state to reset these values with.
 */
export const CLEAR_ALL_DATA = (state) => {
  state.me = null
}
