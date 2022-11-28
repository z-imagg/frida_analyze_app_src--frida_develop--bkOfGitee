//
// Created by z on 2022/11/22.
//

#include "Object.h"

#if _GLIBCXX_HOSTED
using std::malloc;
#else
extern "C" void *malloc (std::size_t);
#endif

extern "C" void free(void*);

InstrmCpp::Object::Object(void* _address,  char * _classFullName) : address(_address), classFullName(_classFullName) {

}

const char* InstrmCpp::Object::classFullNameForShow() {
    return this->classFullName==NULL?"":this->classFullName;
}
InstrmCpp::Object * InstrmCpp::newObject(){

	std::size_t sz=sizeof(Object);
  	Object* pointer = (Object*)malloc (sz);
  	if(pointer==0){
  		//throw 
  	}
  	return pointer;

}


void InstrmCpp::deleteObject(InstrmCpp::Object* pointer){
	free(pointer);
    InstrmCpp::linkedList_delete->beforeInsert(pointer);
}

InstrmCpp::Object * InstrmCpp::newObject(void* _address){
    Object* pointer = InstrmCpp::newObject();
    pointer->address=_address;
    pointer->classFullName=NULL;
    InstrmCpp::linkedList_new->beforeInsert(pointer);
    return pointer;
}

InstrmCpp::Object * InstrmCpp::newObject(void* _address,  char * _classFullName){
	Object* pointer = InstrmCpp::newObject();
	pointer->address=_address;
	pointer->classFullName=_classFullName;
    InstrmCpp::linkedList_new->beforeInsert(pointer);
	return pointer;
}

void InstrmCpp::LinkedList::Header::beforeInsert(InstrmCpp::Object *object) {
    //0. assume: this==header;
    InstrmCpp::LinkedList::Header *header = this;

    InstrmCpp::LinkedList::Node *old_first_node = header->firstNode;
    
    //1. create current node
    InstrmCpp::LinkedList::Node *current_node =  (InstrmCpp::LinkedList::Node*) malloc(sizeof(InstrmCpp::LinkedList::Node));
    current_node->value=object;
    
    //2. link old_first_node to current_node
    current_node->next=old_first_node;
    
    //3. link current_node to header
    header->firstNode=current_node;

    //4. count node
    header->nodeCount+=1;

}


InstrmCpp::LinkedList::Header* InstrmCpp::LinkedList::initHeader(InstrmCpp::LinkedList::Header* header){
    header->firstNode=NULL;
    header->nodeCount=0;
    return header;
}
InstrmCpp::LinkedList::Header * InstrmCpp::linkedList_new=InstrmCpp::LinkedList::initHeader(
        (InstrmCpp::LinkedList::Header*) malloc(sizeof(InstrmCpp::LinkedList::Header))  );
InstrmCpp::LinkedList::Header * InstrmCpp::linkedList_delete=InstrmCpp::LinkedList::initHeader(
        (InstrmCpp::LinkedList::Header*) malloc(sizeof(InstrmCpp::LinkedList::Header)) );
