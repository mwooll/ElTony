<template>
  <div>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3>Profit View of Company: {{ this.selectedCompanyName }}</h3>
    </v-row>
    <div style="height: 80vh">
      <div id='myLinePlot' style="height: inherit"></div>
    </div>
  </div>
</template>



<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
  name: "LinePlot",
  props: [
    "selectedCompanyName",
    "selectedAlgorithm"
  ],

  watch: {
    selectedCompanyName() {
      //console.log("name changed")
      this.companyId = this.companies.indexOf(this.selectedCompanyName)+1
      this.refetchData()
    },
    selectedAlgorithm() {
      //console.log("algorithm changed")
      this.refetchData()
    },
  },

  data: () => ({
    LinePlotData: {x: [], y: [], color: [], symbol: []},
    companyId: null,
    companies: []
  }),
  mounted() {
    //console.log("mounting")
    this.companyId = 1
    this.fetchCompanies()
    this.fetchData()
  },

  methods: {
    async fetchCompanies() {
      // req URL to retrieve companies from backend
      var reqUrl = 'http://127.0.0.1:5000/companies?category=all'
      console.log("ReqURL " + reqUrl)

      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();

      // transform data
      responseData.forEach((company) => {
        this.companies.push(company.name)
      })
    },

    async fetchData() {
      // req URL to retrieve single company from backend
      var reqUrl = 'http://127.0.0.1:5000/companies/' + this.companyId +
          '?algorithm=' + this.$props.selectedAlgorithm
      //console.log("ReqURL " + reqUrl)

      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();
      //console.log(responseData)

      // transform data to usable by line plot
      responseData.profit.forEach((profit) => {
        this.LinePlotData.x.push(profit.year)
        this.LinePlotData.y.push(profit.value)
      })
      // assign color and symbol based on year
      this.LinePlotData.x.forEach((year) => {
        switch (year) {
          case 2022:
            this.LinePlotData.color.push("red")
            this.LinePlotData.symbol.push("star-diamond")
            break;
          default:
            this.LinePlotData.color.push("blue")
            this.LinePlotData.symbol.push("circle")
        }
      })

      // draw the line plot after the data is transformed
      this.drawLinePlot()
    },

    refetchData() {
      this.LinePlotData.x = [];
      this.LinePlotData.y = [];
      this.LinePlotData.color = [];
      this.LinePlotData.symbol = [];
      this.fetchData();
    },

    drawLinePlot() {
      var trace1 = {
        x: this.LinePlotData.x,
        y: this.LinePlotData.y,
        type: 'scatter',
        name: "",
        marker: {
          color: this.LinePlotData.color,
          symbol: this.LinePlotData.symbol,
          size: 10
        },
        hovertemplate: (this.LinePlotData.x === 2022 ? "estimate": "") + "%{x}: %{y}"
      };
      var data = [trace1];
      var layout = {
        xaxis: {title: "Year"},
        yaxis: {title: "Profit"}
      }
      var config = {responsive: true, displayModeBar: false}
      Plotly.newPlot('myLinePlot', data, layout, config);
    }

  }
}
</script>



<style>
  body { margin: 0 !important; }
</style>