<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HeaderComponent from './components/HeaderComponent.vue';
import FormulaListPanel from './components/FormulaListPanel.vue';
import { ref, watch } from 'vue';
import { useUserStore } from './stores/userStore';

const showFormulaListPanel = ref(false);
const userStore = useUserStore();

function openFormulaList() {
  showFormulaListPanel.value = true;
}

// Закрываем панель при выходе из системы
watch(() => userStore.username, (newUsername) => {
  if (!newUsername) {
    showFormulaListPanel.value = false;
  }
});
</script>

<template>
  <HeaderComponent v-if="$route.name !== 'login'" @openFormulaList="openFormulaList" />
  <div :class="{ 'content': $route.name !== 'login' }">
    <RouterView @openFormulaList="openFormulaList" />
  </div>
  <FormulaListPanel v-if="showFormulaListPanel" @close="showFormulaListPanel = false" />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body {
  margin: 0;
  padding: 0;
  background-color: #FCFCFC;

  font-family: 'Inter', sans-serif;
}

.content {
  flex-grow: 1;
  margin-top: 2rem;
  margin-left: 8vw;
  margin-right: 8vw;
}
</style>
