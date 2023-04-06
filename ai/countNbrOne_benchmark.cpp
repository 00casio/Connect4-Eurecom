#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <random>

int countNbrOne_1(const unsigned long long bitboard) {
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

int countNbrOne_2(const unsigned long long bitboard) {
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
    unsigned long long a;
    unsigned long long debut = 0;
    unsigned long long fin = 18446744073709551615;
    double t_1 = 0;
    double t_2 = 0;
    clock_t start;
    clock_t end;
    for (int i = 0; i < 10000000; i++) {
        a = random(debut, fin);
        start = clock();
        countNbrOne_1(a);
        end = clock();
        t_1 += (double) (end - start) / CLOCKS_PER_SEC;
        start = clock();
        countNbrOne_2(a);
        end = clock();
        t_2 += (double) (end - start) / CLOCKS_PER_SEC;
        printf("\r%i", i);
    }
    printf("\n1st: %f\n2nd: %f", t_1, t_2);
    return 0;
}
