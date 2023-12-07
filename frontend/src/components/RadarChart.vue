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
      <v-row align="center" justify="center">
      <v-img :src="getPokemonImage(pokemonStats.image)" height="130" width="130" align="center" style="margin-top: 30px;"></v-img>
      </v-row>
      <p style="color:indigo; font-weight:bold" align="center">{{ pokemonStats.name }}</p>
    </v-col>
    <v-col cols="6" class="info-square right-square">
      <v-row align="center" justify="center">
      <v-img :src="getPokemonImage(clusterStats.image)" height="130" width="130" align="center" style="margin-top: 30px;"></v-img>
      </v-row>
        <p style="color:orange; font-weight:bold" align="center">{{ clusterStats.name }}</p>
    </v-col>
    <v-row align="center" justify="center">
    <v-btn color="yellow" @click="resetFilters" class="button" align="center">Reset
      </v-btn>
    </v-row>
  </v-row>
  </template>

  <script>
  import Plotly from 'plotly.js/dist/plotly';

  export default {
    name: 'SpiderPlot',
    props: ['pokemonStats', 'clusterStats'],
    watch: {
      pokemonStats: function(newStats) {
        // Call drawSpiderPlot
        this.drawSpiderPlot(newStats, this.clusterStats);
      },
      clusterStats: function(newCluster) {
        // Call drawSpiderPlot
        this.drawSpiderPlot(this.pokemonStats, newCluster);
      },
    },
    data: () => ({
      average: {
        hp: 68.38002773925103,
        attack: 75.01386962552012,
        defense: 70.80859916782246,
        spAtk: 68.7378640776699,
        spDef: 69.29126213592232,
        speed: 65.71428571428571
    },
    }),

    mounted() {
    this.drawSpiderPlot(this.pokemonStats, this.clusterStats);
    },

    methods: {
      resetFilters() {
        this.$emit('reset-data');
      },

      getPokemonImage(imageName) {
        if (imageName) {
          // Construct the image path based on the image name
          const imagePath = require(`@/assets/poke_images/${imageName}`);
          return imagePath;
        }
        const imagePath = require(`@/assets/pokeball.png`);
        return imagePath; // Fallback image or an empty string if no image is available
      },

      drawSpiderPlot(stats, clusterStats) {
        // Check if both sets of stats are available
        if (!stats || !clusterStats) {
          Plotly.newPlot('mySpiderPlot', [], {});
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
            text: [stats.hp, stats.attack, stats.defense, stats.spAtk, stats.spDef, stats.speed].map(String),
            hoverinfo: 'text',
          },
          {
            type: 'scatterpolar',
            r: [clusterStats.hp, clusterStats.attack, clusterStats.defense, clusterStats.spAtk, clusterStats.spDef, clusterStats.speed],
            theta: ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
            fill: 'toself',
            name: 'Cluster Pokemon',
            line: { color: 'orange' },
            text: [clusterStats.hp, clusterStats.attack, clusterStats.defense, clusterStats.spAtk, clusterStats.spDef, clusterStats.speed].map(String),
            hoverinfo: 'text', // Change the color of the second trace
          },

          {
            type: 'scatterpolar',
            r: [this.average.hp, this.average.attack, this.average.defense, this.average.spAtk, this.average.spDef, this.average.speed],
            theta: ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
            fill: 'toself',
            name: 'Average stats of Pokémon in the unfiltered set',
            line: { color: 'grey' },
            text: [this.average.hp, this.average.attack, this.average.defense, this.average.spAtk, this.average.spDef, this.average.speed].map(String),
            hoverinfo: 'text', // Change the color of the second trace
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
              range: [0, 175],
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
  height:190px; /* Square size */
  background-color: transparent; /* Square color */
  /* Add more styling as needed */
}

.right-square {
  background-color:transparent;
}

.spiderplot {
  margin-top: 20x;
}

.button {
  margin-top: 10px
}


</style>