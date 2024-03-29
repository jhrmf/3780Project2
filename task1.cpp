//============================================================================
// Name        : 3780Pr2.cpp
// Author      : jthkn9
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C++, Ansi-style
//============================================================================

#include <iostream>
#include <fstream>

using namespace std;

int displayMenu(){
	int choice = -1;
	cout << "MENU:\n";
	while(choice != 1 && choice != 2 && choice != 0 && choice != 3){
		cout << "0) Terminate\n"
					"1) Register an Account\n" <<
					"2) Log in\n" <<
					"3) Change Database" << endl;
		cin >> choice;
	}
	return choice;
}

int main() {
	string::size_type size = 5;
	int choice;
	string username, password;
	bool goodInput;
	string fileName = "DB1";
	ofstream outfile;
	outfile.open("DB1", ios::app);
	ifstream infile;
	infile.open("DB1");
	while((choice = displayMenu()) > 0){
		if(choice == 1){
			//register
			do {
				goodInput = true;

				cout << "Input a username that is no more than 8 Alphanumeric characters" << endl;
				cin >>username;
				if(username.length() > 8){
					goodInput = false;
				}
				string::size_type i = 0;
				while(i < username.length()){
					if(!isalnum(username[i])){
						goodInput = false;
					}
					i++;
				}

			}
			while(goodInput == false);
			do {
							goodInput = true;

							cout << "Input a password of no more than " << size << " lowercase letters in length" << endl;
							cin >>password;
							if(password.length() > size){
								goodInput = false;
							}
							string::size_type i = 0;
							while(i < password.length()){
								if(!islower(password[i])){
									goodInput = false;
								}
								i++;
							}

						}
						while(goodInput == false);
			//have good username and password
			outfile << username << ", " << password << "\n";
		}
		else if(choice == 2){
			//login
			bool login = false;
			string line, checkUName, checkPassword;
			cout << "Input your username: " << endl;
			cin >> username;
			cout << "Input your password " << endl;
			cin >> password;
			while(!infile){
				getline(infile, line, '\n');
				checkUName = line.substr(0, line.find(", "));
				checkPassword = line.substr(line.find(", ")+2,line.length());
				cout << "username = " << checkUName << " password = " << checkPassword << endl;
				if(!checkUName.compare(username) && !checkPassword.compare(password)){
					//check password
					cout << "Sucessfully logged in." << endl;
					login = true;
					break;
				}
			}
			if(!login){
				cout << "Could not log in." << endl;
			}
		}
		else if(choice == 3){
		    outfile.close();
		    infile.close();
		    do {
                cout << "Choose the DB to use:\n1) DB1\n2) DB2\n3) DB3\n";
		        cin >> choice;
		    }
		    while(choice != 1 && choice != 2 && choice != 3);
		    switch(choice){
		        case 1:
		            fileName = "DB1";
		            break;
		        case 2:
		            fileName = "DB2";
		            break;
		        case 3:
		            fileName = "DB3";
		            break;
		    }
		    infile.open(fileName);
		    outfile.open(fileName, ios::app);


		}
	}
	outfile.close();
	cout << "Terminating" << endl; // prints !!!Hello World!!!
	return 0;
}
