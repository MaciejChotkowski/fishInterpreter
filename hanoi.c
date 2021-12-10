#include <stdio.h>

void Hanoi(int n, char from, char to, char help)
{
    if(n == 1)
    {
        printf("Move from %c to %c.\n", from, to);
        return;
    }
    Hanoi(n-1, from, to, help);
    printf("Move from %c to %c.\n", from, to);
    Hanoi(n-1, help, from, to);
}

int main()
{
    Hanoi(3, 'A', 'B', 'C');
}