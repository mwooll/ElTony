<template>
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

    <!-- Team images with name and key feature -->
    <v-col v-for="(pokemon, index) in recommendedPokemon" :key="index" cols="2">
      <v-img
          :src="`/images/${pokemon.image}`"
          aspect-ratio="1"
          cover
          class="team-image"
      >
        <!-- Display the name and key feature below the image -->
        <div class="pokemon-details">
          <p>{{ pokemon.Name }}</p>
          <p>{{ pokemon.Types }}</p>
          <p>{{ pokemon.Key_Feature }}</p>
        </div>
      </v-img>
    </v-col>
    <v-col
      v-for="(photo, index) in photos"
      :key="index"
      class="d-flex child-flex"
      cols="4"
    >
    <div class="image-container">
      <v-img
        class="custom-image"
        :src="photo"
        :lazy-src="photo"
        aspect-ratio="1"
        cover
      >
        <template v-slot:placeholder>
          <v-row
            class="fill-height ma-0"
            align="center"
            justify="center"
          >
            <v-progress-circular
              indeterminate
              color="grey-lighten-5"
            ></v-progress-circular>
          </v-row>
        </template>
      </v-img>
    </div>
    </v-col>
    <!-- Recommend Team Button -->
    <v-col cols="12">
      <v-btn @click="recommendTeam" color="yellow">Recommend Team</v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data() {
    return {
      photos: [
        require('@/assets/images/1.png'),
        require('@/assets/images/2.png'),
        require('@/assets/images/3.png'),
        require('@/assets/images/4.png'),
        require('@/assets/images/5.png'),
        require('@/assets/images/6.png'),
      ],
      recommendedPokemon: [],
      teamImages: [],
      opponentType: null, // Default opponent type is null
      opponentTypes: ['No specific opponent', 'Fire','Normal', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison',
        'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark',
        'Steel', 'Fairy' ], // Add your opponent types here
    };
  },

    methods: {
      setOpponentType(opponentTeamType) {
        this.opponentType = opponentTeamType;
      },
    async recommendTeam() {
      try {
        // Check if opponentTeamType is selected, if not, set it to 'None'

        // Call the backend to get recommended Pokemon data based on filters or any other logic
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

        // Update the component's state with the recommended Pokemon
        this.recommendedPokemon = recommendedPokemon;

        // Fetch additional details (image and key feature) for recommended Pokemon
        await this.fetchPokemonDetails();

        // Update the teamImages array with the fetched image URLs
        this.teamImages = this.recommendedPokemon.map(pokemon => pokemon.image);
      } catch (error) {
        console.error('Error recommending team:', error);
      }
    },
    async fetchPokemonDetails() {
      for (const pokemon of this.recommendedPokemon) {
        const imageResponse = await fetch(`/images/${pokemon.image}`);
        const imageData = await imageResponse.blob();
        const imageUrl = URL.createObjectURL(imageData);

        // Update the Pokemon object with the image URL
        pokemon.image = imageUrl;
      }
    },

    
  },
};
</script>

<style scoped>
.team-image {
  margin-bottom: 10px;
}

.pokemon-details {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 8px;
  text-align: center;
}

.image-container {
  width: 140px; /* Adjust width as needed */
  height: auto; /* Height will adjust to maintain aspect ratio */
  margin: auto;
}
.typeselection {
  margin-bottom: -20px;
}
</style>