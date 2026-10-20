<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import API from './services/api'
import StaffAuthModal from '@/components/StaffAuthModal.vue'

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

const router = useRouter()

const products = ref<Product[]>([])
const addOns = ref<AddOn[]>([])
const cart = ref<CartItem[]>([])
const customerName = ref('')
const successMessage = ref('')
const isSubmitting = ref(false)

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
  router.push('/')
}

const handleLoginSuccess = (token: string) => {
  authToken.value = token
  localStorage.setItem('kyuTeaToken', token)
}

const handleAddToCart = (customizedItem: { id: number; name: string; price: number; category: string; image?: string; quantity: number; selectedAddOns: AddOn[] }) => {
  const newItem: CartItem = {
    cartId: Date.now().toString() + Math.random().toString().slice(2, 5),
    product: {
      id: customizedItem.id,
      name: customizedItem.name,
      category: customizedItem.category,
      price: customizedItem.price,
      is_available: true,
      image: customizedItem.image
    },
    quantity: customizedItem.quantity,
    selectedAddOns: customizedItem.selectedAddOns
  }

  cart.value.push(newItem)
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

    <!-- Top Navigation Header -->
    <header class="bg-[#3D2817] text-[#F4ECD8] py-3 px-4 sm:px-8 shadow-md flex flex-wrap justify-between items-center border-b-4 border-[#5A3D28] print:hidden gap-2">
      <div class="flex items-center space-x-3 cursor-pointer" @click="router.push('/')">
        <img src="/mascot1.gif" alt="Logo" class="w-8 h-8 rounded-full object-cover border border-[#C89D7C]" />
        <h1 class="text-base sm:text-xl font-bold tracking-wide font-serif whitespace-nowrap">
          KyuTea Rustic Café <span class="text-[#D4A373]">✨</span>
        </h1>
      </div>

      <!-- Navigation Links using active-class attribute -->
      <nav class="flex items-center flex-wrap gap-1.5 sm:gap-3 text-xs sm:text-sm font-medium">
        <router-link to="/" active-class="bg-[#5A3D28] text-[#F4ECD8] font-bold border border-[#C89D7C]/50 shadow-inner" class="text-[#D3C1AE] hover:text-white px-3 sm:px-4 py-1.5 rounded-lg transition-all">Home</router-link>
        <router-link to="/order" active-class="bg-[#5A3D28] text-[#F4ECD8] font-bold border border-[#C89D7C]/50 shadow-inner" class="text-[#D3C1AE] hover:text-white px-3 sm:px-4 py-1.5 rounded-lg transition-all">Order Now</router-link>
        <router-link to="/add-ons" @click="loadData()" active-class="bg-[#5A3D28] text-[#F4ECD8] font-bold border border-[#C89D7C]/50 shadow-inner" class="text-[#D3C1AE] hover:text-white px-3 sm:px-4 py-1.5 rounded-lg transition-all">Add-Ons</router-link>
        <router-link to="/checkout" active-class="bg-[#5A3D28] text-[#F4ECD8] font-bold border border-[#C89D7C]/50 shadow-inner" class="text-[#D3C1AE] hover:text-white px-3 sm:px-4 py-1.5 rounded-lg transition-all flex items-center gap-1">
          Checkout
          <span v-if="cart.length > 0" class="bg-[#D4A373] text-[#3D2817] text-xs font-bold rounded-full px-2 py-0.5 ml-1">{{ cart.length }}</span>
        </router-link>
        <router-link to="/admin/orders" active-class="bg-[#8C6239] text-white font-bold border border-[#C89D7C] shadow-inner" class="bg-[#5A3D28] text-[#D3C1AE] hover:text-white px-3 sm:px-4 py-1.5 rounded-lg transition-all border border-[#5A3D28]">Admin Panel ⚙️</router-link>
      </nav>
    </header>

    <!-- Main Container -->
    <main class="flex-grow max-w-5xl mx-auto px-6 py-10 w-full print:hidden flex flex-col justify-center items-center">
      <router-view
          :products="products"
          :add-ons="addOns"
          :cart="cart"
          :success-message="successMessage"
          :customer-name="customerName"
          :active-order-id="activeOrderId"
          :active-order-status="activeOrderStatus"
          :is-submitting="isSubmitting"
          :auth-token="authToken"
          :is-auth-modal-open="isAuthModalOpen"
          @select-product="handleAddToCart"
          @remove-from-cart="removeFromCart"
          @checkout="checkout"
          @clear-active-order="clearActiveOrder"
          @update:customer-name="customerName = $event"
          @open-auth-modal="isAuthModalOpen = true"
          @logout="handleStaffLogout"
      />
    </main>

    <!-- Staff Auth Modal -->
    <StaffAuthModal
        :is-open="isAuthModalOpen"
        @close="isAuthModalOpen = false"
        @login-success="handleLoginSuccess"
    />
  </div>
</template>