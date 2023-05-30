#include <cassert>
#include <cstdint>
#include <ctime>
#include <random>
#define NBR_LINE 6
#define NBR_COL 7

bool method_doing_1(const uint64_t bitboard) {
    if ((bitboard & (bitboard >> 8) & (bitboard >> 16) & (bitboard >> 24)) != 0) {
        return true;
    }
    if ((bitboard & (bitboard >> 1) & (bitboard >> 2) & (bitboard >> 3)) != 0) {
        return true;
    }
    if ((bitboard & (bitboard >> 7) & (bitboard >> 14) & (bitboard >> 21)) != 0) {
        return true;
    }
    if ((bitboard & (bitboard >> 9) & (bitboard >> 18) & (bitboard >> 27)) != 0) {
        return true;
    }
    return false;
}

int countNbrOne(const uint64_t bitboard) {
    int count_one = 0;
    int64_t gaëtan = 1;
    for (int i = 0; i < NBR_LINE; i++) {
        for (int j = 0; j < NBR_COL; j++) {
            if ((gaëtan & bitboard) != 0) {
                count_one++;
            }
            gaëtan <<= 1;
        }
        gaëtan <<= 1;
    }
    return count_one;
}

int method_doing_2(const uint64_t bitboard, bool *state) {
        int nbr_3_in_line = 0;
    int nbr_2_in_line = 0;

    uint64_t tmp = bitboard & (bitboard >> 8);
    if (tmp != 0) {
        nbr_2_in_line += countNbrOne(tmp);
        tmp &= (bitboard >> 16);
        if (tmp != 0) {
            if (tmp & (bitboard >> 24)) {
                *state = true;
                return 0;
            }
            nbr_3_in_line += countNbrOne(tmp);
        }
    }

    tmp = bitboard & (bitboard >> 1);
    if (tmp != 0) {
        nbr_2_in_line += countNbrOne(tmp);
        tmp &= (bitboard >> 2);
        if (tmp != 0) {
            if (tmp & (bitboard >> 3)) {
                *state = true;
                return 0;
            }
            nbr_3_in_line += countNbrOne(tmp);
        }
    }

    tmp = bitboard & (bitboard >> 7);
    if (tmp != 0) {
        nbr_2_in_line += countNbrOne(tmp);
        tmp &= (bitboard >> 14);
        if (tmp != 0) {
            if (tmp & (bitboard >> 21)) {
                *state = true;
                return 0;
            }
            nbr_3_in_line += countNbrOne(tmp);
        }
    }

    tmp = bitboard & (bitboard >> 9);
    if (tmp != 0) {
        nbr_2_in_line += countNbrOne(tmp);
        tmp &= (bitboard >> 18);
        if (tmp != 0) {
            if (tmp & (bitboard >> 27)) {
                *state = true;
                return 0;
            }
            nbr_3_in_line += countNbrOne(tmp);
        }
    }
    *state = false;
    return nbr_3_in_line * 20 + nbr_2_in_line * 2;
}

template<typename T>
T random(T range_from, T range_to) {
    std::random_device                  rand_dev;
    std::mt19937                        generator(rand_dev());
    std::uniform_int_distribution<T>    distr(range_from, range_to);
    return distr(generator);
}

int main() {
    uint64_t a;
    uint64_t debut = 0;
    uint64_t fin = 18446744073709551615;
    double t_1 = 0;
    double t_2 = 0;
    bool state_1 = false;
    bool state_2 = false;
    int trash = 0;
    clock_t start;
    clock_t end;
    for (int i = 0; i < 10000000; i++) {
        a = random(debut, fin);
        start = clock();
        state_1 = method_doing_1(a);
        end = clock();
        t_1 += (double) (end - start) / CLOCKS_PER_SEC;
        start = clock();
        trash = method_doing_2(a, &state_2);
        end = clock();
        t_2 += (double) (end - start) / CLOCKS_PER_SEC;
        assert(state_1 == state_2);
        if (i%200 == 0) {
            printf("\r%i", i);
        }
    }
    printf("\n1st: %f\n2nd: %f", t_1, t_2);
    return 0;
}
