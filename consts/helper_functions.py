import pandas as pd


# Create a function to map each crop to a family
def map_family(crop):
    if 'beans' in crop.lower():
        return 'Beans'
    elif 'maize' in crop.lower():
        return 'Maize'
    elif 'potatoes' in crop.lower():
        return 'Potatoes'
    elif 'wheat' in crop.lower():
        return 'Wheat'
    elif 'cassava' in crop.lower():
        return 'Cassava'
    else:
        return 'Vegetables'


def crop_manure_intake(manure_df):
    # Get the unique elements of manure
    A, V, L = manure_df['Element'].unique()

    # compute the manure that is percieved to be used by the crops i.e does not volatile or leach
    # create a new dataframe to hold the results
    results_df = {'Area': [], 'Year': [], 'Item': [], 'Unit': [], 'Value': []}
    df = manure_df

    # iterate over each row in the original dataframe
    for index, row in df.iterrows():
        if row['Element'] == A:
            # compute the value of D using the formula D = A - (B+C)
            absorbed = row['Value'] - (
                    df[(df['Area'] == row['Area']) & (df['Year'] == row['Year']) & (df['Element'] == V)]['Value'].iloc[
                        0] +
                    df[(df['Area'] == row['Area']) & (df['Year'] == row['Year']) & (df['Element'] == L)]['Value'].iloc[
                        0])

            # add the row values to the new dictionary, including absorbed value
            results_df['Area'].append(row['Area'])
            results_df['Year'].append(row['Year'])
            results_df['Item'].append(row['Element'])
            results_df['Unit'].append(row['Unit'])
            results_df['Value'].append(absorbed)

    # print the results dataframe
    manure_absorbed = pd.DataFrame(results_df)
    return manure_absorbed
