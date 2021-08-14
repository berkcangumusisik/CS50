#include <stdio.h>
#include <cs50.h>
#include <math.h>
int main(void)
{
    float change;
    do
    {
        change = get_float("How much change is owned:");
    }
    while (change < 0);
    int cents = round(change * 100);
    int coin = 0;
    while (cents >= 25)
    {
        cents -= 25;
        coin++;
    }
    while (cents >= 10)
    {
        cents -= 10;
        coin++;
    }
    while (cents >= 5)
    {
        cents -= 5;
        coin++;
    }
    while (cents >= 1 && cents > 0)
    {
        cents -= 1;
        coin++;
    }
    printf("%i\n", coin);  
}