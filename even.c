#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void signal_handler(int signal){
    if (signal == SIGHUP){
        write(STDOUT_FILENO, "Ouch!\n", 6);
    } else if (signal == SIGINT){
        write(STDOUT_FILENO, "Yeah!\n", 6);
    }
}

int main(int argc, char *argv[]){

    int n = atoi(argv[1]);

    struct sigaction sa;
    sa.sa_handler = signal_handler;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGHUP, &sa, NULL);
    sigaction(SIGINT, &sa, NULL);

    for (int i = 0; i < n; i++){
        printf("%d\n", 2 * i);
        sleep(5);
    }

    return 0;
}