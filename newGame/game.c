#include "game.h"
#include <stdio.h>
#include <stdlib.h>

void battle(Player *p, Enemy *e) {
    printf("\n%s vs %s! The battle begins!\n", p->name, e->name);
    int turn = 0; // 0 for player, 1 for enemy
    while (p->health > 0 && e->health > 0) {
        if (turn == 0) {
            printf("\n%s's health: %d | %s's health: %d\n", p->name, p->health, e->name, e->health);
            printf("Choose action:\n1. Attack\n2. Defend\n> ");
            int choice;
            if (scanf("%d", &choice) != 1) {
                // consume invalid input
                int c; while ((c = getchar()) != '\n' && c != EOF); continue;
            }
            switch (choice) {
                case 1: {
                    int dmg = player_attack(p);
                    int mitigated = enemy_defend(e, dmg);
                    printf("%s attacks! Deals %d damage. (%d after defense).\n", p->name, dmg, mitigated);
                    break;
                }
                case 2: {
                    printf("%s defends, reducing incoming damage next turn.", p->name);
                    // Simple: increase defense for one attack
                    p->defense += 5;
                    break;
                }
                default:
                    printf("Invalid choice. Turn skipped.");
            }
        } else {
            int dmg = enemy_attack(e);
            int mitigated = player_defend(p, dmg);
            printf("%s attacks! Deals %d damage. (%d after defense).\n", e->name, dmg, mitigated);
            // reset temporary defense boost
            if (p->defense > 5) p->defense -= 5;
        }
        turn ^= 1; // switch turns
    }
    printf("\nBattle over!\n");
    if (p->health <= 0 && e->health <= 0)
        printf("It's a draw!");
    else if (p->health > 0) {
        printf("%s wins!", p->name);
    } else {
        printf("%s wins!", e->name);
    }
}
