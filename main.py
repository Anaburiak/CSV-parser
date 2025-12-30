import csv

#read a file and convert it to dictionary bc it's more convenient for me
def read_csv_to_dict(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)
      
filename = 'Students.csv'
data_list = read_csv_to_dict(filename)
#print("The first row in the dictionary: ", data_list[0])  # Print the first row as a dictionary to see the headers of columns


#1 compute rows, columns, and blanks to see the amount of the data and to reuse some of the values later
row_number = len(data_list)
#2
columns = {key for student in data_list for key in student} 
#3
blanks = 0 
has_blanks = False
for row in data_list:
    for key, value in row.items():
        if value is None or value == '' or (isinstance(value, str) and value.strip() == ''):
            has_blanks = True
            blanks += 1
#print("Are there any blanks: ", has_blanks, "; How many: ", blanks)


#4 Ckecking and filtering the data to use freely it and not to catch bugs
keys_in_first = set(data_list[0].keys())
all_have_same_keys = all(set(student.keys()) == keys_in_first for student in data_list) #all Return True if bool(x) is True for all values x in the iterable.
#print("Does all have same keys: ", all_have_same_keys)

empty_dicts = [student for student in data_list if not student] #if not d checks if 'd' is 'falsy' (eg 0, '', [], None, etc)

invalid_keys = [key for student in data_list for key in student.keys() if not isinstance(key, str) or not key.strip()]


#5 convert string numbers into integers to compute some average values later
fields_to_convert = ['Student_ID', 'Age', 'Avg_Daily_Usage_Hours', 'Sleep_Hours_Per_Night', 'Mental_Health_Score', 'Conflicts_Over_Social_Media', 'Addicted_Score']
for item in data_list:
    for field in fields_to_convert:
        if field in item and isinstance(item[field], str):
            try:
                if '.' in item[field]:
                    item[field] = float(item[field])
                else:
                    item[field] = int(item[field])
            except ValueError:
                pass
#watch the result
# print("\n5 random rows:")
# for student in random.sample(data_list, min(5, len(data_list))):
#     print(student)


#average computing function
def average_num(dataset, item):
    total = 0
    valid_values = 0
    for student in dataset:
        if item in student:
            value = student[item]
            if value is not None and value != '':
                try:
                    total+=value
                    valid_values+=1
                except (ValueError, TypeError):
                    continue
    if valid_values>0:
        average = total/valid_values
        return average
    else:
        return 0


# top-N elements 9 to see some maximum values
def valid_data(data, item):
    valid_data = [student for student in data if item in student and student[item] is not None]
    return valid_data

top_5_sleep = sorted(valid_data(data_list, 'Sleep_Hours_Per_Night'), key=lambda x: x['Sleep_Hours_Per_Night'], reverse=True) [:5]

top_5_mental = sorted(valid_data(data_list, 'Mental_Health_Score'), key=lambda x: x['Mental_Health_Score'], reverse=True) [:5]


#grouping by country to understand the size of the survey
from collections import defaultdict
grouped_by_country = defaultdict(list)
for student in data_list:
    grouped_by_country[student['Country']].append(student)


#building and formatting a report to present the some important values from the research 11
with open("report.txt", 'w', encoding='utf-8') as r:

    r.write('=' * 60 + '\n')
    report_header = "CSV Report\n"
    r.write(report_header)
    r.write('=' * 60 + '\n')

    r.write("\nThe Student Social Media & Relationships dataset contains anonymized records of students’ social‐media behaviours and related life outcomes. It spans multiple countries and academic levels, focusing on key dimensions such as usage intensity, platform preferences, and relationship dynamics. Each row represents one student’s survey response, offering a cross‐sectional snapshot suitable for statistical analysis and machine‐learning applications.\n\n")

    r.write('-' * 40 + '\n\n')
    r.write("What I've done: \n")
    r.write('''            1. Downloaded data
            2. Checked the data
            3. Cleaned up and filtered the data
            4. Analysed the data and wrote a report
            5. Saved the report\n\n''')
    r.write('-' * 40 + '\n\n')

    r.write("Categories: ")
    for key in data_list[0].keys():
        r.write(f"{key}, ")
    r.write('\n\n')
    
    r.write(f"Statistics:\n")
    r.write(f" * Amount of participants: {row_number}\n")
    r.write(f" * Average age of participants: {average_num(data_list, 'Age'):.2f}\n")
    r.write(f" * Average hours of use: {average_num(data_list, 'Avg_Daily_Usage_Hours'):.2f}\n")
    r.write(f" * Average Hours of sleep per night: {average_num(data_list, 'Sleep_Hours_Per_Night'):.2f}\n")
    r.write(f" * Average mental health score: {average_num(data_list, 'Mental_Health_Score'):.2f}\n")
    r.write(f" * Average amount of conflicts over social media: {average_num(data_list, 'Conflicts_Over_Social_Media'):.2f}\n")
    r.write(f" * Average score of addiction: {average_num(data_list, 'Addicted_Score'):.2f}\n\n")

    
    r.write("Geography: multi‐country coverage - ")
    for country in grouped_by_country.keys():
        r.write(f"{country}, ")
    r.write('\n\n')

    r.write('=' * 60 + '\n')
    r.write("Conclusion: As I can see from the data the average participant is more or less matured so the research is not about kids. The average daily usage hours reveal that the hours spent being on the phone are no that numerous and are completely fine. But I can't make the same statement about the rest of the data: the average hours of sleep are nut sufficient for the young age, beyond that the mental score which is quite low. However, the amount of conflicts is acceptable. And the addiction rate is significantly high. From my perspective as a digital native, I think that young people should pay attention to their purpose of smartphone use and the content they consume.\n")
    r.write('=' * 60 + '\n')

r.close()


