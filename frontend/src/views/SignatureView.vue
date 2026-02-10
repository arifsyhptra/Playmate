<template>
  <div>
    <h2>Digital Signature (FastAPI + Spire)</h2>

    <h3>Sign PDF File</h3>
    <FileUpload @file-selected="selectPDF" />

    <button @click="signPDF" :disabled="!pdfFile">Sign PDF</button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import FileUpload from "../components/FileUpload.vue";

const pdfFile = ref(null);

function selectPDF(file) {
  pdfFile.value = file;
}

async function signPDF() {
  const form = new FormData();
  form.append("pdf", pdfFile.value);

  const res = await axios.post(
    "http://localhost:8000/spire-signature",
    form,
    { responseType: "blob" }
  );

  const url = URL.createObjectURL(res.data);
  const a = document.createElement("a");
  a.href = url;
  a.download = "Signed_output.pdf";
  a.click();
}
</script>
