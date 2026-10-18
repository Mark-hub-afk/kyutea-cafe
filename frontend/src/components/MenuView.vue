<template>
  <div>
    <!-- Category Filter Tabs -->
    <div class="flex justify-center space-x-3 mb-8">
      <button
          @click="selectedCategory = 'All'"
          :class="selectedCategory === 'All' ? 'bg-[#8B5A2B] text-white font-bold' : 'bg-white/80 text-[#5C4A3D] hover:bg-white'"
          class="px-5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shadow-sm cursor-pointer"
      >
        All Items
      </button>
      <button
          @click="selectedCategory = 'Drinks'"
          :class="selectedCategory === 'Drinks' ? 'bg-[#8B5A2B] text-white font-bold' : 'bg-white/80 text-[#5C4A3D] hover:bg-white'"
          class="px-5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shadow-sm cursor-pointer"
      >
        🧋 Drinks
      </button>
      <button
          @click="selectedCategory = 'Foods'"
          :class="selectedCategory === 'Foods' ? 'bg-[#8B5A2B] text-white font-bold' : 'bg-white/80 text-[#5C4A3D] hover:bg-white'"
          class="px-5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shadow-sm cursor-pointer"
      >
        🥐 Foods
      </button>
    </div>

    <!-- Product Grid -->
    <div v-if="filteredProducts.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
          v-for="product in filteredProducts"
          :key="product.id"
          class="bg-[#FAF3E0] border border-[#D4A373] rounded-2xl p-5 shadow-md hover:shadow-xl transition flex flex-col justify-between"
      >
        <div>
          <div v-if="product.image" class="mb-3 h-36 w-full overflow-hidden rounded-xl bg-[#F4ECD8] border border-[#D4A373]/40 flex items-center justify-center">
            <img :src="product.image" :alt="product.name" class="h-full w-full object-contain" />
          </div>
          <h3 class="text-lg font-serif font-bold text-[#3D2817] mb-1">{{ product.name }}</h3>
          <p class="text-xs text-[#8C6239] font-medium mb-3">{{ product.category }}</p>
        </div>

        <div class="flex justify-between items-center mt-4 pt-3 border-t border-[#D4A373]/30">
          <span class="text-lg font-extrabold text-[#3D2817]">₱{{ product.price }}</span>
          <button
              @click="$emit('select-product', product)"
              class="bg-[#8B5A2B] hover:bg-[#6F441F] text-white text-xs font-bold px-4 py-2 rounded-xl transition shadow cursor-pointer"
          >
            + Add to Order
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12 bg-[#FAF3E0] rounded-2xl border border-dashed border-[#D4A373]">
      <p class="text-[#5C4A3D] text-sm">No items found in this category.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import API from '@/services/api'

defineEmits(['select-product'])

const products = ref([])
// 1. Define selectedCategory reactive reference
const selectedCategory = ref('All')

const fetchProducts = async () => {
  try {
    const res = await API.get('products/')
    products.value = res.data
  } catch (err) {
    console.error('Failed to load menu products:', err)
  }
}

// 2. Computed filtering matching your ERD choices (Milktea, Coffee, Fruit Soda -> Drinks | Food -> Foods)
const filteredProducts = computed(() => {
  if (selectedCategory.value === 'Drinks') {
    return products.value.filter(p => ['Milktea', 'Coffee', 'Fruit Soda'].includes(p.category))
  }
  if (selectedCategory.value === 'Foods') {
    return products.value.filter(p => p.category === 'Food')
  }
  return products.value
})

onMounted(() => {
  fetchProducts()
})
</script>