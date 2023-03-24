#include "ai.hpp"
#include <cstdio>
#include <ctime>
#include <fstream>
#include <iostream>

int main(int argc, char **argv) {
    int nbr_test = 1000;
    int nbr_depth = 11;
    FILE *fp;
    FILE *fp_tmp;
    for (int depth = 1; depth < nbr_depth; depth++) {
        double t = 0;
        for (int i = 0; i < nbr_test; i++) {
            Game g;
            clock_t start = clock();
            g.aiMove(depth);
            clock_t end = clock();
            t += (double) (end - start) / CLOCKS_PER_SEC;
            printf("\r%i", i);
            if (depth > 7) {
                fp_tmp = fopen("tmp.out", "w");
                fprintf(fp_tmp, "%i", i);
                fclose(fp_tmp);
            }
        }
        printf("\r%i: ", nbr_test);
        fprintf(stdout, "%i is done, it took %f seconds\n", depth, t);
        fp = fopen("result.csv","a");
        fprintf(fp, "%5i, %25s, %10i, %15f, %10s\n", depth, argv[1], nbr_test, t/nbr_test, argv[2]);
        fclose(fp);
    }
    return 0;
}
