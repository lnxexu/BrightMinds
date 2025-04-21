import { createStore } from 'vuex';


export default createStore({
    state: {
      user: null,
      isLoggedIn: false
    },
    mutations: {
      setUser(state, user) {
        state.user = user;
      },
      setLoggedIn(state, value) {
        state.isLoggedIn = value;
      },
      clearUser(state) {
        state.user = null;
        state.isLoggedIn = false;
      }
    }
  })