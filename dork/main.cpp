#include <iostream>

#include "ZUser.h"


int main() {
    char name[]="tomcat";
    ZUser u1(8,name);
    ZUser *p2=new ZUser(63,"zhangsan");
    if(u1.zUserId>p2->zUserId){
        return 1;
    }
    delete p2;
    return 0;
}
