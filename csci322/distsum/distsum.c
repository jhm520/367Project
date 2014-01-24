#include <stdio.h>

struct core{
	int num;
	int val;
	int idle;
	int master;
};

void idle(struct core *thisCore){
	//
	thisCore->idle = 1;
}

void sendValueToCore(struct core thisCore, struct core targetCore){
	//
	printf("S%02d ",targetCore.num);
}

void receiveValueFromCore(struct core thisCore, struct core targetCore){
	//
	printf("R%02d ", targetCore.num);
}

void dgs(struct core *thisCore, struct core cores[], int numCores, int diff, int *done){
	if (thisCore->num%diff == 0){
		if (thisCore->num%(diff<<1) != 0){
			sendValueToCore(*thisCore, cores[thisCore->num - diff]);
			idle(thisCore);
		}else{
			if(thisCore->num + diff < numCores){
				receiveValueFromCore(*thisCore, cores[thisCore->num + diff]);
			}else{
				printf("... ");
			}
			if (thisCore->num == 0 && diff<<1 >= numCores){
				*done = 1;
			}
		}
	}else{
		printf("    ");
	}
}


int main(int argc, char* argv[])
{
	printf("Cores: %s\n", argv[1]);
	
	int numCores = atoi(argv[1]);
	struct core cores[numCores];
	numCores = sizeof(cores)/sizeof(cores[0]);
	
	int vals[] = {25, 22, 84, 17, 
				90, 55, 23, 66,
				25, 22, 20, 64,
				90, 15, 33, 17};
	
	int i;
	printf("\t");
	for (i = 0; i < numCores; i++){
		cores[i].num = i;
		//cores[i].val = vals[i];
		cores[i].idle = 0;
		cores[i].master = 0;
		printf("%02d  ", i);
	}
	cores[0].master = 1;
	printf("\n");

	int done = 0;
	int diff = 1;
	int time = 0;
	while (done == 0){
		
		printf("%02d\t", time);

		

		for (i = 0; i < numCores; i++){
			dgs(&cores[i], cores, numCores, diff, &done);
		}
		
		time++;
		diff = diff * 2;
		printf("\n");
	}
	//printf("Number of Cores: %lu", sizeof(cores);
	
	
	
	return 0;
}
