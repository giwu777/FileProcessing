import os
import csv

def process_files(input_folder, output_folder):
   
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    result_file_path = os.path.join(output_folder, 'result.csv')


    input_files = [f for f in os.listdir(input_folder) if f.endswith('.dat')]

    all_data = []

    # Process each .dat file
    for file_name in input_files:
        file_path = os.path.join(input_folder, file_name)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')
            data = list(reader)
            all_data.extend(data)

    # Remove duplicate data
    unique_data = {tuple(row.values()) for row in all_data}
    unique_data = [dict(zip(reader.fieldnames, row)) for row in unique_data]

    # Second highest and average salary
    salaries = [int(row['basic_salary']) for row in unique_data]
    sorted_salaries = sorted(set(salaries), reverse=True)
    second_highest_salary = sorted_salaries[1] if len(sorted_salaries) > 1 else 0
    average_salary = sum(salaries) / len(salaries) if len(salaries) > 0 else 0

    # Append 'Gross Salary' to each row
    for row in unique_data:
        row['Gross Salary'] = str(int(row['basic_salary']) + int(row['allowances']))

    # Append second highest and average salary to the last row
    unique_data.append({
        'id': f'Second Highest Salary: {str(second_highest_salary)}',
        'first_name': f'average salary: {str(average_salary)}',
        'last_name': '',
        'email': '',
        'job_title': '',
        'basic_salary': '',
        'allowances': '' ,
        'Gross Salary': ''
    })

    # Write the Result to a CSV file
    with open(result_file_path, 'w', newline='') as result_file:
        fieldnames = ['id', 'first_name', 'last_name', 'email', 'job_title', 'basic_salary', 'allowances', 'Gross Salary']
        writer = csv.DictWriter(result_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(unique_data)

    print(f'Result saved to {result_file_path}')

input_folder_path = './input/'
output_folder_path = './output/'

process_files(input_folder_path, output_folder_path)
