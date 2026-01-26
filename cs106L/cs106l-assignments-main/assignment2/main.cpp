#include <fstream>
#include <iostream>
#include <queue>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_set>

std::string kYourName = "Dexter Ding"; // Don't forget to change this!

/**
 * Takes in a file name and returns a set containing all of the applicant names as a set.
 *
 * @param filename  The name of the file to read.
 *                  Each line of the file will be a single applicant's name.
 * @returns         A set of all applicant names read from the file.
 *
 * @remark Feel free to change the return type of this function (and the function
 * below it) to use a `std::unordered_set` instead. If you do so, make sure
 * to also change the corresponding functions in `utils.h`.
 */
std::set<std::string> get_applicants(std::string filename) {
  // STUDENT TODO: Implement this function.
  std::set<std::string> applicants;
  
  std::ifstream ifs(filename);
   if(!ifs)
   {
      throw std::runtime_error("open failed");
   }
   
   std::string line;
   while(std::getline(ifs,line))
   {
      applicants.insert(line);
   }

   return applicants;
}



/**
 * Takes in a set of student names by reference and returns a queue of names
 * that match the given student name.
 *
 * @param name      The returned queue of names should have the same initials as this name.
 * @param students  The set of student names.
 * @return          A queue containing pointers to each matching name.
 */
std::queue<const std::string*> find_matches(std::string name, std::set<std::string>& students) {
  // STUDENT TODO: Implement this function.
  std::queue<const std::string*> matching_name_pointers;
  
  auto name_first_space = name.find(' ');
  auto name_first_name_initial = *(name.begin());
  auto name_last_name_initial = *(name.begin()+name_first_space+1);

  for(const auto& student:students)
  {
      auto first_space = student.find(' ');
      auto first_name_initial = *(student.begin());
      auto last_name_initial = *(student.begin()+first_space+1);
      if(first_name_initial == name_first_name_initial && last_name_initial==name_last_name_initial)
      {
          matching_name_pointers.push(&student);
      }
  }
  return matching_name_pointers;
}





/**
 * Takes in a queue of pointers to possible matches and determines the one true match!
 *
 * You can implement this function however you'd like, but try to do something a bit
 * more complicated than a simple `pop()`.
 *
 * @param matches The queue of possible matches.
 * @return        Your magical one true love.
 *                Will return "NO MATCHES FOUND." if `matches` is empty.
 */
std::string get_match(std::queue<const std::string*>& matches) 
{
  // STUDENT TODO: Implement this function.
  if (matches.empty()) 
  {
    return "NO MATCHES FOUND.";
  }

  const std::string* best = matches.front();
  matches.pop();

  while (!matches.empty()) 
  {
    const std::string* current = matches.front();
    matches.pop();

    if (*current < *best) 
    {   // 字典序比较
      best = current;
    }
  }
  return *best;
}

/* #### Please don't remove this line! #### */
#include "autograder/utils.hpp"
