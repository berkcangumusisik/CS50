#include <stdio.h>
#include <cs50.h> // to get plain text
#include <string.h> // for strlen()
#include <ctype.h> // for string operation upper, lower

int checkKey(); // for validate key
void Do_substitute(); // for further substitute
void alpha_arr_val(char pos, string key);
// to get the alphabet array value of each plain text element (ex:plaintext = h|alphabet array = 8 {a=0, b=1 .....z=26})

int main(int argc, string argv[])
{
    if (argc == 2) // number of commands in terminal
    {
        if (strlen(argv[1]) == 26)
        {
            for (int i = 0; i < strlen(argv[1]) ; i++) // checking each element of string
            {
    
                if (! isalpha(argv[1][i])) // if contain non-alphabet
                {
                    printf("Key must contain 26 characters.\n");
                    return 1;
                }
    
                for (int j = i + 1 ; j < strlen(argv[1]) ; j++) // checking to the next element of arg[i]
                {
    
                    if (toupper(argv[1][j]) == toupper(argv[1][i])) // checking repeated element
                    {
                        printf("Key must not contain repeated alphabets.\n");
                        return 1;
                    }
                }
            }
            
            Do_substitute(argv[1]);
            
        }
        else
        {
            printf("Key must contain 26 characters.\n");
            return 1;   
        }
        
    }
    else
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    return 0;
}


void Do_substitute(string key)
{
    string p = get_string("plaintext: ");

    printf("ciphertext: ");

    for (int i = 0; i < strlen(p); i++)
    {
        if (isalpha(p[i])) // checking p[i] is alphabet
        {
            char x = p[i];
            if (islower(p[i]))
            {
                alpha_arr_val(tolower(x), key); // passing p[i] in lower-case
            }
            else
            {
                alpha_arr_val(toupper(x), key); // passing p[i] in UPPER-CASE
            }


        }
        else
        {
            printf("%c", p[i]); // print the element as it is (such as space | , | special characters | ? | etc...)
        }
    }

    printf("\n");

}
void alpha_arr_val(char pos, string key) // passing p[i] and upper/lower(alpha array)
{
    string alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"; // alphabet array

    for (int i = 0; i < strlen(alpha); i++) // accessing each element in alpha array
    {
        if (islower(pos)) // p[i] is lower
        {
            if (pos == tolower(alpha[i]))
            {
                printf("%c", tolower(key[i]));
            }
        }
        else // for UPPERCASE // p[i] is upper
        {
            if (pos == toupper(alpha[i]))
            {
                printf("%c", toupper(key[i]));
            }
        }
    }
}