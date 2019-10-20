#include "csvRow.cpp"
#include <unordered_map>


using namespace std;


//struct patentInfo
//{
////    string m_uuid;
////    string m_patentID;
////    string m_assigneeID;
////    string m_rawLocation;
////    string m_type;
////    string firstName;
////    string lastName;
////    string m_firmName;
////    string m_sequence;
//};

unordered_map<string/*lastName*/, vector<unordered_map<string/*firstName*/, vector< vector<string>/*his/her patents*/> > > > table; //transfer csv into table
unordered_map<string, vector<unordered_map<string, vector< vector<string> > > > >::iterator tableIt;// iterator for the table

void fillTable(string firstName, string lastName, vector<string> patent )
{
    unordered_map<string, vector<vector<string> > >::iterator it;
    
    tableIt = table.find(lastName);// checks to see if the last name exists
    if (tableIt != table.end()) // if it exists, check if first name exists
    {
        for (int i=0; i<tableIt->second.size(); i++)//each last name may have multiple first names
        {
            it = tableIt->second[i].find(firstName); //check if a first name exists
            if (it != tableIt->second[i].end())// if the first name exists
            {
                (it->second).push_back(patent);//add the patent to the existing name
                return;
            }
        }
        //last name matches, but no person exists yet
        //create new profile
        vector<vector<string> > patents;
        patents.push_back(patent); //add current patent to his/her array of patents
        unordered_map<string, vector<vector<string> > > newPerson;
        newPerson[firstName] = patents; //link first name to his/her patents
        tableIt->second.push_back(newPerson);// add this person to the table;
        return;
    }
    // if no last name exists, must create a new last name profile
    vector<vector<string> > patents;
    patents.push_back(patent); //add current patent to his/her array of patents
    
    unordered_map<string, vector<vector<string> > > newPerson;
    newPerson[firstName] = patents; //link first name to his/her patents
    
    vector<unordered_map<string, vector<vector<string> > > > vectorOfFirstNames;
    vectorOfFirstNames.push_back(newPerson);
    table[lastName] = vectorOfFirstNames; //add new last name to the table
}


