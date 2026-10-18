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
      <button
          @click="selectedCategory = 'Addons'"
          :class="selectedCategory === 'Addons' ? 'bg-[#8B5A2B] text-white font-bold' : 'bg-white/80 text-[#5C4A3D] hover:bg-white'"
          class="px-5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition-all shadow-sm cursor-pointer"
      >
        ✨ Add-Ons
      </button>
    </div>

    <!-- 1. ADD-ONS CATALOG VIEW -->
    <div v-if="selectedCategory === 'Addons'">
      <div v-if="addOns.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
            v-for="addon in addOns"
            :key="addon.id"
            class="bg-[#FAF3E0] border border-[#D4A373] rounded-2xl p-5 shadow-md hover:shadow-xl transition flex flex-col justify-between"
        >
          <div>
            <div v-if="addon.image" class="mb-3 h-36 w-full overflow-hidden rounded-xl bg-[#F4ECD8] border border-[#D4A373]/40 flex items-center justify-center">
              <img :src="addon.image" :alt="addon.name" class="h-full w-full object-contain" />
            </div>
            <h3 class="text-lg font-serif font-bold text-[#3D2817] mb-1">{{ addon.name }}</h3>
            <p class="text-xs text-[#8C6239] font-medium mb-3">{{ addon.classification }} Add-On</p>
          </div>

          <div class="flex justify-between items-center mt-4 pt-3 border-t border-[#D4A373]/30">
            <span class="text-lg font-extrabold text-[#3D2817]">₱{{ addon.price }}</span>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-12 bg-[#FAF3E0] rounded-2xl border border-dashed border-[#D4A373]">
        <p class="text-[#5C4A3D] text-sm">No add-ons available at the moment.</p>
      </div>
    </div>

    <!-- 2. MAIN PRODUCTS GRID VIEW -->
    <div v-else-if="filteredProducts.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
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
              @click="openCustomizeModal(product)"
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

    <!-- 3. CUSTOMIZE ORDER MODAL POPUP -->
    <div v-if="showCustomizeModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-3xl p-6 max-w-sm w-full shadow-2xl space-y-4">
        <div class="flex justify-between items-center border-b pb-3">
          <h3 class="font-bold text-lg text-[#3D2817]">Customize Order</h3>
          <button @click="showCustomizeModal = false" class="text-gray-400 hover:text-gray-600 font-bold cursor-pointer">✕</button>
        </div>

        <div class="text-center">
          <h4 class="font-bold text-xl text-[#3D2817]">{{ selectedProduct?.name }}</h4>
          <p class="text-sm font-bold text-[#8B5A2B]">₱{{ calculatedUnitPrice }}</p>
        </div>

        <!-- ADD-ONS CHECKBOX LIST -->
        <div v-if="availableAddOnsForProduct.length > 0" class="space-y-2 pt-2 border-t">
          <label class="block text-xs font-bold text-gray-600 uppercase">Available Add-ons</label>
          <div class="max-h-36 overflow-y-auto space-y-1.5 pr-1">
            <label
                v-for="addon in availableAddOnsForProduct"
                :key="addon.id"
                class="flex items-center justify-between text-xs bg-[#FAF3E0] p-2.5 rounded-xl border border-[#D4A373]/40 cursor-pointer hover:bg-amber-100/50"
            >
              <div class="flex items-center gap-2">
                <input
                    type="checkbox"
                    :value="addon.id"
                    v-model="selectedAddOnIds"
                    class="rounded text-[#8B5A2B] focus:ring-[#8B5A2B]"
                />
                <span class="font-bold text-gray-800">{{ addon.name }}</span>
              </div>
              <span class="font-bold text-[#8B5A2B]">+₱{{ addon.price }}</span>
            </label>
          </div>
        </div>

        <!-- QUANTITY SELECTOR -->
        <div class="flex justify-between items-center pt-2">
          <span class="text-xs font-bold text-gray-600 uppercase">Quantity</span>
          <div class="flex items-center gap-3 bg-gray-100 rounded-xl px-3 py-1">
            <button @click="quantity > 1 && quantity--" class="font-bold text-gray-600 cursor-pointer">-</button>
            <span class="font-bold text-sm">{{ quantity }}</span>
            <button @click="quantity++" class="font-bold text-gray-600 cursor-pointer">+</button>
          </div>
        </div>

        <button
            @click="confirmAddToCart"
            class="w-full bg-[#8B5A2B] text-white font-bold py-3 rounded-2xl text-sm hover:bg-[#6F441F] transition cursor-pointer"
        >
          Add To Cart 🛒 (₱{{ (calculatedUnitPrice * quantity).toFixed(2) }})
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import API from '@/services/api'

const props = defineProps({
  initialCategory: {
    type: String,
    default: 'All'
  }
})

const emit = defineEmits(['select-product'])

const products = ref([])
const addOns = ref([])
const selectedCategory = ref(props.initialCategory)

// Keep selectedCategory synced with any parent props
watch(() => props.initialCategory, (newVal) => {
  if (newVal) {
    selectedCategory.value = newVal
  }
})

// Customization Modal State
const showCustomizeModal = ref(false)
const selectedProduct = ref(null)
const selectedAddOnIds = ref([])
const quantity = ref(1)

const fetchProducts = async () => {
  try {
    const res = await API.get('products/')
    products.value = res.data
  } catch (err) {
    console.error('Failed to load menu products:', err)
  }
}

const fetchAddOns = async () => {
  try {
    const res = await API.get('add-ons/')
    addOns.value = res.data
  } catch (err) {
    console.error('Failed to load add-ons:', err)
  }
}

const filteredProducts = computed(() => {
  if (selectedCategory.value === 'Drinks') {
    return products.value.filter(p => ['Milktea', 'Coffee', 'Fruit Soda'].includes(p.category))
  }
  if (selectedCategory.value === 'Foods') {
    return products.value.filter(p => p.category === 'Food')
  }
  return products.value
})

// Dynamically filter add-ons so drinks get drink add-ons and foods get pastry add-ons
const availableAddOnsForProduct = computed(() => {
  if (!selectedProduct.value) return addOns.value
  const isDrink = ['Milktea', 'Coffee', 'Fruit Soda'].includes(selectedProduct.value.category)
  const targetClassification = isDrink ? 'Drink' : 'Pastry'
  return addOns.value.filter(a => a.classification === targetClassification)
})

// Calculate live price (base price + sum of selected add-ons)
const calculatedUnitPrice = computed(() => {
  if (!selectedProduct.value) return 0
  const basePrice = Number(selectedProduct.value.price) || 0
  const chosenAddOns = addOns.value.filter(a => selectedAddOnIds.value.includes(a.id))
  const addOnsTotal = chosenAddOns.reduce((sum, a) => sum + (Number(a.price) || 0), 0)
  return (basePrice + addOnsTotal).toFixed(2)
})

const openCustomizeModal = (product) => {
  selectedProduct.value = product
  selectedAddOnIds.value = []
  quantity.value = 1
  showCustomizeModal.value = true
}

const confirmAddToCart = () => {
  const chosenAddOns = addOns.value.filter(a => selectedAddOnIds.value.includes(a.id))
  const finalPrice = Number(calculatedUnitPrice.value)

  emit('select-product', {
    ...selectedProduct.value,
    price: finalPrice, // Price including selected add-ons
    quantity: quantity.value,
    add_ons: selectedAddOnIds.value, // Backend foreign key IDs array
    selectedAddOns: chosenAddOns
  })

  showCustomizeModal.value = false
}

onMounted(() => {
  fetchProducts()
  fetchAddOns()
})
</script>