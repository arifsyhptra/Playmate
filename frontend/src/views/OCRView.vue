<template>
  <div class="container">
    <h2>Form OCR KTP</h2>

    <input type="file" @change="handleFile" />

    <button @click="uploadOCR" :disabled="!selectedFile || loading">
      {{ loading ? "Memproses..." : "Upload & OCR" }}
    </button>

    <hr />

    <div v-if="formFilled">
      <h3>Data KTP Hasil OCR</h3>

      <form @submit.prevent="submitForm">
        <label>NIK</label>
        <input v-model="form.nik" type="text" />

        <label>Nama</label>
        <input v-model="form.nama" type="text" />

        <label>Tempat Lahir</label>
        <input v-model="form.tempat_lahir" type="text" />

        <label>Tanggal Lahir</label>
        <input v-model="form.tanggal_lahir" type="date" />

        <label>Jenis Kelamin</label>
        <input v-model="form.jenis_kelamin" type="text" />

        <label>Golongan Darah</label>
        <input v-model="form.gol_darah" type="text" />

        <label>Alamat</label>
        <input v-model="form.alamat" type="text" />

        <label>RT/RW</label>
        <input v-model="form.rt_rw" type="text" />

        <label>Kel/Desa</label>
        <input v-model="form.kelurahan" type="text" />

        <label>Kecamatan</label>
        <input v-model="form.kecamatan" type="text" />

        <label>Agama</label>
        <input v-model="form.agama" type="text" />

        <label>Status Perkawinan</label>
        <input v-model="form.status" type="text" />

        <label>Pekerjaan</label>
        <input v-model="form.pekerjaan" type="text" />

        <label>Kewarganegaraan</label>
        <input v-model="form.kewarganegaraan" type="text" />

        <label>Berlaku Hingga</label>
        <input v-model="form.berlaku_hingga" type="date" />

        <button type="submit">Submit Data</button>
      </form>

      <!-- =============================== -->
      <!-- JSON OUTPUT DI BAWAH FORM      -->
      <!-- =============================== -->
      <h3>JSON Output</h3>
      <pre class="json-box">{{ prettyJson }}</pre>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: null,
      loading: false,
      formFilled: false,

      form: {
        nik: "",
        nama: "",
        tempat_lahir: "",
        tanggal_lahir: "",
        jenis_kelamin: "",
        gol_darah: "",
        alamat: "",
        rt_rw: "",
        kelurahan: "",
        kecamatan: "",
        agama: "",
        status: "",
        pekerjaan: "",
        kewarganegaraan: "",
        berlaku_hingga: ""
      }
    };
  },

  computed: {
    // tampilkan JSON rapi
    prettyJson() {
      return JSON.stringify(this.form, null, 2);
    }
  },

  methods: {
    handleFile(event) {
      this.selectedFile = event.target.files[0];
    },

    async uploadOCR() {
      if (!this.selectedFile) return;
      this.loading = true;

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      const res = await fetch("/api/ocr-upload", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      const text = (data.text || "").replace(/[\u2018\u2019\u201c\u201d£]/g, "");

      this.parseOCR(text);

      this.loading = false;
      this.formFilled = true;
    },

    // --- semua parser OCR tetap sama ---
    parseOCR(text) {
      const raw = text;
      const lines = raw.split("\n").map(l => l.trim()).filter(l => l);

      // === NIK ===
      const nikRawMatch = raw.match(/\d{16,18}/);
      if (nikRawMatch) {
        const digits = nikRawMatch[0].replace(/\D/g, "");
        this.form.nik = digits.length > 16 ? digits.slice(-16) : digits;
      } else {
        const allNums = raw.match(/\d+/g) || [];
        const candidate = allNums.find(n => n.length === 16)
          || allNums.sort((a,b)=>Math.abs(a.length-16)-Math.abs(b.length-16))[0]
          || "";
        this.form.nik = candidate.slice(-16);
      }

      // === NAMA ===
      const namaLine = lines.find(l => /^nama\b/i.test(l) || l.toLowerCase().includes("nama "));
      if (namaLine) {
        this.form.nama = namaLine.replace(/^nama[:\s\-\.]*/i, "").trim();
      }

      // === TTL ===
      const ttlLine = lines.find(l => /tempat|lahr|lahir|tgl|tangg(al)? lahir|tempattgl/i.test(l));
      if (ttlLine) {
        const afterColon = ttlLine.includes(":") ? ttlLine.split(/:/).slice(1).join(":").trim() : ttlLine;
        if (afterColon.includes(",")) {
          const [placePart, datePart] = afterColon.split(",").map(s => s.trim());
          this.form.tempat_lahir = placePart;
          const iso = this.extractDate(datePart);
          if (iso) this.form.tanggal_lahir = iso;
        }
      }

      // === JENIS KELAMIN ===
      const jkLine = lines.find(l => /jenis kelamin/i.test(l)) || lines.find(l => /perempuan|laki/i.test(l));
      if (jkLine) {
        const jkMatch = jkLine.match(/(perempuan|laki-laki|laki|pria|wanita)/i);
        if (jkMatch) this.form.jenis_kelamin = this.normalizeCapital(jkMatch[1]);
      }

      // === GOL DARAH ===
      const golLine = lines.find(l => /gol\.|golongan|darah/i.test(l));
      if (golLine) {
        let g = golLine.replace(/.*(gol\.|golongan|darah)[:\s\-]*/i, "").trim();
        g = g.split(/\s|[,;:]/)[0] || g;
        if (/8|0/.test(g) && !/[AB]/i.test(g)) g = g.replace(/8|0/g, "O");
        this.form.gol_darah = g.toUpperCase();
      }

      // === ALAMAT ===
      const alamatLine = lines.find(l => /^alamat\b/i.test(l) || l.toLowerCase().includes("alamat"));
      if (alamatLine) {
        this.form.alamat = alamatLine.replace(/^alamat[:\s\-]*/i, "").trim();
      }

      // === RT / RW ===
      const rtRwMatch = raw.match(/RT\D*?(\d{1,3})\D*?RW\D*?(\d{1,3})/i);
      if (rtRwMatch) {
        this.form.rt_rw = `RT ${rtRwMatch[1]}/RW ${rtRwMatch[2]}`;
      }

      // === Kelurahan / Kecamatan ===
      const kel = lines.find(l => /kelurahan|desa|kel\./i.test(l));
      if (kel) this.form.kelurahan = kel.replace(/.*(kelurahan|kel\/desa|desa|kel\.)[:\s-]*/i, "").trim();

      const kec = lines.find(l => /kecamatan/i.test(l));
      if (kec) this.form.kecamatan = kec.replace(/.*kecamatan[:\s-]*/i, "").trim();

      // === Agama ===
      const agamaLine = lines.find(l => /agama/i.test(l));
      if (agamaLine) {
        const match = agamaLine.match(/agama[:\s\-]*([a-zA-Z]+)/i);
        if (match) this.form.agama = match[1];
      }

      // === STATUS ===
      const statusLine = lines.find(l => /status perkawinan|perkawinan|status/i.test(l));
      if (statusLine) {
        const match = statusLine.match(/(status perkawinan|perkawinan|status)[:\s\-]*([a-zA-Z]+)/i);
        if (match) this.form.status = match[2];
      }

      // === PEKERJAAN ===
      const kerja = lines.find(l => /pekerjaan/i.test(l));
      if (kerja) this.form.pekerjaan = kerja.replace(/.*pekerjaan[:\s-]*/i, "").trim();

      // === KEWARGANEGARAAN ===
      const kew = lines.find(l => /kewarganegaraan|wni|warga negara/i.test(l));
      if (kew) this.form.kewarganegaraan = kew.replace(/.*(kewarganegaraan|wni|warga negara)[:\s-]*/i, "").trim();
    },

    // --- util ---
    normalizeCapital(str) {
      if (!str) return "";
      return str.toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
    },

    extractDate(text) {
      const match = text.match(/(\d{1,2})[^\d](\d{1,2})[^\d](\d{4})/);
      if (!match) return "";
      return `${match[3]}-${match[2].padStart(2,"0")}-${match[1].padStart(2,"0")}`;
    },

    submitForm() {
      alert("Data terkirim!");
      console.log("Data:", this.form);
    }
  }
};
</script>

<style>
.container {
  max-width: 600px;
}

form input {
  display: block;
  width: 100%;
  margin-bottom: 12px;
  padding: 8px;
}

button {
  padding: 10px 20px;
  cursor: pointer;
}

/* BOX JSON */
.json-box {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 8px;
  white-space: pre-wrap;
  font-size: 14px;
  border: 1px solid #ccc;
  margin-top: 20px;
}
</style>
