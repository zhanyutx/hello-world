#include<stdlib.h>
#include<stdio.h>
#define InitSize 10
typedef struct{
    int*date;
    int MaxSize;
    int length;
}SqList;

void InitList(SqList &L){
    L.date = (int*)malloc(InitSize*sizeof(int));
    L.length = 0;
    L.MaxSize = InitSize;
}

void IncreaseSize(SqList &L, int len){
    int*p = L.date;
    L.date = (int*)malloc((InitSize+len)*sizeof(int));
    for(int i = 0; i<L.length; i++){
        L.date[i] = p[i];
    }
    L.MaxSize += len;
    free(p);
}
int main(){
    SqList L;
    InitList(L);
    printf("%d", L.MaxSize);
    IncreaseSize(L, 5);
    printf("%d", L.MaxSize);
    //free(L.date);
    return 0;
}
