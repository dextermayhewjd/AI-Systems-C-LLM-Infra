#include <optional>
#include <string>
class Person
{
    public:
        std::string _first_name;
        std::string _last_name;

        Person();
        Person(std::string fn, 
            std::string ln,
            int bd,
            int bm,
            int by);

        int get_birth_day();
        void set_birth_day(int day);
        
        void do_sth();
        
    private:
        int _birth_day;
        int _birth_month;
        int _birth_year;
        
        std::optional<std::string> super_power;

        void set_super_power(std::string);
};