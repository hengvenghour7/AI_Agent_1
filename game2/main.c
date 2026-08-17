#include "utils.h"
#include "animal.h"

void show_menu() {
    printf("\nWhat will you do?\n");
    printf("[1] Explore\n");
    printf("[2] Eat (if hungry)\n");
    printf("[3] Rest\n");
    printf("[4] Quit\n");
}

int main(void) {
    srand((unsigned int)time(NULL));
    Player player;
    init_player(&player);

    int choice;
    while (1) {
        print_status(&player);
        show_menu();
        if (scanf("%d", &choice) != 1) {
            printf("Invalid input. Try again.\n");
            // clear stdin
            int c;
            while ((c = getchar()) != '\n' && c != EOF);
            continue;
        }

        switch(choice) {
            case 1: { // Explore
                printf("\nYou venture into the wild...\n");
                int event = random_event();
                if (event < 30) {
                    printf("You found a berry patch! You eat some.\n");
                    player.hunger -= 15;
                    if (player.hunger < 0) player.hunger = 0;
                } else {
                    WildAnimal w = get_random_wild_animal();
                    printf("A wild %s attacks! You lose %d health.\n", w.name, w.damage);
                    player.health -= w.damage;
                }
                // time passes
                player.stamina -= 10;
                if (player.stamina < 0) player.stamina = 0;
                player.hunger += 5;
                break;
            }
            case 2: { // Eat
                if (player.hunger <= 20) {
                    printf("\nYou are not hungry enough to eat.\n");
                } else {
                    printf("\nYou ate some food, restoring health and reducing hunger.\n");
                    player.health += 10;
                    if (player.health > 100) player.health = 100;
                    player.hunger -= 30;
                    if (player.hunger < 0) player.hunger = 0;
                }
                break;
            }
            case 3: { // Rest
                printf("\nYou rest and recover stamina.\n");
                player.stamina += 20;
                if (player.stamina > 100) player.stamina = 100;
                player.health += 5;
                if (player.health > 100) player.health = 100;
                player.hunger += 10; // hunger increases while resting
                break;
            }
            case 4: { // Quit
                printf("\nThanks for playing!\n");
                return 0;
            }
            default:
                printf("\nUnknown choice. Try again.\n");
        }

        if (player.health <= 0) {
            printf("\nYou have perished in the wild. Game over.\n");
            break;
        }
    }
    return 0;
}
