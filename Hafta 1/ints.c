#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int x = get_int("x:");
    int y = get_int("y:");
    printf("x + y = %i\n", x+ y);
    printf("x - y = %i\n", x- y);
    printf("x * y = %i\n", x* y);
    printf("x / y = %i\n", x/ y);
    printf("x mod y = %i\n", x% y);
}
