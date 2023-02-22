// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// declare variables
unsigned int word_count;
unsigned int hash_value;

// TODO: Choose number of buckets in hash table
const unsigned int N = 17576;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // hash word
    hash_value = hash(word);

    // point cursor to first node
    node *cursor = table[hash_value];

    // go to linked list
    while (cursor != 0)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned long total = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        total += tolower(word[i]);
    }
    return total % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // open dictionary
    FILE *file = fopen(dictionary, "r");

    // Return NULL if no file
    if (file == NULL)
    {
        printf("unable to open %s\n", dictionary);
        return false;
    }

    // declare variable
    char word[LENGTH+1];

    // scan dictionary
    while (fscanf(file, "%s", word) != EOF)
    {
        node *n = malloc(sizeof(node));

        // if malloc NULL
        if (n == NULL)
        {
            return false;
        }

        // copy into node
        strcpy(n->word, word);
        hash_value = hash(word);
        n->next = table[hash_value];
        table[hash_value] = n;
        word_count++;
    }
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    // iterate through buckets
    for (int i = 0; i < N; i++)
    {
        // set cursor for start of list
        node *cursor = table[i];

        // if not null, free memory
        while(cursor)
        {
            // make tmp
            node *tmp = cursor;
            // move to next node
            cursor = cursor->next;
            // free tmp
            free(tmp);
        }
        if (cursor == NULL && i == N-1)
        {
            return true;
        }
    }
    return false;
}
