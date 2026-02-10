// frontend/src/main.js
import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"

import vue3GoogleLogin from "vue3-google-login"

const app = createApp(App)

app.use(router)

app.use(vue3GoogleLogin, {
  clientId: "711011319246-8avfec3ucl9utgaqqj58l69gpg4tu12n.apps.googleusercontent.com"
})

app.mount("#app")
