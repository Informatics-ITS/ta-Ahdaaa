<template>
  <div class="w-full max-w-2xl p-6 bg-white rounded-xl shadow border">
    <h2 class="text-xl font-semibold mb-4 text-gray-800 pb-3">Predict from Metrics JSON</h2>

    <textarea
      v-model="jsonInput"
      placeholder="Paste JSON with 20 metrics here..."
      rows="12"
      class="w-full text-sm text-black p-3 border border-gray-300 rounded-md focus:outline-none focus:ring focus:ring-blue-300"
    ></textarea>

    <button
      @click="predict"
      class="mt-4 w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
    >
      Predict
    </button>

    <div v-if="result" class="mt-6 text-center pt-5">
      <p class="text-lg font-bold" :class="result.defect ? 'text-red-600' : 'text-green-600'">
        {{ result.defect ? 'Defective 🔴' : 'Not Defective ✅' }}
      </p>

      <div class="mt-4 text-left">
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

        <div class="mt-3 pb-5">
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

        <div v-if="result.ground_truth !== undefined" class="mt-4">
          <p class="text-sm text-gray-700">
            Ground Truth: <strong>{{ result.ground_truth ? 'Defective' : 'Not Defective' }}</strong
            ><br />
            Prediction Correct? <strong>{{ result.correct ? '✅ Yes' : '❌ No' }}</strong>
          </p>
        </div>
      </div>
    </div>

    <div v-if="error" class="mt-4 text-sm text-red-600 text-center">{{ error }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      jsonInput: '',
      result: null,
      error: null,
    }
  },
  methods: {
    async predict() {
      this.result = null
      this.error = null

      try {
        const parsed = JSON.parse(this.jsonInput)
        const res = await fetch('http://localhost:8000/predict-metrics', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(parsed),
        })

        if (!res.ok) throw new Error('Prediction failed')
        const data = await res.json()
        this.result = data
      } catch (err) {
        this.error = err.message
      }
    },
  },
}
</script>
