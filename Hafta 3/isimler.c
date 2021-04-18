#include <cs50.h>
#include <stdio.h>
#include <string.h>
int main(void)
{
    string isimler[] = {"Ahmet","Ali","Berkay","Berkcan","Enes","Nurana","Şevval"};
    for (int i = 0; i < 7; i++)
    {
        if (strcmp(isimler[i], "Berkcan") == 0)
        {
            printf("Bulundu\n");
            return 0;
        }
    }
    printf("Bulunamadı\n");
    return 1;
}