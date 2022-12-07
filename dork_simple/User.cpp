class User{
protected:
    long id;
public:
    User(long _id);
};

User::User(long _id) {
    this->id=_id;
}

int main(){
    User* p=new User(10L);
    return 0;
}