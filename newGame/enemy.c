#include "enemy.h"
#include <string.h>

void init_enemy(Enemy *e, const char *name) {
    strncpy(e->name, name, sizeof(e->name)-1);
    e->name[sizeof(e->name)-1] = '\0';
    e->health = 80;
    e->attack = 15;
    e->defense = 3;
}

int enemy_attack(const Enemy *e) {
    return e->attack; // could add randomness
}

int enemy_defend(Enemy *e, int damage) {      /* removed const qualifier */
    int mitigated = damage - e->defense;
    if (mitigated < 0) mitigated = 0;
    e->health -= mitigated;
    return mitigated;
}
