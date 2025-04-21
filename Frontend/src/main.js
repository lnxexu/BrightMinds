import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./assets/styles.css";
import '@fortawesome/fontawesome-free/css/all.css';
import { supabase } from "./lib/supabaseClient";
import 'vue-toastification/dist/index.css';
import store from './store' 
import Toast, { POSITION } from "vue-toastification";

const app = createApp(App)

const options = {
    position: POSITION.TOP_RIGHT,
    timeout: 5000,
    closeOnClick: true,
    pauseOnFocusLoss: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: true,
    closeButton: false, // Changed from "button" to false
    icon: true,
    rtl: false,
    toastClassName: "custom-toast", // Optional: Add custom class for styling
    filterBeforeCreate: (toast) => {
        if (toast.type === 'error') {
            toast.timeout = 8000; // Longer timeout for errors
        }
        return toast;
    }
}

const initAuth = async () => {
    const { data } = await supabase.auth.getSession()
    if (data.session) {
      // User is logged in
      store.commit('setUser', data.session.user)
      store.commit('setLoggedIn', true)
    }
  }
  
  initAuth()

// Register the Toast plugin with its options
app.use(Toast, options)
app.use(router)
app.use(store) // Use Vuex store

// Mount the app
app.mount('#app')