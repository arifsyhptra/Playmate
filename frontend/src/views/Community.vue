<template>
  <div class="container">
    <h2>Digital Signature Berjenjang</h2>

    <!-- PILIH FILE PDF -->
    <input type="file" accept="application/pdf" @change="selectPDF" />

    <!-- PILIH SIGNER -->
    <div class="select-group">
      <label>Pilih Penandatangan:</label>
      <select v-model="signer">
        <option disabled value="">-- Pilih Jabatan --</option>
        <option value="manager">Manager</option>
        <option value="supervisor">Supervisor</option>
        <option value="staff">Staff</option>
      </select>
    </div>

    <button @click="signPDF" :disabled="!pdfFile || !signer">
      Sign PDF (Berjenjang)
    </button>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const pdfFile = ref(null);
const signer = ref("");

function selectPDF(event) {
  pdfFile.value = event.target.files[0];
}

async function signPDF() {
  const form = new FormData();
  form.append("pdf", pdfFile.value);
  form.append("signer", signer.value);

  const res = await axios.post(
    "http://localhost:8000/spire-signature-berjenjang",
    form,
    { responseType: "blob" }
  );

  // Download file
  const url = URL.createObjectURL(res.data);
  const a = document.createElement("a");
  a.href = url;

  const selectedName =
    signer.value.charAt(0).toUpperCase() + signer.value.slice(1);

  a.download = `TTD_${selectedName}.pdf`;
  a.click();
}
</script>

<style>
.container {
  max-width: 500px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

select,
input[type="file"] {
  margin: 10px 0;
}

button {
  padding: 10px 15px;
  margin-top: 10px;
  cursor: pointer;
}
</style>
