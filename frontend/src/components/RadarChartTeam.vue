<template>
  <v-btn icon class="expand-button" @click="expandPlot">
    <v-icon>mdi-fullscreen</v-icon>
  </v-btn>
  <v-row align="center" justify="center" className="mt-1 mb-0">
    <h3 align = "center">Average Stats for Recommended Team</h3>
  </v-row>
  <div>
    <div id="mySpiderPlotTeam" style="height: inherit"></div>
  </div>
</template>

<script>
import Plotly from 'plotly.js/dist/plotly';
import axios from 'axios';

export default {
  name: 'SpiderPlotTeam',
  data() {
    return {
      pokemonStats: null,
    };
  },
  mounted() {
    setInterval(this.fetchTeamStats, 1000);
  },
  methods: {
    async fetchTeamStats() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/teamstats');
        this.teamStats = response.data;
        this.drawSpiderPlot(this.teamStats);
      } catch (error) {
        console.error('Error fetching team stats:', error);
      }
    },
    drawSpiderPlot(stats) {
      var data = [{
        type: 'scatterpolar',
        r: [stats.HP, stats.Attack, stats.Defense, stats.Sp_Atk, stats.Sp_Def, stats.Speed, stats.HP],
        theta: ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'HP'],
        fill: 'toself'
      }];

      var layout = {
        polar: {
          angularaxis: {rotation: 90},
          radialaxis: {
            visible: true,
            range: [0, 250]
          }
        },
        margin: {
          t: 30
        },
        showlegend: false
      };

      Plotly.newPlot('mySpiderPlotTeam', data, layout);
    }
  }
};
</script>

<style>
body {
  margin: 0 !important;
}
</style>
