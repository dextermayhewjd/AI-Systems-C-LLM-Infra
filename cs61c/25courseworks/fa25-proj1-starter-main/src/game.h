#ifndef _SNK_STATE_H
#define _SNK_STATE_H

#include <stdbool.h>
#include <stdio.h>

typedef struct snake_t {
  unsigned int tail_row;
  unsigned int tail_col;
  unsigned int head_row;
  unsigned int head_col;

  bool live;
} snake_t;

typedef struct game_t {
  unsigned int num_rows;
  char **board;

  unsigned int num_snakes;
  snake_t *snakes;
} game_t;

game_t *create_default_game();
void free_game(game_t *game);
void print_board(game_t *game, FILE *fp);
void save_board(game_t *game, char *filename);
void update_game(game_t *game, int (*add_food)(game_t *game));
char get_board_at(game_t *game, unsigned int row, unsigned int col);
game_t *initialize_snakes(game_t *game);
game_t *load_board(FILE *fp);

#endif
