#include <iostream>

#include "User.h"
int main() {
    std::string * name=new std::string ("zhangsan");
    User * pUser=new User(2, name);
    std::cout << "user:" << pUser->getName() << std::endl;
    return 0;
}
