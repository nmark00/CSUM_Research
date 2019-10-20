#include "assigneeTable.cpp"
//#include "csvRow.cpp"

int main()
{
    std::ifstream file("/Users/nicholasmark/Desktop/IPO_Patent_Data/raw_assignee_mini.csv");
    
    CSVRow row;
    while(file >> row)
    {
        vector<string> patent(7); //each row contains a different patent, regardless of inventor
        for (int i=0; i< 7; i++)
        {
            if (i > 4)
            {
                patent[i] = row[i+2]; //do not include the names of the inventor
                continue;
            }
            patent[i] = row[i]; //stores each cell into the array
        }
        fillTable(row[5], row[6], patent);
    }
}

