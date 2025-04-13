import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import CourseList from "@/components/CourseList.vue";
import CourseDetails from "@/components/CourseDetails.vue";
import MessagingComponent from "@/components/MessagingComponent.vue";
import QuizCreator from "@/components/QuizCreator.vue";
import ParentDashboard from "@/components/ParentDashboard.vue";
import LoginForm from "@/components/LoginForm.vue";
import RegisterForm from "@/components/RegisterForm.vue";
import ProfileView from '@/components/ProfileView.vue';
import SettingsView from '@/components/SettingsView.vue';
import RoleSelection from '@/components/RoleSelection.vue';
import TeacherRegisterForm from '@/components/TeacherRegisterForm.vue';
import Stream from '@/components/Stream.vue';
import store from '@/store';




const routes = [
  {
    path: "/",
    name: 'Home',
    component: Home
  },
  { path: '/role-selection', 
    name: 'RoleSelection', 
    component: RoleSelection 
  },
  { path: '/register', 
    name: 'Register', 
    component: RegisterForm,
    meta: { requiresGuest: true }
  },
  { path: '/register-teacher', 
    name: 'TeacherRegister', 
    component: TeacherRegisterForm 
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
    path: '/stream',
    name: 'Stream',
    component: Stream,
    meta: { requiresAuth: true },

  },
  { 
    path: '/chat/:recipientId?',
    name: 'chat',
    component: MessagingComponent,
    props: true,
    meta: { requiresAuth: true }
  },
  // ✅ Fullscreen messaging page
  {
    path: '/messages',
    component: MessagingComponent,
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
    path: "/profile",
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  {
    path: "/settings",
    name: 'Settings',
    component: SettingsView,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// ✅ Navigation Guard
router.beforeEach((to, from, next) => {
  const isLoggedIn = store.state.isLoggedIn

  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isLoggedIn) {
      next('/login')
      return
    }
  }

  if (to.matched.some(record => record.meta.requiresGuest)) {
    if (isLoggedIn) {
      if (to.path !== '/courses') {
        next('/courses')
        return
      }
    }
  }

  next()
})

router.afterEach(() => {
  // Optional: Handle toast clearing or analytics
})

export default router;
