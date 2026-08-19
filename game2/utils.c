#include "utils.h"

void init_player(Player *p) {
    p->health = 100;
    p->hunger = 0;
    p->stamina = 100;
    p->food_inventory = 0; // initialize food count
    p->distance = 0; // unused in current logic
}

void print_status(const Player *p) {
    printf("\n=== Status ===\n");
    printf("Health: %d\n", p->health);
    printf("Hunger: %d%%\n", p->hunger);
    printf("Stamina: %d\n", p->stamina);
    printf("Food Inventory: %d\n", p->food_inventory);
}

int random_event() {
    return rand() % 100;
}
