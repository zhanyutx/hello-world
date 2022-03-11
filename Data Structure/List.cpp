#include<stdlib.h>
#include<stdio.h>
#define InitSize 10
typedef struct{
    int date[InitSize];
    int length;
}SqList;



bool ListDelete(SqList &L, int i, int &e){
	if(i > InitSize || i < 1)
		return false;
	if(L.length == 0 || L.length > InitSize)
		return false;
	e = L.date[i-1];
	for(i; i < L.length; i++){
		L.date[i-1] = L.date[i];
	}
	L.length--;

	return true;
}


void InitList(SqList &L){
    for(int i = 0; i<InitSize; i++){
		L.date[i] = 0;
	}
	//# L.date = (int *)malloc(InitSize*sizeof(int));
    L.length = 0;
    //# L.MaxSize = InitSize;
}

bool ListInsert(SqList &L, int i, int e){
	if(i > InitSize || i < 1)
		return false;
	if(L.length == InitSize)
		return false;
	for(int j = L.length; j > i-1; j--){
		L.date[j] = L.date[j-1];
	}
	L.date[i-1] = e;
	L.length++;
	return true;
}

//# void IncreaseSize(SqList &L, int len){
//#     int *p = L.date;
//#     L.date = (int *)malloc((InitSize+len)*sizeof(int));
//#     for(int i = 0; i<L.length; i++){
//#         L.date[i] = p[i];
//#     }
//#     L.MaxSize += len;
//#     free(p);
//# }
int main(){
    SqList L;
    InitList(L);
    //# printf("%d", L.MaxSize);
    //# IncreaseSize(L, 5);
    //# printf("%d", L.MaxSize);
    L.date[0] = 12;
	L.date[1] = 26;
	L.date[2] = 27;
	L.date[3] = 28;
	L.date[4] = 29;
	L.length = 5;
	ListInsert(L, 3, 15);
	int e = 0;
	if(ListDelete(L, 3, e))
		printf("%d\n", e);
	else
		printf("error");
    //#free(L.date);
    return 0;
}
