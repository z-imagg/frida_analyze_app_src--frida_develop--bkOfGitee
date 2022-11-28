//
// Created by z on 2022/11/22.
//

#ifndef EXPERIMENT_USER_H
#define EXPERIMENT_USER_H




#include <string>
#include <string.h>
namespace InstrmCpp{

class Object {
public:
    void* address;
    char* classFullName;

public:
    Object(void* _address,  char * _classFullName);
    ~Object();
    const char* classFullNameForShow();

};


Object* newObject();
void deleteObject(Object* pointer);


Object* newObject(void* _address);
Object* newObject(void* _address,  char * _classFullName);

namespace LinkedList{
    class Node{
    public:
        Node* next;
        Object* value;

    };
    class Header{
    public:
        Node* firstNode;
        int  nodeCount;
    public:
        void beforeInsert(Object* node);
    };

    Header* initHeader(Header* header);
}

extern LinkedList::Header *linkedList_new;
extern LinkedList::Header *linkedList_delete;
}//end of namespace InstrmCpp


#endif //EXPERIMENT_USER_H
