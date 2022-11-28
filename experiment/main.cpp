#include <iostream>

#include "ZObject.h"

extern InstrmCpp::ZLinkedList::ZHeader * InstrmCpp::linkedList_new;
extern InstrmCpp::ZLinkedList::ZHeader * InstrmCpp::linkedList_delete;

int main() {
    char name[]="Product";
    InstrmCpp::ZObject * pObj1= InstrmCpp::newZObject((void *) 2);
    InstrmCpp::ZObject * pObj2= InstrmCpp::newZObject((void *) 2, name);
    std::cout << "clzName1:" << pObj1->classFullNameForShow() << std::endl;
    std::cout << "clzName2:" << pObj2->classFullNameForShow() << std::endl;
    InstrmCpp::deleteZObject(pObj1);
    InstrmCpp::deleteZObject(pObj2);
    std::cout << "linkedList_new->nodeCount:" << InstrmCpp::linkedList_new->nodeCount  << std::endl;
    std::cout << "linkedList_delete->nodeCount:" << InstrmCpp::linkedList_delete->nodeCount << std::endl;
    return 0;
}
