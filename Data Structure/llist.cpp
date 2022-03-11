#define ElemType int

typedef struct LNode{
	ElemType date;
	struct LNode *next
}LNode, *LinkList;

//初始化定义带头结点
bool InitList(LinkList &L){
	L = (LinkList)malloc(sizeof(LNode))
	if (L == NULL)
		return false;
	L->next = NULL;
	return true;
}

//按位序插入
bool ListInsert(LinkList &L, int i, ElemType e){
	if(i < 1)
		return false;
	//确保位序合法(>=1) 因为单链表没有ListLength所以此处不能判断需要插入位置是否大于已有数据长度
	//  if(i == 1){
	//  	Node *s = (LNode *)malloc(sizeof(LNode));
	//  	//定义一个节点s并申请内存
	//  	s->date = e;
	//  	s->next = L->next;
	//  	L->next = s;
	//  	return true;
	//  }
	//不带头结点单独讨论第一项，因为此时不用指示指针p
	LNode *p = L;
	//定义P指针，从头节点开始逐个后移
	int j = 0;
	//int j = 1;    //不带头节点从1开始
	//头结点位序为0
	while(j < i-1 && p != NULL)
	{
		p = p->next;
		j++;
	}
	//要在第i个位置插入，即需要找到i-1节点使i-1节点的next指向稍后定义的节点
	//同时确保i值小于等于已有数据个数，若超过（即p指向NULL）则也要跳出
	//此时若i=已有数据数量+1即为尾插法
	InsertNextNode(p, e);
	//  if(p == NULL)
	//  {
	//  	return false;
	//  }
	//  //i>已有数量+2，不合法 意思是跳出while是由于p!=NULL这个条件
	//  LNode *s = (LNode *)malloc(sizeof(LNode));
	//  //定义一个节点s并申请内存
	//  s->date = e;
	//  s->next = p->next;
	//  p->next = s;
	//  return true;
}

//指定节点后插入
bool InsertNextNode(LNode *p, ElemType e){
	if (p == NULL)
		return false;
	LNode *s = (LNode *)malloc(sizeof(LNode));
	if (s == NULL)
		return false;	//内存分配失败，内存满
	s->next = p->next;
	s->date = e;
	p->next = s;
	return true;
}

//指定节点前插入
bool InsertPriorNode(LNode *p, ElemType e){
	if (p == NULL)
		return false;
	LNode *s = (LNode *)malloc(sizeof(LNode));
	if (s == NULL)
		return false;	//内存分配失败，内存满
	s->next = p->next;
	s->date = p->date;
	p->date = e;
	p->next = s;
}

//按位序删除 
bool ListDeleteNode(LinkList &L, int i; ElemType &e){
	if (i<1)
		return false;
	LNode *p = L;
	int j = 0;
	while(p != NULL && j < i-1){
		p = p->next;
		j++;
	}
	if (p == NULL || p->next == NULL)
		return false;
	LNode *q = p->next;
	e = q->data;
	p->next = q->next;
	free(q);
	return true;
	
}


int main(){
	LinkList L;
	InitList(L);
}