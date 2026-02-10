<template>
  <div>
    <input type="file" @change="onFileChange" />
  </div>
</template>

<script setup>
import { defineEmits } from "vue";

const emit = defineEmits(["file-selected"]);

function onFileChange(event) {
  emit("file-selected", event.target.files[0]);
}
</script>
