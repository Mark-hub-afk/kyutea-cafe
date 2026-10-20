<template>
  <div class="p-6 max-w-6xl mx-auto">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h1 class="text-2xl font-bold text-[#4A2E19]">Staff Admin Dashboard</h1>
        <p class="text-sm text-gray-600">
          Logged in as: <span class="font-bold text-[#8B5A2B]">{{ loggedInUser.username || 'Staff User' }}</span>
        </p>
      </div>
      <button @click="$emit('logout')" class="bg-red-600 text-white px-4 py-2 rounded-xl text-sm font-bold hover:bg-red-700 transition cursor-pointer">
        Logout
      </button>
    </div>

    <!-- Navigation Tabs -->
    <div class="flex space-x-6 border-b border-amber-200 pb-3 mb-6 text-sm font-bold overflow-x-auto">
      <button
          @click="currentTab = 'orders'; fetchOrders()"
          :class="currentTab === 'orders' ? 'text-[#8B5A2B] border-b-2 border-[#8B5A2B]' : 'text-gray-400 hover:text-gray-600'"
          class="pb-2 transition cursor-pointer whitespace-nowrap"
      >
        📦 Orders
      </button>
      <button
          @click="currentTab = 'inventory'; fetchProducts()"
          :class="currentTab === 'inventory' ? 'text-[#8B5A2B] border-b-2 border-[#8B5A2B]' : 'text-gray-400 hover:text-gray-600'"
          class="pb-2 transition cursor-pointer whitespace-nowrap"
      >
        ☕ Menu Inventory
      </button>
      <button
          @click="currentTab = 'addons'; fetchAddOns()"
          :class="currentTab === 'addons' ? 'text-[#8B5A2B] border-b-2 border-[#8B5A2B]' : 'text-gray-400 hover:text-gray-600'"
          class="pb-2 transition cursor-pointer whitespace-nowrap"
      >
        extras Add-Ons
      </button>
      <button
          @click="currentTab = 'approvals'; fetchStaffUsers()"
          :class="currentTab === 'approvals' ? 'text-[#8B5A2B] border-b-2 border-[#8B5A2B]' : 'text-gray-400 hover:text-gray-600'"
          class="pb-2 transition cursor-pointer whitespace-nowrap"
      >
        👥 Staff Approvals
      </button>
      <button
          @click="currentTab = 'resets'; fetchPasswordResets()"
          :class="currentTab === 'resets' ? 'text-[#8B5A2B] border-b-2 border-[#8B5A2B]' : 'text-gray-400 hover:text-gray-600'"
          class="pb-2 transition cursor-pointer whitespace-nowrap"
      >
        🔑 Password Resets
      </button>
    </div>

    <!-- TAB 1: ORDERS -->
    <div v-if="currentTab === 'orders'" class="bg-[#FDFBF7] p-6 rounded-2xl shadow-sm border border-amber-100">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-bold text-[#4A2E19]">Recent Orders</h2>
        <button @click="fetchOrders" class="bg-[#8B5A2B] text-white px-3 py-1.5 rounded-lg text-xs font-bold hover:bg-[#6F441F] cursor-pointer">
          🔄 Refresh
        </button>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
          <tr class="border-b border-amber-200 text-xs text-amber-900/60 uppercase">
            <th class="py-3 px-4">Order ID</th>
            <th class="py-3 px-4">Customer</th>
            <th class="py-3 px-4">Items Ordered</th>
            <th class="py-3 px-4">Total</th>
            <th class="py-3 px-4">Status</th>
            <th class="py-3 px-4 text-center">Action</th>
          </tr>
          </thead>
          <tbody class="divide-y divide-amber-100 text-sm">
          <tr v-for="order in orders" :key="order.id" class="hover:bg-amber-50/50 transition">
            <td class="py-3 px-4 font-bold text-gray-800">#{{ order.id }}</td>
            <td class="py-3 px-4 text-gray-600 font-semibold">{{ order.customer_name }}</td>
            <td class="py-3 px-4 text-xs text-gray-700">
              <div v-for="item in (order.items || order.order_items || [])" :key="item.id" class="py-0.5">
                <span class="font-bold text-[#8B5A2B]">{{ item.quantity || 1 }}x</span>
                {{ item.product_name || item.product?.name || item.name || 'Product' }}
                <span v-if="item.selected_size" class="text-gray-505">({{ item.selected_size }})</span>
              </div>
              <span v-if="!order.items && !order.order_items" class="text-gray-400 italic">No items listed</span>
            </td>
            <td class="py-3 px-4 font-bold text-[#8B5A2B]">₱{{ order.total_price }}</td>
            <td class="py-3 px-4">
                <span :class="{
                  'bg-yellow-100 text-yellow-800': order.status === 'Pending',
                  'bg-green-100 text-green-800': order.status === 'Completed',
                  'bg-red-100 text-red-800': order.status === 'Cancelled'
                }" class="px-2.5 py-1 rounded-full text-xs font-bold">
                  {{ order.status }}
                </span>
            </td>
            <td class="py-3 px-4 text-center space-x-2">
              <button v-if="order.status === 'Pending'" @click="updateOrderStatus(order.id, 'Completed')" class="bg-green-700 text-white text-xs px-3 py-1 rounded-lg font-bold hover:bg-green-800 cursor-pointer">Complete</button>
              <button v-if="order.status === 'Pending'" @click="updateOrderStatus(order.id, 'Cancelled')" class="bg-red-700 text-white text-xs px-3 py-1 rounded-lg font-bold hover:bg-red-800 cursor-pointer">Cancel</button>
            </td>
          </tr>
          <tr v-if="orders.length === 0">
            <td colspan="6" class="text-center py-6 text-gray-400 text-xs">No orders placed yet.</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- TAB 2: MENU INVENTORY -->
    <div v-else-if="currentTab === 'inventory'" class="bg-[#FDFBF7] p-6 rounded-2xl shadow-sm border border-amber-100">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-bold text-[#4A2E19]">Menu Catalog Management</h2>
        <button @click="openProductModal(null)" class="bg-[#8B5A2B] text-white px-4 py-2 rounded-xl text-xs font-bold hover:bg-[#6F441F] cursor-pointer">
          + Add New Product
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="prod in products" :key="prod.id" class="bg-white border border-amber-200 p-4 rounded-2xl shadow-sm flex flex-col justify-between">
          <div>
            <div v-if="prod.image" class="h-32 w-full bg-amber-50 rounded-xl overflow-hidden mb-3 flex items-center justify-center">
              <img :src="prod.image" class="h-full w-full object-contain" />
            </div>
            <h4 class="font-bold text-[#4A2E19]">{{ prod.name }}</h4>
            <p class="text-xs text-[#8B5A2B] font-semibold">{{ prod.category }} — ₱{{ prod.price }}</p>
          </div>
          <div class="flex justify-end space-x-2 mt-4">
            <button @click="openProductModal(prod)" class="bg-[#8B5A2B] text-white text-xs px-3 py-1.5 rounded-lg font-bold hover:bg-[#6F441F] cursor-pointer">Edit</button>
            <button @click="deleteProduct(prod.id)" class="bg-red-700 text-white text-xs px-3 py-1.5 rounded-lg font-bold hover:bg-red-800 cursor-pointer">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 3: ADD-ONS MANAGEMENT -->
    <div v-else-if="currentTab === 'addons'" class="bg-[#FDFBF7] p-6 rounded-2xl shadow-sm border border-amber-100">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-bold text-[#4A2E19]">Add-Ons Management</h2>
        <button @click="openAddOnModal(null)" class="bg-[#8B5A2B] text-white px-4 py-2 rounded-xl text-xs font-bold hover:bg-[#6F441F] cursor-pointer">
          + Add New Add-On
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="addon in addOns" :key="addon.id" class="bg-white border border-amber-200 p-4 rounded-2xl shadow-sm flex flex-col justify-between">
          <div>
            <div v-if="addon.image" class="h-32 w-full bg-amber-50 rounded-xl overflow-hidden mb-3 flex items-center justify-center">
              <img :src="addon.image" class="h-full w-full object-contain" />
            </div>
            <h4 class="font-bold text-[#4A2E19]">{{ addon.name }}</h4>
            <p class="text-xs text-[#8B5A2B] font-semibold">{{ addon.classification }} — ₱{{ addon.price }}</p>
          </div>
          <div class="flex justify-end space-x-2 mt-4">
            <button @click="openAddOnModal(addon)" class="bg-[#8B5A2B] text-white text-xs px-3 py-1.5 rounded-lg font-bold hover:bg-[#6F441F] cursor-pointer">Edit</button>
            <button @click="deleteAddOn(addon.id)" class="bg-red-700 text-white text-xs px-3 py-1.5 rounded-lg font-bold hover:bg-red-800 cursor-pointer">Delete</button>
          </div>
        </div>
      </div>
    </div>

    <!-- TAB 4: STAFF APPROVALS -->
    <div v-else-if="currentTab === 'approvals'" class="bg-[#FDFBF7] p-6 rounded-2xl shadow-sm border border-amber-100">
      <h2 class="text-lg font-bold text-[#4A2E19] mb-4">Staff Accounts Approval</h2>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
          <tr class="border-b border-amber-200 text-xs text-amber-900/60 uppercase">
            <th class="py-3 px-4">Username</th>
            <th class="py-3 px-4">Email</th>
            <th class="py-3 px-4">Status</th>
            <th class="py-3 px-4 text-center">Action</th>
          </tr>
          </thead>
          <tbody class="divide-y divide-amber-100 text-sm">
          <tr v-for="user in staffUsers" :key="user.id" class="hover:bg-amber-50/50 transition">
            <td class="py-3 px-4 font-bold text-gray-800">{{ user.username }}</td>
            <td class="py-3 px-4 text-gray-600">{{ user.email || '—' }}</td>
            <td class="py-3 px-4">
                <span
                    :class="user.is_approved ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'"
                    class="px-2.5 py-1 rounded-full text-xs font-bold"
                >
                  {{ user.is_approved ? 'Approved Staff' : 'Pending Approval' }}
                </span>
            </td>
            <td class="py-3 px-4 text-center">
              <div v-if="!user.is_approved" class="flex justify-center gap-2">
                <button
                    @click="updateUserApproval(user, true)"
                    class="px-3 py-1 bg-[#2D6A4F] text-white font-bold rounded-lg text-xs hover:bg-[#1B4332] transition cursor-pointer"
                >
                  Approve Staff
                </button>
              </div>

              <div v-else class="flex justify-center items-center gap-2">
                <button
                    @click="updateUserApproval(user, false)"
                    class="px-3.5 py-1.5 bg-[#A44A1B] text-white font-bold rounded-lg text-xs hover:bg-[#803510] transition cursor-pointer"
                >
                  Revoke Access
                </button>
              </div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- TAB 5: PASSWORD RESETS -->
    <div v-else-if="currentTab === 'resets'" class="bg-[#FDFBF7] p-6 rounded-2xl shadow-sm border border-amber-100">
      <h2 class="text-lg font-bold text-[#4A2E19] mb-4">Pending Password Reset Requests</h2>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
          <tr class="border-b border-amber-200 text-xs text-amber-900/60 uppercase">
            <th class="py-3 px-4">User</th>
            <th class="py-3 px-4">Requested At</th>
            <th class="py-3 px-4">Status</th>
            <th class="py-3 px-4 text-center">Action</th>
          </tr>
          </thead>
          <tbody class="divide-y divide-amber-100 text-sm">
          <tr v-for="reset in passwordResets" :key="reset.id" class="hover:bg-amber-50/50 transition">
            <td class="py-3 px-4 font-bold text-gray-800">{{ reset.username || 'User #' + reset.user }}</td>
            <td class="py-3 px-4 text-gray-500 text-xs">{{ new Date(reset.requested_at).toLocaleString() }}</td>
            <td class="py-3 px-4">
                <span :class="reset.is_approved ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'" class="px-2.5 py-1 rounded-full text-xs font-bold">
                  {{ reset.is_approved ? 'Approved' : 'Pending' }}
                </span>
            </td>
            <td class="py-3 px-4 text-center">
              <button
                  v-if="!reset.is_approved"
                  @click="approvePasswordReset(reset)"
                  class="px-3 py-1 bg-[#2D6A4F] text-white font-bold rounded-lg text-xs hover:bg-[#1B4332] transition cursor-pointer"
              >
                Approve Reset
              </button>
              <span v-else class="text-xs text-gray-400 font-semibold">Done</span>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- PRODUCT MODAL -->
    <div v-if="showProductModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-3xl p-6 max-w-md w-full shadow-2xl space-y-4">
        <div class="flex justify-between items-center border-b pb-3">
          <h3 class="font-bold text-lg text-[#4A2E19]">{{ editingProduct ? 'Edit Product' : 'Add New Product' }}</h3>
          <button @click="showProductModal = false" class="text-gray-400 hover:text-gray-600 font-bold">✕</button>
        </div>

        <div class="space-y-3">
          <div>
            <label class="block text-xs font-bold text-gray-600 uppercase mb-1">Product Name</label>
            <input v-model="prodFormName" type="text" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]" />
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-600 uppercase mb-1">Category</label>
            <select v-model="prodFormCategory" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]">
              <option value="Milktea">Milktea</option>
              <option value="Coffee">Coffee</option>
              <option value="Food">Food</option>
              <option value="Fruit Soda">Fruit Soda</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-600 uppercase mb-1">Price (₱)</label>
            <input v-model="prodFormPrice" type="number" step="0.01" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]" />
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-600 uppercase mb-1">Image File</label>
            <input @change="handleProductImageUpload" type="file" accept="image/*" class="w-full text-xs text-gray-500" />
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button @click="showProductModal = false" class="w-1/2 bg-gray-100 text-gray-600 font-bold py-2 rounded-xl text-xs cursor-pointer">Cancel</button>
          <button @click="saveProduct" class="w-1/2 bg-[#8B5A2B] text-white font-bold py-2 rounded-xl text-xs hover:bg-[#6F441F] cursor-pointer">
            Save Product
          </button>
        </div>
      </div>
    </div>

    <!-- ADD-ON MODAL -->
    <div v-if="showAddOnModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
      <div class="bg-white rounded-3xl p-6 max-w-md w-full shadow-2xl space-y-4">
        <div class="flex justify-between items-center border-b pb-3">
          <h3 class="font-bold text-lg text-[#4A2E19]">{{ editingAddOn ? 'Edit Add-On' : 'Add New Add-On' }}</h3>
          <button @click="showAddOnModal = false" class="text-gray-400 hover:text-gray-600 font-bold">✕</button>
        </div>

        <div class="space-y-3">
          <div>
            <label class="block text-xs font-bold text-gray-600 uppercase mb-1">Add-On Name</label>
            <input v-model="addonFormName" type="text" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]" />
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-600 uppercase mb-1">Classification</label>
            <select v-model="addonFormClassification" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]">
              <option value="Drink">Drink</option>
              <option value="Pastry">Pastry</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-600 uppercase mb-1">Price (₱)</label>
            <input v-model="addonFormPrice" type="number" step="0.01" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]" />
          </div>

          <div>
            <label class="block text-xs font-bold text-gray-600 uppercase mb-1">Image File</label>
            <input @change="handleAddOnImageUpload" type="file" accept="image/*" class="w-full text-xs text-gray-500" />
          </div>
        </div>

        <div class="flex gap-2 pt-2">
          <button @click="showAddOnModal = false" class="w-1/2 bg-gray-100 text-gray-600 font-bold py-2 rounded-xl text-xs cursor-pointer">Cancel</button>
          <button @click="saveAddOn" class="w-1/2 bg-[#8B5A2B] text-white font-bold py-2 rounded-xl text-xs hover:bg-[#6F441F] cursor-pointer">
            Save Add-On
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import API from '@/services/api'

const loggedInUser = ref({ username: '' })
const currentTab = ref('orders')

const orders = ref([])
const products = ref([])
const addOns = ref([])
const staffUsers = ref([])
const passwordResets = ref([])

// Product Modal State
const showProductModal = ref(false)
const editingProduct = ref(null)
const prodFormName = ref('')
const prodFormCategory = ref('Milktea')
const prodFormPrice = ref('')
const prodFormImage = ref(null)

// Add-On Modal State
const showAddOnModal = ref(false)
const editingAddOn = ref(null)
const addonFormName = ref('')
const addonFormClassification = ref('Drink')
const addonFormPrice = ref('')
const addonFormImage = ref(null)

const initializeUserSession = () => {
  try {
    const stored = JSON.parse(localStorage.getItem('user') || '{}')
    loggedInUser.value = stored
  } catch {
    loggedInUser.value = {}
  }
}

const fetchOrders = async () => {
  try {
    const res = await API.get('orders/')
    orders.value = res.data
  } catch (err) {
    console.error('Failed to load orders', err)
  }
}

const fetchProducts = async () => {
  try {
    const res = await API.get('products/')
    products.value = res.data
  } catch (err) {
    console.error('Failed to load products', err)
  }
}

const fetchAddOns = async () => {
  try {
    const res = await API.get('add-ons/')
    addOns.value = res.data
  } catch (err) {
    console.error('Failed to load add-ons', err)
  }
}

const fetchStaffUsers = async () => {
  try {
    const res = await API.get('users/')
    staffUsers.value = res.data
  } catch (err) {
    console.error('Failed to load staff list', err)
  }
}

const fetchPasswordResets = async () => {
  try {
    const res = await API.get('password-resets/')
    passwordResets.value = res.data
  } catch (err) {
    console.error('Failed to load password resets', err)
  }
}

const updateOrderStatus = async (orderId, newStatus) => {
  try {
    await API.patch(`orders/${orderId}/`, { status: newStatus })
    fetchOrders()
  } catch (err) {
    alert('Failed to update order status')
  }
}

const updateUserApproval = async (user, isApproved) => {
  try {
    await API.patch(`users/${user.id}/`, {
      is_approved: isApproved,
      is_staff: isApproved
    })
    user.is_approved = isApproved
    fetchStaffUsers()
  } catch (err) {
    alert('Failed to update staff status.')
  }
}

const approvePasswordReset = async (reset) => {
  try {
    await API.patch(`password-resets/${reset.id}/`, {
      is_approved: true
    })
    reset.is_approved = true
    alert('Password reset approved!')
  } catch (err) {
    alert('Failed to approve password reset.')
  }
}

const openProductModal = (prod = null) => {
  editingProduct.value = prod
  if (prod) {
    prodFormName.value = prod.name
    prodFormCategory.value = prod.category
    prodFormPrice.value = String(prod.price)
  } else {
    prodFormName.value = ''
    prodFormCategory.value = 'Milktea'
    prodFormPrice.value = ''
  }
  prodFormImage.value = null
  showProductModal.value = true
}

const handleProductImageUpload = (event) => {
  if (event.target.files && event.target.files[0]) {
    prodFormImage.value = event.target.files[0]
  }
}

const saveProduct = async () => {
  try {
    const formData = new FormData()
    formData.append('name', prodFormName.value)
    formData.append('category', prodFormCategory.value)
    formData.append('price', String(prodFormPrice.value))
    if (prodFormImage.value) {
      formData.append('image', prodFormImage.value)
    }

    if (editingProduct.value) {
      await API.patch(`products/${editingProduct.value.id}/`, formData)
    } else {
      await API.post('products/', formData)
    }
    showProductModal.value = false
    fetchProducts()
  } catch (err) {
    alert('Failed to save product.')
  }
}

const deleteProduct = async (productId) => {
  if (!confirm('Are you sure you want to delete this product?')) return
  try {
    await API.delete(`products/${productId}/`)
    fetchProducts()
  } catch (err) {
    alert('Failed to delete product.')
  }
}

const openAddOnModal = (addon = null) => {
  editingAddOn.value = addon
  if (addon) {
    addonFormName.value = addon.name
    addonFormClassification.value = addon.classification
    addonFormPrice.value = String(addon.price)
  } else {
    addonFormName.value = ''
    addonFormClassification.value = 'Drink'
    addonFormPrice.value = ''
  }
  addonFormImage.value = null
  showAddOnModal.value = true
}

const handleAddOnImageUpload = (event) => {
  if (event.target.files && event.target.files[0]) {
    addonFormImage.value = event.target.files[0]
  }
}

const saveAddOn = async () => {
  try {
    const formData = new FormData()
    formData.append('name', addonFormName.value)
    formData.append('classification', addonFormClassification.value)
    formData.append('price', String(addonFormPrice.value))
    if (addonFormImage.value) {
      formData.append('image', addonFormImage.value)
    }

    if (editingAddOn.value) {
      await API.patch(`add-ons/${editingAddOn.value.id}/`, formData)
    } else {
      await API.post('add-ons/', formData)
    }
    showAddOnModal.value = false
    fetchAddOns()
  } catch (err) {
    alert('Failed to save add-on.')
  }
}

const deleteAddOn = async (addonId) => {
  if (!confirm('Are you sure you want to delete this add-on?')) return
  try {
    await API.delete(`add-ons/${addonId}/`)
    fetchAddOns()
  } catch (err) {
    alert('Failed to delete add-on.')
  }
}

onMounted(() => {
  initializeUserSession()
  fetchOrders()
})
</script>