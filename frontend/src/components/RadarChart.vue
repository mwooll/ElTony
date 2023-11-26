<template>
  <v-btn icon class="expand-button" @click="expandPlot">
      <v-icon>mdi-fullscreen</v-icon>
    </v-btn>  
    <v-row align="center" justify="center" className="mt-1 mb-0">
    <h3 align = "center">Pokemon comparison</h3>
  </v-row>
    <div>
    <div id="mySpiderPlot" style="width: 100%; height: 100%; margin-top: 0px;" class="spiderplot"></div>
    </div>
    
  <v-row class="additional-info">
    <v-col cols="6" class="info-square left-square">
      <v-img :src="getPokemonImage(pokemonStats.image)" height="100" width="100"></v-img>
      <p>{{ pokemonStats.name }}</p>

    </v-col>
    <v-col cols="6" class="info-square right-square">
      <v-row align="center" justify="center" class="mt-1 mb-0">
        <p>{{ clusterStats.name }}</p>
      </v-row>
    </v-col>
  </v-row>
  </template>

  <script>
  import Plotly from 'plotly.js/dist/plotly';

  export default {
    name: 'SpiderPlot',
    props: ['pokemonStats', 'clusterStats'], // Add 'clusterStats' as a prop
    watch: {
      pokemonStats: function(newStats) {
        // Call drawSpiderPlot with both sets of stats
        this.drawSpiderPlot(newStats, this.clusterStats);
      },
      clusterStats: function(newCluster) {
        // Call drawSpiderPlot with both sets of stats
        this.drawSpiderPlot(this.pokemonStats, newCluster);
      },
    },

    mounted() {
    this.drawSpiderPlot(this.pokemonStats, this.clusterStats);
    },

    methods: {

      getPokemonImage(imageName) {
          if (imageName) {
            return require(`@/assets/poke_images/${imageName}`);
          }
          return ''; // Fallback image or an empty string if no image is available
        },
        
      drawSpiderPlot(stats, clusterStats) {
        // Check if both sets of stats are available
        if (!stats || !clusterStats) {
          return;
        }

        var data = [
          {
            type: 'scatterpolar',
            r: [stats.hp, stats.attack, stats.defense, stats.spAtk, stats.spDef, stats.speed],
            theta: ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
            fill: 'toself',
            name: 'Original Pokemon',
            line: { color: 'indigo' },
          },
          {
            type: 'scatterpolar',
            r: [clusterStats.hp, clusterStats.attack, clusterStats.defense, clusterStats.spAtk, clusterStats.spDef, clusterStats.speed],
            theta: ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
            fill: 'toself',
            name: 'Cluster Pokemon',
            line: { color: 'yellow' }, // Change the color of the second trace
          },
        ];

        var layout = {
          
          margin: {
            t: 30  // Top margin, increase this value to add more space above the chart
          },

          polar: {
            angularaxis: { rotation: 90 },
            radialaxis: {
              visible: true,
              range: [0, 250],
            },
          },
          paper_bgcolor: 'rgba(0,0,0,0)',  // Transparent background for the whole chart
          plot_bgcolor: 'rgba(0,0,0,0)',  
          showlegend: true,
          legend: {
            orientation: "h", // Set legend orientation to horizontal
            x: 0.5, // Center the legend horizontally
            xanchor: "center",
            y: -0.2, // Position the legend below the chart
            yanchor: "bottom"
          },      
        };

        Plotly.newPlot('mySpiderPlot', data, layout);
      },
    },
  };
  </script>

<style>
body {
  margin: 0 !important;
}

.info-square {
  width: 235px; /* Square size */
  height:240px; /* Square size */
  background-color: #ddd; /* Square color */
  /* Add more styling as needed */
}

.right-square {
  background-color: #c51b1b;
}

.spiderplot {
  margin-top: 20x;
}

</style>