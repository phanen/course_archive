#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int main(int argc, char *argv[])
{
  char *giao = malloc(4);
  // strcpy(giao, "giaogiaogiaogiaogiaogaiogaiogaio");
  strcpy(giao, argv[1]);
  printf("input at %p, %s\n", giao, giao);

  return EXIT_SUCCESS;
}

