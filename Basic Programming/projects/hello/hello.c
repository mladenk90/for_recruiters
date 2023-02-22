#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt for name
    string name = get_string("What's your name? ");
    // Prompt for response
    printf("hello, %s\n", name);
}