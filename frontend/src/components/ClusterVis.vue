<template>
  <div>
    <h2>Cluster Scatter Plot</h2>
    <div id="PCAScatter" style="height: 400px;"></div>
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist';

export default {
  data() {
    return {
      clusterInfo: null,
    };
  },
  mounted() {
    this.fetchClusterInfo();
  },
  methods: {
    async fetchClusterInfo() {
      try {
        // Fetch the cluster information from the API
        const response = await fetch('http://127.0.0.1:5000/cluster-info');
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        this.clusterInfo = await response.json();

        // Render the scatter plot with the fetched data
        this.drawScatterPCA();
      } catch (error) {
        console.error('Error fetching cluster information:', error);
      }
    },

    drawScatterPCA() {
      const trace1 = {
        x: this.clusterInfo.map(entry => entry.PCA1),
        y: this.clusterInfo.map(entry => entry.PCA2),
        mode: 'markers',
        type: 'scatter',
        marker: {
          size: 5,
          color: this.clusterInfo.map(entry => entry.Cluster),
        },
        name: '',
        hovertemplate: '<b>%{text}</b>' +
            '<br>PCA1: %{x}' +
            '<br>PCA2: %{y}',
        text: this.clusterInfo.map(entry => entry.Name),
      };

      const data = [trace1];
      const layout = {
        xaxis: { title: 'PCA1' },
        yaxis: { title: 'PCA2' },
      };
      const config = {
        responsive: true,
        displayModeBar: false,
      };

      Plotly.newPlot('PCAScatter', data, layout, config);

      document.getElementById('PCAScatter').on('plotly_click', (data) => {
        const pointIndex = data.points[0].pointIndex;
        const selectedPokemonStats = {
          name: this.clusterInfo[pointIndex].Name,
          cluster: this.clusterInfo[pointIndex].Cluster,
          pca1: this.clusterInfo[pointIndex].PCA1,
          pca2: this.clusterInfo[pointIndex].PCA2,
        };
        // Do something with selectedPokemonStats
        console.log('Selected Pokemon Stats:', selectedPokemonStats);
      });
    },
  },
};
</script>

<style scoped>
#myScatterPlot {
  width: 100%;
}
</style>