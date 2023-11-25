<template>
  <v-dialog v-model="dialog" persistent>
      <v-card>
        <v-card-title align="center">Welcome to our Pokemon Recommentation Dashboard</v-card-title>
        <v-card-text align="center">
          The dashboard consists of 5 components
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  <v-dialog v-model="isScatterPlotExpanded" fullscreen>
    <ScatterPlot
      :key="scatterPlotId"
      :selectedCategory="pokemons.selectedValue"
      @pokemonSelected="handlePokemonSelection"
      :data="scatterPlotData"
      :isExpanded="isScatterPlotExpanded"
    />
  </v-dialog>

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
      <SidebarPoke :style="{ marginTop: '80px' }" @toggle-sidebar="handleSidebarToggle" @openDialog="dialog = true"/>
      <ConfigurationPanel :style="{ marginLeft: '220px', marginTop: '15px' }" @expandScatterPlot="handleExpandPlot"/>
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
      dialog: true,
      isScatterPlotExpanded: false,

      pokemons: {
        values: [], // Assuming this is an array
        selectedValue: null, // or a default value
      },
    };

    
  },

  methods: {
    handleExpandPlot() {
      console.log(this.scatterPlotData); // Check the data being passed
      this.isScatterPlotExpanded = true;
    },

    handlePokemonSelection(stats) {
      this.selectedPokemonStats = stats;
    },
    handleClusterSelection(stats) {
      this.selectedClusterStats = stats;
    },
    fetchData: async function () {
      // req URL to retrieve pokemons from backend
      var reqUrl = 'http://127.0.0.1:5000/pokemons'
      console.log("ReqURL " + reqUrl)

      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();

      this.scatterPlotData = {x: [], y: [], name: []};

      // transform data
      responseData.forEach((pokemon) => {
        this.scatterPlotData.x.push(pokemon.Attack);
        this.scatterPlotData.y.push(pokemon.Defense);
        this.pokemons.values.push(pokemon.Name)
      })
    },

    async applyFilters() {
      // Apply filters and fetch filtered data
      try {


        const filterResponse = await fetch('http://127.0.0.1:5000/api/filter', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ params: this.filters }),
        });

        if (!filterResponse.ok) {
          throw new Error(`HTTP error! Status: ${filterResponse.status}`);
        }

        const filteredData = await filterResponse.json();

        this.scatterPlotData = { x: [], y: [], name: [] };

        filteredData.forEach((pokemon) => {
          this.scatterPlotData.x.push(pokemon.Attack);
          this.scatterPlotData.y.push(pokemon.Defense);
          this.pokemons.values.push(pokemon.Name)
        })
        this.drawScatterPlot();
        // Update scatter plot with filtered data
      } catch (error) {
        console.error('Error applying filters:', error);
      }
    },

    updateScatterPlot() {
      this.fetchData();
    },
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

