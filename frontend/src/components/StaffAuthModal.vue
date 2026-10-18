<template>
  <div v-if="isOpen" class="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
    <div class="bg-white rounded-3xl p-6 max-w-sm w-full shadow-2xl space-y-4">
      <!-- Modal Header -->
      <div class="flex justify-between items-center border-b pb-3">
        <h3 class="font-bold text-lg text-[#4A2E19]">Staff Portal</h3>
        <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600 font-bold text-lg cursor-pointer">✕</button>
      </div>

      <!-- Mode Selector (Login vs Register) -->
      <div v-if="!showForgotPassword" class="flex border-b text-xs font-bold text-center">
        <button
            @click="authMode = 'login'"
            :class="authMode === 'login' ? 'border-b-2 border-[#8B5A2B] text-[#8B5A2B]' : 'text-gray-400'"
            class="w-1/2 py-2 cursor-pointer"
        >
          Login
        </button>
        <button
            @click="authMode = 'register'"
            :class="authMode === 'register' ? 'border-b-2 border-[#8B5A2B] text-[#8B5A2B]' : 'text-gray-400'"
            class="w-1/2 py-2 cursor-pointer"
        >
          Register Staff
        </button>
      </div>

      <!-- 1. LOGIN FORM -->
      <div v-if="authMode === 'login' && !showForgotPassword" class="space-y-3">
        <input v-model="loginData.username" type="text" placeholder="Username" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]" />
        <input v-model="loginData.password" type="password" placeholder="Password" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]" />
        <button @click="handleLogin" class="w-full bg-[#8B5A2B] text-white font-bold py-2 rounded-xl text-sm hover:bg-[#6F441F] transition-all cursor-pointer">Log In</button>

        <div class="text-center pt-2">
          <button @click="showForgotPassword = true; resetStatusMsg = ''; isError = false;" class="text-xs text-[#8B5A2B] font-semibold underline hover:text-[#6F441F] cursor-pointer">
            Forgot Password?
          </button>
        </div>
      </div>

      <!-- 2. STAFF REGISTRATION FORM -->
      <div v-else-if="authMode === 'register' && !showForgotPassword" class="space-y-3">
        <input v-model="regData.username" type="text" placeholder="Username" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]" />
        <input v-model="regData.email" type="email" placeholder="Email" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]" />
        <input v-model="regData.password" type="password" placeholder="Password" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]" />

        <div v-if="regMessage" class="text-xs p-2 rounded-lg bg-amber-50 text-amber-800 font-semibold">
          {{ regMessage }}
        </div>

        <button @click="handleRegister" class="w-full bg-[#8B5A2B] text-white font-bold py-2 rounded-xl text-sm hover:bg-[#6F441F] transition-all cursor-pointer">
          Submit Registration
        </button>
      </div>

      <!-- 3. FORGOT PASSWORD REQUEST FORM -->
      <div v-else-if="showForgotPassword" class="space-y-3">
        <!-- Mascot Feature -->
        <div class="flex justify-center mb-2">
          <img src="/mascot6.gif" alt="KyuTea Mascot" class="w-16 h-16 object-contain" />
        </div>

        <p class="text-xs text-gray-600 text-center">Enter your username, new password, and confirm it. An admin will review and approve your request.</p>

        <input v-model="resetIdentifier" type="text" placeholder="Username" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]" />
        <input v-model="newPassword" type="password" placeholder="New Password" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]" />
        <input v-model="confirmPassword" type="password" placeholder="Confirm New Password" class="w-full px-3 py-2 border rounded-xl text-sm outline-none focus:ring-2 focus:ring-[#8B5A2B]" />

        <!-- Feedback Message Box -->
        <div v-if="resetStatusMsg" :class="isError ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-green-50 text-green-700 border border-green-200'" class="text-xs font-semibold p-2.5 rounded-xl">
          {{ resetStatusMsg }}
        </div>

        <div class="flex gap-2 pt-2">
          <button @click="showForgotPassword = false" class="w-1/2 bg-gray-100 text-gray-600 font-bold py-2 rounded-xl text-xs cursor-pointer">Back</button>
          <button @click="handleResetRequest" :disabled="isSubmittingReset" class="w-1/2 bg-[#8B5A2B] hover:bg-[#6F441F] disabled:bg-gray-400 text-white font-bold py-2 rounded-xl text-xs cursor-pointer">
            {{ isSubmittingReset ? 'Submitting...' : 'Submit Request' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import API from '@/services/api'

defineProps({
  isOpen: Boolean
})

const emit = defineEmits(['close', 'login-success', 'request-submitted'])

const authMode = ref('login')
const showForgotPassword = ref(false)

const loginData = ref({ username: '', password: '' })
const regData = ref({ username: '', email: '', password: '' })
const regMessage = ref('')

const resetIdentifier = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const resetStatusMsg = ref('')
const isError = ref(false)
const isSubmittingReset = ref(false)

const handleLogin = async () => {
  try {
    const res = await API.post('token-auth/', loginData.value)
    const token = res.data.token

    localStorage.setItem('kyuTeaToken', token)
    loginData.value = { username: '', password: '' }

    emit('login-success', token)
    emit('close')
  } catch (err) {
    alert('Invalid username or password.')
  }
}

const handleRegister = async () => {
  try {
    await API.post('users/', regData.value)
    regMessage.value = 'Registration submitted! Awaiting admin approval.'
    regData.value = { username: '', email: '', password: '' }
  } catch (err) {
    regMessage.value = 'Registration failed. Try a different username/email.'
  }
}

const handleResetRequest = async () => {
  if (!resetIdentifier.value.trim() || !newPassword.value || !confirmPassword.value) {
    isError.value = true
    resetStatusMsg.value = 'All fields are required.'
    return
  }

  if (newPassword.value !== confirmPassword.value) {
    isError.value = true
    resetStatusMsg.value = 'New passwords do not match.'
    return
  }

  isSubmittingReset.value = true
  resetStatusMsg.value = ''
  isError.value = false

  try {
    const response = await API.post('password-resets/submit/', {
      username: resetIdentifier.value.trim(),
      new_password: newPassword.value,
      confirm_password: confirmPassword.value
    })

    console.log('Reset response:', response.data)
    isError.value = false
    resetStatusMsg.value = 'Reset request sent to admin dashboard!'

    emit('request-submitted')

    setTimeout(() => {
      resetStatusMsg.value = ''
      showForgotPassword.value = false
      resetIdentifier.value = ''
      newPassword.value = ''
      confirmPassword.value = ''
    }, 2000)
  } catch (err) {
    console.error('Detailed Password Reset Error:', err.response || err)
    isError.value = true
    resetStatusMsg.value = err.response?.data?.error || 'Failed to submit request. Please check connection.'
  } finally {
    isSubmittingReset.value = false
  }
}
</script>