#include <cs50.h>
#include <stdio.h>

int main(void)
{
    char c = get_char("Katılıyor musun?");
    if (c == 'Y' || c == 'y')
    {
        printf("Kabul\n");
    }
    else if (c == 'N' || c == 'n')
    {
        printf("Kabul değil\n");
    }
}