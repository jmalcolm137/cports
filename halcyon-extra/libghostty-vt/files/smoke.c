#include <stdio.h>
#include <string.h>

#include <ghostty/vt.h>

int main(void) {
    printf("headers %s, library %s\n", GHOSTTY_VT_VERSION, ghostty_version());
    return strcmp(GHOSTTY_VT_VERSION, ghostty_version()) != 0;
}
