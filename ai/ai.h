#include <cmath>
#include <cstdint>
#include <cstdio>
#include <ctime>
#include <vector>

/*
The reason we are using (internally) a 8x8 board is because we are using an
uint64_t (so 64 bits long) variable to put the pieces in places. We
could use a 7*7 board or even a 7x6 but it would require to rework how the
pieces are handled, and it may slow down a lot the algorithm.
*/

#define NBR_LINE 6
#define NBR_COL 7
#define BOARDLEN 64
#define MAX_ALLOWED_HEIGHT 48
#define MAX_NBR_MOVE NBR_LINE*NBR_COL
#define SYMBOL_AI "x"
#define SYMBOL_HUMAN "o"
#define NOT_ALLOWED -1
#define SCORE_NOT_ALLOWED 42587268
#define SCORE_SOMEONE_WIN 10000
#define SIZE_VECT 8388593


// Adapted from PascalPons' connect 4 AI
class Table {
public:
    struct Entry {
        uint64_t id: 56;
        int8_t value;
    };
    std::vector<Entry> t;
    Table(): t(SIZE_VECT) {
    };

    void put(uint64_t id, int8_t value) {
        int i = id % SIZE_VECT;
        t[i].id = id;
        t[i].value = value;
    }

    int8_t get(uint64_t id) {
        int i = id % SIZE_VECT;
        if (t[i].id == id) {
            return t[i].value;
        } else {
            return 0;
        }
    }
};


/**
 * @brief The class that contains all information about the game
 * 
 */
class Game {
private:
    // Players variables
    int HUMAN = 1;
    int AI = ~HUMAN; // This way we are sure they are not the same
    int current_player = HUMAN; // Not used when in mode shared library

    // The depth of the current move
    int current_depth = 0;

    int8_t col_ordering[7] = {3, 4, 2, 5, 1, 6, 0};
    Table transTable; // Should reverse 2GB of memory

    // The bitboards for the two players
    uint64_t human_board = 0b0;
    uint64_t ai_board = 0b0;
    uint8_t col_heights[7] = {7, 6, 5, 4, 3, 2, 1};

    int count = 0; // This is used to know how many times something is done

    /**
     * @brief Place the new piece on the board
     * 
     * @param player The board representation
     * @param col The column in which we want to put the new piece
     * @param heights The list of the heights of the different columns
     * @return Return NOT_ALLOWED if the column is not valid (full or out of bound), or the column otherwise
     */
    int putPiece(uint64_t *player, const int col, uint8_t *heights);

    /**
     * @brief Remove the piece at the top of the column chosen
     * 
     * @param player The board representation
     * @param col The column we want to remove the piece
     * @param heights The list of the heights of the different columns
     */
    void removePiece(uint64_t *player, const int col, uint8_t *heights);

    /**
     * @brief Count the number of 1 in bitboard
     * 
     * @param bitboard The board representation
     * @return the number of 1
     */
    int countNbrOne(const uint64_t bitboard);

    /**
     * @brief Count the number of 4, 3, and 2 aligned disks
     * 
     * @param bitboard The board representation
     * @param state The state of the board (if winning or not)
     * @return the score associated with the bitboard
     */
    int countPoints(const uint64_t bitboard, bool *state);

    /**
     * @brief Compute if the bitboard passed is one of a winning state
     * 
     * @param bitboard  The board representation
     * @return true if the board have 4 token aligned
     * @return false in all other cases
     */
    bool quickWinning(const uint64_t bitboard);

    /**
     * @brief Compute the score of the board
     * 
     * @param bitboard The board representation
     * @param oppBitboard The opponent board representation
     * @param depth The depth at wich we are looking
     * @return The score computed
     */
    int evaluateBoard(const uint64_t bitboard, const uint64_t oppBitboard, const int depth);

    /**
     * @brief The negamax variant of the minimax algorithm
     * 
     * @param player The board representation of the player
     * @param opponent The board representation of the opponent
     * @param heights The list of the heights of the different columns
     * @param max_depth The maximun depth to search
     * @param alpha The alpha parameter
     * @param beta The beta parameter
     * @return The score of the negamax algorithm at this level
     */
    int negamax(uint64_t *player, uint64_t *opponent, uint8_t *heights, const int max_depth, int alpha, int beta);

    /**
     * @brief Return the best starting move when no evaluation is done
     * 
     * @param heights The list of the heights of the different columns
     * @return the column played
     */
    int bestStartingMove(const uint8_t *heights);

    /**
     * @brief Search the best move the AI can make
     * 
     * @param player The bitboard of the AI
     * @param opponent The bitboard of the opponent
     * @param depth The depth at which we want the AI to look
     * @param heights The list of the heights of the different columns
     * @return The number of the column in which we should play
     */
    int aiSearchMove(uint64_t *player, uint64_t *opponent, const int depth, uint8_t *heights);

public:

    /**
     * @brief A wrapper around the AI
     * 
     * @param depth The depth at which the AI should look
     * @return The column in which the AI played or NOT_ALLOWED if the col is not valid
     */
    int aiMove(const int depth);

    /**
     * @brief A wrapper around the Human
     * 
     * @param col The column in which the human want to play
     * @return The column in which the Human played or NOT_ALLOWED if the col is not valid
     */
    int humanMove(const int col);

    /**
     * @brief Reset the state of the board
     * 
     */
    void resetBoard();

    /**
     * @brief Print the board on the screen
     * 
     */
    void printBoard();

    /**
     * @brief Launch a match of connect 4 against the AI
     * 
     * @return the status code
     */
    int run();

    /**
     * @brief Get the count object
     * 
     * @return long 
     */
    int get_count() {
        return count;
    }

    bool human_winning();
    bool ai_winning();
    bool draw();

    int forceAIMove(const int col);
    int scoreAIpos();
};
