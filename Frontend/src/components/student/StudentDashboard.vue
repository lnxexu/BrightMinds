<template>
    <div class="student-dashboard">
      <StudentNavBar />
      <div class="dashboard-content">
        <router-view />
      </div>
    </div>
  </template>
  
  <script setup>
  import StudentNavBar from './StudentNavBar.vue';
  </script>
  
  <style scoped>
  .student-dashboard {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }
  
  .dashboard-content {
    flex: 1;
    padding: 2rem;
    background-color: #f9fafb;
  }
  </style>