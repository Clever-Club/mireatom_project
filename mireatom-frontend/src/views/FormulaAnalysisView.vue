<template>
  <div class="formula-analysis">
    <main class="formula-analysis__content">
      <div class="formula-analysis__form-section">
        <h1 class="formula-analysis__title">Анализ формулы</h1>
        <p class="formula-analysis__description">Проанализируйте интересующую вас формулу</p>

        <div class="formula-analysis__editor">
          <FormulaEditor v-model="latex" :isDisabled="true" />
        </div>

        <div class="formula-analysis__buttons">
          <button class="formula-analysis__submit" @click="submitFormula" :disabled="isLoading">
            {{ isLoading ? 'Анализируем...' : 'Анализировать' }}
          </button>

          <button class="formula-analysis__back" @click="$router.push('formula-input')">
            {{ 'Ввести другую формулу' }}
          </button>
        </div>

        <p v-if="errorMessage" class="formula-analysis__error">{{ errorMessage }}</p>
      </div>
      <div class="formula-analysis__display">
        <h2>Результат анализа</h2>

        <div class="formula-analysis__table-container">
          <table class="formula-analysis__table" v-if="processedMatches.length">
            <thead>
              <tr>
                <th>Ваша формула</th>
                <th>Найденная формула</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in processedMatches" :key="item.original">
                <td>
                  <FormulaEditor v-model="item.original" :isDisabled="true" />
                </td>
                <td>
                  <FormulaEditor v-model="item.found" :isDisabled="true" />
                </td>
              </tr>
            </tbody>
          </table>

          <div v-else>
            <p>{{ fetched ? "Совпадений нет" : "Вы еще не начали анализ" }}</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import FormulaEditor from '@/components/FormulaEditor.vue';
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { apiFetch } from '../utils/apiClient';

interface Index {
  original: string;
  found: string;
}

interface Match {
  percentage: number;
  value: string;
  indexes: Index[];
}

const route = useRoute();

const formulaId = route.query.formulaId;

const latex = ref('');
const isLoading = ref(false);
const errorMessage = ref('');

const fetched = ref(false);
const match = ref<Match[]>([]);
const processedMatches = ref<{ original: string; found: string }[]>([]);

async function fetchLatexFormula() {
  if (!formulaId) return;
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const response = await apiFetch(`library/formula/${formulaId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    latex.value = response.formula.value;
  } catch (error) {
    console.error('Error fetching LaTeX formula:', error);
    errorMessage.value = 'Не удалось загрузить формулу. Пожалуйста, попробуйте еще раз.';
  } finally {
    isLoading.value = false;
  }
}

fetchLatexFormula();

async function submitFormula() {
  isLoading.value = true;
  errorMessage.value = '';

  fetched.value = true;

  try {
    const response = await apiFetch(`library/formula/${formulaId}/analysis`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    match.value = response.match
      .filter((item: Match) => item.percentage >= 85.0)
      .sort((a: Match, b: Match) => b.percentage - a.percentage)
      .slice(0, 10);

    processedMatches.value = match.value.map((item) => {
      const original = insertPercentages(latex.value, item.indexes.map(i => i.original));
      const found = insertPercentages(item.value, item.indexes.map(i => i.found));
      return { original, found };
    });

    console.log('Formula is sent:', response);
  } catch (error) {
    console.error('Error sending formula:', error);
    errorMessage.value = 'Произошла ошибка при анализе формулы. Пожалуйста, попробуйте еще раз.';
  } finally {
    isLoading.value = false;
  }
}

function insertPercentages(formula: string, indexes: string[]): string {
  let result = formula.replace("\\\\", "\\");

  indexes.forEach(index => {
    const [start, end] = index.split(':').map(Number);
    result = result.slice(0, start) + '\\colorbox{red}{$ ' + result.slice(start, end + 1) + ' $}' + result.slice(end + 1);
  });

  return result;
}
</script>

<style lang="scss" scoped>
.formula-analysis {
  display: flex;
  flex-direction: row;
  align-items: center;

  &__content {
    display: flex;
    justify-content: space-between;
    gap: 1rem;
    width: 100%;
  }

  // Form section
  &__form-section {
    flex: 1;
  }

  &__title {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
  }

  &__description {
    color: #aaa;
    margin-bottom: 1rem;
  }

  &__editor {
    width: 100%;
    margin-bottom: 1rem;
  }

  &__error {
    color: #ff4444;
    margin-top: 0.5rem;
  }

  // Buttons
  &__buttons {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
  }

  &__submit {
    padding: 0.5rem 1rem;
    background-color: #b2ff59;
    border: none;
    border-radius: 0.4rem;
    min-width: 150px;
    font-size: 0.9rem;
    font-weight: 300;
    cursor: pointer;
    transition: opacity 0.2s;

    &:disabled {
      opacity: 0.7;
      cursor: not-allowed;
    }
  }

  &__back {
    padding: 0.5rem 1rem;
    border: 2px solid #000;
    border-radius: 0.4rem;
    min-width: 150px;
    background-color: transparent;
    font-size: 0.9rem;
    cursor: pointer;
    transition: background-color 0.2s;

    &:hover {
      background-color: rgba(0, 0, 0, 0.05);
    }
  }

  &__display {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;

    h2 {
      font-size: 1.25rem;
      margin-bottom: 1rem;
    }
  }

  &__table-container {
    padding: 1rem;
    max-height: 40vh;
    overflow-y: auto;
    border: 1px solid #ccc;
    border-radius: 5px;
  }

  &__table {
    width: 100%;
    border-collapse: collapse;

    th, td {
      padding: 1rem;
      padding-top: 0;
      text-align: center;
    }

    th {
      font-weight: 500;
    }

    tr:first-child {
      padding-left: 0;
    }
  }
}
</style>