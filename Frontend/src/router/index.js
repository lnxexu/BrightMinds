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
import Auth from "@/components/Success.vue";



const routes = [
  {
    path: "/",
    name: 'Login',
    component: LoginForm,
  },
  {
    path: "/home",
    name: 'Home',
    component: Home
  },
  {
    path: '/auth',
    name: 'Auth',
    component: Auth,
    meta: { requiresAuth: true }
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
    path: "/register",
    component: RegisterForm,
    meta: { requiresGuest: true }
  },
  {
    path: "/profile",
    name: 'Profile',
    component: ProfileView,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: "/settings",
    name: 'Settings',
    component: SettingsView,
    meta: { requiresAuth: true },
    props: true
  },
  {
    path: '/quiz/:quizId',
    name: 'QuizTaker',
    component: () => import('@/components/QuizTaker.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router;
