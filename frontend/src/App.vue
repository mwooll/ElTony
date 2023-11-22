<template>
  <v-app>
    <v-app-bar app color=indigo>
      <h2 class="header1">  Pokemon Rec </h2>
    </v-app-bar>
    <v-main>
      <ConfigurationPanel/>
    </v-main>
  </v-app>
</template>


<script>
import ConfigurationPanel from './components/ConfigurationPanel'

export default {
  name: 'App',

  components: {
    ConfigurationPanel,
  },

  data: () => ({
  }),
}
</script>

<style>
/* disable scrolling */
html, body {
  scrollbar-width: none; /* For Firefox */
  -ms-overflow-style: none; /* For Internet Explorer and Edge */
  max-height: 100vh; 
  overflow-y: hidden;
}
html::-webkit-scrollbar {
  width: 0px; /* For Chrome, Safari, and Opera */
}
.header1 {
  margin-left: 0.5cm;
}
</style>

