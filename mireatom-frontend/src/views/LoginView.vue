<template>
  <div class="login-view">
    <div class="login-view__form-container">
      <div class="login-view__headline">
        <h1 class="login-view__title">Вход или регистрация</h1>
        <p class="login-view__subtitle">Введите ваши данные</p>
      </div>

      <form class="login-view__form" @submit.prevent="handleSubmit">
        <label for="username" class="login-view__label">Имя пользователя</label>
        <input 
          type="text" 
          id="username" 
          placeholder="Ваш логин" 
          v-model="username" 
          class="login-view__input"
          :class="{ 'login-view__input--error': error }" 
        />

        <label for="password" class="login-view__label">Пароль</label>
        <input 
          type="password" 
          id="password" 
          placeholder="Ваш пароль" 
          v-model="password" 
          class="login-view__input"
          :class="{ 'login-view__input--error': error }" 
        />

        <p :class="{ 'login-view__error': true, 'login-view__error--hidden': !error }">{{ error }}</p>

        <button 
          type="submit" 
          class="login-view__button"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Загрузка...' : 'Продолжить' }}
        </button>
      </form>
    </div>
    <div class="login-view__image-container">
      <img src="@/assets/images/login.webp" alt="Decorative Image" class="login-view__image" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import { apiFetch } from '@/utils/apiClient';

const router = useRouter();
const route = useRoute();

const userStore = useUserStore();

const username = ref('');
const password = ref('');
const error = ref('');
const isLoading = ref(false);

async function handleSubmit() {
  if (!username.value || !password.value) {
    error.value = 'Пожалуйста, заполните все поля';
    return;
  }

  error.value = '';
  isLoading.value = true;

  try {
    const response = await apiFetch('auth/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    }, false);

    userStore.setToken(response.token);
    userStore.setUsername(username.value);
    
    router.push({ path: '/formula-input', query: { formula: route.query.formula } }); // Перенаправление на страницу с формулами с параметром username
  } catch (e: any) {
    if (e.message.includes('401')) {
      error.value = 'Неверный логин или пароль';
    } else {
      error.value = 'Произошла ошибка при входе';
    }
  } finally {
    isLoading.value = false;
  }
}
</script>

<style lang="scss" scoped>
.login-view {
  display: flex;
  height: 100vh;
  position: relative;

  &__form-container {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 40%;
    background-color: #fff;
    border-top-right-radius: 20px;
    border-bottom-right-radius: 20px;
    z-index: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    box-shadow: 2px 0 20px rgba(0, 0, 0, 0.2);
    padding-left: 8vw;
    padding-top: 7rem;
  }

  &__headline {
    margin-bottom: 5rem;
  }
  &__title {
    font-size: 2rem;
    font-weight: 600;
    margin: 0;
  }

  &__subtitle {
    font-size: 1.5rem;
    color: #D7D7D7;
    margin: 0;
  }

  &__label {
    margin-bottom: 0.5rem;
    font-weight: bold;
    display: block;
    margin-top: 1rem;
  }

  &__form {
    max-width: 20rem;
  }

  &__input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }

  &__input--error {
    border-color: #ff4444;
  }

  &__error {
    color: #ff4444;
    font-size: 0.9rem;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;

    &--hidden {
      visibility: hidden;
    }
  }

  &__button {
    margin-top: 1.5rem;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.4rem;
    cursor: pointer;
    min-width: 150px;
    background-color: #b2ff59;
    font-size: 0.9rem;
    font-weight: 600;

    &:disabled {
      opacity: 0.7;
      cursor: not-allowed;
    }
  }

  &__image-container {
    flex: 1;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    overflow: hidden;
  }

  &__image {
    height: 100%;
    object-fit: cover;
  }
}
</style>