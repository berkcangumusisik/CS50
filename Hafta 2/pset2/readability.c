#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

int main(void)
{
    string user = get_string("Text:");
    int n = strlen(user);
    int lettercount = 0;
    for (int i = 0; i < n ; i++)
    {
        if (isalpha(user[i]))
        {
            lettercount += 1;
        }
    }
    int x = strlen(user);
    int wordcount = 1;
    for (int i = 1; i < x; i++)
    {
        if ((isspace(user[i])) && (isalpha(user[i + 1])))
        {
            wordcount += 1;
        }

    }
    int z = strlen(user);
    int sentencecount = 0;
    for (int i = 1; i < x; i++)
    {
        if (user[i] == '.' || user[i] == '?' || user[i] == '!' || user[i] == ':') 
        { 
            sentencecount += 1;
        }

    }
    float averagenumberoflettersper100words = ((float)lettercount * 100) / (float)wordcount;
    float averagenumberofsentencesper100words = ((float)sentencecount * 100) / (float)wordcount;
    float grade = 0.0588 * averagenumberoflettersper100words - 0.296 * averagenumberofsentencesper100words - 15.8;
    if (grade >= 1 && grade <= 16)
    {
        printf("Grade %i\n", (int) round(grade));
    }
    else
    {
        if (grade < 1)
        {
            printf("Before Grade 1\n");
    
        }
    }
    
    {
        if (grade > 16)
        {
            printf("Grade 16+\n");
        
        }
    }
}