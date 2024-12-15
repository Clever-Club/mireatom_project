<template>
    <div class="dropdown">
        <div class="dropdown__trigger" @click="$emit('toggle')">
            <p>{{ props.title }}</p>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 12H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                <path d="M3 6H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
                <path d="M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
            </svg>
        </div>
        <div class="dropdown__menu" v-if="isOpen">
            <slot name="menu-items"></slot>
        </div>
    </div>
</template>

<script setup lang="ts">
import { defineProps, onMounted, onBeforeUnmount } from 'vue';

const props = defineProps<{ isOpen: boolean, title: string }>();

function handleClickOutside(event: MouseEvent) {
    const dropdown = document.querySelector('.dropdown');
    if (props.isOpen && dropdown && !dropdown.contains(event.target as Node)) {
        const toggleEvent = new CustomEvent('toggle');
        dropdown.dispatchEvent(toggleEvent);
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside);
});
</script>

<style lang="scss" scoped>
.dropdown {
    cursor: pointer;

    &__trigger {
        display: flex;
        align-items: center;
        gap: .5rem;
        cursor: pointer;
    }

    &__menu {
        position: absolute;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        top: 100%;
        right: -5vw;
        background-color: #fff;
        border: 1px solid #E6E6E6;
        border-radius: 0.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        min-width: 10vw;
        max-width: 15vw;
        padding: 1rem;
    }

    &__item {
        padding: 0.5rem 1rem;
        color: #333;
        text-decoration: none;
        display: block;

        &:hover {
            background-color: #f5f5f5;
        }

        &--button {
            background: none;
            border: none;
            width: 100%;
            min-width: 0 !important;
            text-align: left;
            cursor: pointer;
        }
    }
}
</style>