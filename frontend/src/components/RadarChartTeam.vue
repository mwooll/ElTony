<template>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3> Team v Team </h3>
    </v-row>
    <div>
    <div id="mySpiderPlotTeam" style="height: inherit"></div>
    </div>
  </template>
  
  <script>
  import Plotly from 'plotly.js/dist/plotly';
  
  export default {
    name: 'SpiderPlotTeam',
    props: ['pokemonStats'],
    watch: {
      pokemonStats: function(newStats) {
        this.drawSpiderPlot(newStats);
      }
    },
    methods: {
      drawSpiderPlot(stats) {
        var data = [{
          type: 'scatterpolar',
          r: [stats.hp, stats.attack, stats.defense, stats.spAtk, stats.spDef, stats.speed],
          theta: ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed'],
          fill: 'toself'
        }];
        
        var layout = {
          polar: {
            angularaxis: { rotation: 90 },
            radialaxis: {
              visible: true,
              range: [0, 250]  
            }
          },
          showlegend: false
        };
        
        Plotly.newPlot('mySpiderPlotTeam', data, layout);
      }
    }
  }
  </script>

<style>
body {
  margin: 0 !important;
}

</style>