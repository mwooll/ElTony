<template>
  <v-row>
    <!-- Dropdown menu for selecting opponent type -->
    <v-col cols="12">
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

    <!-- Recommend Team Button -->
    <v-col cols="12">
      <v-btn @click="recommendTeam" color="primary">Recommend Team</v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data: () => ({
    recommendedPokemon: [],
    teamImages: [],
    opponentType: null, // Default opponent type is null
    opponentTypes: ['No specific opponent','Normal' , 'Fire', 'Water', 'Electric', 'Grass', 'Ice', 'Fighting', 'Poison',
      'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Dark',
      'Steel', 'Fairy' ], // Add your opponent types here
  }),

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
</style>