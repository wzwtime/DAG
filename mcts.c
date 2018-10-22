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
#define MAXTIME 0.3	//s
#define CP 10
#define DBL_MIN -100000


int i, j, k, ti, pi, est, eft, makespan, count, edges_number = 0, ready_queue[MAXLENGTH];
int **comp_costs, **comm_costs, **data_transfer_rate, **data;		//这个指针指向的是一个指针的地址
FILE *fp1, *fp2;
int avail_pi[P];
int path_index;
long long int *path[2*V];
int *child_pi;
int *child_ti;
int temp_schedule[V];
int tree_entry;		//记录搜索树的入口地址 
int temp_succ[V]={}, succ_index=0;		//temp_succ[]记录ti的（后继的前驱不唯一）后继 
int NN=1;


struct TaskProcessor
{
    int PI;
    int EST;
    int EFT;
};

struct TaskProcessor *schedule;


struct Odd_Node	//奇数层 任务 Ti
{
	int Ti; 	//task ti 命名规则：i_Ti，i_N， lli_ 
	int Ti_N;				// visit times
	long long int Ti_Q;			// count costs
	struct Evon_Node *Ti_Parent;		// Pointer to father
	int *Child_pi[P];		//Store child cpussor pointer address
	
};

struct Evon_Node	//偶数层 处理器 Pi
{
	int Pi; 	//cpussor pi
	int Pi_N;				// visit times
	long long int Pi_Q;			// count the time costs
	struct Odd_Node *Pi_Parent;		// Pointer to father
	int *Child_ti[V];			//Store child task pointer address
};

typedef struct Odd_Node Node_1;
typedef struct Evon_Node Node_2;


/*返回数组中数据个数*/ 
int len(int array[])
{
	int length;
	for(length=0;array[length];length++);
	return length;
}

void Update_Ready_Queue(int ti)
{/*加入临时后继列表函数*/
	int task_num = len(ready_queue);
	//在ready_queue中删除ti
	for(j=0;ready_queue[j];j++)
		if(ti==ready_queue[j])
			for(k=j;k<task_num;k++)
				ready_queue[k]=ready_queue[k+1];
	task_num -=1;
	for(i=0;i<edges_number;i++)
 	{
 		int succ;
 		if(comm_costs[i][0]==ti)
		{
			succ = comm_costs[i][1];	 	
			/*进行后继的前驱个数判断*/ 
			int pred_num=0;
			for(j=0;j<edges_number;j++)
			{
				if(comm_costs[j][1]==succ)
				{
					pred_num++;
				}
			}
			//printf("pred_num=%d\n", pred_num);
			/*若ti后继的前驱只有一个则直接加入就绪队列 */
			if(pred_num==1)
			{
				printf("%d加入就绪队列！\n", succ);
				ready_queue[task_num++] = succ;		//!!!!!!!!!用到task_num 
			}
			else
			{
				//判断后继是否已经加入临时后继列表 
				int label=1;		//标记是否出现过 ,label=1未出现过 
				for(k=0;temp_succ[k];k++)
				{
					if(succ==temp_succ[k])
					{
						label = 0; 
					}
				}
				if(label)
				{
					temp_succ[succ_index++] = succ;
				}					
			} 		
		}
	} 
	
 	//判断临时后继任务是否可以加入就绪队列
	for(i=0;temp_succ[i];i++)
	{
		//printf("temp_succ=%d\n", temp_succ[i]);
		ti = temp_succ[i];
		
		//计算ti的前驱个数 
		int ti_pred_num=0,ti_pred_sched_num=0, pred[V]={}, pred_index=0;
		for(j=0;j<edges_number;j++)
	 	{
 			if(comm_costs[j][1]==ti)
		 	{
		 		ti_pred_num++;
				pred[pred_index++]=	comm_costs[j][0];
			} 
 		}
 		
 		//计算ti前驱调度完成的数量
 		for(j=0;pred[j];j++)
 		{
		 	for(k=0;temp_schedule[k];k++)
	 		{
	 			if(pred[j]==temp_schedule[k])
	 			{
			 		ti_pred_sched_num++;
			 	}
	 		}	
	 	}
 		//printf("ti_pred_num=%d, ti_pred_sched_num=%d\n", ti_pred_num, ti_pred_sched_num);
 		//判断
		if(ti_pred_num==ti_pred_sched_num)
		{
			printf("%d加入就绪队列！\n", ti);
			ready_queue[task_num++]=ti;
			
			//从临时后继列表中删除ti
		 	for(j=0;temp_succ[j];j++)
				if(ti==temp_succ[j])
					for(k=j;k<succ_index;k++)
						temp_succ[k]=temp_succ[k+1];
			
			succ_index--;	//索引减一 ！！！！！ 
		} 	
	}
} 


int TreePolicy(int nn)
{
	int ready_job; 
	path_index=0;
	succ_index=0;
	
	//clear array 
	memset(path, 0, sizeof(path));
	memset(temp_schedule, 0, sizeof(temp_schedule));
	memset(temp_succ, 0, sizeof(temp_succ));
	
	//初始化调度信息，重复利用 
	for(i=0; i<V; i++)
        schedule[i].PI=-1;
 	
 	
	Node_1 *job;	//奇层任务结点 
	Node_2 *Proce;		//处理器指针 

	if(nn==1)
	{ 
		job = (Node_1 *)malloc(sizeof(Node_1)); 	//申请新结点所需内存空间
		tree_entry = job;		//将搜索树的入口地址记录下来 
	} 
	else
	{
		//非首次迭代 
		job=tree_entry;
		printf("job->Ti_Q=%d\n", job->Ti_Q);
	}
		
	//printf("---job pointer addres = %d\n", job);
	
	//记录路径 
	path[path_index++]=job;

	
	ready_queue[0]=1; 
	ready_job = 1;
	Update_Ready_Queue(ready_job);

	/*Check if the current node is the terminal node*/
	while (ready_job != V)
	{
		//判断job奇数层节点是否完全扩展Judge whether nodes are fully expanded.
		count=0;
		//job=path[0];
		for(i=0;i<P;i++)
		{ 
			if(job->Child_pi[i]!=0)		//job需要修改 !!!!!!!!!!!
			{ 
				count++;
			} 
		} 
				
		printf("Child_pi count=%d\n", count);
		
		//未扩展完 
		if(count!=P)
		{
			printf("-----Not fully expanded.\n");
			//printf("job->Ti=%d\n", job->Ti);
			if(count==0)
			{
				//printf("job=%d的第一次迭代\n", ready_job);
				job->Ti = ready_job;
				job->Ti_N = 0;
				job->Ti_Q = 0;
				job->Ti_Parent = NULL;
				printf("job->Child_pi=%d,%d,%d\n", job->Child_pi[0],job->Child_pi[1],job->Child_pi[2]); 
			}
			
			//将入口任务后继加入就绪队列 
			//if(ready_job==1) 
//			{
//				for (i=0,j=0;i<edges_number;i++)
//				{
//					if(comm_costs[i][0]== 1)
//					{
//						ready_queue[j++] = comm_costs[i][1]; //j就绪任务数					
//					}
//				}
//			}
			
			return Expand(job);                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
		}
		//job层完全扩展 
		else
		{
			printf("-----Yes, job=%d fully expanded.\n", ready_job);
			
			//寻找最好的UCB值节点 --处理器层 
		 	BestChild_Pi(job);
			
			
			//////将入口任务后继加入就绪队列 ,有问题！！！！！！！！！！！！！！ 
//			for (i=0,j=0;i<edges_number;i++)
//			{
//				if(comm_costs[i][0]== 1)
//				{
//					ready_queue[j++] = comm_costs[i][1]; //j就绪任务数			
//				}
//			}
			
			int task_num = len(ready_queue);
			printf("task num=%d\n", task_num); 
			
			
			//判断处理器偶数层节点是否完全扩展
			Node_2 *Proce;		//处理器指针 
			//printf("len(path)=%d\n", len(path));
			Proce = path[len(path)-1];		//最后一个地址就是最优UCB值的节点地址 
			
		 	pi = Proce->Pi;
		 	
		 	int ti_count=0; 
		 	int temp_ready_queue[V] = {},temp_ready_indes=0;
		 	//复制就绪队列 
			memcpy(temp_ready_queue, ready_queue, sizeof(int)*task_num); //不改变原始的就绪队列 
			
			for(i=0;i<task_num;i++)		//计算处理器孩子任务完成数量 
			{	
				//printf("-------------------------i=%d\n", i);
				//printf("Proce->Child_ti[%d]=%d\n", i, Proce->Child_ti[i]);
				if(Proce->Child_ti[i]!=0)
				{
					ti_count++;
					job = Proce->Child_ti[i];		//更新job 
					ready_job = job->Ti;
					
					//在temp_ready_queue中删除ready_job
					for(j=0;temp_ready_queue[j];j++)
						if(ready_job==temp_ready_queue[j])
							for(k=j;k<task_num;k++)
								temp_ready_queue[k]=temp_ready_queue[k+1];
					
					printf("----兄弟任务ready_job=%d\n", ready_job);

				}
			} 
			printf("ti_count=%d\n", ti_count);
			
			if(ti_count!=task_num)		//处理器孩子任务节点未扩展完 
			{
				printf("Pi=%d------Not Full expanded!\n", pi);
				job = (Node_1 *)malloc(sizeof(Node_1));		//申请新结点所需内存空间
				
				ready_job = temp_ready_queue[rand()%len(temp_ready_queue)];	
					
				job->Ti = ready_job; 
				job->Ti_N = 0;
				job->Ti_Q = 0;
				printf("---ready_job=%d----job->Child_pi=%d,%d,%d\n", ready_job, job->Child_pi[0],job->Child_pi[1],job->Child_pi[2]); 
				task_num = len(ready_queue);		//更新任务数量 
				//在ready_queue中删除ready_job
				//for(j=0;ready_queue[j];j++)
//					if(ready_job==ready_queue[j])
//						for(k=j;k<task_num;k++)
//							ready_queue[k]=ready_queue[k+1];
				//更新就绪队列 
				Update_Ready_Queue(ready_job);
				
				for(i=0;ready_queue[i];i++)
					printf("ready_job=%d\n",ready_queue[i]);
				printf("---------后继队列------------\n");
				for(i=0;temp_succ[i];i++) 
					printf("Temp_succ[%d]=%d\n", i, temp_succ[i]);
				printf("---------后继队列------------\n");
				//存储处理器孩子job地址 
				Proce->Child_ti[ti_count++]=job;		
				path[path_index++] = job;
				return Expand(job);
				
			}
			else
			{
				printf("Pi=%d------Full expanded!\n", pi);
				
				/*选择最好的任务Ti调度，计算UCB*/ 
				Proce = path[path_index-1];
				
				//更新ready_job 
				ready_job = BestChild_Ti(task_num, Proce);
				Update_Ready_Queue(ready_job); 
				
				//更新job地址 
				job = path[path_index-1];
			}

		}
		printf("------------------Ready_job=%d\n", ready_job);
	}
	
	return 0;
}


int Expand(Node_1 *job)
{	
	//printf("job address path[0]=%d\n", path[0]);
	Node_2 *cpu, *temp_cpu; 
	
	//申请孩子处理器结点空间 
	cpu = (Node_2 *)malloc(sizeof(Node_2));
	//printf("---cpu pointer addres = %d\n", cpu);
	
	//加入路径 
	path[path_index++] = cpu; 

	//初始化处理器选择空间 
	for(i=0;i<P;i++)
	{
		avail_pi[i]= i+1;
	} 
	for(count=0;job->Child_pi[count];count++);	//计算当前节点孩子处理器数量 
	if(count>0)
	{
		//删除已占用的pi
		for(j=0;j<count;j++)		//!!!!!count 
		{
			temp_cpu = job->Child_pi[j];
			pi= temp_cpu->Pi;
			printf("----PI=%d\n", pi);
			avail_pi[pi-1]=0;
		} 
	}
	//for(i=0;job->Child_pi[i];i++);	//计算当前节点孩子处理器数量 
//	if(i==0)
//	{
//		for(j=0; j< P; j++)
//		{ 	
//			avail_pi[j] = j+1;
//		} 
//	}

	//随机选择一个处理器 
	pi=0;
	while(pi==0)
	{
		pi = avail_pi[rand()%P];
	}
	
	printf("pi=%d\n",pi);
	
	//在avail_pi中删除pi：
	for(i=0;i<P;i++)
	{
		if(pi==avail_pi[i])
		{
			avail_pi[i]=0;
		}
	}

	//测试输出可选处理器 
	for(i=0;i<P;i++)
	{
		if(avail_pi[i])
		{
			printf("avail_pi=%d\t", avail_pi[i]);
		}
	}
	printf("\n");
	//为新处理器结点cpu赋值 
	cpu->Pi = pi;
	cpu->Pi_N = 0;
	cpu->Pi_Q = 0;
	
	//parent指针指向父亲 
	cpu->Pi_Parent = path[path_index-2];
	//printf("cpu->Pi_Parent=%d\n",cpu->Pi_Parent);
	
	//更新job结点孩子处理器数组：child_pi
	for(i=0;i<P;i++)
	{
		if(job->Child_pi[i]==0)
		{
			job->Child_pi[i] = cpu;
			break;
		}
	}
	
	//打印job结点孩子处理器数组
	//for(i=0;i<P;i++)
//		printf("job->Child_pi[%d]=%d\n", i, job->Child_pi[i]);
		
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
            	//printf("--------Yes\n");
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
        //计算EST-EFT 有错！！！！！！！！！！考虑处理器的可执行时间 
        //记录处理器的可执行时间 
       	if(schedule[i].PI==processor)
		{
			if(max_avail<schedule[i].EFT)
			{
				max_avail= schedule[i].EFT;
			}	
		}
    }
    
    //EST与avail[j]比较
 	return EST>max_avail?EST:max_avail;
}


int DefaultPolicy(int nn) 
{
  	//# 2. Random run to add node and get reward
  	int job_remin_num=0, index=0;
  	printf("----DefaultPolicy----\n");
	for(i=0;ready_queue[i];i++)
		printf("ready_job=%d\n",ready_queue[i]);
	
	/*随机调度*/
	Node_1 *job_temp;
	Node_2 *cpu_temp;
	
 	//确定的任务-处理器对 
 	//for(i=0, j=1;path[i]&&path[j];i+=2,j+=2)
 	printf("------确定的任务-处理器对------\n"); 
 	int ii,jj;
 	for(ii=0, jj=1;ii<len(path);ii+=2,jj+=2)
 	{
 		
 		//printf("ii=%d\tjj=%d\n", ii, jj);
 		//奇数层 ti 
		job_temp = path[ii];
		ti = job_temp->Ti;
	 	
	 	//偶数层 pi
	 	cpu_temp = path[jj];
		pi = cpu_temp->Pi;
	 	
		//printf("ti=%d, pi=%d\n", ti, pi);
		
		//初始任务 
		if(ti==1)
		{
			est = 0;	//计算EST
		}
		else
		{			
			est = find_EST(ti-1, pi-1);	//计算EST,!!!!!!!!!!改变了i的值，i为全局变量 
		}
		
		//加入临时调度列表 
		temp_schedule[index++]=ti;
		
		//计算EFT 
		eft = comp_costs[ti-1][pi-1]+est;

		//添加信息至schedule
	 	schedule[ti-1].PI = pi-1;
		schedule[ti-1].EST = est;
		schedule[ti-1].EFT = eft;
		
 		printf("Ti=%d\t", ti);
		printf("PI=%d\t", pi); 
		printf("EST=%d\t", est);
		printf("EFT=%d\n", eft);
		
		//调度完成任务数加1 
		job_remin_num++;
 	}
 	
 	/*其余任务：随机任务、随机处理器 */
 	printf("-----随机任务、随机处理器------\n");
 	//int m, temp_succ[V]={}, succ_index=0;		//temp_succ[]记录ti的（后继的前驱不唯一）后继 
 	
	int m;
 	for(m=0;m<V-job_remin_num;m++)
 	{
	 	printf("----------------------------------m=%d, nn=%d\n", m, nn); 
	 	int task_num;
	 	
 		/*计算就绪队列中的任务数*/
 		
 		task_num = len(ready_queue);
 		printf("task_num=%d\n", task_num);
 		
	 	//for(task_num=0;ready_queue[task_num];task_num++);
	 	
	 	/*随机选择任务*/
 		//测试输出就绪队列 
		for(j=0;ready_queue[j];j++)
			printf("ready_queue=%d\n", ready_queue[j]);
			
	 	ti=ready_queue[rand()%task_num];
	 	
	 	//加入临时调度列表 
		temp_schedule[index++]=ti;
		
		//随机处理器 
	 	pi= rand()%P + 1;
	 	
	 	printf("---------------------\n");
	 	//printf("Ti= %d,Pi= %d\n", ti, pi);
	 	est = find_EST(ti-1, pi-1);
	 	eft = comp_costs[ti-1][pi-1]+est;
	 	
		
	 	schedule[ti-1].PI = pi-1;
		schedule[ti-1].EST = est;
		schedule[ti-1].EFT = eft;
		
 		printf("Ti=%d\t", ti);
		printf("PI=%d\t", schedule[ti-1].PI+1); 
		printf("EST=%d\t", schedule[ti-1].EST);
		printf("EFT=%d\n", schedule[ti-1].EFT);
		
		
	 	//更新就绪队列 
	 	Update_Ready_Queue(ti);

	}
	makespan = eft;
	return -makespan;
}

int BestChild_Pi(Node_1 *job)
{
	/*计算UCB值，选取最大值进入搜索（选处理器）*/

	double ucb, max_ucb=DBL_MIN; 
	Node_2 *ucb_pi, *max_ucb_pi;
	
	for(i=0;i<P;i++)
	{
		ucb_pi=job->Child_pi[i];
		
		printf("PI=%d\t", ucb_pi->Pi);
		ucb = ucb_pi->Pi_Q/ucb_pi->Pi_N + CP*sqrt(2*(log(job->Ti_N)/ucb_pi->Pi_N));
		
		printf("Pi_N=%d\tPi_Q=%d\t", ucb_pi->Pi_N, ucb_pi->Pi_Q);
		printf("ucb=%.2lf\n", ucb); 
		
		if(ucb>max_ucb)
		{
			max_ucb = ucb;
			max_ucb_pi = ucb_pi; 
		}	
	}
	printf("max_ucb=%.2lf, Best Pi=%d\n", max_ucb, max_ucb_pi->Pi);
	//加入路径 
	path[path_index++]=max_ucb_pi;

	return 0;
}

int BestChild_Ti(int task_num, Node_2 *proce)
{
	/*计算UCB值，选取最大值进入搜索（选任务）*/
	printf("---------------------------------------------------task_num=%d, NN=%d\n", task_num, NN++);
	double ucb, max_ucb=DBL_MIN; 
	Node_1 *ucb_ti, *max_ucb_ti;
	
	for(i=0;i<task_num;i++)
	{
		ucb_ti=proce->Child_ti[i];
		
		printf("TI=%d\t", ucb_ti->Ti);
		ucb = ucb_ti->Ti_Q/ucb_ti->Ti_N + CP*sqrt(2*(log(proce->Pi_N)/ucb_ti->Ti_N));
		
		printf("Ti_N=%d\tTi_Q=%d\t", ucb_ti->Ti_N, ucb_ti->Ti_Q);
		printf("ucb=%.2lf\n", ucb); 
		
		if(ucb>max_ucb)
		{
			max_ucb = ucb;
			max_ucb_ti = ucb_ti; 
		}	
	}
	printf("max_ucb=%.2lf, Best Ti=%d\n", max_ucb, max_ucb_ti->Ti);
	//加入路径 
	path[path_index++]=max_ucb_ti;

	return max_ucb_ti->Ti;
}

int BackUp()
{
	//打印调度结果信息 
	printf("------------调度结果------------\n");
	for(i=0;i<V;i++)
	{	
		ti=temp_schedule[i];
		printf("Ti=%d\tPi=%d\tEST=%d\tEFT=%d\n", ti, schedule[ti-1].PI+1, schedule[ti-1].EST, schedule[ti-1].EFT);
	} 
	
	Node_1 *temp_1;		//临时指针 
	Node_2 *temp_2;
	
	for(i=0, j=1;path[i];i+=2, j+=2)
	{ 
		//printf("path=%d\n", path[i]);
		//更新N，Q值
	
	 	temp_1 = path[i];
	 	temp_2 = path[j];

	 	ti = temp_1->Ti;
	 	pi = temp_2->Pi;
		
		//更新N值 
	 	temp_1->Ti_N += 1;
	 	temp_2->Pi_N += 1;
	 	
	 	est = schedule[ti-1].EST;
	 	eft = schedule[ti-1].EFT;
	 	
		//更新Q值 
 		temp_1->Ti_Q = temp_1->Ti_Q + makespan + est;
		temp_2->Pi_Q = temp_2->Pi_Q + makespan + eft;
			
		printf("---------------------------%d\n", (j+1)/2); 
	 	printf("Ti=%d\tTi_N=%d\tTi_Q=%d\n", temp_1->Ti, temp_1->Ti_N, temp_1->Ti_Q);
	
	 	printf("Pi=%d\tPi_N=%d\tPi_Q=%d\n", temp_2->Pi, temp_2->Pi_N, temp_2->Pi_Q);	
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
	Node_1 *entry;
	entry = path[0];
	return entry->Ti_Q*1.0/entry->Ti_N;
}



int main()
{

	//避免随机数重复 
	srand((unsigned)time(NULL));
	
    fp1 = fopen("_1_comp_costs.txt", "r+");
    fp2 = fopen("_1_comm_costs.txt", "r+");
    //printf("1-%d\n", fp2);
    
    //初始化 任务-处理器结构体 
	schedule=(struct TaskProcessor*)calloc(V,sizeof(struct TaskProcessor));
    for(i=0; i<V; i++)
        schedule[i].PI=-1;
 
    // Initialize Computation Cost Table
    comp_costs = (int **)calloc(V, sizeof(int *));		//int* int型的指针变量。	
	/*在内存的动态存储区中分配v
	个长度为size的连续空间，函数返回一个指向分配起始地址的指针*/
	
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

   	//赋值data 矩阵（邻接矩阵） 
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
    
    //打印 
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
  	//赋值
	 for(i=0; i<P; i++)
        for(j=0; j<P; j++)
        {
        	if(i==j)
        		data_transfer_rate[i][j]=0;
       		else
       			data_transfer_rate[i][j]=1; 
		} 
		
   	//打印 data_transfer_rate
    printf("data_transfer_rate:\n");
    for(i=0; i<P; i++)
    {
    	for(j=0; j<P; j++)
    		printf("%d ", data_transfer_rate[i][j]);
   		printf("\n");
    }
    
   
   	/*蒙特卡罗树搜索 */ 
   	double best_makespan;
   	
  	best_makespan = UCT_Seach();
  	
  	printf("best_makespan=%.2lf\n", best_makespan);
  	
	return 0;
}
