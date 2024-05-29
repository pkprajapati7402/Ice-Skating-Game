#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <time.h>

#define MAX_WORDS 10
#define MAX_WORD_LENGTH 20
#define MAX_ATTEMPTS 6

char *words[MAX_WORDS] = {"programming", "hangman", "computer", "keyboard", "software", "algorithm", "developer", "variable", "function", "language"};
char secretWord[MAX_WORD_LENGTH];
char guessedWord[MAX_WORD_LENGTH];
int attemptsLeft;



//hangman is a number guessing console based game, do play and enjoy the game. Thank You

// Initialize the game
void initializeGame() {
    srand(time(NULL));
    int randomIndex = rand() % MAX_WORDS;
    strcpy(secretWord, words[randomIndex]);
    strcpy(guessedWord, secretWord);
    for (int i = 0; i < strlen(guessedWord); i++) {
        guessedWord[i] = '_';
    }
    attemptsLeft = MAX_ATTEMPTS;
}

// Display the current state of the game
void displayGame() {
    printf("\nSecret word: %s\n", guessedWord);
    printf("Attempts left: %d\n", attemptsLeft);
}

// Check if the guessed letter is present in the word
int checkGuess(char guess) {
    int found = 0;
    for (int i = 0; i < strlen(secretWord); i++) {
        if (secretWord[i] == guess) {
            guessedWord[i] = guess;
            found = 1;
        }
    }
    return found;
}

int main() {
    
    char guess;
    int gameWon = 0;

    // Initialize the game
    initializeGame();

    // Game loop
    while (attemptsLeft > 0 && !gameWon) {
        displayGame();

        // Get user input
        printf("Enter your guess: ");
        scanf(" %c", &guess);
        guess = tolower(guess);

        // Check if the guessed letter is correct
        if (checkGuess(guess)) {
            printf("Correct guess!\n");
        } else {
            attemptsLeft--;
            printf("Incorrect guess! Attempts left: %d\n", attemptsLeft);
        }

        // Check if the word is guessed completely
        if (strcmp(secretWord, guessedWord) == 0) {
            gameWon = 1;
            printf("\nCongratulations! You guessed the word: %s\n", secretWord);
        }
    }

    // Display the result
    if (!gameWon) {
        printf("\nGame over! You ran out of attempts. The word was: %s\n", secretWord);
    }

    return 0;
}
