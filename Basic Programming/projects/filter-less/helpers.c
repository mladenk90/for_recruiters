#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // for each row
    for (int i = 0; i < height; i++)
    {
        // for each column
        for (int j = 0; j < width; j++)
        {
           // convert to float
           float red = image[i][j].rgbtRed;
           float green = image[i][j].rgbtGreen;
           float blue = image[i][j].rgbtBlue;

           // Find average
           int average = round((red + green + blue) / 3);
           image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // for each row
    for (int i = 0; i < height; i++)
    {
        // for each column
        for (int j = 0; j < width; j++)
        {
           // convert to float
           float originalred = image[i][j].rgbtRed;
           float originalgreen = image[i][j].rgbtGreen;
           float originalblue = image[i][j].rgbtBlue;

           // Sepia value
           int  sepiaRed = round(.393 * originalred + .769 * originalgreen + .189 * originalblue);
           int sepiaGreen = round(.349 * originalred + .686 * originalgreen + .168 * originalblue);
           int sepiaBlue = round(.272 * originalred + .534 * originalgreen + .131 * originalblue);

           // If over 255
           if (sepiaRed > 255)
           {
            sepiaRed = 255;
           }
           if (sepiaGreen > 255)
           {
            sepiaGreen = 255;
           }
           if (sepiaBlue > 255)
           {
            sepiaBlue = 255;
           }

           image[i][j].rgbtRed = sepiaRed;
           image[i][j].rgbtGreen = sepiaGreen;
           image[i][j].rgbtBlue = sepiaBlue;
    }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
     // for each row
    for (int i = 0; i < height; i++)
    {
        // for each column
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE temp = image[i][j];
            image[i][j] = image[i][width - (j + 1)];
            image[i][width - (j + 1)] = temp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // temp copy
    RGBTRIPLE temp[height][width];
     // for each row
            for (int i = 0; i < height; i++)
            {
                // for each column
                for (int j = 0; j < width; j++)
                {
                temp[i][j] = image[i][j];
                }
            }
             // for each row
            for (int i = 0; i < height; i++)
            {
                // for each column
                for (int j = 0; j < width; j++)

            {
                int totalRed, totalGreen, totalBlue;
                totalRed = totalGreen = totalBlue = 0;
                float counter = 0.0;


                // for neighboring pixels
                for (int x = -1; x < 2; x++)
                {
                    for (int y = -1; y < 2; y++)
                    {
                        int currentX = i + x;
                        int currentY = j + y;

                        // check if valid
                        if (currentX < 0 || currentX > (height - 1) || currentY < 0 || currentY > (width -1))
                        {
                            continue;
                        }


                    // image value
                    totalRed += image[currentX][currentY].rgbtRed;
                    totalGreen += image[currentX][currentY].rgbtGreen;
                    totalBlue += image[currentX][currentY].rgbtBlue;

                    counter++;
                }

                // avg of neighboting pixels
                temp[i][j].rgbtRed = round(totalRed / counter);
                temp[i][j].rgbtGreen = round(totalGreen / counter);
                temp[i][j].rgbtBlue = round(totalBlue / counter);
            }
        }
    }

    // copy new pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }
    return;
}
