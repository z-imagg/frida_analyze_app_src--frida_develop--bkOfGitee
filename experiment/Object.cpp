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

void InstrmCpp::NodeLinked::beforeInsert(InstrmCpp::Object *object) {
    //0. assume: this==header;
    NodeLinked *header = this;
    
    NodeLinked *old_first_node = header->next;
    
    //1. create current node
    NodeLinked *current_node =  (InstrmCpp::NodeLinked*) malloc(sizeof(InstrmCpp::NodeLinked));
    current_node->value=object;
    
    //2. link old_first_node to current_node
    current_node->next=old_first_node;
    
    //3. link current_node to header
    header->next=current_node;

}

InstrmCpp::NodeLinked * InstrmCpp::linkedList_new=(InstrmCpp::NodeLinked*) malloc(sizeof(InstrmCpp::NodeLinked));
InstrmCpp::NodeLinked * InstrmCpp::linkedList_delete=(InstrmCpp::NodeLinked*) malloc(sizeof(InstrmCpp::NodeLinked));