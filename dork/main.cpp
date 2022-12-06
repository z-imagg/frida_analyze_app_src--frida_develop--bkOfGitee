#include <iostream>

#include "ZUser.h"

long calcId(int age){
    if(age>100){
        return 2048*age;
    }
    return age+64;
}
int main() {
    char name[]="tomcat";
    ZUser u1(8,name);
    ZUser *p2=new ZUser(calcId(32),"zhangsan");
    if(u1.zUserId>p2->zUserId){
        return 1;
    }
    delete p2;
    return 0;
}
