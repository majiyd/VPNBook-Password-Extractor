#python 2
import requests, BeautifulSoup as bs, sqlite3 as sql, pyperclip as pcp

def getPasswordFromVpnBook():
    try:
        print 'Connecting to http://vpnbook.com....'
        dataDump = requests.get('http://vpnbook.com/freevpn')
        htmlDump = bs.BeautifulSoup(dataDump.text)
        Strong = htmlDump.findAll('strong')
        password =  str(Strong[8].getText())
        print 'Succesfully gotten password from http://vpnbook.com'
        return password

    except requests.exceptions.ConnectionError:
        print 'Failed to connect to vpnbook'
        raw_input('Press any key too retry or just quit the console to end')
        getPasswordFromVpnBook()

def connectToDB():
    #connect to sqlite engine
    # print 'Starting Sqlite Engine....'
    # print "Connecting to db...."
    try:
        global conn
        conn = sql.connect('password.db')
        # print "Successfully connected to db...."
    except sql.Error, e:
        print e.args[1]
        print 'Fatal Error: Failed to connect to database'

    #Create Cursor Object
    global cursor
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS password_table (password varchar(30) )")





def getCurrentPassword():
    print 'Attempting to Get Stored Password.......'
    query = 'SELECT password FROM password_table'
    try:
        cursor.execute(query)
        currentPassword =  cursor.fetchone()[0]
        print 'Current Password has been obtained and copied to clipboard'
        return str(currentPassword)
    except :
        print 'Failed to retrieve current password from db'
        print('Please retrieve accurate password from vpnbook.com')
        return ' '





def insertNewPassword(newPass):
    # print 'Now attempting to update database with data from  vpnbbok'
    query = "UPDATE password_table SET password =  ('%s')"%newPass
    try:
        cursor.execute(query)
        print 'Database has been updated with new password'
        conn.commit()
    except sql.Error, e:
        print e
        print 'Failed to insert new password'

def comparePasswords(old,new):
    if(old == new):
        print ('Current password is %s' % old)
        pcp.copy(old)
        print 'password unchanged\n Current password has been copied to your clipboard'

    elif(old != new):
        print ('Vpn book has updated the password\nThe new password is %s'%new)
        print('The new password has been copied to your clipboard ')
        pcp.copy(new)
        insertNewPassword(new)




def main():
    connectToDB()
    oldPassword = getCurrentPassword()
    newPassword = getPasswordFromVpnBook()
    comparePasswords(oldPassword, newPassword)
    raw_input('press any key to quit...')


main()
