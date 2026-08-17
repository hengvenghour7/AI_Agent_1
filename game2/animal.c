#include "animal.h"
#include <stdlib.h>
#include <time.h>

static const WildAnimal animals[] = {
    {"Bear", 20},
    {"Wolf", 15},
    {"Snake", 10}
};

WildAnimal get_random_wild_animal(void) {
    int idx = rand() % (sizeof(animals)/sizeof(animals[0]));
    return animals[idx];
}
