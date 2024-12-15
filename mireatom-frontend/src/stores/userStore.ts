import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import { eventBus } from '../utils/eventBus';

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token'));
  const username = ref<string>(localStorage.getItem('username') || '');

  function setToken(newToken: string) {
    token.value = newToken;
    localStorage.setItem('token', newToken);
  }

  function setUsername(newUsername: string) {
    username.value = newUsername;
    localStorage.setItem('username', newUsername);
  }

  function clearUser() {
    token.value = null;
    username.value = '';
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    eventBus.emit('formulas-update');
  }

  watch(token, (newToken) => {
    if (newToken) {
      localStorage.setItem('token', newToken);
    } else {
      localStorage.removeItem('token');
    }
  });

  watch(username, (newUsername) => {
    if (newUsername) {
      localStorage.setItem('username', newUsername);
    } else {
      localStorage.removeItem('username');
    }
  });

  return {
    token,
    username,
    setToken,
    setUsername,
    clearUser,
  };
});