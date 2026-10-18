<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue'
import API from './services/api'
import MenuView from '@/components/MenuView.vue'
import StaffAuthModal from '@/components/StaffAuthModal.vue'
import AdminPanel from '@/components/AdminPanel.vue'

interface Product {
  id: number;
  name: string;
  category: string;
  price: string | number;
  is_available: boolean;
  image?: string | null;
  description?: string;
}

interface AddOn {
  id: number;
  name: string;
  price: string | number;
  classification: string;
  image?: string | null;
}

interface CartItem {
  cartId: string;
  product: Product;
  quantity: number;
  selectedAddOns: AddOn[];
}

// Persistent state across page reloads
const currentTab = ref<'home' | 'order' | 'extras' | 'checkout' | 'admin'>(
    (localStorage.getItem('kyuTeaCurrentTab') as any) || 'home'
)

watch(currentTab, (newTab) => {
  localStorage.setItem('kyuTeaCurrentTab', newTab)
})

// Shop State
const products = ref<Product[]>([])
const addOns = ref<AddOn[]>([])
const cart = ref<CartItem[]>([])
const customerName = ref('')
const successMessage = ref('')
const isSubmitting = ref(false)

// Active Order Tracking State
const activeOrderId = ref<number | null>(
    localStorage.getItem('kyuTeaActiveOrderId') ? Number(localStorage.getItem('kyuTeaActiveOrderId')) : null
)
const activeOrderStatus = ref<string>(
    localStorage.getItem('kyuTeaActiveOrderStatus') || ''
)
let statusPollInterval: any = null

const checkOrderStatus = async () => {
  if (!activeOrderId.value) return
  try {
    const res = await API.get(`orders/${activeOrderId.value}/`)
    activeOrderStatus.value = res.data.status
    localStorage.setItem('kyuTeaActiveOrderStatus', res.data.status)
  } catch (err) {
    console.error('Failed to check active order status')
  }
}

const startPolling = () => {
  if (statusPollInterval) clearInterval(statusPollInterval)
  checkOrderStatus()
  statusPollInterval = setInterval(checkOrderStatus, 5000)
}

// Customization Modal State
const activeProduct = ref<Product | null>(null)
const selectedAddOns = ref<AddOn[]>([])
const itemQuantity = ref(1)

// Auth State
const authToken = ref(localStorage.getItem('kyuTeaToken') || '')
const isAuthModalOpen = ref(false)

const loadData = async () => {
  try {
    const [prodRes, addonRes] = await Promise.all([
      API.get('products/'),
      API.get('add-ons/')
    ])
    products.value = prodRes.data
    addOns.value = addonRes.data
  } catch (err) {
    console.error('Failed to load café catalog.')
  }
}

onMounted(() => {
  loadData()
  if (activeOrderId.value) {
    startPolling()
  }
})

onUnmounted(() => {
  if (statusPollInterval) clearInterval(statusPollInterval)
})

const handleStaffLogout = () => {
  authToken.value = ''
  localStorage.removeItem('kyuTeaToken')
}

const handleLoginSuccess = (token: string) => {
  authToken.value = token
  localStorage.setItem('kyuTeaToken', token)
}

const openCustomizeModal = (product: Product) => {
  activeProduct.value = product
  selectedAddOns.value = []
  itemQuantity.value = 1
}

const toggleAddOn = (addon: AddOn) => {
  const index = selectedAddOns.value.findIndex(a => a.id === addon.id)
  if (index > -1) {
    selectedAddOns.value.splice(index, 1)
  } else {
    selectedAddOns.value.push(addon)
  }
}

const isAddOnSelected = (addonId: number) => {
  return selectedAddOns.value.some(a => a.id === addonId)
}

const addToCart = () => {
  if (!activeProduct.value) return

  const newItem: CartItem = {
    cartId: Date.now().toString() + Math.random().toString().slice(2, 5),
    product: activeProduct.value,
    quantity: itemQuantity.value,
    selectedAddOns: [...selectedAddOns.value]
  }

  cart.value.push(newItem)
  activeProduct.value = null
  successMessage.value = `${newItem.product.name} added to cart!`

  setTimeout(() => {
    successMessage.value = ''
  }, 3000)
}

const removeFromCart = (cartId: string) => {
  cart.value = cart.value.filter(item => item.cartId !== cartId)
}

const itemPrice = (item: CartItem) => {
  const base = Number(item.product.price)
  const addonsTotal = item.selectedAddOns.reduce((sum, a) => sum + Number(a.price), 0)
  return (base + addonsTotal) * item.quantity
}

const cartTotal = () => {
  return cart.value.reduce((total, item) => total + itemPrice(item), 0).toFixed(2)
}

const checkout = async () => {
  if (cart.value.length === 0) return
  isSubmitting.value = true
  successMessage.value = ''

  try {
    const orderPayload = {
      customer_name: customerName.value.trim() || 'Guest Customer',
      total_price: cartTotal(),
      status: 'Pending',
      items_data: cart.value.map(item => ({
        product: item.product.id,
        quantity: item.quantity,
        add_ons: item.selectedAddOns.map(a => a.id)
      }))
    }

    const response = await API.post('orders/', orderPayload)
    const newOrderId = response.data.id

    activeOrderId.value = newOrderId
    activeOrderStatus.value = 'Pending'
    localStorage.setItem('kyuTeaActiveOrderId', String(newOrderId))
    localStorage.setItem('kyuTeaActiveOrderStatus', 'Pending')

    startPolling()

    cart.value = []
    customerName.value = ''
  } catch (err) {
    alert('Failed to submit order.')
  } finally {
    isSubmitting.value = false
  }
}

const clearActiveOrder = () => {
  activeOrderId.value = null
  activeOrderStatus.value = ''
  localStorage.removeItem('kyuTeaActiveOrderId')
  localStorage.removeItem('kyuTeaActiveOrderStatus')
  if (statusPollInterval) clearInterval(statusPollInterval)
}
</script>

<template>
  <div class="min-h-screen bg-[#F4ECD8] text-[#3D2817] flex flex-col font-sans">

    <!-- Header Bar -->
    <header class="bg-[#3D2817] text-[#F4ECD8] py-3 px-4 sm:px-8 shadow-md flex flex-wrap justify-between items-center border-b-4 border-[#5A3D28] print:hidden gap-2">
      <div class="flex items-center space-x-3 cursor-pointer" @click="currentTab = 'home'">
        <img src="/mascot1.gif" alt="Logo" class="w-8 h-8 rounded-full object-cover border border-[#C89D7C]" />
        <h1 class="text-base sm:text-xl font-bold tracking-wide font-serif whitespace-nowrap">
          KyuTea Rustic Café <span class="text-[#D4A373]">✨</span>
        </h1>
      </div>

      <nav class="flex items-center flex-wrap gap-1.5 sm:gap-3 text-xs sm:text-sm font-medium">
        <button @click="currentTab = 'home'" :class="currentTab === 'home' ? 'bg-[#5A3D28] text-[#F4ECD8] font-bold border border-[#C89D7C]/50 shadow-inner' : 'text-[#D3C1AE] hover:text-white'" class="px-3 sm:px-4 py-1.5 rounded-lg transition-all cursor-pointer">Home</button>
        <button @click="currentTab = 'order'" :class="currentTab === 'order' ? 'bg-[#5A3D28] text-[#F4ECD8] font-bold border border-[#C89D7C]/50 shadow-inner' : 'text-[#D3C1AE] hover:text-white'" class="px-3 sm:px-4 py-1.5 rounded-lg transition-all cursor-pointer">Order Now</button>
        <button @click="currentTab = 'extras'; loadData()" :class="currentTab === 'extras' ? 'bg-[#5A3D28] text-[#F4ECD8] font-bold border border-[#C89D7C]/50 shadow-inner' : 'text-[#D3C1AE] hover:text-white'" class="px-3 sm:px-4 py-1.5 rounded-lg transition-all cursor-pointer">Add-Ons</button>
        <button @click="currentTab = 'checkout'" :class="currentTab === 'checkout' ? 'bg-[#5A3D28] text-[#F4ECD8] font-bold border border-[#C89D7C]/50 shadow-inner' : 'text-[#D3C1AE] hover:text-white'" class="px-3 sm:px-4 py-1.5 rounded-lg transition-all cursor-pointer flex items-center gap-1">
          Checkout
          <span v-if="cart.length > 0" class="bg-[#D4A373] text-[#3D2817] text-xs font-bold rounded-full px-2 py-0.5 ml-1">{{ cart.length }}</span>
        </button>
        <button @click="currentTab = 'admin'" :class="currentTab === 'admin' ? 'bg-[#8C6239] text-white font-bold border border-[#C89D7C] shadow-inner' : 'bg-[#5A3D28] text-[#D3C1AE] hover:text-white'" class="px-3 sm:px-4 py-1.5 rounded-lg transition-all border border-[#5A3D28] cursor-pointer">Admin Panel ⚙️</button>
      </nav>
    </header>

    <!-- MAIN CONTENT CONTAINER -->
    <main class="flex-grow max-w-5xl mx-auto px-6 py-10 w-full print:hidden flex flex-col justify-center items-center">

      <!-- HOME TAB -->
      <div v-if="currentTab === 'home'" class="w-full flex justify-center items-center">
        <div class="bg-[#FAF3E0] rounded-3xl p-8 sm:p-10 shadow-2xl border-2 border-[#D4A373] flex flex-row items-center justify-between max-w-[720px] w-full gap-8">
          <div class="flex justify-center items-center border-r-2 border-dashed border-[#C89D7C] pr-8 w-2/5">
            <img src="/mascot1.gif" alt="Mascot" class="w-44 h-44 object-contain" />
          </div>
          <div class="flex-1 flex flex-col items-start text-left w-3/5">
            <h2 class="text-2xl font-serif font-bold text-[#3D2817] mb-2">Cozy Wooden Lodge ✨</h2>
            <p class="text-[#5C4A3D] text-sm mb-6 leading-relaxed">
              Step in from the cold! Relax with our freshly roasted espresso, rustic baked treats, and warm anime timber atmosphere.
            </p>
            <div class="flex flex-col gap-3 w-full max-w-[220px]">
              <button @click="currentTab = 'order'" class="bg-[#8C6239] hover:bg-[#704E2D] text-white font-semibold py-2.5 px-5 rounded-xl text-sm transition-all shadow cursor-pointer text-center block w-full">🧋 Place an Order</button>
              <button @click="currentTab = 'extras'; loadData()" class="bg-[#D4A373] hover:bg-[#C28E5F] text-[#3D2817] font-semibold py-2.5 px-5 rounded-xl text-sm transition-all shadow cursor-pointer text-center block w-full">🌿 Browse Add-Ons</button>
            </div>
          </div>
        </div>
      </div>

      <!-- ORDER NOW TAB -->
      <div v-else-if="currentTab === 'order'" class="w-full self-start">
        <div v-if="successMessage" class="bg-[#E2EBD0] border border-[#A4C270] text-[#324515] p-4 rounded-xl mb-6 text-sm font-semibold">{{ successMessage }}</div>
        <div class="mb-6">
          <h2 class="text-2xl font-serif font-bold text-[#3D2817]">Featured Menu</h2>
          <p class="text-[#5C4A3D] text-sm">Freshly brewed milk tea, coffee, and delicious rustic snacks served daily.</p>
        </div>
        <MenuView @select-product="openCustomizeModal" />
      </div>

      <!-- ADD-ONS TAB -->
      <div v-else-if="currentTab === 'extras'" class="w-full self-start">
        <div class="mb-6">
          <h2 class="text-2xl font-serif font-bold text-[#3D2817]">Café Add-Ons & Extras</h2>
          <p class="text-[#5C4A3D] text-sm">Customize your drinks with pearls, nata de coco, and extra espresso shots.</p>
        </div>
        <div v-if="addOns.length > 0" class="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div v-for="addon in addOns" :key="addon.id" class="bg-[#FAF3E0] border border-[#D4A373] rounded-2xl p-6 shadow-md flex flex-col justify-between">
            <div>
              <div v-if="addon.image" class="mb-3 h-28 w-full overflow-hidden rounded-xl bg-[#F4ECD8] border border-[#D4A373]/50 flex items-center justify-center">
                <img :src="addon.image" alt="Add-on Image" class="h-full w-full object-contain" />
              </div>
              <h3 class="text-lg font-serif font-bold text-[#3D2817] mb-1">{{ addon.name }}</h3>
              <p class="text-xs text-[#8C6239] mb-4 capitalize">Type: {{ addon.classification }}</p>
            </div>
            <div class="text-[#8C6239] font-extrabold text-lg">+₱{{ addon.price }}</div>
          </div>
        </div>
        <div v-else class="text-center py-16 bg-[#FAF3E0] rounded-2xl border border-dashed border-[#D4A373]">
          <p class="text-[#5C4A3D] text-sm">No add-ons available at the moment.</p>
        </div>
      </div>

      <!-- CHECKOUT TAB -->
      <div v-else-if="currentTab === 'checkout'" class="max-w-md mx-auto w-full self-start">
        <!-- ACTIVE ORDER TRACKING BANNER -->
        <div v-if="activeOrderId" class="mb-6">
          <div v-if="activeOrderStatus === 'Pending'" class="bg-amber-50 border-2 border-amber-300 rounded-3xl p-6 text-center shadow-lg space-y-3">
            <div class="flex justify-center">
              <img src="/mascot7.gif" alt="Preparing" class="w-20 h-20 object-contain animate-bounce" />
            </div>
            <h3 class="text-lg font-serif font-bold text-[#3D2817]">Order #{{ activeOrderId }}</h3>
            <div class="inline-block bg-amber-200 text-amber-900 font-extrabold text-sm px-4 py-1.5 rounded-full">
              ⏳ Your order is being prepared!
            </div>
            <p class="text-xs text-amber-800">Hang tight! Our staff is crafting your order.</p>
          </div>

          <div v-else-if="activeOrderStatus === 'Completed'" class="bg-emerald-50 border-2 border-emerald-400 rounded-3xl p-6 text-center shadow-lg space-y-3">
            <div class="flex justify-center">
              <img src="/mascot8.gif" alt="Ready" class="w-20 h-20 object-contain" />
            </div>
            <h3 class="text-lg font-serif font-bold text-[#3D2817]">Order #{{ activeOrderId }}</h3>
            <div class="inline-block bg-emerald-600 text-white font-extrabold text-sm px-4 py-1.5 rounded-full shadow">
              🎉 Your order is ready!
            </div>
            <p class="text-xs text-emerald-800 font-semibold">Please head to the counter to pick up your order.</p>
            <button @click="clearActiveOrder" class="mt-2 text-xs text-gray-500 underline font-bold cursor-pointer hover:text-gray-700">
              Dismiss / Place New Order
            </button>
          </div>
        </div>

        <!-- Checkout Form -->
        <div class="bg-[#FAF3E0] border border-[#D4A373] rounded-2xl p-8 shadow-xl">
          <h2 class="text-2xl font-serif font-bold text-[#3D2817] mb-4 border-b border-[#D4A373]/40 pb-3">Complete Your Order</h2>
          <div v-if="cart.length === 0" class="text-[#5C4A3D] text-sm italic py-8 text-center">Your cart is empty. Pick a drink from the <button @click="currentTab = 'order'" class="text-[#8C6239] underline font-semibold cursor-pointer">Order Now</button> tab!</div>
          <div v-else class="space-y-6">
            <div>
              <label class="block text-xs font-bold text-[#5C4A3D] uppercase mb-2">Customer Name</label>
              <input v-model="customerName" type="text" placeholder="Enter your name" class="w-full bg-white border border-[#D4A373] rounded-xl px-4 py-2.5 text-sm text-[#3D2817] focus:outline-none focus:border-[#8C6239]" />
            </div>
            <div class="space-y-3 max-h-60 overflow-y-auto pr-1">
              <div v-for="item in cart" :key="item.cartId" class="flex justify-between items-center text-sm border-b border-[#D4A373]/30 pb-3">
                <div>
                  <div class="font-semibold text-[#3D2817]">{{ item.product.name }} (x{{ item.quantity }})</div>
                  <div v-if="item.selectedAddOns.length > 0" class="text-xs text-[#8C6239]">+ {{ item.selectedAddOns.map(a => a.name).join(', ') }}</div>
                </div>
                <div class="flex items-center space-x-4">
                  <span class="font-bold text-[#8C6239]">₱{{ itemPrice(item).toFixed(2) }}</span>
                  <button @click="removeFromCart(item.cartId)" class="text-red-600 hover:text-red-800 font-bold text-xs cursor-pointer">✕</button>
                </div>
              </div>
            </div>
            <div class="pt-4 border-t border-[#D4A373]/40 flex justify-between text-xl font-extrabold text-[#3D2817]">
              <span>Total Amount:</span><span>₱{{ cartTotal() }}</span>
            </div>
            <button @click="checkout" :disabled="isSubmitting" class="w-full bg-[#527941] hover:bg-[#3E5C31] disabled:bg-gray-400 text-white font-medium py-3 rounded-xl transition-colors shadow-lg cursor-pointer">
              {{ isSubmitting ? 'Placing Order...' : 'Confirm & Place Order 🎉' }}
            </button>
          </div>
        </div>
      </div>

      <!-- ADMIN PANEL TAB -->
      <div v-else-if="currentTab === 'admin'" class="w-full self-start">
        <div v-if="!authToken" class="max-w-md mx-auto bg-[#FAF3E0] rounded-3xl p-8 shadow-2xl border-2 border-[#D4A373] text-center space-y-4">
          <img src="/mascot4.gif" alt="Staff Mascot" class="w-24 h-24 mx-auto object-contain" />
          <h3 class="text-xl font-serif font-bold text-[#3D2817]">Staff Portal Access Required</h3>
          <p class="text-xs text-[#5C4A3D]">Please log in to manage orders, inventory, staff approvals, and password reset requests.</p>
          <button @click="isAuthModalOpen = true" class="w-full bg-[#8C6239] hover:bg-[#704E2D] text-white py-2.5 rounded-xl font-medium text-sm transition-colors shadow cursor-pointer">Open Staff Portal</button>
        </div>

        <div v-else class="w-full">
          <AdminPanel @logout="handleStaffLogout" />
        </div>
      </div>
    </main>

    <!-- ITEM CUSTOMIZATION MODAL -->
    <div v-if="activeProduct" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-3xl p-6 max-w-sm w-full shadow-2xl space-y-4">
        <div class="flex justify-between items-center border-b pb-3">
          <h3 class="font-bold text-lg text-[#3D2817]">Customize Order</h3>
          <button @click="activeProduct = null" class="text-gray-400 hover:text-gray-600 font-bold cursor-pointer">✕</button>
        </div>

        <div class="text-center">
          <div v-if="activeProduct.image" class="h-28 w-full bg-[#F4ECD8] rounded-xl overflow-hidden mb-3 flex items-center justify-center">
            <img :src="activeProduct.image" class="h-full w-full object-contain" />
          </div>
          <h4 class="font-serif font-bold text-[#3D2817] text-lg">{{ activeProduct.name }}</h4>
          <p class="text-xs text-[#8C6239] font-bold">₱{{ activeProduct.price }}</p>
        </div>

        <!-- Add-Ons Selection -->
        <div v-if="addOns.length > 0">
          <label class="block text-xs font-bold text-gray-600 uppercase mb-2">Optional Add-Ons</label>
          <div class="space-y-2 max-h-40 overflow-y-auto pr-1">
            <div
                v-for="addon in addOns"
                :key="addon.id"
                @click="toggleAddOn(addon)"
                :class="isAddOnSelected(addon.id) ? 'border-[#8B5A2B] bg-amber-50' : 'border-gray-200'"
                class="flex justify-between items-center p-2.5 border rounded-xl cursor-pointer text-xs transition"
            >
              <span class="font-semibold text-gray-800">{{ addon.name }}</span>
              <span class="font-bold text-[#8B5A2B]">+₱{{ addon.price }}</span>
            </div>
          </div>
        </div>

        <!-- Quantity Selector -->
        <div class="flex justify-between items-center pt-2 border-t">
          <span class="text-xs font-bold text-gray-600 uppercase">Quantity</span>
          <div class="flex items-center space-x-3">
            <button @click="itemQuantity = Math.max(1, itemQuantity - 1)" class="w-7 h-7 bg-gray-100 rounded-lg text-sm font-bold text-gray-700 hover:bg-gray-200 cursor-pointer">-</button>
            <span class="font-bold text-sm text-[#3D2817]">{{ itemQuantity }}</span>
            <button @click="itemQuantity++" class="w-7 h-7 bg-gray-100 rounded-lg text-sm font-bold text-gray-700 hover:bg-gray-200 cursor-pointer">+</button>
          </div>
        </div>

        <button @click="addToCart" class="w-full bg-[#8B5A2B] hover:bg-[#6F441F] text-white font-bold py-2.5 rounded-xl text-sm transition shadow cursor-pointer">
          Add To Cart 🎉
        </button>
      </div>
    </div>

    <!-- STAFF AUTH MODAL -->
    <StaffAuthModal
        :is-open="isAuthModalOpen"
        @close="isAuthModalOpen = false"
        @login-success="handleLoginSuccess"
    />
  </div>
</template>