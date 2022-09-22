import mysql.connector
import requests, json
import pandas as pd
import numpy as np


# Indicies that need parsing: 3 subjects, 4 notes, 7
def parse_data_values(record):
  pass


def parse_subjects(record):
  full_str = ""
  for i, dic in enumerate(record):
    full_str += dic['value']

    if i != len(record) - 1:
      full_str += ", "

  return full_str


def parse_notes(record):
  
  full_str = ""
  for i, dic in enumerate(record):
    
    
    # Skip bibliographical data
    if "label" in dic:
      if dic['label'] == "Bibliography":
        continue

      # Join strings in a list if they exist
      list_str = ""

      list_str = ", ".join(dic['values'])

      full_str += dic['label'] + ": " + list_str + "\n"

      if i != len(record) - 1:
        full_str += ", "
    
  
  return full_str


# What should we do in terms of handling multiple editions/holdings (include ebook data?)
def parse_holdings(record):
  call_number = None
  for i, dic in enumerate(record):


    # Get call number for print copies only
    if dic['holdingType'] == "book":

      # Check if there is a call number key in teh dictionary
      if "callNumber" in dic:

        # Save call number and exit loop
        call_number = dic['callNumber']
        break
  
  # If no call number is found, save None as placeholder
  if call_number is None:
    call_number = "None"

  return call_number

def parse_publishers(record):
  publisher_str = ""

  for j, publisher_dict in enumerate(record):
    curr_pub = ""
    for i, key in enumerate(publisher_dict.keys()):
      curr_pub += publisher_dict[key]
      
      if i != len(publisher_dict) - 1:
        curr_pub += ", "
    
    publisher_str += curr_pub

    if j != len(record) - 1:
      publisher_str += ","

  return publisher_str

def split_cut(curr_num):

   bf_split = curr_num.split(' ')[1]

   check_split = bf_split.split('.')
   new_call = ""

   # If len <= 1, ignore this entry
   if len(check_split) > 1:
      # Rewrite this entry to separate cutter number from this entry
      if check_split[1][0].isalpha():
         print("Found entry to change")
         print(curr_num)

         
         for j, split in enumerate(curr_num.split(' ')):
               if j == 0:
                  new_call += split + ' '
               elif j != 1:
                  new_call += ' ' + split
               else:
                  new_call += check_split[0] + ' .' + check_split[1]
      else:
         return curr_num
   else:
      return curr_num

   return new_call

      



if __name__ == "__main__":

   # Connect to MYSQL Database
   mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="Gksdnihon101!",
      database='library_books'
   )

   # Create Cursor
   mycursor = mydb.cursor()


   # Load and read ids from csv
   df = pd.read_csv('Data/gregr_report.csv')


   # Extract IDS
   vals = set(df.to_numpy()[:, 0])
   cat_val = []

   for val in vals:
      cat_val.append(val)

   category_ids = np.array(cat_val)


   # Set up url for requests
   fields_to_save = ["titleId", "fullTitle", "subjects", "publicationDate", "notes", "thumbnail", "holdings"]
   url_base = "https://search.lib.byu.edu/green/byu/record/cat."
   num_added = 0

   # Loop through each id and make request
   for num, id in enumerate(category_ids):
      print("Entry number {} / {}".format(num+1, len(category_ids)))
      url = requests.get(url_base + str(id))
      text = url.text
      data = json.loads(text)

      data_vals = [None for i in range(7)]

      # Iterate over every field in json string from website
      for field in data:

         # Check for selected fields that I have decided to save
         if field == "titleId":
            data_vals[0] = data[field]
         elif field == "fullTitle":
            data_vals[1] = data[field]
         elif field == "subjects":
            data_vals[2] = data[field]
         elif field == "publicationDate":
            data_vals[3] = data[field]
         elif field == "notes":
            data_vals[4] = data[field]
         elif field == "thumbnail":
            data_vals[5] = data[field]
         elif field == "holdings":
            data_vals[6] = data[field]


      
      # Use functions to extract desired information from these json headers and format it
      if data_vals[2] is not None:
         data_vals[2] = parse_subjects(data_vals[2])
      if data_vals[4] is not None:
         data_vals[4] = parse_notes(data_vals[4])
      if data_vals[6] is not None:
         data_vals[6] = parse_holdings(data_vals[6])

      # Check for any blank fields and temporarily fill with None
      for i, value in enumerate(data_vals):
         if value == "" or value is None:
            data_vals[i] = "N/A"

      ## Ghetto rip all the values needed to write to sql
      final_out = [None for i in range(6)]

      # Table index
      final_out[0] = num
      
      #TitleID
      final_out[1] = id

      # Separate title and author
      split = data_vals[1].split('/')

      title = split[0]

      if len(split) > 1:
         author = split[1]

      else:
         author = "N/A"

      
      # Title
      final_out[2] = title.replace("\"", "\\\"")

      # Author 
      final_out[3] = author.replace("\"", "\\\"")

      # Call Number
      final_out[4] = data_vals[6]

      if not final_out[4][2].isspace():
         final_out[4] = final_out[4][:2] + " " + final_out[4][2:]

      # Thumbnail_link
      final_out[5] = data_vals[5]
      

      if final_out[4] == 'None':
         print("No call number, skipping this entry")

      elif final_out[4][:2] != "BF":
         print("Not a BF, not adding to database")
      else:
         final_out[4] = split_cut(final_out[4])
         print("Adjusted call: ", final_out[4])

         split = final_out[4].split(' ')
         val = float(split[1])

         print("Call num: ", split[1])

         if len(split) > 2:
            print("Author letter: ", split[2][1])


         sql = f"""INSERT INTO ala (
                  TableIndex, TitleID, Title, Resource_Type, Author, Call_Number, Thumbnail_Link)
                  VALUES ({num_added}, {final_out[1]}, "{final_out[2]}","Print", "{final_out[3]}", "{final_out[4]}", "{final_out[5]}")"""
         num_added += 1

         print("Call to add: ", final_out[4])

         if i == 20:
            break

         # Execute and commit
         mycursor.execute(sql)
         mydb.commit()

