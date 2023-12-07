<template>
  <div class="container">
    <v-row align="center" justify="center" className="mt-1 mb-0">
      <h3 class="team-title" align = "center">Get a Team Recommendation</h3>
    </v-row>
    <v-row>
      <!-- Dropdown menu for selecting opponent type -->
      <v-col cols="12" class="typeselection">
        <v-select
            v-model="opponentType"
            :items="opponentTypes"
            label="Select Opponent Type"
            @input="setOpponentType"
        ></v-select>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" class="recommend-row">
        <v-btn @click="recommendTeam" color="yellow">Recommend Team</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <!-- Team images with name, key feature, and swap button -->
      <v-col v-for="(pokemon, index) in recommendedPokemon" :key="index" cols="4">
        <v-row align="center" justify="center">
          <div @click="navigateToPokemonDetails(pokemon)">
            <v-img :src="getPokemonImage(pokemon.image)" height="120" width="120" align="center"></v-img>
          </div>
        </v-row>
        <v-row align="center" justify="center">
          <div class="pokemon-details-wrapper">
            <!-- Pokemon details container -->
            <div class="pokemon-details" :class="getPokemonTypeClass(pokemon.Types)">
              <p>{{ pokemon.Name }}</p>
              <p>{{ displayType(pokemon.Types) }}</p>
              <p>{{ pokemon.Key_Feature }}</p>
              <!-- Swap button -->
              <v-btn @click="swapPokemon(pokemon)" color="primary" class="swap" icon fab><v-icon>
                mdi-swap-horizontal
              </v-icon></v-btn>
            </div>
          </div>

        </v-row>
      </v-col>
    </v-row>

    <v-row v-if="swapButtonClicked">
      <v-select
          v-model="selectedOtherPokemon"
          :items="otherPokemonsInCluster"
          label="Select Pokémon to Swap"
      ></v-select>
      <v-btn @click="confirmSwap()" color="primary">Confirm Swap</v-btn>
    </v-row>
  </div>
</template>

<script>

export default {

  data() {
    return {
      currentPokemon:null,
      selectedOtherPokemon: null,
      otherPokemonsInCluster: [],
      swapButtonClicked: false,
      recommendedPokemon: [],
      teamImages: [],
      opponentType: null, // Default opponent type is null
      opponentTypes: ['No specific opponent', 'Fire','Normal', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison',
        'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark',
        'Steel', 'Fairy' ], // Add your opponent types here
    };
  },

  methods: {
    getPokemonTypeClass(type) {
      const typeClasses = {
        Fire: 'fire-background',
        Normal: 'normal-background',
        Water: 'water-background',
        Electric: 'electric-background',
        Grass: 'grass-background',
        Ice: 'ice-background',
        Fighting: 'fighting-background',
        Poison: 'poison-background',
        Ground: 'ground-background',
        Flying: 'flying-background',
        Psychic: 'psychic-background',
        Bug: 'bug-background',
        Rock: 'rock-background',
        Ghost: 'ghost-background',
        Dragon: 'dragon-background',
        Dark: 'dark-background',
        Steel: 'steel-background',
        Fairy: 'fairy-background',
      };

      // Default class if type not found
      const defaultClass = 'default-background';

      // Split types if necessary and get the class for the first type
      if (typeof type === 'string' && type.trim() !== '') {
        // Split types and get the class for the first type
        const firstType = type.split(',')[0].trim();
        return typeClasses[firstType] || defaultClass;
      } else {
        console.error('Invalid type:', type);
        return defaultClass;
      }
    },
    displayType(typing) {
      let splitted = typing.split(",")
      console.log(splitted)
      if (splitted[1] == "nan") {
        return splitted[0]
      }
      return splitted[0] + ", " + splitted[1]
    },
    navigateToPokemonDetails(pokemon) {

      this.$emit('navigateToPokemonDetails', pokemon.Name);
      this.$emit('highlightSelectedPokemon', pokemon.Name);


      console.log(`Clicked on ${pokemon.Name}. Redirect to details page.`);
    },

    getPokemonImage(imageName) {
      if (imageName) {
        // Construct the image path based on the image name
        const imagePath = require(`@/assets/poke_images/${imageName}`);
        return imagePath;
      }
      const imagePath = require(`@/assets/pokeball.png`);
      return imagePath; // Fallback image or an empty string if no image is available
    },


    async swapPokemon(pokemon) {
      try {
        // Identify the name of the Pokémon to be swapped out
        const pokemonToSwapOut = pokemon.Name;
        this.currentPokemon = pokemon.Name;
        // Fetch data for the selected Pokemon
        const response = await fetch(`http://127.0.0.1:5000/othersInCluster`);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        // Find the data for the selected Pokemon
        const selectedPokemonData = data.find(item => item.Recommended_Pokemon === pokemonToSwapOut);

        // Update otherPokemonsInCluster with the data
        this.otherPokemonsInCluster = selectedPokemonData
            ? selectedPokemonData.Other_Pokemon_In_Cluster
            : [];

        // Check if the current pokemonName is in the otherPokemonsInCluster
        const isPokemonInCluster = this.otherPokemonsInCluster.length > 0;

        if (!isPokemonInCluster) {
          console.warn(`${pokemonToSwapOut} is not found in the cluster.`);
        }

        // Set swapButtonClicked to true
        this.swapButtonClicked = true;
        // Send the data to the backend

      } catch (error) {
        console.error('Error swapping Pokémon:', error);
      }
    },

    async sendSwapPokemonData(pokemonToSwapOut, selectedOtherPokemon) {
      try {
        // Make a POST request to your backend endpoint
        const response = await fetch('http://127.0.0.1:5000/api/swapPokemon', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            pokemonToSwapOut,selectedOtherPokemon
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const recommendation = await response.json();
        console.log(recommendation); // Log the result from the backend
        this.swapButtonClicked = false;
        // You can handle the result from the backend as needed

      } catch (error) {
        console.error('Error sending :', error);
      }
    },

    async confirmSwap() {
      try {
        const pokemonToSwapOut = this.currentPokemon;
        console.log(`Swap ${pokemonToSwapOut} with ${this.selectedOtherPokemon}`)

        await this.sendSwapPokemonData(pokemonToSwapOut, this.selectedOtherPokemon);
        this.recommendTeam()
      } catch (error) {
        console.error('Error sending swap data to the backend:', error);
      }
    },


    setOpponentType(opponentTeamType) {
      this.opponentType = opponentTeamType;
    },
    async recommendTeam() {
      try {

        const recommendationResponse = await fetch('http://127.0.0.1:5000/api/recommend', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            opponentType: this.opponentType,
          }),
        });

        if (!recommendationResponse.ok) {
          throw new Error(`HTTP error! Status: ${recommendationResponse.status}`);
        }

        const recommendedPokemon = await recommendationResponse.json();
        this.$emit('recommendationMade', recommendedPokemon);

        this.recommendedPokemon = recommendedPokemon;


      } catch (error) {
        console.error('Error recommending team:', error);
      }
    },

  }
};
</script>

<style scoped>
.team-title {
  margin-top: 40px;
  margin-bottom: 10px;
}

.recommend-row {
  display: flex;
  justify-content: center;
  align-items: center;
}

.container {
//display: flex;
  justify-content: center;
  align-items: center;
//flex-direction: column;
}
.swap{
  margin-top: 5px;
  width: 36px;
  height: 36px;
  min-width: 24px;
  min-height: 24px;
}
.team-image {
  margin-bottom: 10px;
}
.pokemon-details-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 120px; /* Set the desired height for consistency */
}

.pokemon-details {
  background-color: rgba(255, 255, 255, 0.8);
  text-align: center;
  font-size: small;
  padding: 12px;
  border-radius: 10px;
  width: 100px;
  height: 120px;
}

.image-container {
  width: 140px; /* Adjust width as needed */
  height: auto; /* Height will adjust to maintain aspect ratio */
  margin: auto;
}
.typeselection {
  margin-bottom: -20px;
}

/* Flexbox to position the Recommend Team button */
.pokemon-row {
  display: flex;
  flex-wrap: wrap;
}


.fire-background {
  background-color: #EE8130; /* Fire */
}

.normal-background {
  background-color: #A8A77A; /* Normal */
}

.water-background {
  background-color: #6390F0; /* Water */
}

.electric-background {
  background-color: #F7D02C; /* Electric */
}

.grass-background {
  background-color: #7AC74C; /* Grass */
}

.ice-background {
  background-color: #96D9D6; /* Ice */
}

.fighting-background {
  background-color: #C22E28; /* Fighting */
}

.poison-background {
  background-color: #A33EA1; /* Poison */
}

.ground-background {
  background-color: #E2BF65; /* Ground */
}

.flying-background {
  background-color: #A98FF3; /* Flying */
}

.psychic-background {
  background-color: #F95587; /* Psychic */
}

.bug-background {
  background-color: #A6B91A; /* Bug */
}

.rock-background {
  background-color: #B6A136; /* Rock */
}

.ghost-background {
  background-color: #735797; /* Ghost */
}

.dragon-background {
  background-color: #6F35FC; /* Dragon */
}

.dark-background {
  background-color: #705746; /* Dark */
}

.steel-background {
  background-color: #708090; /* Steel */
}

.fairy-background {
  background-color: #D685AD; /* Fairy */
}

/* Default color if type not found */
.default-background {
  background-color: #ccc;
}

</style>