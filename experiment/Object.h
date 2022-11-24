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

};
}


#endif //EXPERIMENT_USER_H
