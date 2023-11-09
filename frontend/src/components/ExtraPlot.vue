<template>
  <div>
    <v-row align="center" justify="center" class="mt-1 mb-0">
      <h3>Averages for {{ $props.selectedCategory }} Companies</h3>
    </v-row>
    <div style="height: 80vh">
      <div id='myExtraPlot' style="height: inherit"></div>
    </div>
  </div>
</template>


<script>
import Plotly from 'plotly.js/dist/plotly';
export default {
  name: 'ExtraPlot',
  props: [
    'selectedCategory',
    'selectedYear'
  ],

  watch: {
    selectedCategory: function() {
      this.refetchData()
    },
    selectedYear: function() {
      this.refetchData()
    }
  },

  data: () => ({
    ExtraPlotData: {x: [], y: [], name: [], category: [], color: [], symbol: [],
                    avgEmployees: {"all": 0, "tech": 0, "health": 0, "bank": 0},
                    avgProfit: {"all": 0, "tech": 0, "health": 0, "bank": 0}
    },
    colors: {"tech": "orange", "health": "purple", "bank": "green", "all": "rgba(0.1, 0.1, 1, 1)"},
    symbols: {"tech": "star", "health": "cross", "bank": "square"},
    minYRange: {"all": null, "tech": null, "health": null, "bank": null},
    maxYRange: {"all": null, "tech": null, "health": null, "bank": null},
    minXRange: {"all": null, "tech": null, "health": null, "bank": null},
    maxXRange: {"all": null, "tech": null, "health": null, "bank": null}
  }),
  mounted() {
    this.getPlotRangeForCategory()
  },

  methods: {
    getPlotRangeForCategory: async function () {
      // req URL to retrieve companies from backend
      var reqUrl = 'http://127.0.0.1:5000/companies?category=' + this.$props.selectedCategory
      //console.log("ReqURL " + reqUrl)

      let yRanges = {"all": [], "tech": [], "health": [], "bank": []}
      let xRanges = {"all": [], "tech": [], "health": [], "bank": []}

      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();

      responseData.forEach((company) => {
        company.profit.forEach((tuple) => {
          let profit = tuple["value"]
          yRanges[company.category].push(profit)
          yRanges["all"].push(profit)
        })
        xRanges[company.category].push(company.employees)
        xRanges["all"].push(company.employees)
      })

      let categories = ["all", "tech", "health", "bank"]
      categories.forEach((cat) => {
        let yMin = Math.min.apply(null, yRanges[cat])
        let yMax = Math.max.apply(null, yRanges[cat])
        let yDif = (yMax - yMin)/20
        this.minYRange[cat] = yMin - yDif
        this.maxYRange[cat] = yMax + yDif

        let xMin = Math.min.apply(null, xRanges[cat])
        let xMax = Math.max.apply(null, xRanges[cat])
        let xDif = xMax - xMin
        this.minXRange[cat] = xMin - xDif/60
        this.maxXRange[cat] = xMax + xDif/5
      })

      this.fetchData()
    },

    refetchData() {
      this.ExtraPlotData.x = [];
      this.ExtraPlotData.y = [];
      this.ExtraPlotData.name = [];
      this.ExtraPlotData.category = [];
      this.ExtraPlotData.color = [];
      this.ExtraPlotData.symbol = [];
      this.ExtraPlotData.avgEmployees = {"all": 0, "tech": 0, "health": 0, "bank": 0};
      this.ExtraPlotData.avgProfit = {"all": 0, "tech": 0, "health": 0, "bank": 0};
      this.fetchData();
    },

    fetchData: async function () {
      // req URL to retrieve companies from backend
      var reqUrl = 'http://127.0.0.1:5000/companies?category=' + this.$props.selectedCategory
      //console.log("ReqURL " + reqUrl)

      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();

      // transform data to usable by scatter plot
      responseData.forEach((company) => {
        this.ExtraPlotData.name.push(company.name)

        var cat = company.category
        this.ExtraPlotData.category.push(cat)

        var employ = company.employees
        this.ExtraPlotData.x.push(employ)
        this.ExtraPlotData.avgEmployees[cat] += employ

        var profit = company.profit[2021 - this.selectedYear].value
        this.ExtraPlotData.y.push(profit)
        this.ExtraPlotData.avgProfit[cat] += profit
      })
      let categoriesSet = new Set(this.ExtraPlotData.category)

      // calculate the sum for all categories
      if (this.$props.selectedCategory === "all") {
        categoriesSet.forEach((cat) => {
          this.ExtraPlotData.avgEmployees["all"] += this.ExtraPlotData.avgEmployees[cat]
          this.ExtraPlotData.avgProfit["all"] += this.ExtraPlotData.avgProfit[cat]
        })
        categoriesSet.add("all")
      }

      // divide the sums to get averages
      categoriesSet.forEach((cat) => {
        let numCompanies = (cat === "all") ? 15 : 5
        this.ExtraPlotData.avgEmployees[cat] /= numCompanies
        this.ExtraPlotData.avgProfit[cat] /= numCompanies
      })

      // assign color and symbol based on category
      this.stylizeMarkers()

      // after the data is loaded, draw the plot
      this.drawExtraPlot(categoriesSet)
    },

    stylizeMarkers() {
      this.ExtraPlotData.category.forEach((cat) => {
            this.ExtraPlotData.color.push(this.colors[cat])
            this.ExtraPlotData.symbol.push(this.symbols[cat])
          }
      )
    },

    drawExtraPlot(categoriesSet) {
      var trace1 = {
        x: this.ExtraPlotData.x,
        y: this.ExtraPlotData.y,
        mode: 'markers',
        type: 'scatter',
        name: "", // hides "trace0" when hovering
        marker: {
          color: this.ExtraPlotData.color,
          symbol: this.ExtraPlotData.symbol,
          size: 10,
        },
        hovertemplate: '<b>%{text}</b>' +
            '<br>employees: %{x}' +
            '<br>profit ' + this.selectedYear + ': %{y}',
        text: this.ExtraPlotData.name,
      }
      const data = [trace1];

      let steps = 100
      let yRange = this.numberRange(
          this.minYRange[this.selectedCategory],
          this.maxYRange[this.selectedCategory],
          steps)
      categoriesSet.forEach((cat) => {
        let employeeLine = {
          x: Array(steps).fill(this.ExtraPlotData.avgEmployees[cat]),
          y: yRange,
          mode: "lines",
          name: "",
          line: {
            color: this.colors[cat],
            width: 1,
            dash: (cat === "all") ? "dot" : "dash"
          },
          hovertemplate: "<b>" + cat + "</b><br>average employees: %{x:$.2f}",
          text: "skip"
        }
        data.push(employeeLine)

        let xRange = this.numberRange(
            this.minXRange[this.selectedCategory],
            this.maxXRange[this.selectedCategory],
            steps)
        let profitLine = {
          x: xRange,
          y: Array(steps).fill(this.ExtraPlotData.avgProfit[cat]),
          mode: "lines",
          name: "",
          line: {
            color: this.colors[cat],
            width: 1,
            dash: (cat === "all") ? "dot" : "dash"
          },
          category: cat,
          hovertemplate: "<b>" + cat + "</b><br>average profit " + this.selectedYear + ": %{y:$.2f}",
          text: "skip"
        }
        data.push(profitLine)
      })

      var layout = {
        xaxis: {
          title: "Employees",
          type: "log"
        },
        yaxis: {
          title: "Profit for " + this.selectedYear,
          type: "linear",
          range: [this.minYRange[this.selectedCategory],
            this.maxYRange[this.selectedCategory]]
        },
        showlegend: false,
      }
      var config = {
        responsive: true,
        displayModeBar: false,
      }
      Plotly.newPlot('myExtraPlot', data, layout, config);
      this.clickExtraPlot()
    },

    numberRange(start, end, steps) {
      let value = start
      let range = []
      let stepSize = (end - start) / steps
      for (let i = 0; i < steps; i++) {
        value += stepSize
        range.push(value)
      }
      return range
    },

    clickExtraPlot() {
      var pn = 0
      var that = this
      var myPlot = document.getElementById('myExtraPlot')
      myPlot.on('plotly_click', function (data) {
        if (data.points[0].curveNumber > 0) return
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
          var update = {
            marker: {
              color: colors,
              symbol: symbols,
              size: 10,
            }
          };
          Plotly.restyle('myExtraPlot', update);
        }
      });
    },
  }
}
</script>


<style>
body { margin: 0 !important; }
</style>