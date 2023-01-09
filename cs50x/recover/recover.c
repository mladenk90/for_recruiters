#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // one command line arg
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // open file
    FILE *input_file = fopen(argv[1], "r");

    // check for invalid file
    if (input_file == NULL)
    {
        printf("Could not open file");
        return 2;
    }

        // 512bytes into buffer
        unsigned char buffer[512];

            // number of images
            int count_image = 0;

            // pointer for output
            FILE *output_file = NULL;

            char *filename = malloc(8 * sizeof(char));

        // Read 512 bytes
        while (fread(buffer, sizeof(char), 512, input_file))
        {
            //if new jpeg
            if (buffer[0] == 0xff && buffer [1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
            {
                // create JPEG filename
                sprintf(filename, "%03i.jpg", count_image);

                // open file
                output_file = fopen(filename, "w");

                count_image++;
            }
            //check if valid
            if (output_file != NULL)
            {
                fwrite(buffer, sizeof(char), 512, output_file);
            }
        }

    // close files and free memory
    free(filename);
    fclose(output_file);
    fclose(input_file);

    return 0;
}