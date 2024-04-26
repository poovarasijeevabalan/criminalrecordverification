import pandas as pd

def input_combinations(Name_Combinations):
    if isinstance(Name_Combinations, str):
        # Split the 'Name_Combinations' string by '|'
        name_combinations_list = Name_Combinations.split('|')
    elif isinstance(Name_Combinations, pd.DataFrame):
        # Load data from the Excel file
        name_combinations_list = Name_Combinations['Name_Combinations'].tolist()

    first_names = []
    last_names = []

    # For each name combination, split it by ',' to separate the first name and last name
    for name_combination in name_combinations_list:
        name_combinations_list = list(Name_Combinations.split('|'))
        # print(name_combinations_list)
        names = name_combination.split(',')
        if len(names) >= 2:
            last_name = names[1]
            first_name = names[0]
            first_names.append(first_name)
            last_names.append(last_name)
        else:
            print(f"Ignore invalid name combination: {name_combination}")
    name_df = pd.DataFrame({'firstname': first_names, 'lastname': last_names})
    # name_df.to_csv('Name_combinations_split.csv', index = True)
    return name_df

if __name__ == "__main__":
    df = pd.read_excel("NSOR Clear_and_Hit_Cases.xlsx")
    for i, row in df.iterrows():
        name = row['Name_Combinations']
        output = input_combinations(name)
        print(row['Name_Combinations'])
        print("----------------")
        print(output)
        print("----------------------------------------------------")

