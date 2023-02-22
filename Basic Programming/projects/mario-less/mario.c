#include <cs50.h>
#include <stdio.h>

int main(void)
{
   int n;
   do
   {
        n = get_int("Height: ");
   }
   while (n < 1 || n > 8);

   // For each row
    for (int i = 0 ; i < n ; i++)
    {
        // For each column
        for (int j = n -1; j > i; j--)
        {
            // For print space
            printf(" ");
        }
        for (int x = -1; x < i; x++)
    {
            // Print a brick
            printf("#");
        }

        // Move to next row
        printf("\n");
    }

}