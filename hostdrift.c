// pyboard version of hostdrift  pybord sending ascii millis every 10s
#include <stdio.h>
#include <string.h>
char buff[32];
FILE *fp;
static double tickrate = 1000.;


/* rclock.c   return elapsed time */
double
rclock()
{
#include <sys/time.h>
    struct timeval t;
    (void) gettimeofday(&t, (struct timezone *)0);
    return(t.tv_sec+ t.tv_usec/1.e6);
}


main() {

	unsigned long ms;
	int ms0=0, ppm, cnt=0, msprev=0;
	double t,t0,t1;
	fp = fopen("/dev/ttyACM0","r");
	while(1) {
		memset(buff,0,sizeof(buff));
		fgets(buff,sizeof(buff),fp);
		t=rclock();
		sscanf(buff,"%d",&ms);
		if (ms0 == 0) {
			ms0 = ms;
			t0=t;
		}
		ppm = 1.e6 * (((ms-ms0)/tickrate) - (t-t0))/(t-t0);
		printf("%f  %d %d %f %f %d \n",
         t,ms,ms-msprev,t-t0, (ms-ms0)/tickrate,ppm);
		msprev=ms;
	}
}
