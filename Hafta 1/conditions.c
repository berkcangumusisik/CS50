#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int x = get_int("x: ");
    int y = get_int("y: ");

    if (x < y)
    {
        printf("y, x'ten büyüktür.\n");
    }
    else if (x > y)
    {
        printf("x, y'den büyüktür.\n");
    }
    else
    {
        printf("x, y'ye eşittir.\n");
    }
}