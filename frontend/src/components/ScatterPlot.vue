<template>
  <div style="width: 100%; height: 100%;">
    <v-btn icon class="expand-button" @click="expandPlot">
      <v-icon>mdi-fullscreen</v-icon>
    </v-btn>
    <v-row align="center" justify="center" className="mt-1 mb-0">
      <h3 align="center"> Attack/Defense </h3>
    </v-row>
    <div style="height: 50vh">
      <div id="myScatterPlot" style="width: 100%; height: 100%;"></div>
    </div>
  </div>

</template>


<script>
import Plotly from 'plotly.js/dist/plotly';

export default {
  name: 'ScatterPlot',
  props: {
    selectedCategory: {
      type: String,
      default: ''
    },
    isExpanded(newValue) {
      if (newValue) {
        this.$nextTick(() => {
          this.drawScatterPlot(); // Re-render the plot after the dialog opens
        });
      }
    }
  },

  data() {
    return {
      ScatterPlotData: {
        x: [],
        y: [],
        name: [],
        Type_1: [],
        hp: [],
        attack: [],
        defense: [],
        spAtk: [],
        spDef: [],
        speed: [],
        image: [],
      },
    };
  },

  mounted() {
    setInterval(this.fetchData, 1000);
  },

  methods: {
    expandPlot() {
      this.$emit('expandPlotEvent');
    },

    fetchData: async function () {
      var reqUrl = 'http://127.0.0.1:5000/pokemons';
      const response = await fetch(reqUrl);
      const responseData = await response.json();

      this.ScatterPlotData.x = [];
      this.ScatterPlotData.y = [];
      this.ScatterPlotData.name = [];
      this.ScatterPlotData.Type_1 = [];

      responseData.forEach((pokemon) => {
        this.ScatterPlotData.x.push(pokemon.Attack);
        this.ScatterPlotData.y.push(pokemon.Defense);
        this.ScatterPlotData.name.push(pokemon.Name);
        this.ScatterPlotData.Type_1.push(pokemon.Type_1);
        this.ScatterPlotData.hp.push(pokemon.HP);
        this.ScatterPlotData.attack.push(pokemon.Attack);
        this.ScatterPlotData.defense.push(pokemon.Defense);
        this.ScatterPlotData.spAtk.push(pokemon.Sp_Atk);
        this.ScatterPlotData.spDef.push(pokemon.Sp_Def);
        this.ScatterPlotData.speed.push(pokemon.Speed);
        this.ScatterPlotData.image.push(pokemon.image);
      });

      this.drawScatterPlot();
    },

    drawScatterPlot() {
      // Predefined color mapping for Type_1
      const typeColorMapping = {
        'Fire': '#EE8130',
        'Normal': '#A8A77A',
        'Water': '#6390F0',
        'Electric': '#F7D02C',
        'Grass': '#7AC74C',
        'Ice': '#96D9D6',
        'Fighting': '#C22E28',
        'Poison': '#A33EA1',
        'Ground': '#E2BF65',
        'Flying': '#A98FF3',
        'Psychic': '#F95587',
        'Bug': '#A6B91A',
        'Rock': '#B6A136',
        'Ghost': '#735797',
        'Dragon': '#6F35FC',
        'Dark': '#708090',
        'Steel': '#705746',
        'Fairy': '#D685AD',
      };

      // Map Type_1 to predefined colors
      const colors = this.ScatterPlotData.Type_1.map(type => typeColorMapping[type] || '#ccc');

      const uniqueTypes = [...new Set(this.ScatterPlotData.Type_1)];

      // Create a trace for each unique type
      const traces = uniqueTypes.map((type) => {
        const filteredIndices = this.ScatterPlotData.Type_1.reduce((acc, curr, i) => {
          if (curr === type) {
            acc.push(i);
          }
          return acc;
        }, []);

        return {
          x: filteredIndices.map(i => this.ScatterPlotData.x[i]),
          y: filteredIndices.map(i => this.ScatterPlotData.y[i]),
          mode: 'markers',
          type: 'scatter',
          marker: {
            size: 5,
            color: colors[filteredIndices[0]],
          },
          name: type,
          hovertemplate: `<b>%{text}</b>` +
              `<br>Attack: %{x}` +
              `<br>Defense: %{y}`,
          text: filteredIndices.map(i => this.ScatterPlotData.name[i]),
        };
      });

      var layout = {
        xaxis: {
          title: "Attack",
          showgrid: false,
        },
        yaxis: {
          title: "Defense",
          showgrid: false,
        },
        margin: {
          t: 30
        },
        showlegend: true
      };

      var config = {
        responsive: true,
        displayModeBar: false,
      };

      Plotly.newPlot('myScatterPlot', traces, layout, config);
    },
  },
};
</script>




<style>
body {
  margin: 0 !important;
  background-color: transparent;
}

h3 {
  color: indigo
  
}

.expand-button {
  top: 0;
  right: 0;
  z-index: 10;
}

</style>
