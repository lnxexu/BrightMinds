import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from './store'
import "./assets/styles.css";
import '@fortawesome/fontawesome-free/css/all.css';
import 'vue-toastification/dist/index.css';
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

// Register the Toast plugin with its options
app.use(Toast, options)
app.use(store)
app.use(router)

// Mount the app
app.mount('#app')