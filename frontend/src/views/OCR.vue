<template>
  <div>
    <h2>OCR dari Python (FastAPI)</h2>

    <!-- Upload File -->
    <input type="file" @change="handleFile" />

    <button @click="uploadOCR" :disabled="!selectedFile || loading">
      {{ loading ? "Memproses..." : "Upload & OCR" }}
    </button>

    <!-- Hasil OCR -->
    <div v-if="ocrText">
      <h3>Hasil OCR:</h3>
      <pre>{{ ocrText }}</pre>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      ocrText: "",
      loading: false
    };
  },

  methods: {
    handleFile(event) {
      this.selectedFile = event.target.files[0];
    },

    async uploadOCR() {
      if (!this.selectedFile) return;

      this.loading = true;

      const form = new FormData();
      form.append("file", this.selectedFile);

      // FETCH melalui proxy → otomatis mengarah ke FastAPI
      const res = await fetch("/api/ocr-upload", {
        method: "POST",
        body: form,
      });

      const data = await res.json();

      this.ocrText = data.text;
      this.loading = false;
    },
  },
};
</script>
