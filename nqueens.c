#include <stdio.h>
#include <stdlib.h>
#include <time.h>

unsigned long long calc_atks (register unsigned long long *vector_p, unsigned long long d, register unsigned long long *vector_c_p);
int climb (register unsigned long long *vector_p, unsigned long long *conflicts_p, unsigned long long d, register unsigned long long *vector_c_p);

unsigned int 
main(int argc, char **argv)
{
    srand(time(NULL));
    register unsigned long long *god_vector;
    register unsigned long long *conflict_vec;
    unsigned long long dimension, conflicts;

    //init variables
    dimension       = atoi   (argv[1]);
    god_vector      = malloc (dimension*sizeof( unsigned long long ));
    conflict_vec    = malloc (dimension*sizeof( unsigned long long ));
    conflicts       = 0;

    //rand new start
    unsigned long long index, zero_index, rand_index;    
    for(index = 0; index < dimension; index++)
    {
        conflict_vec[index] = 0;
        rand_index = rand() % dimension;
        if(index == 0)
        {
            god_vector[rand_index]  = index;
            zero_index              = rand_index;
        }
        else
        {
            if(god_vector[rand_index] == 0 && rand_index != zero_index) god_vector[rand_index] = index;
            else                                                        --index;         
        }        
    }

    //Calculate initial conflicts
    conflicts = calc_atks(god_vector, dimension, conflict_vec);

    if (conflicts == 0)
    {
	printf("%d\n", dimension);
	int final[dimension][dimension];
	
	int i = 0;
        int j = 0;
	
	for(i = 0; i < dimension; i++)	for(j = 0; j < dimension; j++)	final[i][j]= 0;
			
	for(i = 0; i < dimension; i++) final[i][god_vector[i]] = 1;
	
	for(i = 0; i < dimension; i++)
	{
		for(j = 0; j < dimension; j++)
		{
			printf("%d ", final[i][j]);
		}
		printf("\n");
	}	

        return EXIT_SUCCESS;
    } 
    else
    {
        unsigned int    a = climb(god_vector, &conflicts, dimension, conflict_vec);
        while(a != 1)   a = climb(god_vector, &conflicts, dimension, conflict_vec);
        
	printf("%d\n", dimension);
	int final[dimension][dimension];
	
	int i = 0;
        int j = 0;
	
	for(i = 0; i < dimension; i++) for(j = 0; j < dimension; j++) final[i][j]= 0;
		
	for(i = 0; i < dimension; i++) final[i][god_vector[i]] = 1;
	
	for(i = 0; i < dimension; i++)
	{
		for(j = 0; j < dimension; j++)
		{
			printf("%d ", final[i][j]);
		}
		printf("\n");
	}	

        return EXIT_SUCCESS;
    }               
    return EXIT_SUCCESS;
}

unsigned long long 
calc_atks(register unsigned long long *vector_p, unsigned long long d, register unsigned long long *vector_c_p)
{
    register unsigned long long confli = 0;
    unsigned long long i, j;
    register unsigned long long queen_in_1, queen_in_2, queen_in_3, queen_in_4;
    
    i = 0;
    for (i = 0; i < d; i++) vector_c_p[i] = 0;
    
    i = 0;
    //Diagonal calcs
    for(i = 0; i < d; i ++)
    {
        queen_in_1 = 0;
        queen_in_2 = 0;
        queen_in_3 = 0;
        queen_in_4 = 0;
        for(j = 0; j < d - i; j++)
        {
            if (vector_p[j] == j + i)
            {
                if (queen_in_1 == 1)
                {
                    ++confli;
                    ++vector_c_p[j];
                } 
                queen_in_1 = 1;
            }
            if (vector_p[j] == d - j - i - 1)
            {
                if (queen_in_2 == 1)
                {
                    ++confli;
                    ++vector_c_p[j];
                } 
                queen_in_2 = 1;
            }
            if( i > 0 )
            {
                if (vector_p[j + i] == j)
                {
                    if (queen_in_3 == 1)
                    {
                        ++confli;
                        ++vector_c_p[j+i];
                    }       
                    queen_in_3 = 1;
                }
                if (vector_p[j + i] == d - j - 1)
                {
                    if (queen_in_4 == 1)
                    {
                        ++confli;
                        ++vector_c_p[j+i];
                    } 
                    queen_in_4 = 1;
                }
            }
        }
    }
    return confli;
}

int 
climb(register unsigned long long *vector_p, unsigned long long *conflicts_p, unsigned long long d, register unsigned long long *vector_c_p)
{
    
    //random changes
    register unsigned long long rand_line       = rand() % d;
    register unsigned long long rand_line2      = rand() % d;
    int a = 0;

    while(a == 0)
    {
        if ((rand_line != rand_line2) && (vector_c_p[rand_line] > 0 || vector_c_p[rand_line2] > 0)) a = 1;
        else
        {
            rand_line       = rand() % d;
            rand_line2      = rand() % d;
        }

    } 
    
    //change
    unsigned long long backup_1                 = vector_p[rand_line];
    vector_p[rand_line]                         = vector_p[rand_line2];
    vector_p[rand_line2]                        = backup_1;

    unsigned long long last_conflicts           = *conflicts_p;

    *conflicts_p = calc_atks(vector_p, d, vector_c_p);

    //show
   // printf("dimensao = %llu \n",d);
   // printf("conflitos = %llu \n", *conflicts_p);
    
    if (*conflicts_p >= last_conflicts)
    {
        backup_1                = vector_p[rand_line];
        vector_p[rand_line]     = vector_p[rand_line2];
        vector_p[rand_line2]    = backup_1;
        *conflicts_p            = last_conflicts;
    }

    if (*conflicts_p == 0)  return 1;    
    else                    return 0;        
    
}
