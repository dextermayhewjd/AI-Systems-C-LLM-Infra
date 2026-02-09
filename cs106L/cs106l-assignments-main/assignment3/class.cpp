#include "class.h"
#include <string>
#include <iostream>

Person::Person()
{
    _first_name = "Dexter";
    _last_name = "Mayhew";
    _birth_day = 1;
    _birth_month = 1;
    _birth_year = 2026;
}

Person::Person(std::string fn, 
            std::string ln,
            int bd,
            int bm,
            int by):_birth_day{bd},
            _birth_month{bm},
            _birth_year{by},
            _first_name{fn},
            _last_name{ln}
            {};

int Person::get_birth_day(){
    return (*this)._birth_day;
}

void Person::set_birth_day(int day){
    this->_birth_day = day;
}

void Person::set_super_power(std::string power){
    this->super_power = power;
}
void Person::do_sth(){
    if(this->super_power.has_value())
    {
        std::cout<<"using super power"<<this->super_power.value()<<std::endl;
    }
}