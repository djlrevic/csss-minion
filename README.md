# csss-minion

The csss-minion bot is programmed by Henry using the language Python and discord.py. The bot accepts user input from Discord chat channels and runs a script to execute the command. Commands available include WolframAlpha math functions, grouping users by courses and admin commands. When an invalid input is detected, the bot sends feedback to the user indicating the command does not exist. Valid inputs are processed by the bot and the specific command is executed. The bot then displays the command output to the user.


# Commands: #

There are currently 7 commands available, and more commands will be added in future updates.  

## .help ##
The help command will display the infomation menu in the chat. This menu contains brief descriptions of all possible commands, and provides a link to the source code. 

## .newclass \<class\> ##
This command will create a new class role, and give you that role. The name of the role will either be the first word typed after the .newclass command, or will be the entire string between the first quotation marks. An example is shown below. It is also worth noting that all roles created using this command will be converted to lowercase for security reasons. 

.newclass one two three = a new role with the name "one."
.newclass "one two three" = a new role with the name "one two three."

## .iam \<class\> ##
You can use this command to give yourself any roles that already exist, and consists of entirely lowercase letters or numbers. The \<class\> format follows the same rules as the .newclass command shown above. If the role you attempted to join does not exist, it will be created and you will be given it. 

## .voteresult ##
Voteresult is used to display the winners of the CSSS annual election. It contains information about the following elected positions: President, Vice President, Treasurer, Director of Resources, Director of Events, Director of Communications, and Director of Archives.

## .help mc ##
This can only be used within the #minecraft channel. When the command is used in correct channel, it will display commands specific to minecraft. Outide of the correct channel, it will display a message alerting the user to move to that channel. 
