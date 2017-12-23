# simple text-based interface over CIA World Factbook DB
import mysql.connector
import config

# main menu being displayed to user
def displayMenu():
    # while loop that keeps running while it is True
    while True:
        # display menu choices
        print ("1. List countries")
        print ("2. Add country")
        print ("3. Find countries based on gdp and inflation")
        print ("4. Update country\'s gdp and inflation")
        print ("5. Exit")
        choice = input("Enter your choice (1-5): ")
        if choice == 1:
            print ("You have selected choice 1...List countries")
            print("")
            listCountries()
        elif choice == 2:
            print ("You have selected choice 2...Add country")
            print("")
            addCountry()
        elif choice == 3:
            print ("You have selected choice 3...Find countries based on gdp and inflation")
            print("")
            findCountries()
        elif choice == 4:
            print ("You have selected choice 4...Update country\'s gdp and inflation")
            print("")
            updateCountries()
        elif choice == 5:
            print ("You have selected choice 5...Exit")
            print("")
            quit()    # halts the loop and exits script
        else:
            raw_input("Not a valid choice. Please enter any key and try again...")
            print("")
            
# displays the names and codes of all countries in DB       
def listCountries():
    try:
        # connection info
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        dab = 'cvillagomez_DB'
        # create a connection
        con = mysql.connector.connect(user=usr,password=pwd, host=hst, database=dab)

        # create a result set
        rs = con.cursor()
        query = 'SELECT country_name, code FROM country'
        rs.execute(query)
        # print results
        for (name, code) in rs:
            print ("{} ({})".format(name, code))
        print("")
        displayMenu()
        
        rs.close()
        con.close()

    except mysql.connector.Error as err:
        print (err)

# prompts the user for information to add a new country to DB
# by asking for country code, name, gdp, and inflation and
# performs exception handling if the country already exists in DB
# query used to retrieve country code that is equivalent to
# the country code entered by user
def addCountry():
    try: 
        # connection info
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        dab = 'cvillagomez_DB'

        # create a connection
        con = mysql.connector.connect(user=usr,password=pwd, host=hst,
                                      database=dab)
        # get a category from the user
        input_code = str(raw_input("Country code................: "))
        name = str(raw_input("Country name................: "))
        gdp = float(raw_input("Country per capita gdp (USD): "))
        inflation = float(raw_input("Country inflation (pct).....: "))

        rs = con.cursor()
        code_country = 'SELECT code, country_name FROM country'
        rs.execute(code_country)
        
        # sets flag for country code to false
        code_flag = False

        # assigns code and country name to rs
        for code, country_name in rs:
            if code == input_code:
                code_flag = True
                
        rs.close()

        if code_flag == True:
            print ("Country already exists in database")
        else:
            # inserts new country values into db
            try:
                rs2 = con.cursor()
                # insert the country into the db
                insert = 'INSERT INTO country VALUES(%s, %s, %s, %s)'
                rs2.execute(insert,(input_code, name, gdp, inflation))
                print ("Country added to database!")
                con.commit()
                rs2.close()
            except mysql.connector.Error as err:
                print (err)
                
            print("")
            con.close()
            displayMenu()
    except mysql.connector.Error as err:
            print (err)

# displays all countries with a gdp equal to or higher
# than the value given and an inflation equal to or lower
# than the inflation given and countries are displayed
# from highest-to-lowest gdp such that if two countries
# have the same gdp, they are displayed from
# lowest-to-highest inflation, and only the number of
# countries entered should be displayed
def findCountries():
    try: 
        # connection info
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        dab = 'cvillagomez_DB'

        # create a connection
        con = mysql.connector.connect(user=usr,password=pwd, host=hst,
                                      database=dab)
        # get a category from the user
        num_countries = int(raw_input("Number of countries to display: "))
        min_gdp = float(raw_input("Minimum per capita gdp (USD)..: "))
        max_inflation = float(raw_input("Maximum inflation (pct).......: "))

        # create and execute query
        rs = con.cursor()
        # query used to retrieve the country's name, code, gdp, and inflation values
        # using constraints given in comments of function header
        query = 'SELECT country_name, code, gdp, inflation FROM country WHERE country.gdp >= %s AND country.inflation <= %s ORDER BY gdp DESC, inflation LIMIT %s'
        rs.execute(query, (min_gdp, max_inflation, num_countries))

        # print the result
        for (country_name, code, gdp, inflation) in rs:
            print ("{} ({}), {}, {}".format(country_name, code, gdp, inflation))
        print ("")
        displayMenu()
        
        rs.close()
        con.close()

    except mysql.connector.Error as err:
        print (err)
        
# updates a previously existing country's information in DB
# by prompting user for the country code, new gdp, and new
# inflation, and performs exception handling if the country
# does not already exist in DB
def updateCountries():
    try: 
        # connection info
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        dab = 'cvillagomez_DB'

        # create a connection
        con = mysql.connector.connect(user=usr,password=pwd, host=hst,
                                      database=dab)

        # updating the db
        code = str(raw_input("Country code................: "))
        gdp = str(raw_input("Country per capita gdp (USD): "))
        inflation = str(raw_input("Country inflation (pct).....: "))

        rs = con.cursor()
        # query used to retrieve country code that is equivalent to
        # the country code entered by user
        country_codes = "SELECT code FROM country WHERE code='" + code+"';"
        
        rs.execute(country_codes, (code))

        text = ""
        # saves resulting equivalent DB country code from query into text
        for x in rs:
            text += str(x)
        # checks if there was no equivalent country code found
        # in DB based on the user's input country code
        if(text == ""):
            print ("Country does not exist in database")
            print ("")
            return
        else:
            # performs update on country's gdp and inflation if there is a match
            update = 'UPDATE country SET gdp = %s, inflation = %s  WHERE code = %s'
            rs.execute(update, (gdp, inflation, code))
            con.commit()
        # commit the changes
        con.commit()

        print ("")
        displayMenu()
        
        rs.close()
        con.close()

    except mysql.connector.Error as err:
        print (err)
    
def main():
    try:
        # connection info
        usr = config.mysql['user']
        pwd = config.mysql['password']
        hst = config.mysql['host']
        dab = 'cvillagomez_DB'

        # create a connection
        con = mysql.connector.connect(user=usr,password=pwd, host=hst,
                                      database=dab)
        displayMenu()
        con.commit()
        rs.close()
        con.close()
                
    except mysql.connector.Error as err:
        print (err)

if __name__ == '__main__':
    main()
