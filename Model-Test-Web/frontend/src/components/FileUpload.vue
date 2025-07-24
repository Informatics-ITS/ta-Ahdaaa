<template>
  <div
    class="w-full max-w-6xl mx-auto mt-10"
    :class="fileContent ? 'flex gap-2' : 'flex justify-center'"
  >
    <!-- Upload & Result Panel -->
    <div
      class="bg-white shadow-md rounded-xl border border-gray-200 p-6 transition-all duration-500 ease-in-out self-start"
      :class="fileContent ? 'w-1/2 mr-6' : 'w-full max-w-2xl'"
    >
      <h2 class="text-xl font-semibold mb-5 pb-5 text-gray-800">Upload Python File</h2>

      <input
        type="file"
        accept=".py"
        @change="handleFileChange"
        class="block w-full text-sm pb-5 text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 mb-4"
      />

      <button
        @click="uploadFile"
        :disabled="!selectedFile"
        class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        Upload & Predict
      </button>

      <div v-if="result !== null" class="mt-6 pt-5">
        <div class="text-center">
          <p class="text-lg font-bold" :class="result.defect ? 'text-red-600' : 'text-green-600'">
            {{ result.defect ? 'Defective 🔴' : 'Not Defective ✅' }}
          </p>
        </div>

        <div class="mt-4">
          <p class="text-sm font-medium text-gray-700 mb-1">Probability:</p>

          <div class="mb-2">
            <p class="text-sm text-gray-600 mb-1">
              Non-Defect: {{ (result.probability?.non_defect * 100).toFixed(1) }}%
            </p>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div
                class="bg-green-500 h-3 rounded-full"
                :style="{ width: result.probability?.non_defect * 100 + '%' }"
              ></div>
            </div>
          </div>

          <div class="mt-3">
            <p class="text-sm text-gray-600 mb-1">
              Defect: {{ (result.probability?.defect * 100).toFixed(1) }}%
            </p>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div
                class="bg-red-500 h-3 rounded-full"
                :style="{ width: result.probability?.defect * 100 + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="error" class="mt-4 text-red-500 text-sm text-center">Error: {{ error }}</div>

      <div v-if="result?.metrics" class="mt-6 border-t pt-5">
        <h3 class="text-md font-semibold text-gray-800 mb-4">Software Metrics:</h3>

        <div class="grid grid-cols-2 gap-x-6 gap-y-3 text-sm">
          <div
            v-for="(value, key) in result.metrics"
            :key="key"
            class="flex justify-between border-b pb-1 text-gray-700"
          >
            <span class="font-medium capitalize">{{ key.replaceAll('_', ' ') }}</span>
            <span class="text-right font-mono">{{
              typeof value === 'number' ? value.toFixed(2) : value
            }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- File Preview Panel -->
    <div
      v-if="fileContent"
      class="w-1/2 bg-gray-50 border border-gray-200 rounded-xl p-6 max-h-[80vh] overflow-auto transition-all duration-500 ease-in-out"
    >
      <pre
        class="bg-white text-sm text-gray-800 p-4 rounded-lg overflow-x-auto whitespace-pre-wrap border border-gray-300"
      >
<code>{{ fileContent }}</code>
</pre>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      result: null,
      error: null,
      fileContent: '', // <-- new
    }
  },
  methods: {
    handleFileChange(event) {
      this.selectedFile = event.target.files[0]
      this.result = null
      this.error = null
      this.fileContent = ''

      // Read and store file content
      const reader = new FileReader()
      reader.onload = (e) => {
        this.fileContent = e.target.result
      }
      if (this.selectedFile) reader.readAsText(this.selectedFile)
    },

    async uploadFile() {
      this.result = null
      this.error = null

      const formData = new FormData()
      formData.append('file', this.selectedFile)

      try {
        const response = await fetch('http://localhost:8000/predict', {
          method: 'POST',
          body: formData,
        })

        if (!response.ok) throw new Error('Upload failed')

        const data = await response.json()
        this.result = data
      } catch (err) {
        this.error = err.message
      }
    },
  },
}
</script>
