#ifndef ENEMY_H
#define ENEMY_H

#include <stdio.h>

typedef struct {
    char name[50];
    int health;
    int attack;
    int defense;
} Enemy;

void init_enemy(Enemy *e, const char *name);
int enemy_attack(const Enemy *e);
/* enemy_defend modifies the Enemy; remove const qualifier */
int enemy_defend(Enemy *e, int damage);

#endif // ENEMY_H