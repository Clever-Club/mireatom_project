<template>
  <div class="formula-input-page">
    <main class="formula-input-page__main">
      <div class="formula-input-page__input-section">
        <h1 class="formula-input-page__input-section-title">Ввод формулы</h1>
        <p class="formula-input-page__input-section-description">Введите интересующую вас формулу</p>
        <FormulaEditor v-model="latex" />

        <div class="formula-input-page__input-section-buttons">
          <button class="formula-input-page__input-section-button" @click="saveFormula"
            :disabled="isLoading || formulaId.length > 0">
            {{ isLoading ? 'Сохранение...' : 'Сохранить' }}
          </button>

          <button class="formula-input-page__input-section-button--analysis"
            @click="$router.push({ name: 'formula-analysis', query: { formulaId: formulaId } })"
            :disabled="formulaId.length === 0">
            {{ 'Анализ' }}
          </button>
        </div>
        <p v-if="errorMessage" class="formula-input-page__input-section-error">{{ errorMessage }}</p>
      </div>
      <div class="formula-input-page__preview-section">
        <button class="formula-input-page__library-button" @click="openFormulaList">
          <img src="@/assets/icons/paste.svg" alt="library" width="24" height="24">
          <span>Мои формулы</span>
        </button>
        <div class="formula-input-page__preview-content">
          <h3>Как вводить формулы:</h3>
          <ul class="formula-input-page__instructions">
            <li><b>Нажмите на картинку клавиатуры для удобного ввода</b></li>
            <li>Вы также можете использовать коды LaTex:</li>
            <li><code>\frac{a}{b}</code> для дробей</li>
            <li>Степень записывается как <code>x^{2}</code></li>
            <li>Индекс записывается как <code>x_{i}</code></li>
            <li>Греческие буквы: <code>\alpha</code>, <code>\beta</code>, <code>\pi</code></li>
            <li>Корень: <code>\sqrt{x}</code></li>
          </ul>
          <div class="formula-input-page__example">
            <p>Пример, уже есть в базе данных:</p>
            <p class="formula-input-page__formula">
              v=\frac{s}{t}
            </p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import FormulaEditor from '../components/FormulaEditor.vue';
import { useRoute } from 'vue-router';
import { apiFetch } from '../utils/apiClient';
import { eventBus } from '../utils/eventBus';

const route = useRoute();

const formulaId = ref('');

const latex = ref(route.query.formula as string || '');
const isLoading = ref(false);
const errorMessage = ref('');

const emit = defineEmits(['openFormulaList']);

function openFormulaList() {
  emit('openFormulaList');
}

async function saveFormula() {
  if (latex.value.trim().length == 0) { return; }

  isLoading.value = true;
  errorMessage.value = '';
  try {
    const response = await apiFetch('library/formula', {
      method: 'POST',
      body: JSON.stringify({ formula: { value: latex.value } }),
      headers: {
        'Content-Type': 'application/json',
      },
    });

    formulaId.value = response.id;
    eventBus.emit('formulas-update');

    console.log('Formula saved:', response);
  } catch (error) {
    console.error('Error saving formula:', error);
    errorMessage.value = 'Произошла ошибка при сохранении формулы. Пожалуйста, попробуйте еще раз.';
  } finally {
    isLoading.value = false;
  }
}
</script>

<style lang="scss" scoped>
.formula-input-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  box-sizing: border-box;

  &__main {
    display: flex;
    justify-content: space-between;
    width: 100%;
    max-width: 1200px;
    flex-grow: 1;
  }

  &__input-section {
    flex: 1;
    margin-right: 2rem;

    &-title {
      font-size: 1.5rem;
      color: #000;
    }

    &-description {
      color: #aaa;
    }

    &-buttons {
      display: flex;
      gap: 1rem;
    }

    &-button {
      margin-top: 1rem;
      padding: 0.5rem 1rem;
      background-color: #b2ff59;
      border: none;
      cursor: pointer;
      border-radius: 0.4rem;
      min-width: 150px;
      font-size: 0.9rem;
      font-weight: 300;

      &--analysis {
        margin-top: 1rem;
        border: 2px solid #000;
        border-radius: 0.4rem;
        cursor: pointer;
        min-width: 150px;
        background-color: transparent;

        font-size: 0.9rem;
        font-weight: 600;
      }
    }

    &-error {
      color: #ff4444;
      margin-top: 0.5rem;
    }
  }

  &__preview-section {
    flex: 1;
    background-color: #f9f9f9;
    padding: 2rem;
    border-radius: 0.7rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  &__library-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 1rem;
    background-color: #b2ff59;
    border: none;
    border-radius: 0.4rem;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    align-self: flex-start;
  }

  &__preview-content {
    h3 {
      margin-bottom: 1rem;
      font-size: 1.2rem;
    }
  }

  &__instructions {
    list-style: none;
    padding: 0;
    margin-bottom: 2rem;

    li {
      margin-bottom: 0.8rem;
      color: #666;
    }

    code {
      background-color: #fff;
      padding: 0.2rem 0.4rem;
      border-radius: 0.3rem;
      font-family: monospace;
    }
  }

  &__example {
    background-color: #fff;
    padding: 1rem;
    border-radius: 0.5rem;

    p:first-child {
      margin-bottom: 1rem;
      color: #666;
    }
  }

  &__formula {
    display: flex;
    justify-content: center;
  }
}
</style>