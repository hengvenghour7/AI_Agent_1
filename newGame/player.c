#include "player.h"
#include <string.h>

void init_player(Player *p, const char *name) {
    strncpy(p->name, name, sizeof(p->name)-1);
    p->name[sizeof(p->name)-1] = '\0';
    p->health = 100;
    p->attack = 20;
    p->defense = 5;
}

int player_attack(const Player *p) {
    /* Simple damage formula: base attack +/- random offset */
    return p->attack;   /* can add randomness later */
}

int player_defend(Player *p, int damage) {      // removed const qualifier
    int mitigated = damage - p->defense;
    if (mitigated < 0) mitigated = 0;
    p->health -= mitigated;
    return mitigated;
}
