//
// Created by z on 2022/11/22.
//

#ifndef EXPERIMENT_USER_H
#define EXPERIMENT_USER_H




namespace InstrmCpp{

class ZObject {
public:
    void* address;
    char* classFullName;

public:
    ZObject(void* _address,  char * _classFullName);
    ~ZObject();
    const char* classFullNameForShow();

};


ZObject* newZObject();
void deleteZObject(ZObject* pointer);


ZObject* newZObject(void* _address);
ZObject* newZObject(void* _address, char * _classFullName);

namespace ZLinkedList{
    class ZNode{
    public:
        ZNode* next;
        ZObject* value;

    };
    class ZHeader{
    public:
        ZNode* firstNode;
        int  nodeCount;
    public:
        void beforeInsert(ZObject* node);
    };

    ZHeader* initZHeader(ZHeader* header);
}

extern ZLinkedList::ZHeader *linkedList_new;
extern ZLinkedList::ZHeader *linkedList_delete;
}//end of namespace InstrmCpp


#endif //EXPERIMENT_USER_H
