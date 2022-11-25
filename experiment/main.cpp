#include <iostream>

#include "Object.h"
int main() {
    char name[]="Product";
    InstrmCpp::Object * pObj=InstrmCpp::newObject((void*)2, name);
    std::cout << "clzName:" << pObj->classFullName << std::endl;
    return 0;
}
