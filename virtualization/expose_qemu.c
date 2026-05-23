#include <stdio.h>
#include <sys/utsname.h>
#include <stddef.h>

int main(int argc, char **argv) {
    struct utsname sys_info;
    uname(&sys_info);

    printf("Welcome to the Matrix.\n");
    printf("The OS tells me my hardware CPU is: %s\n", sys_info.machine);

    // If we pass any argument, crash the program
    if (argc > 1) {
        printf("\nInitiating deliberate crash...\n");
        int *crash = NULL;
        *crash = 42;
    }
    return 0;
}
