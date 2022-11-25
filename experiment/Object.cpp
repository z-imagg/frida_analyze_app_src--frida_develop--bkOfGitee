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

InstrmCpp::Object * InstrmCpp::newObject(){

	std::size_t sz=sizeof(Object);
  	Object* pointer = (Object*)malloc (sz);
  	if(pointer==0){
  		//throw 
  	}
  	return pointer;

}


void deleteObject(InstrmCpp::Object* pointer){
	free(pointer);
}


InstrmCpp::Object * InstrmCpp::newObject(void* _address,  char * _classFullName){
	Object* pointer = InstrmCpp::newObject();
	pointer->address=_address;
	pointer->classFullName=_classFullName;
	return pointer;
}