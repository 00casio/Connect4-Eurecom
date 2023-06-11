#include <cstdio>
#include <cstdint>

#define MAX_ALLOWED_HEIGHT 48
#define NBR_COL 7

class Recursive {
public:
uint64_t count = 0;

void putPiece(uint64_t *player, const int col, uint8_t *heights) {
    *player ^= 1ULL << heights[col];
    heights[col] += 8;
}

void removePiece(uint64_t *player, const int col, uint8_t *heights) {
    heights[col] -= 8;
    *player &= ~(1ULL << heights[col]);
}

bool quickWinning(const uint64_t bitboard) {
    // |
    if ((bitboard & (bitboard >> 8) & (bitboard >> 16) & (bitboard >> 24)) != 0) {
        return true;
    }
    // -
    if ((bitboard & (bitboard >> 1) & (bitboard >> 2) & (bitboard >> 3)) != 0) {
        return true;
    }
    // /
    if ((bitboard & (bitboard >> 7) & (bitboard >> 14) & (bitboard >> 21)) != 0) {
        return true;
    }
    // \ _
    if ((bitboard & (bitboard >> 9) & (bitboard >> 18) & (bitboard >> 27)) != 0) {
        return true;
    }
    return false;
}

void recurse(uint64_t *player, uint64_t *opponent, uint8_t *heights, const int depth) {
    count++;
    if (count % 100000 == 0) {
        printf("%15lu\r", count);
    }
    if (quickWinning(*player)) {
        return;
    }
    if (quickWinning(*opponent)) {
        return;
    }
    if ((*player | *opponent) == 280371153272574) {
        return;
    }
    if (depth == 0) {
        return;
    }

    for (int i = 0; i < NBR_COL; i++) {
        if (heights[i] > MAX_ALLOWED_HEIGHT) {
            continue;
        }
        putPiece(player, i, heights);
        recurse(opponent, player, heights, depth - 1);
        removePiece(player, i, heights);
    }
}
};

int main() {
    for (int depth = 17; depth < 18; depth++) {
        uint64_t player_1 = 0b0;
        uint64_t player_2 = 0b0;
        uint8_t col[7] = {7, 6, 5, 4, 3, 2, 1};
        Recursive R;
        R.recurse(&player_1, &player_2, col, depth);
        printf("%2d, %lu\n", depth, R.count -1);
    }
}
