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

#define MAXJ 128
#define NV 20			/* max number of command tokens */
#define NL 100			/* input buffer size */
char            line[NL];	/* command input buffer */

struct job {pid_t pid; int id; char cmd[NL];};
static struct job jobs[MAXJ];
static int njobs = 0;
static int next_job_int= 1;

static int remember_job(pid_t pid, const char *cmd){
  int id = next_job_int++;
  if (njobs < MAXJ) {
    jobs[njobs].pid = pid;
    jobs[njobs].id = id;
    if (cmd) {
      strncpy(jobs[njobs].cmd, cmd, NL-1);
      jobs[njobs].cmd[NL-1] = '\0';
    } else {
      jobs[njobs].cmd[0] = '\0';
    }
    njobs++;
  }
  return id;
}

static int forget_job(pid_t pid, char *out_cmd){
  for (int k = 0; k < njobs; k++){
    if (jobs[k].pid == pid){
      int id = jobs[k].id;
      if (out_cmd){
        strncpy(out_cmd, jobs[k].cmd, NL-1);
        out_cmd[NL-1] = '\0';
      }
      jobs[k] = jobs[njobs - 1];
      njobs--;
      return id;
    }
  }
  if (out_cmd) out_cmd[0] = '\0';
  return 0;
}
static void trim_cmd(char *s) {
  size_t n = strlen(s);
  while (n && (s[n-1] == '\n' || s[n-1] == ' ' || s[n-1] == '\t' ||
               s[n-1] == '&'  || s[n-1] == ';')) {
    s[--n] = '\0';
  }
}

/*
	shell prompt
 */

static void wait_for_all_jobs(void){
  int status;
  pid_t done;
  while ((done = waitpid(-1, &status, WNOHANG)) > 0){
    //int id = forget_job(done);
    //if (!id) id = remember_job(done);
    //printf("[%d] %d\n", id, done);
    char cmd[NL];
    int id = forget_job(done, cmd);
    if (!id) {
      id = next_job_int++;
      snprintf(cmd, NL, "%d", (int)done);
    }
    printf("[%d]+ Done %s\n", id, cmd);
    fflush(stdout);
  }
  if (done == -1 && errno != ECHILD) perror("waitpid");
}

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
    if (!fgets(line, NL, stdin)){
      if (ferror(stdin)) perror("fgets");
      exit(0);
    }

    // This if() required for gradescope
    if (feof(stdin)) {		/* non-zero on EOF  */
      exit(0);
    }
    if (line[0] == '#' || line[0] == '\n' || line[0] == '\0'){
      wait_for_all_jobs();
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
      wait_for_all_jobs();
      continue;
    }
      //int status_bg; pid_t done;
      //while ((done = waitpid(-1, &status_bg, WNOHANG)) > 0){
        //int id = forget_job(done);
        //printf("[%d] %d\n", id ? id : 0, done);
        //fflush(stdout);
      //}
      //if (done == -1 && errno != ECHILD) perror ("waitpid");
      //continue;
      
    //}

    int background = 0;
    if (i > 1 && v[i-1] && strcmp(v[i-1], "&") == 0){
      background = 1;
      v[i-1] = NULL;
    }

    char cmdcopy[NL];
    strncpy(cmdcopy, line, NL-1);
    cmdcopy[NL-1] = '\0';
    trim_cmd(cmdcopy);

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
        if (background){
          int job_id = remember_job(frkRtnVal, cmdcopy);
          printf("[%d] %d\n", job_id, frkRtnVal);
          fflush(stdout);
        } else {
          int status_fg;
          if (waitpid(frkRtnVal, &status_fg, 0) == -1)
            perror("waitpid");
        }

        wait_for_all_jobs();
        break;
        //int status_bg;
        //pid_t done;
        //while ((done = waitpid(-1, &status_bg, WNOHANG)) > 0){
          //int id = forget_job(done);
          //printf("[%d] %d\n", id ? id : 0, done);
          //fflush(stdout);
        //}
        //if (done == -1 && errno != ECHILD) perror("waitpid");
        // REMOVE PRINTF STATEMENT BEFORE SUBMISSION
        //printf("%s done \n", v[0]);
    	  //break;
      }
    }				/* switch */
  }				/* while */
}				/* main */
