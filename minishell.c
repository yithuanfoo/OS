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

struct job { pid_t pid; int id; char cmd[NL]; };  // job structure stores pid, job id and command string
static struct job jobs[MAXJ]; // array of jobs
static int njobs = 0; // number of jobs currently tracked
static int next_job_int= 1; // counter for assigning job IDs

static int remember_job(pid_t pid, const char *cmd){  // remembers background job
  int id = next_job_int++;  // assigns a new job id
  if (njobs < MAXJ) { // if there is space in the jobs array
    jobs[njobs].pid = pid;  // save the pid
    jobs[njobs].id = id;  // save the job id
    if (cmd) {  // if command string exists
      strncpy(jobs[njobs].cmd, cmd, NL-1);  // copy the string
      jobs[njobs].cmd[NL-1] = '\0'; // make sure its terminated
    } else {  
      jobs[njobs].cmd[0] = '\0';  // empty string if there is no command
    }
    njobs++;  // increments the number of jobs
  }
  return id; // returns the job id
}

static int forget_job(pid_t pid, char *out_cmd){  // removes finish job from list
  for (int k = 0; k < njobs; k++){  // loops through jobs
    if (jobs[k].pid == pid){  // if pid is found
      int id = jobs[k].id;  // get the job id
      if (out_cmd){ // if command is wanted back
        strncpy(out_cmd, jobs[k].cmd, NL-1);  // copy the command
        out_cmd[NL-1] = '\0';
      }
      jobs[k] = jobs[njobs - 1];  // replace it with the last job
      njobs--;  // decrease the number of jobs
      return id;  // returns the job id that has been removed
    }
  }
  if (out_cmd){ // if no job found set the string to be empty
    out_cmd[0] = '\0';
  }
  return 0;
}

// cleans up commands
static void trim_cmd(char *s){
  size_t n = strlen(s);
  while (n && (s[n-1] == '\n' || s[n-1] == ' ' || s[n-1] == '\t' || s[n-1] == '&' || s[n-1] == ';'))
    s[--n] = '\0';
}

static void wait_for_all_jobs(void){  // checks for finished background jobs
  int status;
  pid_t done; // pid of finished job
  while ((done = waitpid(-1, &status, WNOHANG)) > 0){ // clears of finished jobs
    char cmd[NL]; 
    int id = forget_job(done, cmd); // rempves job from list
    if (!id) {  // if job is not found in the list
      id = next_job_int++;  // assign the job a new id
      snprintf(cmd, NL, "%d", (int)done); // use pid as the command string
    }
    printf("[%d]+ Done %s\n", id, cmd); 
    fflush(stdout); // flush output
  }
  if (done == -1 && errno != ECHILD) perror("waitpid"); // if error print error
}

/*
	shell prompt
 */

void prompt(void)
{
  // ## REMOVE THIS 'fprintf' STATEMENT BEFORE SUBMISSION
  //fprintf(stdout, "\n msh> ");
  fflush(stdout); // flush output
}


/* argk - number of arguments */
/* argv - argument vector from command line */
/* envp - environment pointer */
int main(int argk, char *argv[], char *envp[])
{
   int             frkRtnVal;	    /* value returned by fork sys call */
  char           *v[NV];	        /* array of pointers to command line tokens */
  //char           *sep = " \t\n";  /* command line token separators    */
  int             i;		          /* parse index */

    /* prompt for and process one command line at a time  */

  while (1) {			/* do Forever */
    prompt();
    if (!fgets(line, NL, stdin)){ // reads line of input
      if (ferror(stdin)) perror("fgets"); // if error reading
      exit(0);  // exit
    }

    if (feof(stdin)) {		/* non-zero on EOF  */
      exit(0);
    }
    if (line[0] == '#' || line[0] == '\n' || line[0] == '\0'){  
      wait_for_all_jobs();  // skips empty or comment lines
      continue;			/* to prompt */
    }

    char *save_outer = NULL;
    char *cmd = strtok_r(line, ";\n", &save_outer); // splits input with ;

    while (cmd){  // processes each command seperated by ;
      char chunk[NL];
      strncpy(chunk, cmd, NL-1);
      chunk[NL-1] = '\0';
    
      char *save_inner = NULL;  // split chunk into different words
      v[0] = strtok_r(chunk, " \t\n", &save_inner);
      for (i = 1; i < NV; i++){
        v[i] = strtok_r(NULL, " \t\n", &save_inner);
        if (!v[i]) break; // stops if no more words
      }
    
    if (!v[0]){ // if there is nothing in the chunk
      cmd = strtok_r(NULL, ";\n", &save_outer);
      continue;
    }

    if (strcmp(v[0], "cd") == 0){
      if (chdir(v[1] ? v[1] : getenv("HOME")) == -1)
        perror("chdir");  // change directory
      wait_for_all_jobs(); 
      cmd = strtok_r(NULL, ";\n", &save_outer);
      continue;
    }

    int background = 0; // check if background job
    if (i > 1 && v[i-1] && strcmp(v[i-1], "&") == 0){
      background = 1; // if it is mark as background and remove &
      v[i-1] = NULL;
    }
    
    char cmdcopy[NL]; // tracks job by copying command string
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
        if (background){  // if its a background job
          int job_id = remember_job(frkRtnVal, cmdcopy);  // print job started
          printf("[%d] %d\n", job_id, frkRtnVal);
          fflush(stdout);
        } else {  // if its a foreground job
          int status_fg;
          if (waitpid(frkRtnVal, &status_fg, 0) == -1)  // wait for the child process to finish
            perror("waitpid");
        }

        wait_for_all_jobs();
        break;
      }
  }
      cmd = strtok_r(NULL, ";\n", &save_outer); // move to the next command

    }				/* switch */
  }				/* while */
}				/* main */
