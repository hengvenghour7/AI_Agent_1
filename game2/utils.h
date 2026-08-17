#ifndef UTILS_H
#define UTILS_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct {
    int health;
    int hunger; // 0-100
    int stamina;
} Player;

void init_player(Player *p);
void print_status(const Player *p);
int random_event();

#endif /* UTILS_H */
