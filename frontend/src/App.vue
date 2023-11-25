<template>
  <v-app>
    <v-app-bar app fixed color="teal-darken-4" image="@/assets/pokelogo.png" class="app-bar">
      <template v-slot:image>
          <v-img
            gradient="to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)"
          ></v-img>
        </template>

      <v-spacer></v-spacer>
      <h2 class="header1">Pokemon Recommendation Platform
      </h2>
      <v-spacer></v-spacer>
    </v-app-bar>
    <v-main>
      <SidebarPoke :style="{ marginTop: '60px' }" @toggle-sidebar="handleSidebarToggle"/>
      <ConfigurationPanel :style="{ marginLeft: computedMargin, marginTop: appBarHeight }"/>
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
      collapsed: false,
      sidebarWidthExpanded: '200px',
      sidebarWidthCollapsed: '55px',
    };

    
  },

  methods: {
    handleSidebarToggle(collapsedState) {
      this.collapsed = collapsedState; 
    },
  },

  computed: {
    computedMargin() {
      // Adjust the margin based on the sidebar's collapsed state
      return this.collapsed ? '55px' : '200px';
    }
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
    width: 200px; /* Example width */
  }
  .config-panel {
    margin-left: 200px; /* Same as sidebar width */
  }
  .content {
    margin-left: 200px; /* Adjusted based on sidebar width */
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
  height: 60px; /* Set the app bar height to match your v-app-bar height */
}
</style>

