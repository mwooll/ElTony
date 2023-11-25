<template>
    <div class="sidebar" :style="{ width: sidebarWidth }">
      <h1>
        <span v-if="collapsed">
          <i class="fa-solid fa-filter"></i>
        </span>
        <span v-else> Filters </span>
      </h1>  
      <span v-if="collapsed">
      </span>
        <span v-else> 
          <v-col cols="12" sm="12" class="filters">
            <v-select
                  :items="types.values"
                  label="Type"
                  multiple
                  v-model="filters.type"
              ></v-select>
            </v-col> 
      </span>
      <span v-if="collapsed">
      </span>
        <span v-else> 
          <v-col cols="12" sm="12" class="filters">
            <v-select
                  :items="legendary.values"
                  label="Legendary"
                  dense
                  v-model="filters.legendary"
              ></v-select>
            </v-col> 
      </span>
      <span v-if="collapsed">
      </span>
        <span v-else> 
          <v-col cols="12" sm="12" class="filters">
            <v-select
                  :items="colors.values"
                  label="Color"
                  multiple
                  v-model="filters.color"
              ></v-select>
            </v-col> 
      </span>
      <span v-if="collapsed">
      </span>
      <span v-else> 
      <v-btn color="primary" @click="resetFilters" class="button">Reset Filters
      </v-btn>
      </span>
      
      <span
        class="collapse-icon"
        :class="{ 'rotate-180': collapsed }"
        @click="toggleSidebar"
        >
        <i class="fas fa-angle-double-left" />
        </span>
    </div>

</template>

<script>
import { collapsed, toggleSidebar, sidebarWidth } from './state'

export default {
  props: {},
  components: { },
  setup() {
    return { collapsed, toggleSidebar, sidebarWidth }
  },
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

    resetFilters() {
            // Resetting each filter to its default value
            this.filters.type = [];
            this.filters.legendary = null;
            this.filters.color = [];
            // Add any other filters you need to reset

            // Optionally, you can also update the filtered data
            this.applyFilters();
    },

    handlePokemonSelection(stats) {
      this.selectedPokemonStats = stats;
    },
    handleClusterSelection(stats) {
      this.selectedClusterStats = stats;
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
}
</script>

<style>
:root {
    --sidebar-bg-color: #3F51B5;
}

.sidebar {
  color: white;
  background-color: var(--sidebar-bg-color);

  float: left;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  bottom: 0;
  padding: 0.5em;
  text-align: center;

  transition: 0.3s ease;

  display: flex;
  flex-direction: column;
}

.collapse-icon {
  position: absolute;
  bottom: 0;
  padding: 0.75em;

  color: rgba(255, 255, 255, 0.7);

  transition: 0.2s linear;
}

.rotate-180 {
  transform: rotate(180deg);
  transition: 0.2s linear;
}

.filters {
  position: center;
}

.button {
  margin-top: 10px
}
</style>