<template>
  <div>
    <v-row align="center" justify="center" className="mt-1 mb-0">
      <h3>Attacke/Defense </h3>
    </v-row>
    <div style="height: 80vh">
      <div id='myScatterPlot' style="height: inherit"></div>
    </div>
  </div>
</template>


<script>
import Plotly from 'plotly.js/dist/plotly';

export default {
  name: 'ScatterPlot',
  props: [
    'selectedCategory'
  ],

  watch: {
    selectedCategory: function () {
      this.ScatterPlotData.x = [];
      this.ScatterPlotData.y = [];
      this.ScatterPlotData.name = [];
      this.ScatterPlotData.category = [];
      this.ScatterPlotData.color = [];
      this.ScatterPlotData.symbol = [];
      this.fetchData();
    }
  },

  data() {
    return {
      ScatterPlotData: {
        x: [],
        y: [],
        name: [],
        typeColor: [],
        hp: [],
        attack: [],
        defense: [],
        spAtk: [],
        spDef: [],
        speed: []
      },
    };
  },
  mounted() {
    setInterval(this.fetchData, 1000);
  },

  methods: {
    fetchData: async function () {
      var reqUrl = 'http://127.0.0.1:5000/pokemons';
      const response = await fetch(reqUrl);
      const responseData = await response.json();

      this.ScatterPlotData.x = [];
      this.ScatterPlotData.y = [];
      this.ScatterPlotData.name = [];

      responseData.forEach((pokemon) => {
        this.ScatterPlotData.x.push(pokemon.Attack);
        this.ScatterPlotData.y.push(pokemon.Defense);
        this.ScatterPlotData.name.push(pokemon.Name);
        this.ScatterPlotData.typeColor.push(pokemon.TypeColor);
        this.ScatterPlotData.hp.push(pokemon.HP);
        this.ScatterPlotData.attack.push(pokemon.Attack);
        this.ScatterPlotData.defense.push(pokemon.Defense);
        this.ScatterPlotData.spAtk.push(pokemon.Sp_Atk);
        this.ScatterPlotData.spDef.push(pokemon.Sp_Def);
        this.ScatterPlotData.speed.push(pokemon.Speed);
      });

      this.drawScatterPlot();
    },

    stylizeMarkers() {
      this.ScatterPlotData.category.forEach((cat) => {
            this.ScatterPlotData.color.push(this.colors[cat])
            this.ScatterPlotData.symbol.push(this.symbols[cat])
          }
      )
    },

    drawScatterPlot() {
      var trace1 = {
        x: this.ScatterPlotData.x, // Attack
        y: this.ScatterPlotData.y, // Defense
        mode: 'markers',
        type: 'scatter',
        marker: {
          size: 10,
          color: this.ScatterPlotData.typeColor,
        },
        name: "",
        hovertemplate: '<b>%{text}</b>' +
            '<br>Attack: %{x}' +
            '<br>Defense: %{y}',
        text: this.ScatterPlotData.name, // Name of the Pokemon
      };
      var data = [trace1];
      var layout = {
        xaxis: {title: "Attack"},
        yaxis: {title: "Defense"}
      };
      var config = {
        responsive: true,
        displayModeBar: false,
      };
      Plotly.newPlot('myScatterPlot', data, layout, config);

      document.getElementById('myScatterPlot').on('plotly_click', function (data) {
        var pointIndex = data.points[0].pointIndex;
        this.selectedPokemonStats = {
          hp: this.ScatterPlotData.hp[pointIndex],
          attack: this.ScatterPlotData.attack[pointIndex],
          defense: this.ScatterPlotData.defense[pointIndex],
          spAtk: this.ScatterPlotData.spAtk[pointIndex],
          spDef: this.ScatterPlotData.spDef[pointIndex],
          speed: this.ScatterPlotData.speed[pointIndex],
        };
        this.$emit('pokemonSelected', this.selectedPokemonStats);
      }.bind(this));
    },


  }
}
</script>


<style>
body {
  margin: 0 !important;
}
</style>