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

  data() {
    return {
      clusterData: [],
      clusterData2: {
        name: [],
        hp: [],
        attack: [],
        defense: [],
        spAtk: [],
        spDef: [],
        speed: [],
      },
      clusterInfo: {
        x: [],
        y: [],
        name: [],
        typeColor: [],
      },
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
          this.clusterInfo.typeColor.push(pokemon.Cluster);
        });

        this.drawScatterPCA();
      } catch (error) {
        console.error('Error fetching cluster information:', error);
      }
    },

    drawScatterPCA() {
      // Initialize the trace with default values
      const trace1 = {
        x: this.clusterInfo.x,
        y: this.clusterInfo.y,
        mode: 'markers',
        type: 'scatter',
        marker: {
          size: 5,
          color: this.clusterInfo.typeColor,
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

      // Check if highlightedPokemon is set
      if (this.highlightedPokemon) {
        // Find the index of the highlightedPokemon in the cluster
        console.log(this.highlightedPokemon)
        const highlightedIndex = this.clusterInfo.name.indexOf(this.highlightedPokemon);

        if (highlightedIndex !== -1) {
          // Modify the line properties for the highlighted Pokemon
          trace1.marker.line.width = 4;
          trace1.marker.line.color = 'red';

          // Use the modified trace for the highlighted point only
          const data = [trace1];
          const layout = {
            width: 400,
            height: 400,
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

          // Move Plotly initialization and event handling outside the conditional block
          Plotly.newPlot('PCAScatter', data, layout, config);

          document.getElementById('PCAScatter').on('plotly_click', async (data) => {
            const pointIndex = data.points[0].pointIndex;
            const selectedPokemonName = this.clusterInfo.name[pointIndex];
            console.log('Selected Pokemon:', this.clusterInfo.name[pointIndex]);
            try {
              const response = await fetch(`http://127.0.0.1:5000/pokemons/${selectedPokemonName}`);
              const additionalStats = await response.json();
              console.log('Selected Pokemon stats:', additionalStats);

              this.clusterData = [];

              // Reset clusterData object before adding data for the new selected point
              this.clusterData.push({
                name: additionalStats.Name,
                hp: additionalStats.HP,
                attack: additionalStats.Attack,
                defense: additionalStats.Defense,
                spAtk: additionalStats.Sp_Atk,
                spDef: additionalStats.Sp_Def,
                speed: additionalStats.Speed,
                image: additionalStats.image
              });

              this.$emit('pokemonSelectedCluster', this.clusterData);
              console.log('Event emitted:', this.clusterData);
            } catch (error) {
              console.error('Error fetching additional Pokemon data:', error);
            }
          });
          return; // Exit the method early after handling the highlighted Pokemon
        }
      }

      // If highlightedPokemon is not set or not found, use the default trace for all points
      const data = [trace1];
      const layout = {
        width: 400,
        height: 400,
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

      // Move Plotly initialization and event handling outside the conditional block
      Plotly.newPlot('PCAScatter', data, layout, config);

      document.getElementById('PCAScatter').on('plotly_click', async (data) => {
        const pointIndex = data.points[0].pointIndex;
        const selectedPokemonName = this.clusterInfo.name[pointIndex];
        console.log('Selected Pokemon:', this.clusterInfo.name[pointIndex]);
        try {
          const response = await fetch(`http://127.0.0.1:5000/pokemons/${selectedPokemonName}`);
          const additionalStats = await response.json();
          console.log('Selected Pokemon stats:', additionalStats);

          this.clusterData = [];

          // Reset clusterData object before adding data for the new selected point
          this.clusterData.push({
            name: additionalStats.Name,
            hp: additionalStats.HP,
            attack: additionalStats.Attack,
            defense: additionalStats.Defense,
            spAtk: additionalStats.Sp_Atk,
            spDef: additionalStats.Sp_Def,
            speed: additionalStats.Speed,
            image: additionalStats.image
          });

          this.$emit('pokemonSelectedCluster', this.clusterData);
          console.log('Event emitted:', this.clusterData);
        } catch (error) {
          console.error('Error fetching additional Pokemon data:', error);
        }
      });
    },
  },
};
</script>

<style scoped>
#PCAScatter {
  width: 100%;
}
</style>