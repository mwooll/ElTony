<template>
  <div>
    <v-row align="center" justify="center" className="mt-1 mb-0">
      <h3> Cluster Information </h3>
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
        // Replace the URL with your actual endpoint
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

        // Render the scatter plot with the fetched data
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
        width: 400, // Set the desired width
        height: 400,
        xaxis: {
          title: 'PCA1',
          aspectratio: {
            // Set the aspect ratio to make it quadratic
            x: 1,
            y: 1,
          },
        },
        yaxis: {
          title: 'PCA2',
          aspectratio: {
            // Set the aspect ratio to make it quadratic
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

      document.getElementById('PCAScatter').on('plotly_click', (data) => {
        const pointIndex = data.points[0].pointIndex;
        const selectedPokemonStats = {
          name: this.clusterInfo.name[pointIndex],
          cluster: this.clusterInfo.typeColor[pointIndex],
          pca1: this.clusterInfo.x[pointIndex],
          pca2: this.clusterInfo.y[pointIndex],
        };
        // Do something with selectedPokemonStats
        console.log('Selected Pokemon Stats:', selectedPokemonStats);
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