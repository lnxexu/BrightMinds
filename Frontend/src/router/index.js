import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import CourseList from "@/components/CourseList.vue";
import CourseDetails from "@/components/CourseDetails.vue";
import QuizCreator from "@/components/QuizCreator.vue";
import ParentDashboard from "@/components/ParentDashboard.vue";
import LoginForm from "@/components/LoginForm.vue";
import RegisterForm from "@/components/RegisterForm.vue";
import ProfileView from '@/components/ProfileView.vue';
import SettingsView from '@/components/SettingsView.vue';
import ChatView from '@/components/Messaging.vue';
import MessagingComponent from '@/components/MessagingComponent.vue';
import store from '@/store';


const routes = [
  { 
    path: "/", 
    name: 'Home',
    component: Home 
  },
  { 
    path: "/courses", 
    component: CourseList,
    meta: { requiresAuth: true }
  },
  { 
    path: "/courses/:course_id", 
    name: 'CourseDetails',
    component: CourseDetails,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/chat/:teacherId?',
    name: 'chat',
    component: ChatView,
    meta: { requiresAuth: true } 
  },
  {
    path: '/messages/:recipientId',
    name: 'messages',
    component: MessagingComponent,
    props: true,
    meta: { requiresAuth: true }
  },
  { 
    path: "/messages", 
    component: MessagingComponent,
    meta: { requiresAuth: true }
  },
  { 
    path: "/quiz-creator", 
    component: QuizCreator,
    meta: { requiresAuth: true }
  },
  { 
    path: "/parent", 
    component: ParentDashboard,
    meta: { requiresAuth: true }
  },
  { 
    path: "/login", 
    component: LoginForm,
    meta: { requiresGuest: true }
  },
  { 
    path: "/register", 
    component: RegisterForm,
    meta: { requiresGuest: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsView,
    meta: { requiresAuth: true }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard
router.beforeEach((to, from, next) => {
  const isLoggedIn = store.state.isLoggedIn;

  // Handle auth required routes
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      next('/login');
      return;
    }
  }

  // Handle guest-only routes (login, register)
  if (to.matched.some(record => record.meta.requiresGuest)) {
    if (isLoggedIn) {
      // Don't redirect if already going to courses
      if (to.path !== '/courses') {
        next('/courses');
        return;
      }
    }
  }

  next();
});

// After navigation is complete
router.afterEach(() => {
  // Let toasts handle their own cleanup via their built-in timer
  // No manual cleanup needed
});

export default router;