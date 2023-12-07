<template>
  <div>
    <v-container fluid class="container">
      <v-row class="rows">
        <!-- Left: Scatter Plot -->
        <v-col cols="12" md="6" lg="4" class="columns">
          <ScatterPlot
              :key="scatterPlotId"
              :selectedCategory="pokemons.selectedValue"
              @pokemonSelected="handlePokemonSelection"
              :data="scatterPlotData"
              @expandPlotEvent="handleExpandPlot"
          />
        </v-col>

        <!-- Middle: Radar Chart  -->
        <v-col cols="12" md="6" lg="4" class="columns">
          <v-row>
            <v-col>
              <SpiderPlot
                  :pokemonStats="selectedPokemonStats"
                  :cluster-stats="selectedClusterStats"
                  :series="formattedSeriesForRadarChart"
                  @reset-data="handleReset"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <SpiderPlotTeam
                  v-if="recommendedPokemon.length > 0"
              />
            </v-col>
          </v-row>
        </v-col>

        <!-- Right: Team Section -->
        <v-col cols="12" md="12" lg="4" class="columns">
          <v-col mb="2">

          <TeamSection @recommendationMade="updateRecommendedPokemon" @navigateToPokemonDetails="handleNavigateToPokemon" />
          </v-col >
          <v-col>

          <ClusterVis
                  v-if="recommendedPokemon.length > 0"
                  :key="PCAScatter"
                  :selectedCategory="pokemons.selectedValue"
                  @pokemonSelectedCluster="handleClusterSelection"
                  :data="scatterPlotData"
                  :highlightedPokemon="highlightedPokemon"
              />
          </v-col>


        </v-col>
      </v-row>
    </v-container>
  </div>
</template>


<script>
import ScatterPlot from './ScatterPlot';
import SpiderPlot from "./RadarChart.vue";
import SpiderPlotTeam from "./RadarChartTeam.vue"
import TeamSection from './TeamSection.vue';
import ClusterVis from './ClusterVis'; // Import ClusterVis component

export default {
  components: {ScatterPlot, SpiderPlot, SpiderPlotTeam,TeamSection,ClusterVis},
  data: () => ({
    recommendedPokemon: [],

    scatterPlotId: 0,
    PCAScatter: 0,
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
    selectedClusterStats: {
      name:0,
      hp: 0,
      attack: 0,
      defense: 0,
      spAtk: 0,
      spDef: 0,
      speed: 0,
    },
    pokemons: {
      values: [],
      selectedValue: null,
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
    highlightedPokemon:null
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
    updateRecommendedPokemon(recommendedPokemon) {
      this.recommendedPokemon = recommendedPokemon;
    },

    handleNavigateToPokemon(pokeName) {
      // Update the highlighted Pokemon
      this.highlightedPokemon = pokeName;
    },

    handleReset() {
      this.selectedPokemonStats = {
        hp: 0,
        attack: 0,
        defense: 0,
        spAtk: 0,
        spDef: 0,
        speed: 0,
      };
      this.selectedClusterStats = {
        name: 0,
        hp: 0,
        attack: 0,
        defense: 0,
        spAtk: 0,
        spDef: 0,
        speed: 0,
      };
    },

    handleExpandPlot() {
      // You can emit another event that App.vue will listen to
      this.$emit('expandScatterPlot');

    },
    showFullPagePlot() {
    },

    handlePokemonSelection(stats) {
      this.selectedPokemonStats = stats;
    },
    handleClusterSelection(stats) {
      console.log('Cluster selection stats:', stats);
      this.selectedClusterStats = stats[0];
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

.columns {
  border: 1px solid indigo;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}


</style>
