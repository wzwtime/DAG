#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <string.h>

#ifdef __unix__
#include <unistd.h>
#elif defined _WIN32
#include <windows.h>
#define sleep(x) Sleep(1000 * x)
#endif
//#include <float.h>


#define MAXLENGTH 10
#define V 10	//Task number
#define P 3		//The number of processors 
#define MAXTIME 0.8	//s
#define CP 10
#define DBL_MIN -100000


int i, j, k, ti, pi, est, eft, makespan, count, edges_number = 0, ready_queue[MAXLENGTH];
int **comp_costs, **comm_costs, **data_transfer_rate, **data;		//���ָ��ָ�����һ��ָ��ĵ�ַ
FILE *fp1, *fp2;
int avail_pi[P];
int path_index;
long long int *path[2*V];
int *child_pi;
int *child_ti;
int temp_schedule[V];
int tree_entry;		//��¼����������ڵ�ַ 



struct TaskProcessor
{
    int PI;
    int EST;
    int EFT;
};

struct TaskProcessor *schedule;


struct Evon_Node	//ż���� ���� Ti
{
	int Ti; 	//task ti ��������i_Ti��i_N�� lli_ 
	int Ti_N;				// visit times
	long long int Ti_Q;			// count costs
	struct Evon_Node *Ti_Parent;		// Pointer to father
	int *Child_pi[P];		//Store child cpussor pointer address
	
};

struct Odd_Node	//������ ������ Pi
{
	int Pi; 	//cpussor pi
	int Pi_N;				// visit times
	long long int Pi_Q;			// count the time costs
	struct Odd_Node *Pi_Parent;		// Pointer to father
	int *Child_ti[V];			//Store child task pointer address
};


typedef struct Evon_Node Node_0;

typedef struct Odd_Node Node_1;


int TreePolicy(int nn)
{
	int ready_job; 
	path_index=0;
	
	//clear array 
	memset(path, 0, sizeof(path));
	memset(temp_schedule, 0, sizeof(temp_schedule));
	
	//��ʼ��������Ϣ���ظ����� 
	for(i=0; i<V; i++)
        schedule[i].PI=-1;
 	
 	
	//��������� 
	Node_0 *job;
	
	//������������ڵ�ַ��¼���� 
	if(nn==1)
	{ 
		job = (Node_0 *)malloc(sizeof(Node_0)); 	//�����½�������ڴ�ռ�
		tree_entry = job;
	} 
	else
	{
		//���״ε��� 
		job=tree_entry;
		printf("job->Ti_Q=%d\n", job->Ti_Q);
	}
		
	printf("---job pointer addres = %d\n", job);
	
	//��¼·�� 
	path[path_index++]=job;

	ready_job = 1;
	
	/*Check if the current node is the terminal node*/
	while (ready_job != V)
	{
		//�ж�job�ڵ��Ƿ���ȫ��չJudge whether nodes are fully expanded.
		count=0;
		for(i=0;i<P;i++)
			if(job->Child_pi[i]!=0)
				count++;
		printf("Child_pi count=%d\n", count);
		
		//δ��չ�� 
		if(count!=P)
		{
			printf("-----Not fully expanded.\n");
			//printf("job->Ti=%d\n", job->Ti);
			if(count==0)
			{
				printf("��һ�ε���\n");
				job->Ti = ready_job;
				job->Ti_N = 0;
				job->Ti_Q = 0;
				job->Ti_Parent = NULL;
				printf("job->Child_pi=%d,%d,%d\n", job->Child_pi[0],job->Child_pi[1],job->Child_pi[2]); 
			}

			//get the succ of ready_job
			
			//����������̼���������� 
			if(ready_job==1) 
			{
				for (i=0,j=0;i<edges_number;i++)
				{
					if(comm_costs[i][0]== 1)
					{
						ready_queue[j] = comm_costs[i][1]; 
						j++;		//����������	
					}
				}
			}
			
			return Expand(job);                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
		}
		//��ȫ��չ 
		else
		{
			printf("-----Yes, fully expanded.\n");
			//printf("ready_job=%d\n",ready_job);
			//����������̼���������� 
			for (i=0,j=0;i<edges_number;i++)
			{
				if(comm_costs[i][0]== 1)
				{
					ready_queue[j++] = comm_costs[i][1]; 
					//j++;		//J����������	
				}
			}
		
			//Ѱ����õ�UCBֵ�ڵ� 
		 	BestChild(job);
		 	int task_num;
		 	for(task_num=0;ready_queue[task_num];task_num++)
		 		printf("ready_job=%d\n",ready_queue[task_num]);
	 		
	 		ready_job=ready_queue[rand()%task_num];
	 		//��ready_queue��ɾ��ready_job
			for(j=0;ready_queue[j];j++)
				if(ready_job==ready_queue[j])
					for(k=j;k<task_num;k++)
						ready_queue[k]=ready_queue[k+1];
			//����ti�ĺ��
			
			for(i=0;i<edges_number;i++)
			{
				if(comm_costs[i][0]==ready_job)
				{
					
					//int succ; 
//					succ = comm_costs[i][1];
//					//�жϺ�̵�ǰ������
//					printf("���=%d\n", succ);
//					count = 0;
//					for(i=0;i<succ;i++)
//				 	{
//			 			if(data[i][succ-1]>0)
//					 	{
//							printf("%d��ǰ��Ϊ��%d\n",succ, i+1);
//							count++;
//			 			}
//			 			
//			 		}
//			 		printf("count=%d\n", count);
//			 		//�����ֻ��һ��ǰ�� ����ֱ�Ӽ���������� 
//					if(count==1)
//					{
//						ready_queue[task_num++]=comm_costs[i][1];
//					}
//					else	//����ж��ǰ�� 
//					{
//						printf("���ǰ��\n");
//						
//						
//					}  
			 		
					 
					 
				 
						
					//���ti�ĺ���Ƿ��Ѿ��ھ���������
					k=0;
					for(j=0;ready_queue[j];j++)
					{
						if(comm_costs[i][1]==ready_queue[j])
							k++; 
					}
					if(k==0) //���ھ��������� 
					{	
						
						ready_queue[task_num++]=comm_costs[i][1];
						printf("-----------Yes!count=%d\n",count);
					}	
				}
				
			}
		 	//Node_0 * job;
		 	job = (Node_0 *)malloc(sizeof(Node_0)); 	//�����½�������ڴ�ռ�
		 	printf("��2���������\n");
			job->Ti = ready_job;
			job->Ti_N = 0;
			job->Ti_Q = 0;
			//job->Ti_Parent = NULL;
			printf("job->Child_pi=%d,%d,%d\n", job->Child_pi[0],job->Child_pi[1],job->Child_pi[2]); 
	 		path[path_index++]=job;
	 		printf("ready_job=%d\n",ready_job);
		}
	
	}
	
	return 0;
}


int Expand(Node_0 *job)
{	
	printf("job address path[0]=%d\n", path[0]);
	Node_1 *cpu; 
	
	//���뺢�Ӵ��������ռ� 
	cpu = (Node_1 *)malloc(sizeof(Node_1));
	printf("---cpu pointer addres = %d\n", cpu);
	
	//����·�� 
	path[path_index++] = cpu; 

	//������ѡ��ռ� 
	for(i=0;job->Child_pi[i];i++);	//���㵱ǰ�ڵ㺢�Ӵ��������� 
	if(i==0)
	{
		for(j=0; j< P; j++)
		{ 	
			avail_pi[j] = j+1;
		} 
	}

	
	//���ѡ��һ�������� 
	pi=0;
	while(pi==0)
	{
		pi = avail_pi[rand()%P];
	}
	
	printf("pi=%d\n",pi);
	
	//��avail_pi��ɾ��pi��
	for(i=0;i<P;i++)
	{
		if(pi==avail_pi[i])
		{
			avail_pi[i]=0;
		}
	}
	
			
	//���������ѡ������ 
	for(i=0;i<P;i++)
		printf("avail_pi=%d\n", avail_pi[i]);
		
	//Ϊ�´��������cpu��ֵ 
	cpu->Pi = pi;
	cpu->Pi_N = 0;
	cpu->Pi_Q = 0;
	
	//parentָ��ָ���� 
	cpu->Pi_Parent = path[path_index-2];
	printf("cpu->Pi_Parent=%d\n",cpu->Pi_Parent);
	
	//����job��㺢�Ӵ��������飺child_pi
	for(i=0;i<P;i++)
	{
		if(job->Child_pi[i]==0)
		{
			job->Child_pi[i] = cpu;
			break;
		}
	}
	
	//��ӡjob��㺢�Ӵ���������
	for(i=0;i<P;i++)
		printf("job->Child_pi[%d]=%d\n", i, job->Child_pi[i]);
	
	//���ݴ�������ַ������ѡ������
//	Node_1 *test;
//	test=job->child_pi[0];
//	printf("pi=%d\n", test->pi) ;
//	printf("job->ti=%d\n",job->ti);
	
	
	return 0;
}



// Find EST
int find_EST(int task,int processor)
{
    int ST,EST=-99999,comm_cost, max_avail=0;;
    
    for(i=0; i<V; i++)
    {
        if(data[i][task]!=-1)
        {
            // If they use the same processor, the cost will be 0
            //printf("-------schedule[%d].PI=%d, processor=%d\n",i, schedule[i].PI,processor);
            if(data_transfer_rate[schedule[i].PI][processor]==0)
            {
            	comm_cost=0;
            	printf("--------Yes\n");
            }
            // Otherwise
            else
                //comm_cost=data[i][task]/data_transfer_rate[schedule[i].PI][processor];
                comm_cost=data[i][task];
            ST=schedule[i].EFT + comm_cost;
            // Try to find the max EST
            if(EST<ST)
                EST=ST;
        }
        //����EST-EFT �д����������������������Ǵ������Ŀ�ִ��ʱ�� 
        //��¼�������Ŀ�ִ��ʱ�� 
       	if(schedule[i].PI==processor)
		{
			if(max_avail<schedule[i].EFT)
			{
				max_avail= schedule[i].EFT;
			}	
		}
    }
    
    //EST��avail[j]�Ƚ�
 	return EST>max_avail?EST:max_avail;
}




/*
// Calculate the EST and EFT
void calculate_EST_EFT(int task,int processor,struct TaskProcessor *EST_EFT)
{
    double **machineFreeTime,EST;
    int i;
    machineFreeTime=(double**)calloc(100,sizeof(double*));
    for(i=0; i<100; i++)
        machineFreeTime[i]=(double*)calloc(2,sizeof(double));
    int noslots=0;
    findfreeslots(processor,machineFreeTime,&noslots);
    //if(task==2)
    //for(i=0;i<noslots;i++)
    //{
    //	printf("%lf %lf\n",machineFreeTime[i][0],machineFreeTime[i][1]);
    //}
    printf("\n\n");
    EST=find_EST(task,processor);
    //printf("%lf\n",EST);
    EST_EFT->AST=EST;
    EST_EFT->processor=processor;
    for(i=0; i<noslots; i++)
    {
        if(EST<machineFreeTime[i][0])
        {
            if((machineFreeTime[i][0] + computation_costs[task][processor]) <= machineFreeTime[i][1])
            {
                EST_EFT->AST=machineFreeTime[i][0];
                EST_EFT->AFT=machineFreeTime[i][0] + computation_costs[task][processor];
                return;
            }
        }
        if(EST>=machineFreeTime[i][0])
        {
            if((EST + computation_costs[task][processor]) <= machineFreeTime[i][1])
            {
                EST_EFT->AFT=EST_EFT->AST + computation_costs[task][processor];
                return;
            }
        }
    }
}

//ִ�е��� 
void make_schedule()
{
    int i,j,k,t=0,processor,task;
    double minCost=99999.99,min_EFT=99999.99;
    struct TaskProcessor *EST_EFT;
    EST_EFT=(struct TaskProcessor *)calloc(1,sizeof(struct TaskProcessor));

    for(i=0; i<no_tasks; i++)
    {
        min_EFT=9999.99;
        task=sorted_tasks[i];
        // Check if it is a start task
        if(isEntryTask(task))
        {
            for(j=0; j<no_machines; j++)
            {
                if(minCost>computation_costs[task][j])
                {
                    minCost=computation_costs[task][j];
                    processor=j;
                }
            }
            schedule[task].processor=processor;
            schedule[task].AST=0;
            schedule[task].AFT=minCost;
        }
        else
        {
            for(j=0; j<no_machines; j++)
            {
                calculate_EST_EFT(task,j,EST_EFT);
                printf("%lf %lf %d",EST_EFT->AST,EST_EFT->AFT,EST_EFT->processor);
                if(min_EFT>(EST_EFT->AFT))
                {
                    schedule[task]=*EST_EFT;
                    min_EFT=EST_EFT->AFT;
                }
            }
        }

        printf("\nTask scheduled %d\n",task);
        printf("%d %lf %lf\n",schedule[task].processor,schedule[task].AST,schedule[task].AFT);
        printf("------\n");
    }
}*/



int DefaultPolicy(int nn) 
{
  	//# 2. Random run to add node and get reward
  	int job_remin_num=0, index=0;
	for(i=0;ready_queue[i];i++)
		printf("ready_job=%d\n",ready_queue[i]);
	
	/*�������*/
	Node_0 *job_temp;
	Node_1 *cpu_temp;
	
 	//ȷ��������-�������� 
 	for(i=0, j=1;path[i]&&path[j];i+=2,j+=2)
 	{
 		//ż���� ti 
		job_temp = path[i];
		ti = job_temp->Ti;
	 	
	 	//������ pi
	 	cpu_temp = path[j];
		pi = cpu_temp->Pi;
	 	
		printf("ti=%d, pi=%d\n", ti, pi);
		
		//��ʼ���� 
		if(ti==1)
		{
			schedule[ti-1].PI = pi-1;
			//������ʱ�����б� 
			temp_schedule[index++]=ti;
			
			schedule[ti-1].EST = 0;
			schedule[ti-1].EFT = comp_costs[0][pi-1];
			printf("Ti=%d\t", ti);
			printf("PI=%d\t", schedule[ti-1].PI); 
			printf("EST=%d\t", schedule[ti-1].EST);
			printf("EFT=%d\n", schedule[ti-1].EFT);
			
		}
		else
		{
			//����EST-EFT 
			est = find_EST(ti-1, pi-1);
			eft = comp_costs[ti-1][pi-1]+est;
			
	 		//������ʱ�����б� 
			temp_schedule[index++]=ti;
			
			//�����Ϣ��schedule
		 	schedule[ti-1].PI = pi-1;
			schedule[ti-1].EST = est;
			schedule[ti-1].EFT = eft;
			
	 		printf("Ti=%d\t", ti);
			printf("PI=%d\t", schedule[ti-1].PI); 
			printf("EST=%d\t", schedule[ti-1].EST);
			printf("EFT=%d\n", schedule[ti-1].EFT);
			
		} 
		job_remin_num++;

 	}
 	
 	//������������������������ 
 	printf("-----����������������------\n");
 	int m, temp_succ[V]={}, succ_index=0;		//temp_succ[]��¼ti�ģ���̵�ǰ����Ψһ����� 
 	
 	for(m=0;m<V-job_remin_num;m++)
 	{
	 	printf("----------------------------------m=%d, nn=%d\n", m, nn); 
	 	
	 	//������������е������� 
	 	int task_num;
	 	
 	L1: 
	 	for(task_num=0;ready_queue[task_num];task_num++);
	 	//���ѡ������
	 	ti=ready_queue[rand()%task_num];
	 	
	 	
	 	//�ж�ti��ǰ���Ƿ����ɵ���
	 	/*1.�ҵ�ti��ǰ������count*/
	 	count=0;
	 	int pred[V]={};
		j=0; 
	 	for(i=0;i<ti;i++)
	 	{
 			if(data[i][ti-1]>0)
		 	{
				printf("%d��ǰ��Ϊ��%d\n",ti, i+1);
				pred[j++]=i+1;
				count++;
 			}
 			
 		}
 		/*������ɵĵ��ȵ�������*/
 		int temp_count=0;
 		for(k=0;pred[k];k++)
 		{
		 	for(j=0;temp_schedule[j];j++)
	 		{
	 			if(pred[k]==temp_schedule[j])
	 			{
			 		temp_count++;
			 	}
	 		}	
	 	}
	 	//��ӡ�����б� 
	 	for(k=0;temp_schedule[k];k++)
 		{
 			printf("temp_schedule[k]=%d\n", temp_schedule[k]);
	 	}
 		printf("temp_count=%d, count=%d\n", temp_count, count); 
 		
	 	//ǰ������ɵ��� 
	 	if(count==temp_count)
	 	{
	 		pi= rand()%P + 1;
	 		//printf("ti= %d,pi= %d\n", ti, pi);

	 		//��ready_queue��ɾ��ti
			for(j=0;ready_queue[j];j++)
				if(ti==ready_queue[j])
					for(k=j;k<task_num;k++)
						ready_queue[k]=ready_queue[k+1];
						
			//��������������� 
			for(j=0;ready_queue[j];j++)
				printf("ready_queue=%d\n", ready_queue[j]);
				
			//��������һ 
			task_num-=1;
			
			
			/*��Ҫ�Ż�:
			1. ��tiֻ��һ��ǰ����ֱ�Ӽ���������У�
			2. ��ti�ж��ǰ����ti��̼���һ����ʱ�б���, ��ǰ������ɵ���ʱ�ټ���������С�*/
				
			//����ti�ĺ��
			
			for(i=0;i<edges_number;i++)
			{
				if(comm_costs[i][0]==ti)
				{
					
					//int succ; 
//					succ = comm_costs[i][1];
//					//�жϺ�̵�ǰ������
//					printf("���=%d\n", succ);
//					count = 0;
//					for(i=0;i<succ;i++)
//				 	{
//			 			if(data[i][succ-1]>0)
//					 	{
//							printf("%d��ǰ��Ϊ��%d\n",succ, i+1);
//							count++;
//			 			}
//			 			
//			 		}
//			 		printf("count=%d\n", count);
//			 		//�����ֻ��һ��ǰ�� ����ֱ�Ӽ���������� 
//					if(count==1)
//					{
//						ready_queue[task_num++]=comm_costs[i][1];
//					}
//					else	//����ж��ǰ�� 
//					{
//						printf("���ǰ��\n");
//						
//						
//					}  
			 		
					 
					 
				 
						
					//���ti�ĺ���Ƿ��Ѿ��ھ���������
					k=0;
					for(j=0;ready_queue[j];j++)
					{
						if(comm_costs[i][1]==ready_queue[j])
							k++; 
					}
					if(k==0) //���ھ��������� 
					{	
						
						ready_queue[task_num++]=comm_costs[i][1];
						printf("-----------Yes!count=%d\n",count);
					}	
				}
				
			}
			
					
		 //	//��������������� 
//			for(j=0;ready_queue[j];j++)
//				printf("ready_queue=%d\n", ready_queue[j]);
				
		 	printf("---------------------\n");
		 	printf("Ti= %d,Pi= %d\n", ti, pi);
		 	est = find_EST(ti-1, pi-1);
		 	eft = comp_costs[ti-1][pi-1]+est;
		 	//������ʱ�����б� 
			temp_schedule[index++]=ti;
			
		 	schedule[ti-1].PI = pi-1;
			schedule[ti-1].EST = est;
			schedule[ti-1].EFT = eft;
	 		printf("Ti=%d\t", ti);
			printf("PI=%d\t", schedule[ti-1].PI); 
			printf("EST=%d\t", schedule[ti-1].EST);
			printf("EFT=%d\n", schedule[ti-1].EFT);
			makespan = eft;
			
			//printf("m=%d\n",m);
	 	}
	 	else
		{
			printf("��ת.....\n");
			//��������������� 
			for(j=0;ready_queue[j];j++)
				printf("ready_queue=%d\n", ready_queue[j]);
				
			goto L1;
		} 
	}
	return -makespan;
}

int BestChild(Node_0 *job)
{
	/*����UCBֵ��ѡȡ���ֵ��������*/
	//for(i=0;path[i];i++)
//	{
//		printf("path=%d\n", path[i]);
//	}
	double ucb, max_ucb=DBL_MIN; 
	Node_1 *ucb_pi, *max_ucb_pi;
	for(i=0;i<P;i++)
	{
		ucb_pi=job->Child_pi[i];
		
		//printf("CP*sqrt(2*(log(job->Ti_N)/ucb_pi->Pi_N)=%.2lf\n", CP*sqrt(2*(log(job->Ti_N)/ucb_pi->Pi_N)));
		ucb = ucb_pi->Pi_Q/ucb_pi->Pi_N + CP*sqrt(2*(log(job->Ti_N)/ucb_pi->Pi_N));
		printf("Pi_N=%d\tPi_Q=%d\t", ucb_pi->Pi_N, ucb_pi->Pi_Q);
		printf("ucb=%.2lf\n", ucb); 
		if(ucb>max_ucb)
		{
			max_ucb = ucb;
			max_ucb_pi = ucb_pi; 
		}
		//printf("max_ucb=%.2lf\n",max_ucb); 	
	}
	printf("max_ucb=%.2lf\n", max_ucb);
	path[path_index++]=max_ucb_pi;
	//for(i=0;path[i];i++)
//	{
//		printf("path=%d\n", path[i]);
//	}
	return 0;
}

int BackUp()
{
	//��ӡ������Ϣ 
	printf("------������Ϣ------\n");
	for(i=0;i<V;i++)
	{	
		ti=temp_schedule[i];
		printf("Ti=%d\tPi=%d\tEST=%d\tEFT=%d\n", ti, schedule[ti-1].PI+1, schedule[ti-1].EST, schedule[ti-1].EFT);
	} 
	
	Node_0 *temp_0;		//��ʱָ�� 
	Node_1 *temp_1;
	
	for(i=0, j=1;path[i];i+=2, j+=2)
	{ 
		//printf("path=%d\n", path[i]);
		//����N��Qֵ
	
	 	temp_0 = path[i];
	 	temp_1 = path[j];

	 	ti = temp_0->Ti;
	 	pi = temp_1->Pi;
	 		 	
	 	temp_0->Ti_N += 1;
	 	temp_1->Pi_N += 1;
	 	
	 	est = schedule[ti-1].EST;
	 	eft = schedule[ti-1].EFT;
	 	
	 	if(ti==1)
 		{
 			temp_0->Ti_Q += makespan;
 			temp_1->Pi_Q = temp_1->Pi_Q + makespan + eft;
 		}	
 		else
 		{
		 	printf("������������");
		 	
		 	
		 	
 		}
		printf("-------------------------%d\n", (i+j)/2+1); 
	 	printf("Ti=%d\tTi_N=%d\tTi_Q=%d\n", temp_0->Ti, temp_0->Ti_N, temp_0->Ti_Q);
	
	 	printf("Pi=%d\tPi_N=%d\tPi_Q=%d\n", temp_1->Pi, temp_1->Pi_N, temp_1->Pi_Q);

	 	//temp_1.Pi_Q
		
		
	} 
	
	 
		
		
		
	return 0;
}

float UCT_Seach()
{
	int nn=1;
	
 	clock_t t_start, t_end;
	float running_time=0.0;
 	
	t_start = clock();

	while (running_time < MAXTIME)
	{
		
		printf("--------------------------------------------nn = %d\n", nn);
		printf("--running_time = %.3f s--\n", running_time);
		
 		/*1. Find the best node to expand*/
		
 		
		//for (i=0;ready_queue[i]!=0;i++)
// 			printf("ready_queue[%d] = %d\n", i, ready_queue[i]);
 		
 		TreePolicy(nn);
 		
 		/*2. Random run to add node and get reward*/
 		makespan = DefaultPolicy(nn);
 		printf("makespan=%d\n", makespan);
 		
 		/*3.Update all passing nodes with reward */
 		BackUp();
 		
 		
		t_end = clock();
		running_time = (t_end - t_start)/1000.0;
		printf("--running_time = %.3f s--\n", running_time);
		nn++; 
	}
	Node_0 *entry;
	entry = path[0];
	return entry->Ti_Q/entry->Ti_N;
}



int main()
{

	//����������ظ� 
	srand((unsigned)time(NULL));
	
    fp1 = fopen("_1_comp_costs.txt", "r+");
    fp2 = fopen("_1_comm_costs.txt", "r+");
    //printf("1-%d\n", fp2);
    
    //��ʼ�� ����-�������ṹ�� 
	schedule=(struct TaskProcessor*)calloc(V,sizeof(struct TaskProcessor));
    for(i=0; i<V; i++)
        schedule[i].PI=-1;
 
    // Initialize Computation Cost Table
    comp_costs = (int **)calloc(V, sizeof(int *));		//int* int�͵�ָ�������	
	/*���ڴ�Ķ�̬�洢���з���v
	������Ϊsize�������ռ䣬��������һ��ָ�������ʼ��ַ��ָ��*/
	
    // Initialize each row
    for(i=0; i<V; i++)
        comp_costs[i]=(int *)calloc(P, sizeof(int));
        
        
    
    /*get edges_number*/
	int flag = 0;
	//printf("2-%d\n", fp2);
    while(!feof(fp2))	//int feof(FILE *fp)
 	{
	    flag = fgetc(fp2);	//int fgetc(FILE *stream)
	    //printf("--%c", flag);
	    if(flag == '\n')
	      	edges_number++;
 	}
 	//printf("3-%d\n", fp2);
 	//printf("edges_number=%d\n", edges_number);
	fclose(fp2);
	
	fp2 = fopen("_1_comm_costs.txt", "r+");

	// Initialize comm_costs 
    comm_costs = (int **)calloc(edges_number, sizeof(int *));
    // Initialize each row
    for(i=0; i<edges_number; i++)
        comm_costs[i]=(int *)calloc(P, sizeof(int));
        

	// Read the computation costs of each task
    for(i=0; i<V; i++)
        for(j=0; j<P; j++)
            fscanf(fp1,"%d", &comp_costs[i][j]);
            
    /*
	//Print computation costs
   	printf("computation costs:\n");
    for(i=0; i<V; i++)
    {
    	for(j=0; j<P; j++)
    		printf("%d ", comp_costs[i][j]);
   		printf("\n");
    }*/
    
    // Read the communication costs
    for(i=0; i<edges_number; i++)
    {
    	for(j=0; j<3; j++)
        {
        	fscanf(fp2, "%d", &comm_costs[i][j]);
        	//printf("%d ", comm_costs[i][j]);
        }
        //printf("\n");
    }
    
     // Initialize Data Table
    data=(int**)calloc(V ,sizeof(int*));
    // Initialize each row
    for(i=0; i<V; i++)
        data[i]=(int*)calloc(V,sizeof(int));

   	//��ֵdata �����ڽӾ��� 
   	for(i=0; i<V; i++)
    {
    	for(j=0; j<V; j++)
        {
			data[i][j]=-1;
       		//printf("%d\t", data[i][j]);
        }
    }
    
	
    //Print communication costs
    printf("communication costs:\n");
    for(i=0; i<edges_number; i++)
    {
    	int ci,cj,w;
    	ci=comm_costs[i][0];
    	cj=comm_costs[i][1];
    	w=comm_costs[i][2];
    	data[ci-1][cj-1] = w;
    	//for(j=0; j<3; j++)
//    	{
//	    	printf("%d ", comm_costs[i][j]);
//	    }
//    		
//   		printf("\n");
    }
    
    //��ӡ 
    for(i=0; i<V; i++)
    {
    	for(j=0; j<V; j++)
        {
        	printf("%d\t", data[i][j]);
        }
        printf("\n");
    }
    
    // Initialize Data Transfer Rate Table
    data_transfer_rate=(int**)calloc(P,sizeof(int*));
    // Initialize each row
    for(i=0; i<P; i++)
        data_transfer_rate[i]=(int*)calloc(P, sizeof(int));
  	//��ֵ
	 for(i=0; i<P; i++)
        for(j=0; j<P; j++)
        {
        	if(i==j)
        		data_transfer_rate[i][j]=0;
       		else
       			data_transfer_rate[i][j]=1; 
		} 
		
   	//��ӡ data_transfer_rate
    printf("data_transfer_rate:\n");
    for(i=0; i<P; i++)
    {
    	for(j=0; j<P; j++)
    		printf("%d ", data_transfer_rate[i][j]);
   		printf("\n");
    }
    
   
   	//���ؿ��������� 
   	double best_makespan;
  	best_makespan=UCT_Seach();
  	printf("best_makespa%.2lf\n", best_makespan);
 	//getchar();

	return 0;
}
