<template>
  <header class="header">
    <div class="header__logo-container" @click="router.push('/')">
      <img src="@/assets/logo.jpg" alt="The Company" class="header__logo" />
      Формул/А\том
    </div>

    <div class="header__auth-buttons" v-if="!username">
      <button class="header__button header__button--secondary" @click="$router.push('/login')">Войти</button>
      <button class="header__button header__button--primary" @click="$router.push('/login')">Присоединиться</button>
    </div>
    <div class="header__auth-profile" v-else>
      <p>С возвращением, <b>{{ username }}</b>!</p>

      <DropdownMenu title="Меню" :isOpen="isDropdownOpen" @toggle="isDropdownOpen = !isDropdownOpen" @logout="logout">
        <template #menu-items>
          <button class="header__button dropdown__item header__button--primary"
            @click="openFormulaList">Мои формулы</button>

          <button class="header__button dropdown__item dropdown__item--button header__button--danger"
            @click="logout">
            Выйти
          </button>
        </template>
      </DropdownMenu>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/userStore';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import DropdownMenu from '@/components/DropdownMenu.vue';

const router = useRouter();
const userStore = useUserStore();

const { username } = storeToRefs(userStore);
const isDropdownOpen = ref(false);

const emit = defineEmits(['openFormulaList']);

function logout() {
  userStore.clearUser();
  isDropdownOpen.value = false;
  router.push('/');
}

function openFormulaList() {
  emit('openFormulaList');
}
</script>

<style lang="scss" scoped>
.header {
  display: flex;
  justify-content: space-between;
  padding: 1rem 8vw;
  background-color: #FFFFFF;

  &__logo-container {
    display: flex;
    align-items: center;
    gap: 1rem;

    font-size: 1.25rem;
    font-weight: 700;
    cursor: pointer;
  }

  &__logo {
    height: 40px;
  }

  &__auth-buttons {
    display: flex;
    gap: 1rem;
  }

  &__button {
    padding: 0.5rem 1rem;
    border: 2px solid #000;
    border-radius: 0.4rem;
    cursor: pointer;
    min-width: 150px;
    background-color: transparent;

    font-size: 0.9rem;
    font-weight: 600;

    &--secondary {
      background-color: transparent;
    }

    &--primary {
      border: none;
      background-color: #b2ff59;
    }

    &--danger {
      border: none;
      font-weight: 500;
      background-color: #ff4444;
      color: #fff;
    }
  }

  &__auth-profile {
    position: relative;
    display: flex;
    align-items: center;
    gap: 2rem;
  }
}
</style>