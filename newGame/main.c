#include "game.h"
#include <stdio.h>

int main() {
    Player player;
    Enemy enemy;
    init_player(&player, "Hero");
    init_enemy(&enemy, "Goblin");
    battle(&player, &enemy);
    return 0;
}
