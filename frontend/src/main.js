import { createApp } from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import Vue from 'vue';
import VueApexCharts from 'vue-apexcharts';

loadFonts()

createApp(App)
  .use(vuetify)
  .mount('#app')

  Vue.use(VueApexCharts);

Vue.component('apex-chart', VueApexCharts);