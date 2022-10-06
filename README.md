# encryptingPasswords
A Python applicationa that takes username and a password from the user where the password is encrypted and salted by the following algorithm
1- XOR each byte ( 8-bits ) with ( 8-bits ) from the public key. 
2- Swap the first and last char of the encrypted password.
3- Add a random string of N chars to the end of the result of step 2.

All of the usernames and passwords are stored in a DB using Sqlite3 
