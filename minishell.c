/*********************************************************************
   Program  : miniShell                   Version    : 1.3
 --------------------------------------------------------------------
   skeleton code for linix/unix/minix command line interpreter
 --------------------------------------------------------------------
   File			: minishell.c
   Compiler/System	: gcc/linux

********************************************************************/

#include <sys/types.h>
#include <sys/wait.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <errno.h>

#define NV 20			/* max number of command tokens */
#define NL 100			/* input buffer size */
char            line[NL];	/* command input buffer */


/*
	shell prompt
 */

void prompt(void)
{
  // ## REMOVE THIS 'fprintf' STATEMENT BEFORE SUBMISSION
  //fprintf(stdout, "\n msh> ");
  fflush(stdout);
}


/* argk - number of arguments */
/* argv - argument vector from command line */
/* envp - environment pointer */
int main(int argk, char *argv[], char *envp[])
{
   int             frkRtnVal;	    /* value returned by fork sys call */
  char           *v[NV];	        /* array of pointers to command line tokens */
  char           *sep = " \t\n";  /* command line token separators    */
  int             i;		          /* parse index */

    /* prompt for and process one command line at a time  */

  while (1) {			/* do Forever */
    prompt();
    fgets(line, NL, stdin);
    fflush(stdin);

    // This if() required for gradescope
    if (feof(stdin)) {		/* non-zero on EOF  */
      exit(0);
    }
    if (line[0] == '#' || line[0] == '\n' || line[0] == '\000'){
      continue;			/* to prompt */
    }

    v[0] = strtok(line, sep);
    for (i = 1; i < NV; i++) {
      v[i] = strtok(NULL, sep);
      if (v[i] == NULL){
	      break;
      }
    }
    
    if (v[0] && strcmp(v[0], "cd") == 0){
      if (chdir(v[1] ? v[1] : getenv("HOME")) == -1)
        perror("chdir");
      continue;
      
    }

    int background = 0;
    if (i > 1 && v[i-1] && strcmp(v[i-1], "&") == 0){
      background = 1;
      v[i-1] = NULL;
    }
    /* assert i is number of tokens + 1 */

    /* fork a child process to exec the command in v[0] */
    switch (frkRtnVal = fork()) {
      case -1:			/* fork returns error to parent process */
      {
        perror("fork");
	      break;
      }
      case 0:			/* code executed only by child process */
      {
	      execvp(v[0], v);
        perror("execvp");
        _exit(1);
      }
      default:			/* code executed only by parent process */
      {
        if (!background){
          if (waitpid(frkRtnVal, NULL, 0) == -1){
            perror("waitpid");
          }
        }
        int status;
        pid_t done;
        while ((done = waitpid(-1, &status, WNOHANG)) > 0){
          printf("Done %d\n", done);
          fflush(stdout);
        }
        // REMOVE PRINTF STATEMENT BEFORE SUBMISSION
        //printf("%s done \n", v[0]);
    	  break;
      }
    }				/* switch */
  }				/* while */
}				/* main */
