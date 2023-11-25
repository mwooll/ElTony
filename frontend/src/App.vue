<template>
  <v-app>
    <v-app-bar app fixed color="indigo" class="app-bar">
      <v-img 
        src="@/assets/pokelogo.png" 
        class="flex-grow-1"
        style="height: 200px; margin-top: 15px;"
      >
      </v-img>
    </v-app-bar>
    <v-main>
      <SidebarPoke :style="{ marginTop: '80px' }" @toggle-sidebar="handleSidebarToggle"/>
      <ConfigurationPanel :style="{ marginLeft: '220px', marginTop: '15px' }"/>
      <div class="content" :style="{ 'margin-left': sidebarWidth }">
        <router-view />
      </div>
    </v-main>
  </v-app>

</template>

<script>
import ConfigurationPanel from './components/ConfigurationPanel'
import '@fortawesome/fontawesome-free/js/all'
import SidebarPoke from "@/components/SidebarPoke"

export default {
  name: 'App',

  components: {
    ConfigurationPanel,
    SidebarPoke,
  },

  
  data() {
    return {
    };

    
  },

  methods: {
  },
}
</script>

<style>

html::-webkit-scrollbar {
  width: 0px; /* For Chrome, Safari, and Opera */
}
.header1 {
  margin-left: 0.5cm;
}

.sidebar {
    position: absolute;
    left: 0;
    width: 220px; /* Example width */
  }

  .main-content {
  /* Adjust this padding to match the height of your app bar */
  padding-top: 60px; /* Example height, adjust as needed */
}

html, body, #app, .v-application--wrap {
  margin: 0;
  padding: 0;
  height: 100%;
}

.app-bar {
  height: 80px; /* Set the app bar height to match your v-app-bar height */
}
</style>

