#include <cstdio>

struct a {
    unsigned long long p;
    double *b;

    a(unsigned long long dez, double *q) {
        p = dez;
        b = q;
    }
};

a test(unsigned long long *z, double *p) {
    a s = a(*z, p);
    return s;
}

void test2(unsigned long long *z) {
    *z += 4372;
}

int main() {

    double i = 425622;
    unsigned long long z = 0;
    a s = test(&z, &i);
    printf("%llu, %llu\n", s.p, z);
    z = 362828;
    s.p = 9020;
    printf("%llu, %llu\n", s.p, z);
    test2(&z);
    // test2(&s.p);
    printf("%llu, %llu\n", s.p, z);
    printf("%llu, %llu\n", s.p, z);
    return 0;
}