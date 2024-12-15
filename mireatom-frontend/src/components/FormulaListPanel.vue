<template>
  <div class="formula-list">
    <div class="formula-list__overlay" @click="$emit('close')"></div>
    <div class="formula-list-panel">
      <div class="formula-list-panel__content">
        <div class="formula-list-panel__header">
          <button class="formula-list-panel__back-button" @click="$emit('close')">
            <svg width="36" height="20" viewBox="0 0 36 20" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M34 12H4M4 12L10 6M4 12L10 18" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"
                stroke-linejoin="round" />
            </svg>
            <span>Вернуться</span>
          </button>
          <h2 class="formula-list-panel__title">Ваши формулы</h2>
        </div>
        <ul class="formula-list-panel__list" v-if="formulas.length">
          <li v-for="formula in formulas" :key="formula.value" class="formula-list-panel__item">
            <div class="formula-item">
              <span class="formula-item__value" v-html="katex.renderToString(formula.value, {
                throwOnError: false,
                output: 'mathml'
              }).replace(/\\displaylines/g, ' ')">
              </span>
              <span class="formula-item__name">{{ formula.name ?? "Без имени" }}</span>
              <div class="formula-item__actions">
                <button class="formula-item__copy" @click="copyToClipboard(formula.value)">
                  <img v-if="copiedFormulaId !== formula.value" src="@/assets/icons/paste.svg" alt="paste" width="24" height="24">
                  <img v-else src="@/assets/icons/check.svg" alt="copied" width="24" height="24">
                </button>
              </div>
            </div>
          </li>
        </ul>
        <div class="formula-list-panel__list--empty" v-else>
          <p>У вас нет формул</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { apiFetch } from '../utils/apiClient';
import katex from 'katex';
import { eventBus } from '../utils/eventBus';

interface Variable {
  value: string;
  name: string;
}

interface Formula {
  value: string;
  name: string;
  variables: Variable[];
}

const formulas = ref<Formula[]>([]);
const copiedFormulaId = ref<string | null>(null);

const copyToClipboard = async (text: string) => {
  await window.navigator.clipboard.writeText(text);
  copiedFormulaId.value = text;
  setTimeout(() => {
    copiedFormulaId.value = null;
  }, 1000);
};

async function fetchFormulas() {
  try {
    const response = await apiFetch('library/user/formulas?limit=100&page=1');
    formulas.value = response.formulas;
  } catch (error) {
    console.error('Error fetching formulas:', error);
  }
}

onMounted(() => {
  fetchFormulas();
  eventBus.on('formulas-update', fetchFormulas);
});

onUnmounted(() => {
  eventBus.off('formulas-update', fetchFormulas);
});
</script>

<style lang="scss" scoped>
.formula-list {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 3000;

  &__overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(.3rem);
    z-index: 3000;
    cursor: pointer;
  }
}

.formula-list-panel {
  position: fixed;
  top: 0;
  right: 0;
  width: 50vw;
  height: 100vh;
  border-radius: .7rem 0 0 .7rem;
  background-color: #fff;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  z-index: 9999999;
  display: flex;
  flex-direction: column;
  transform: translateX(0);
  transition: transform 0.3s ease-in-out;

  &__content {
    display: flex;
    flex-direction: column;
    flex-grow: 1;

    overflow-y: auto;
  }

  &__header {
    display: flex;
    flex-direction: column;
    align-items: left;
    gap: 3rem;
    justify-content: space-between;
  }

  &__back-button {
    display: flex;
    align-items: normal;
    gap: 1rem;
    padding: 0;

    font-weight: 500;
    font-size: 1.2rem;
    background: none;
    border: none;
    color: #E6E6E6;
    cursor: pointer;

    &>span {
      margin-top: 3rem;
    }

    &>svg {
      margin-left: 2rem;
      margin-top: 3rem;
    }
  }

  &__title {
    font-size: 2rem;
    color: #000;

    margin-left: 5.2rem;
    margin-bottom: 0.8rem;
  }

  &__list {
    list-style: none;
    padding: 0;
    margin-left: 5.2rem;
    margin-right: 2rem;

    &--empty  {
      margin-left: 5.2rem;
      font-size: 1.2rem;
      color: #E6E6E6;
    }
  }

  &__item {
    padding: 0.3rem 0;
  }

  &__variables {
    list-style: none;
    padding: 0;
    margin-top: 0.5rem;
  }

  &__variable {
    font-size: 0.9rem;
    color: #666;
  }
}

.formula-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: .7rem;
  border: 1px solid #E6E6E6;
  border-radius: 0.5rem;
  background-color: #fff;

  &__value {
    max-width: 9rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex-grow: 1;
  }

  &__name {
    font-size: 1rem;
    max-width: 15rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex-grow: 1;
  }

  &__actions {
    display: flex;
    align-items: center;
    gap: .5rem;
    justify-content: flex-end;
    flex-direction: row;
  }

  &__copy {
    background-color: #b2ff59;
    border: none;
    border-radius: 0.3rem;
    padding: 0.5rem 0.5rem 0.2rem 0.5rem;
    cursor: pointer;


  }

  &__menu {
    background: none;
    border: none;
    cursor: pointer;
  }
}
</style>