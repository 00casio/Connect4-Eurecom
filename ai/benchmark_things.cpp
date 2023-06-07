#include <cstdint>
#include <ctime>
#include <random>
#include <cassert>

int method_doing_1(const uint32_t bitboard) {
    int count = 0;
    int gaëtan = 1;
    for (int i = 0; i < 6; i++) {
        for (int j = 0; j < 7; j++) {
            if ((gaëtan & bitboard) != 0) {
                count++;
            }
            gaëtan <<= 1;
        }
        gaëtan <<= 1;
    }
    return count;
}

int method_doing_2(const uint32_t bitboard) {
    int count = 0;
    int gaëtan = 1;
    for (int i = 0; i < 64; i++) {
        if ((gaëtan & bitboard) != 0) {
            count++;
        }
        gaëtan <<= 1;
    }
    return count;
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
    int result_1 = 0;
    int result_2 = 0;
    clock_t start_1;
    clock_t end_1;
    clock_t start_2;
    clock_t end_2;
    for (int i = 0; i < 10000000; i++) {
        a = random(debut, fin);
        start_1 = clock();
        method_doing_1(a);
        end_1 = clock();
        start_2 = clock();
        method_doing_2(a);
        end_2 = clock();

        t_1 += (double) (end_1 - start_1) / CLOCKS_PER_SEC;
        t_2 += (double) (end_2 - start_2) / CLOCKS_PER_SEC;
        if (i%1000 == 0) {
            printf("\r%i", i);
        }
    }
    printf("\n1st: %f\n2nd: %f", t_1, t_2);
    return 0;
}
