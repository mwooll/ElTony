<template>
  <v-dialog v-model="dialog" persistent>
      <v-card>
        <v-card-title align="center" style="color:indigo">Welcome to our Pokemon Recommentation Dashboard</v-card-title>
        <v-card-text >
          <p>Welcome to our data visualization app. This guide will help you navigate and utilize the app's features effectively for comprehensive data analysis.</p>
          <p>&nbsp;</p>
        <p><strong>Understanding the Interface:</strong> The app presents all visualization components on a single page for a seamless experience. The main area of the screen displays various data charts, while the sidebar is dedicated to filters that can be applied to these charts.</p>
        <p>&nbsp;</p> 
        <p><strong>Using Radar Charts:</strong> The radar chart, visible on the main screen, is excellent for comparing multiple variables. It displays data in a spider-web-like diagram, ideal for evaluating attributes of two specific pokemons. </p>
        <p>&nbsp;</p>
        <p><strong>Exploring Scatter Plots:</strong> Alongside the radar chart, you'll find the scatter plot. In here you will be able to see the relation between attack and defense of a pokemon. They are also colored by their type for an easier distinction.</p>
        <p>&nbsp;</p>
        <p><strong>Adjusting Filters via the Sidebar:</strong> Use the sidebar to refine the data displayed on your charts. Filters allow you to focus on specific data ranges, categories, or criteria, enhancing the relevance and precision of the visualizations.</p>
        <p>&nbsp;</p>
        <p><strong>Analyzing Team Data:</strong> For insights into team dynamics or performance, refer to the 'Team Stats' visualizations. Here you will be able to see how balanced your recommended team is and where there is place for improvement.</p>
        <p>&nbsp;</p>
        <p><strong>Cluster Visualization:</strong> The 'Cluster Vis' feature on the main screen helps in identifying patterns and clusters within large datasets. You will be able to see why a certain pokemon was chose, and which pokemons would have a similar effect on your team.</p>
        <p>&nbsp;</p>
        <p><strong>Interactive Features for Enhanced Analysis:</strong> The app is interactive, allowing you to hover over data points for detailed information or select a certain pokemon in the scatter plot to compare him in the spyder chart to the one that got recommended to you.</p>



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

