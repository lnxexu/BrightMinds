import { createStore } from "vuex";

export default createStore({
  state: {
    users: [],
    courses: [],
    messages: [],
    assessments: [],
    currentUser: null,
    isLoggedIn: false,
    error: null,
  },
  actions: {
    checkAuthState({ commit }) {
      return new Promise((resolve) => {
        const token = localStorage.getItem("token");
        commit("setLoggedIn", !!token);
        resolve();
      });
    },
    logout({ commit }) {
      // Clear all stored data and reset state synchronously
      localStorage.removeItem('token');
      localStorage.removeItem('email');
      
      // Reset store state
      commit('setUser', null);
      commit('setLoggedIn', false);
      commit('resetState');
      
      // Return resolved promise immediately
      return Promise.resolve();
    }
  },
  mutations: {
    setUser(state, user) {
      if (user) {
        // Ensure first name is extracted from full name if not already set
        if (!user.firstName && user.full_name) {
          user.firstName = user.full_name.split(' ')[0];
        }
      }
      state.currentUser = user;
    },
    setLoggedIn(state, value) {
      state.isLoggedIn = value;
    },
    setError(state, error) {
      state.error = error;
    },
    addCourse(state, course) {
      state.courses.push(course);
    },
    addMessage(state, message) {
      state.messages.push(message);
    },
    addAssessment(state, assessment) {
      state.assessments.push(assessment);
    },
    resetState(state) {
      // Reset all state to initial values
      state.users = [];
      state.courses = [];
      state.messages = [];
      state.assessments = [];
      state.currentUser = null;
      state.isLoggedIn = false;
      state.error = null;
    }
  },
});
