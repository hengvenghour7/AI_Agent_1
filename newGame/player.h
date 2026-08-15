#ifndef PLAYER_H
#define PLAYER_H

#include <stdio.h>

typedef struct {
    char name[50];
    int health;
    int attack;
    int defense;
} Player;

void init_player(Player *p, const char *name);
int player_attack(const Player *p);
/* player_defend modifies the Player; remove const qualifier */
int player_defend(Player *p, int damage);

#endif // PLAYER_H