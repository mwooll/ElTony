<template>
  <div>
    <v-container fluid>
      <v-row>
        <v-col md="2" class="sideBar">
            <v-row>
              <v-col cols="12" sm="12">
                <div class="control-panel-font">Pokemon Overview</div>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" sm="12">
                <v-select
                    :items="pokemons.values"
                    label="Select a Pokemon"
                    dense
                    v-model="pokemons.selectedValue"
                ></v-select>

              </v-col>
            </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <div class="control-panel-font">Filters</div>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-select
                  label="Filter 1"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-select
                  label="Filter 2"
              ></v-select>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="12">
              <v-select
                  label="Filter 3"
              ></v-select>
            </v-col>
          </v-row>
        </v-col>

        <v-col md="4">
          <ScatterPlot :key="scatterPlotId"
                        :selectedCategory="categories.selectedValue"
                        @pokemonSelected="handlePokemonSelection"
          />
        </v-col>
        <v-col md="4">
          <SpiderPlot :pokemonStats="selectedPokemonStats"
                      :series="formattedSeriesForRadarChart"  
          />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>

import ScatterPlot from './ScatterPlot';
import SpiderPlot from "./RadarChart.vue";

export default {
  components: {ScatterPlot, SpiderPlot},
  data: () => ({
    scatterPlotId: 0,
    linePlotId: 0,
    extraPlotId: 0,
    columnWidth: "11",
    
    selectedPokemonStats: {
      hp: 0,
      attack: 0,
      defense: 0,
      spAtk: 0,
      spDef: 0,
      speed: 0,
    },

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
    pokemons: {
      values: [],
      selectedValue: null
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
    
    handlePokemonSelection(stats) {
    this.selectedPokemonStats = stats;
    },

    fetchData: async function () {
      // req URL to retrieve pokemons from backend
      var reqUrl = 'http://127.0.0.1:5000/pokemons'
      console.log("ReqURL " + reqUrl)

      // await response and data
      const response = await fetch(reqUrl)
      const responseData = await response.json();

      this.scatterPlotData = {x: [], y: [], name: []};

      // transform data
      responseData.forEach((pokemon) => {
        this.scatterPlotData.x.push(pokemon.Attack);
        this.scatterPlotData.y.push(pokemon.Defense);
        this.pokemons.values.push(pokemon.Name)
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
