//
// Created by z on 2022/11/22.
//

#ifndef EXPERIMENT_USER_H
#define EXPERIMENT_USER_H


#include <string>
class User {
protected:
    long id;
    std::string* name;

public:
    User(long _id,  std::string *_name);
    ~User();
    std::string getName(){return * (this->name);}

};


#endif //EXPERIMENT_USER_H
