//
// Created by z on 2022/11/22.
//

#include "ZUser.h"
#include <stdlib.h>
ZUser::ZUser(long _zUserId, char *_zUserName) {
    this->zUserId=_zUserId;
    this->zUserName=_zUserName;
}
ZUser::~ZUser() {
    this->zUserId=0;
    this->zUserName=NULL;
}