<template>
  <div>
    <v-row align="center" justify="center" className="mt-1 mb-0">
      <h3 align = "center"> Cluster Information </h3>
    </v-row>
    <div id="PCAScatter" style="height: 400px;"></div>
  </div>
</template>


<script>
import Plotly from 'plotly.js-dist';

export default {
  name: 'ClusterPlot',
  props: ['SelectedCluster'],

  watch: {
    selectedCategory: function () {
      this.clusterInfo.x = [];
      this.clusterInfo.y = [];
      this.clusterInfo.name = [];
      this.clusterInfo.typeColor = [];
      this.fetchData();
    }
  },

  data() {
    return {
      clusterData:{
        name: [],
        hp: [],
        attack:[] ,
        defense:[] ,
        spAtk:[] ,
        spDef:[] ,
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
      const trace1 = {
        x: this.clusterInfo.x,
        y: this.clusterInfo.y,
        mode: 'markers',
        type: 'scatter',
        marker: {
          size: 5,
          color: this.clusterInfo.typeColor,
        },
        name: '',
        hovertemplate: '<b>%{text}</b>' +
            '<br>PCA1: %{x}' +
            '<br>PCA2: %{y}',
        text: this.clusterInfo.name,
      };

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

      Plotly.newPlot('PCAScatter', data, layout, config);
      document.getElementById('PCAScatter').on('plotly_click', async (data) => {
        const pointIndex = data.points[0].pointIndex;
        const selectedPokemonName = this.clusterInfo.name[pointIndex];

        try {
          const response = await fetch(`http://127.0.0.1:5000/pokemon/${selectedPokemonName}`);
          const additionalStats = await response.json();

          this.$set(this.clusterData, selectedPokemonName, {
            name: additionalStats.name,
            hp: additionalStats.hp,
            attack: additionalStats.attack,
            defense: additionalStats.defense,
            spAtk: additionalStats.spAtk,
            spDef: additionalStats.spDef,
            speed: additionalStats.speed,
          });

          this.$emit('pokemonSelectedCluster', this.clusterData);
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