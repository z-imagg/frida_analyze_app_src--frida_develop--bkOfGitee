#include <iostream>

#include "Object.h"
int main() {
    char name[]="Product";
    InstrmCpp::Object * pObj1=InstrmCpp::newObject((void*)2);
    InstrmCpp::Object * pObj2=InstrmCpp::newObject((void*)2, name);
    std::cout << "clzName1:" << pObj1->classFullNameForShow() << std::endl;
    std::cout << "clzName2:" << pObj2->classFullNameForShow() << std::endl;
    InstrmCpp::deleteObject(pObj1);
    InstrmCpp::deleteObject(pObj2);
    return 0;
}
