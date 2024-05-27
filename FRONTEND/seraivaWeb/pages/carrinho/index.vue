<script setup>
    import Carrinho from "~~/components/Carrinho.vue";

    definePageMeta({
        middleware: "auth",
    });
</script>
<template>
    <Carrinho />
</template>