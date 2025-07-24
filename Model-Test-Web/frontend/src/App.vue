<!-- Predictor.vue -->
<template>
  <div class="min-h-screen bg-gray-100 flex flex-col items-center justify-center px-4 py-8">
    <div class="mb-6 flex gap-2 pb-5">
      <button @click="mode = 'file'" :class="mode === 'file' ? activeClass : inactiveClass">
        Upload File
      </button>
      <button
        @click="mode = 'json'"
        :class="mode === 'json' ? activeClass : inactiveClass"
        class="ml-2"
      >
        Predict from JSON
      </button>
    </div>

    <div class="w-full flex justify-center">
      <FileUpload v-if="mode === 'file'" />
      <MetricsPredictor v-else />
    </div>
  </div>
</template>

<script>
import FileUpload from './components/FileUpload.vue'
import MetricsPredictor from './components/MetricsPredictor.vue'

export default {
  components: { FileUpload, MetricsPredictor },
  data() {
    return {
      mode: 'file',
    }
  },
  computed: {
    activeClass() {
      return 'bg-blue-600 text-white font-semibold py-2 px-4 rounded-md'
    },
    inactiveClass() {
      return 'bg-white text-blue-600 border border-blue-600 font-semibold py-2 px-4 rounded-md'
    },
  },
}
</script>
