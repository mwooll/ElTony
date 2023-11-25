<template>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3> Pokemon Comparison</h3>
    </v-row>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <p>{{ pokemonStats.name }}</p>
     </v-row>
  <v-row align="center" justify="center" class="mt-1 mb-0">
    <p>{{ clusterStats.name }}</p>
  </v-row>
    <div>
    <div id="mySpiderPlot" style="height: inherit"></div>
    </div>
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
    methods: {
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
          },
          {
            type: 'scatterpolar',
            r: [clusterStats.hp, clusterStats.attack, clusterStats.defense, clusterStats.spAtk, clusterStats.spDef, clusterStats.speed],
            theta: ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
            fill: 'toself',
            name: 'Cluster Pokemon',
            line: { color: 'orange' }, // Change the color of the second trace
          },
        ];

        var layout = {
          polar: {
            angularaxis: { rotation: 90 },
            radialaxis: {
              visible: true,
              range: [0, 250],
            },
          },
          showlegend: true, // Show legend to distinguish between the two traces
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
</style>