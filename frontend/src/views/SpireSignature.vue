<template>
  <div class="container">
    <h3>Tambah QR ke PDF (Spire)</h3>

    <input type="file" @change="selectPDF" accept="application/pdf" />

    <button :disabled="!pdfFile" @click="signPDF">Generate PDF dengan QR</button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const pdfFile = ref(null);

function selectPDF(e) {
  pdfFile.value = e.target.files[0];
}

async function signPDF() {
  const form = new FormData();
  form.append("pdf", pdfFile.value);

  const res = await axios.post("http://localhost:8000/spire-signature",
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

<style>
/* styling mirip Flask HTML kamu */
.container {
  background: #1a1a1a;
  padding: 40px;
  border-radius: 16px;
  width: 450px;
  text-align: center;
  margin: 40px auto;
  box-shadow: 0 0 25px rgba(255, 0, 0, 0.25);
  border-top: 4px solid #e60000;
  color: white;
}
</style>
