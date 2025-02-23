import { createStore } from "vuex";

export default createStore({
  state: {
    users: [],
    courses: [],
    messages: [],
    assessments: [],
    currentUser: null,
    isLoggedIn: false,
  },
  actions: {
    checkAuthState({ commit }) {
      return new Promise((resolve) => {
        const token = localStorage.getItem("token");
        commit("setLoginState", !!token);
        resolve();
      });
    },
    logout({ commit }) {
      localStorage.removeItem('token');
      localStorage.removeItem('email');
      commit('setUser', null);
      commit('setIsLoggedIn', false);
      commit('setToken', null);
    }
  },
  mutations: {
    login(state, user) {
      state.currentUser = user;
    },
    logout(state) {
      state.currentUser = null;
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
    setLoginState(state, value) {
      state.isLoggedIn = value;
    },
  },
});
