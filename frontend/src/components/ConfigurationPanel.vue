<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col md="2" class="sideBar">
            <v-row>
              <v-col cols="12" sm="12">
                <div class="control-panel-font">Company Overview</div>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="12">
                <v-select
                    :items="categories.values"
                    label="Select a category"
                    dense
                    v-model="categories.selectedValue"
                ></v-select>

              </v-col>
            </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <div class="control-panel-font">Profit View of Company</div>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-select
                  :items="companies.values"
                  label="Select a company"
                  dense
                  v-model="companies.selectedValue"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-select
                  :items="year.values"
                  label="Select a year"
                  dense
                  v-model="year.selectedValue"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-select
                  :items="algorithm.values"
                  label="Select an algorithm"
                  dense
                  v-model="algorithm.selectedValue"
              ></v-select>
            </v-col>
          </v-row>
        </v-col>

        <v-col md="3">
          <ScatterPlot :key="scatterPlotId"
                       :selectedCategory="categories.selectedValue"
                       @changeCurrentlySelectedCompany="changeCompanyId"
          />
        </v-col>
        <v-col md="3">
          <LinePlot :key="linePlotId"
                    :selectedCompanyName="companies.selectedValue"
                    :selectedAlgorithm="algorithm.selectedValue"/>
        </v-col>
        <v-col md="4">
          <ExtraPlot :key="extraPlotId"
                     :selectedCategory="categories.selectedValue"
                     :selectedAlgorithm="algorithm.selectedValue"
                     :selectedYear="year.selectedValue"
                     @changeCurrentlySelectedCompany="changeCompanyId"
          />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>

import ScatterPlot from './ScatterPlot';
import LinePlot from './LinePlot';
import ExtraPlot from "./ExtraPlot.vue";

export default {
  components: {ScatterPlot, LinePlot, ExtraPlot},
  data: () => ({
    scatterPlotId: 0,
    linePlotId: 0,
    extraPlotId: 0,
    columnWidth: "11",

    categories: {
      values: ['all', 'tech', 'health', 'bank'],
      selectedValue: 'all'
    },
    companies: {
      values: [],
      selectedValue: "alphabet"
    },
    algorithm: {
      values: ['none', 'random', 'regression'],
      selectedValue: 'none'
    },
    year: {
      values: [2017, 2018, 2019, 2020, 2021],
      selectedValue: 2021
    }
  }),

  mounted() {
    this.fetchData()
  },

  methods: {
    changeCompanyId(companyId) {
      this.companies.selectedValue = this.companies.values[companyId-1]
      //this.linePlotId += 1 // why do we need this?
    },

    fetchData: async function () {
      // req URL to retrieve companies from backend
      var reqUrl = 'http://127.0.0.1:5000/companies?category=' + this.categories.selectedValue
      console.log("ReqURL " + reqUrl)

      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();

      // transform data
      responseData.forEach((company) => {
        this.companies.values.push(company.name)
      })
    },
  }


}

</script>

<style scoped>
.control-panel-font {
  font-family: "Open Sans", verdana, arial, sans-serif;
  align-items: center;
  font-size: 15px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  font-weight: 500;
  height: 40px;
}
.sideBar {
  border-right: 1px solid rgba(0, 0, 0, 0.1);
  background: #f0f0ffff;
  padding-left: 17px;
  height: calc(100vh - 72px);
}
</style>
