#include <iostream>

#include "Object.h"
int main() {
    char name[]="lisi";
    InstrmCpp::Object * pUser=new InstrmCpp::Object((void*)2, name);
    std::cout << "user:" << pUser->classFullName << std::endl;
    return 0;
}
