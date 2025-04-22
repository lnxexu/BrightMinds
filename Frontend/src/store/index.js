import { createStore } from 'vuex';

export default createStore({
    state: {
      user: null,
      isLoggedIn: false,
      userRole: null // Add userRole to store
    },
    mutations: {
      setUser(state, user) {
        state.user = user;
      },
      setLoggedIn(state, value) {
        state.isLoggedIn = value;
      },
      setUserRole(state, role) { // Add mutation for role
        state.userRole = role;
      },
      clearUser(state) {
        state.user = null;
        state.isLoggedIn = false;
        state.userRole = null;
      }
    }
  })