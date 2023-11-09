<template>
  <div>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3>Overview of {{ $props.selectedCategory }} Companies</h3>
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
    selectedCategory: function() {
      this.ScatterPlotData.x = [];
      this.ScatterPlotData.y = [];
      this.ScatterPlotData.name = [];
      this.ScatterPlotData.category = [];
      this.ScatterPlotData.color = [];
      this.ScatterPlotData.symbol = [];
      this.fetchData();
    }
  },

  data: () => ({
    ScatterPlotData: {x: [], y: [], name: [], category: [], color: [], symbol: []},
    colors: {"tech": "orange", "health": "purple", "bank": "green"},
    symbols: {"tech": "star", "health": "cross", "bank": "square"},
  }),
  mounted() {
    this.fetchData()
  },

  methods: {
    fetchData: async function () {
      // req URL to retrieve companies from backend
      var reqUrl = 'http://127.0.0.1:5000/companies?category=' + this.$props.selectedCategory
      //console.log("ReqURL " + reqUrl)

      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();
      // transform data to usable by scatter plot
      responseData.forEach((company) => {
        this.ScatterPlotData.x.push(company.founding_year)
        this.ScatterPlotData.y.push(company.employees)
        this.ScatterPlotData.name.push(company.name)
        this.ScatterPlotData.category.push(company.category)
      })
      // assign color and symbol based on category
      this.stylizeMarkers()

      // after the data is loaded, draw the plot
      this.drawScatterPlot()
    },

    stylizeMarkers() {
      this.ScatterPlotData.category.forEach((cat) => {
        this.ScatterPlotData.color.push(this.colors[cat])
        this.ScatterPlotData.symbol.push(this.symbols[cat])}
      )
    },

    drawScatterPlot() {
      var trace1 = {
        x: this.ScatterPlotData.x,
        y: this.ScatterPlotData.y,
        mode: 'markers',
        type: 'scatter',
        marker: {
          color: this.ScatterPlotData.color,
          symbol: this.ScatterPlotData.symbol,
          size: 10,
        },
        name: "",
        hovertemplate: '<b>%{text}</b>'+
                        '<br>Founding Year: %{x}' +
                        '<br>Employees: %{y}',
        text: this.ScatterPlotData.name,
      };
      var data = [trace1];
      var layout = {
        xaxis: {title: "Founding Year"},
        yaxis: {title: "Employees"}
      }
      var config = {
        responsive: true,
        displayModeBar: false,
      }
      Plotly.newPlot('myScatterPlot', data, layout, config);
      this.clickScatterPlot()
    },

    clickScatterPlot() {
      var pn = 0
      var that = this
      var myPlot = document.getElementById('myScatterPlot')
      myPlot.on('plotly_click', function (data) {
        for (var i = 0; i < data.points.length; i++) {

          // get the index of point
          pn = data.points[i].pointNumber;

          // get symbols
          var symbols = data.points[0].data.marker.symbol
          var offset = 0
          if (symbols.length <= 5) {
            offset = symbols[pn] === "square" ? 10 : (symbols[pn] === "cross" ? 5 : 0);
          }

          // emit event to change the currently selected company in the a) configuration panel
          // and b) update the Profit View
          that.$emit('changeCurrentlySelectedCompany', pn + 1 + offset)

          // get the colors
          var colors = []
          let symToCol = {"star": "orange", "cross": "purple", "square": "green"}
          symbols.forEach((sym) => {
                colors.push(symToCol[sym])
              }
          )

          // color the selected point blue
          colors[pn] = "blue";

          // update the marker and plot
          var update = {marker: {
              color: colors,
              symbol: symbols,
              size: 10,
            }};
          Plotly.restyle('myScatterPlot', update);
        }
      });
    }
  }
}
</script>


<style>
  body { margin: 0 !important; }
</style>