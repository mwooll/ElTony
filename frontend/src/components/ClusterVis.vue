<template>
  <div>
    <v-row align="center" justify="center" className="mt-1 mb-0">
      <h3 align="center"> Cluster Information </h3>
    </v-row>
    <div id="PCAScatter" style="height: 400px;"></div>
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist';

export default {
  name: 'ClusterPlot',
  props: ['selectedCategory', 'highlightedPokemon'],
  watch: {
    highlightedPokemon: function (newPokemon) {
      this.selectedPokemonName = newPokemon;
      this.updateMarkerColors();
    },

  },
  data() {
    return {
      clusterData: [],
      clusterInfo: {
        x: [],
        y: [],
        name: [],
        typeColor: [],
      },
      selectedPokemonName: null,
    };
  },
  mounted() {
    setInterval(this.fetchData, 1000);

  },
  methods: {
    fetchData: async function () {
      try {
        var reqUrl = 'http://127.0.0.1:5000/cluster-info';
        const response = await fetch(reqUrl);
        const responseData = await response.json();
        this.clusterInfo.x = [];
        this.clusterInfo.y = [];
        this.clusterInfo.name = [];
        this.clusterInfo.typeColor = [];

        responseData.forEach((pokemon) => {
          this.clusterInfo.x.push(pokemon.PCA1);
          this.clusterInfo.y.push(pokemon.PCA2);
          this.clusterInfo.name.push(pokemon.Name);
        });

        this.drawScatterPCA();
      } catch (error) {
        console.error('Error fetching cluster information:', error);
      }
    },
    drawScatterPCA() {
      const markerColors = this.clusterInfo.name.map(name => (name === this.selectedPokemonName ? 'red' : 'grey'));
      const markerSize = this.clusterInfo.name.map(name => (name === this.selectedPokemonName ? 8 : 5));

      const trace1 = {
        x: this.clusterInfo.x,
        y: this.clusterInfo.y,
        mode: 'markers',
        type: 'scatter',
        marker: {
          size: markerSize,
          color: markerColors,
          line: {
            width: 1,
            color: 'black',
          },
        },
        name: '',
        hovertemplate: '<b>%{text}</b>' +
            '<br>PCA1: %{x}' +
            '<br>PCA2: %{y}',
        text: this.clusterInfo.name,
      };

      const data = [trace1];
      const layout = {
        width: 600,
        height: 600,
        xaxis: {
          title: 'PCA1',
          aspectratio: {
            x: 1,
            y: 1,
          },
        },
        yaxis: {
          title: 'PCA2',
          aspectratio: {
            x: 1,
            y: 1,
          },
        },
      };
      const config = {
        responsive: true,
        displayModeBar: false,
      };

      Plotly.newPlot('PCAScatter', data, layout, config);

      document.getElementById('PCAScatter').on('plotly_click', async (data) => {
        const pointIndex = data.points[0].pointIndex;
        const selectedPokemonName = this.clusterInfo.name[pointIndex];
        console.log('Selected Pokemon:', selectedPokemonName);
        try {
          const response = await fetch(`http://127.0.0.1:5000/pokemons/${selectedPokemonName}`);
          const additionalStats = await response.json();
          console.log('Selected Pokemon stats:', additionalStats);

          this.clusterData = [];

          this.clusterData.push({
            name: additionalStats.Name,
            hp: additionalStats.HP,
            attack: additionalStats.Attack,
            defense: additionalStats.Defense,
            spAtk: additionalStats.Sp_Atk,
            spDef: additionalStats.Sp_Def,
            speed: additionalStats.Speed,
            image: additionalStats.image,
          });

          this.$emit('pokemonSelectedCluster', this.clusterData);
          console.log('Event emitted:', this.clusterData);
        } catch (error) {
          console.error('Error fetching additional Pokemon data:', error);
        }
      });
    },
// Add a new method to update marker colors
    updateMarkerColors() {
      const markerColors = this.clusterInfo.name.map(name => (name === this.selectedPokemonName ? 'red' : 'grey'));
      const markerSize = this.clusterInfo.name.map(name => (name === this.selectedPokemonName ? 8 : 5));

      const updatedTrace = {
        marker: {
          size: markerSize,
          color: markerColors,
        },
      };

      Plotly.react('PCAScatter', [updatedTrace]);
    },

  },
};
</script>

<style scoped>
#PCAScatter {
  width: 100%;
}
</style>