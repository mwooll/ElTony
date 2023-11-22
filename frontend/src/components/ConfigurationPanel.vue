<template>
  <div>
    <v-container fluid>
      <v-row>
        <!-- Filters column -->
        <v-col cols="12" md="6" lg="3" class="sideBar">
          <v-col cols="12" sm="12">
              <div class="control-panel-font">Filters</div>
            </v-col>
          <v-col cols="12" sm="12">
              <v-select
                  :items="pokemons.values"
                  label="Select a Pokemon"
                  dense
                  v-model="pokemons.selectedValue"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="12">
              <v-select
                  :items="types.values"
                  label="Type"
                  multiple
                  v-model="filters.type"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="12">
              <v-select
                  :items="legendary.values"
                  label="Legendary"
                  dense
                  v-model="filters.legendary"
              ></v-select>
            </v-col>
            <v-col cols="12" sm="12">
              <v-select
                  :items="colors.values"
                  label="Color"
                  multiple
                  v-model="filters.color"
              ></v-select>
            </v-col>
        </v-col>

        <!-- Top left -->
        <v-col cols="12" md="6" lg="3">
          
        </v-col>

        <!-- Top right -->
        <v-col cols="12" md="6" lg="3">
          
        </v-col>
      </v-row>

      <v-row>
        <!-- Scatter plot -->
        <v-col cols="12" md="6" lg="3">
          <ScatterPlot :key="scatterPlotId"
                       :selectedCategory="categories.selectedValue"
                       @pokemonSelected="handlePokemonSelection"
                       :data="scatterPlotData"
          />
        </v-col>

        <!--Spider Chart -->
        <v-col cols="12" md="6" lg="3" class = "spiderchart">
          <SpiderPlot :pokemonStats="selectedPokemonStats"
                      :series="formattedSeriesForRadarChart"
          />
        </v-col>

        <!-- Bottom right -->
        <v-col cols="12" md="6" lg="3">

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
      selectedValue: 'all',
    },
    companies: {
      values: [],
      selectedValue: "alphabet",
    },
    algorithm: {
      values: ['none', 'random', 'regression'],
      selectedValue: 'none',
    },
    pokemons: {
      values: [],
      selectedValue: null,
    },
    year: {
      values: [2017, 2018, 2019, 2020, 2021],
      selectedValue: 2021,
    },
    filters: {
      type: [],
      legendary: null,
      color: [],
    },
    types: {
      values: ['Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison',
        'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark',
        'Steel', 'Fairy' ],
    },
    legendary: {
      values: ['TRUE', 'FALSE'],
    },
    colors: {
      values: ['Black','Blue','Brown','Green', 'Grey','Pink', 'Purple','Red','White','Yellow'],
    },
    scatterPlotData: { x: [], y: [], name: [] },
    filteredData: [],
  }),

  mounted() {
    this.fetchData()
  },
  watch: {
    // Watch for changes in the filters and update the data
    filters: {
      handler(newFilters) {
        // Do any additional processing if needed
        console.log('Filters have been updated:', newFilters);

        // Call the function to apply filters when filters are updated
        this.applyFilters();
      },
      deep: true, // This is important for deep watching the properties of the object
    },
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

    async applyFilters() {
      // Apply filters and fetch filtered data
      try {


        const filterResponse = await fetch('http://127.0.0.1:5000/api/filter', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ params: this.filters }),
        });

        if (!filterResponse.ok) {
          throw new Error(`HTTP error! Status: ${filterResponse.status}`);
        }

        const filteredData = await filterResponse.json();

        this.scatterPlotData = { x: [], y: [], name: [] };

        filteredData.forEach((pokemon) => {
          this.scatterPlotData.x.push(pokemon.Attack);
          this.scatterPlotData.y.push(pokemon.Defense);
          this.pokemons.values.push(pokemon.Name)
        })
        this.drawScatterPlot();
        // Update scatter plot with filtered data
      } catch (error) {
        console.error('Error applying filters:', error);
      }
    },

    updateScatterPlot() {
      this.fetchData();
    },
  },
};
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
  height: 40vh;
}

.spiderchart {
  justify-content: center;
  align-items: center;
  height: calc(50vh);
  overflow: hidden;
}
</style>