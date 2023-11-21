<template>
  <v-app>
    <v-app-bar app color=indigo>
      <h2>    Pokemon Rec </h2>
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
html {
  scrollbar-width: none; /* For Firefox */
  -ms-overflow-style: none; /* For Internet Explorer and Edge */
}
html::-webkit-scrollbar {
  width: 0px; /* For Chrome, Safari, and Opera */
}
</style>

