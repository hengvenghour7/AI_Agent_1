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

    // Distance to destination (in arbitrary units)
    int destination = 100; // You win when this reaches 0 or below

    int choice;
    while (1) {
        print_status(&player);
        printf("\nDestination steps remaining: %d\n", destination > 0 ? destination : 0);
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
                    printf("You found a berry patch! You collect some.\n");
                    player.food_inventory += 5;
                } else {
                    WildAnimal w = get_random_wild_animal();
                    printf("A wild %s attacks! You lose %d health.\n", w.name, w.damage);
                    player.health -= w.damage;
                }
                // time passes
                player.stamina -= 10;
                if (player.stamina < 0) player.stamina = 0;
                player.hunger += 5;

                // Move towards destination
                int step = rand() % 10 + 1; // 1 to 10 steps per exploration
                destination -= step;
                if (destination < 0) destination = 0;
                printf("You moved %d steps towards your destination.\n", step);
                break;
            }
            case 2: { // Eat
                if (player.hunger <= 20) {
                    printf("\nYou are not hungry enough to eat.\n");
                } else if (player.food_inventory <= 0) {
                    printf("\nYou have no food collected to eat.\n");
                } else {
                    printf("\nYou ate some stored food, restoring health and reducing hunger.\n");
                    player.health += 10;
                    if (player.health > 100) player.health = 100;
                    player.hunger -= 30;
                    if (player.hunger < 0) player.hunger = 0;
                    player.food_inventory--;
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

        if (destination <= 0) {
            printf("\nCongratulations! You have reached your destination and won the game!\n");
            return 0;
        }
    }
    return 0;
}
