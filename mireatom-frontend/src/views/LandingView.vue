<template>
    <main class="landing">
        <div class="landing__headline">
            <h1 class="landing__headline-title">Хотите проанализировать ваши формулы?</h1>
            <p class="landing__headline-subtitle">Начните вводить одну из них!</p>
        </div>
        <div class="landing__content">
            <FormulaEditor v-model="latex" />
            <button class="landing__submit" @click="submitFormula">Продолжить</button>
        </div>
    </main>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import FormulaEditor from '@/components/FormulaEditor.vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/userStore';
import { storeToRefs } from 'pinia';

const { token } = storeToRefs(useUserStore());
const router = useRouter();

const latex = ref('');

function submitFormula() {
    if (latex.value.trim().length == 0) { return; }
    
    if (!token.value) {
        router.push({ path: '/login', query: { formula: latex.value } });
        return;
    }

    router.push({ path: '/formula-input', query: { formula: latex.value } });
}

// Компонент главной страницы
</script>

<style lang="scss" scoped>
.landing {
    text-align: center;

    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4rem;

    &__headline {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: .4rem;

        &-title {
            font-size: 2rem;
            margin-bottom: 0;
        }

        &-subtitle {
            color: #D7D7D7;
            font-size: 1.5rem;
            font-weight: 400;
            margin: 0;
        }
    }

    &__content {
        min-width: 50%;
        max-width: 50%;

        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 1rem;

        margin-bottom: 10rem;
    }

    &__submit {
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 0.4rem;
        cursor: pointer;
        min-width: 150px;
        background-color: #b2ff59;

        font-size: 0.9rem;
        font-weight: 300;
    }
}
</style>