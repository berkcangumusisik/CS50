#include <cs50.h>
#include <stdio.h>
int main(void)
{
    int sayilar[] = {4, 6, 8, 2, 7, 5, 0};
    for (int i = 0; i < 7; i++)
    {
        if (sayilar[i] == 0)
        {
            printf("Bulundu\n");
            return 0;
        }
    }
    printf("Bulunamadı\n");
    return 1;
}