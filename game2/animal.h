#ifndef ANIMAL_H
#define ANIMAL_H

#include <stdio.h>

typedef struct {
    const char *name;
    int damage; // health loss when attacking
} WildAnimal;

WildAnimal get_random_wild_animal(void);

#endif /* ANIMAL_H */
