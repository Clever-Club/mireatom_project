<template>
    <div class="formula-editor">
        <math-field ref="mathField" v-model="latex" :options="{
            virtualKeyboardMode: 'auto',
            smartMode: true
        }" :disabled="props.isDisabled"></math-field>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { MathfieldElement } from 'mathlive';

const props = defineProps<{
    isDisabled?: boolean;
}>();

if (!customElements.get('math-field')) {
    customElements.define('math-field', MathfieldElement);
}

const latex = defineModel();
const mathField = ref<MathfieldElement | null>(null);

watch(latex, (newValue) => {
    if (mathField.value) {
        mathField.value.value = newValue as string;
    }
});
</script>

<style lang="scss" scoped>
.formula-editor {
    width: 100%;
}

math-field {
    width: 100%;
    min-height: 100px;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 0.5rem;
    background: white;

    &:disabled {
        opacity: 1;
    }
}
</style>