// stores/cart.js
import { defineStore } from 'pinia';

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [],
  }),
  actions: {
    addToCart(item) {
      this.items.push(item);
    },
    removeFromCart(index) {
      this.items.splice(index, 1);
    },
    clearCart() {
      this.items = [];
    },
  },
  getters: {
    cartItems: (state) => state.items,
    cartItemCount: (state) => state.items.length,
  },
});
