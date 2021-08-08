import sqlite3
import random
from hashlib import sha256
from array import *

db = sqlite3.connect('main.sqlite')
cursor = db.cursor()
cursor.execute('''
	CREATE TABLE IF NOT EXISTS main(
	name TEXT,
	password TEXT,
	day TEXT,
	money TEXT,
	UNIQUE(name)
	)
  	''')

menu = {
	'Coffee' :
	{
		'Cost' : 2,
		'cashierID' : 723
	},
	'Burrito Wrap' :
	{
		'Cost' : 3,
		'cashierID' : 953
	},
	'Soft Drink' :
	{
		'Cost' : 1,
		'cashierID' : 782
	},
	'Ice Cream' :
	{
		'Cost' : 1,
		'cashierID' : 215
	},
	'Snow Cone' :
	{
		'Cost' : 1.50,
		'cashierID' : 158
	},
	'String Cheese' :
	{
		'Cost': 2.50,
		'cashierID' : 900
	},
	'Apples' :
	{
		'Cost' : 1,
		'cashierID' : 313
	}
}
arr = ['Coffee', 'Burrito Wrap', 'Soft Drink', 'Ice Cream', 'Snow Cone', 'String Cheese', 'Apples']

def createUser(name, password):
	sql = 'INSERT INTO main(name, password, day, money) VALUES(?, ?, ?, ?)'
	password = hashPassword(password)
	money = 0
	day = 0
	try: 
		cursor.execute(sql, (name, password, day, money))
		db.commit()
	except sqlite3.Error as error:
		print("Failed to create user: ", error)

def deleteUser(user):
	sql = 'DELETE FROM main WHERE name = ?'
	try:
		cursor.execute(sql, (user,))
		db.commit()
	except sqlite3.Error as error:
		print("Failed to delete user: ", error)

def updateUser(username, addmoney):
	sql = 'UPDATE main SET money = money + ? WHERE name = ?'
	cursor.execute(sql,(addmoney, username))
	db.commit()

def updateUserDay(username):
	sql = 'UPDATE main SET day = day + 1 WHERE name = ?'
	cursor.execute(sql,(username, ))
	db.commit()

def hashPassword(password):
	h = sha256()
	h.update(b'password')
	return h.hexdigest()

def signIn(username, password):
	password = hashPassword(password)
	sqlSgnIn = 'SELECT * FROM main WHERE name = ?'
	sqlPassword = 'SELECT * FROM main WHERE password = ?'
	cursor.execute(sqlSgnIn, (username,))
	counter = 0
	if cursor.fetchone():
		print("username validated")
		counter = 1
	cursor.execute(sqlPassword, (password,))
	if cursor.fetchone():
		print("password validated")
		counter = 2
	if counter == 2:
		print("Login Successful")
		return True
	elif counter != 2:
		print("Username or password is wrong. Please try again")
		return False
def playGame(username):
	receipt = []
	receiptId = []
	tax = 0
	amtOfItems = random.randint(1,4)
	aotc = amtOfItems
	print("This customer wants a:")
	while aotc != 0:
		x = random.randint(0, (len(arr)-1))
		print(arr[x],menu[arr[x]]['cashierID'])
		receipt.append(menu[arr[x]]['Cost'])
		receiptId.append(menu[arr[x]]['cashierID'])
		aotc -= 1
	while amtOfItems != 0:
		idipt = input("Please enter the item ids that the customer wants: ")
		if int(idipt) in receiptId:
			receiptId.remove(int(idipt))
			print("Item entered")
			amtOfItems -= 1
		else:
			print("This customer did not order this. This will not be added to their receipt and you will be taxed $1 of the total.")
			tax += 1
	print(f"Customer pays {sum(receipt)} dollars")
	userMoney = (sum(receipt)) - tax
	updateUser(username,userMoney)

def playDay(username):
	amtOfCustomers = random.randint(1, 8)
	while amtOfCustomers != 0:
		playGame(username)
		amtOfCustomers -= 1
	anotherDay = input("Do you want to play another day(yes or no): ")
	if anotherDay == "yes":
		playDay(username)

print("Welcome to Cashier Simulator")
ipt = input("If you want to sign up in order to save your progress, please type in yes. If you want to sign in, please type in no: ")
if ipt == "yes":
	newUsername = input("Enter in a username: ")
	newPassword = input("Please enter in your password: ")
	createUser(newUsername, newPassword)
	if signIn(newUsername, newPassword) == True:
		playDay(newUsername)
elif ipt == "no":	
	uname = input("username: ")
	passw = input("password: ")
	if signIn(uname, passw) == True:
		playDay(uname)
#createUser("Gamerbot", "thisgameisamazing")
#deleteUser("Gamerbot")