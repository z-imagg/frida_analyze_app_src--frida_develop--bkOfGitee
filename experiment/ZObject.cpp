//
// Created by z on 2022/11/22.
//

#include "ZObject.h"

#include <stdlib.h>
#if _GLIBCXX_HOSTED
using std::malloc;
#else
extern "C" void *malloc (std::size_t);
#endif

extern "C" void free(void*);

InstrmCpp::ZObject::ZObject(void* _address,  char * _classFullName) : address(_address), classFullName(_classFullName) {

}

const char* InstrmCpp::ZObject::classFullNameForShow() {
    return this->classFullName==NULL?"":this->classFullName;
}
InstrmCpp::ZObject * InstrmCpp::newZObject(){

	std::size_t sz=sizeof(ZObject);
  	ZObject* pointer = (ZObject*)malloc (sz);
  	if(pointer==0){
  		//throw 
  	}
  	return pointer;

}


void InstrmCpp::deleteZObject(InstrmCpp::ZObject* pointer){
	free(pointer);
    InstrmCpp::linkedList_delete->beforeInsert(pointer);
}

InstrmCpp::ZObject * InstrmCpp::newZObject(void* _address){
    ZObject* pointer = InstrmCpp::newZObject();
    pointer->address=_address;
    pointer->classFullName=NULL;
    InstrmCpp::linkedList_new->beforeInsert(pointer);
    return pointer;
}

InstrmCpp::ZObject * InstrmCpp::newZObject(void* _address, char * _classFullName){
	ZObject* pointer = InstrmCpp::newZObject();
	pointer->address=_address;
	pointer->classFullName=_classFullName;
    InstrmCpp::linkedList_new->beforeInsert(pointer);
	return pointer;
}

void InstrmCpp::ZLinkedList::ZHeader::beforeInsert(InstrmCpp::ZObject *object) {
    //0. assume: this==header;
    InstrmCpp::ZLinkedList::ZHeader *header = this;

    InstrmCpp::ZLinkedList::ZNode *old_first_node = header->firstNode;
    
    //1. create current node
    InstrmCpp::ZLinkedList::ZNode *current_node =  (InstrmCpp::ZLinkedList::ZNode*) malloc(sizeof(InstrmCpp::ZLinkedList::ZNode));
    current_node->value=object;
    
    //2. link old_first_node to current_node
    current_node->next=old_first_node;
    
    //3. link current_node to header
    header->firstNode=current_node;

    //4. count node
    header->nodeCount+=1;

}


InstrmCpp::ZLinkedList::ZHeader* InstrmCpp::ZLinkedList::initZHeader(InstrmCpp::ZLinkedList::ZHeader* header){
    header->firstNode=NULL;
    header->nodeCount=0;
    return header;
}
InstrmCpp::ZLinkedList::ZHeader * InstrmCpp::linkedList_new= InstrmCpp::ZLinkedList::initZHeader(
        (InstrmCpp::ZLinkedList::ZHeader *) malloc(sizeof(InstrmCpp::ZLinkedList::ZHeader)));
InstrmCpp::ZLinkedList::ZHeader * InstrmCpp::linkedList_delete= InstrmCpp::ZLinkedList::initZHeader(
        (InstrmCpp::ZLinkedList::ZHeader *) malloc(sizeof(InstrmCpp::ZLinkedList::ZHeader)));
