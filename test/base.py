import csv


class ConfigBase:

    BASEURL = "http://127.0.0.1:5000/api/"

    MORBIDITY_POST_KEYS = ['MorbidityTestName', 'MorbidityTestUnit', 'MorbidityMarkerRef', 'MorbidityName']
    MORBIDITY_PUT_KEYS = ['MorbidityTestUnit', 'MorbidityMarkerRef']

    USER__POST_KEYS = ['UserType', 'FirstName', 'LastName', 'Contact', 'Email', 'Allergy', 'FoodCategory',
                     'DieticianId', 'Address1', 'Address2', 'City', 'State', 'Country', 'LoginUsername', 'Password']

    USER_PUT_KEYS = ['FirstName', 'LastName', 'Contact', 'Email', 'Allergy', 'FoodCategory',
                     'Address1', 'Address2', 'City', 'State', 'Country']

    MORBIDITY_ENDPOINT = BASEURL+"Morbidity"
    MORBIDITY_NAME_ENDPOINT = BASEURL+"Morbidity/MorbidityName={}"
    MORBIDITY_TESTID_ENDPOINT = BASEURL+"Morbidity/MorbidityTestId={}"
    MORBIDITY_PUT_ENDPOINT = BASEURL+"Morbidity/MorbidityName={}&MorbidityTestId={}"
    MORBIDITY_DEL_ENDPOINT = BASEURL + "Morbidity/MorbidityName={}&MorbidityTestId={}"

    USER_ENDPOINT = BASEURL+"Users"
    USER_FNAME_ENDPOINT = BASEURL+"Users/FirstName={}"
    USER_TYPE_ENDPOINT = BASEURL+"Users/UserType={}"
    USER_DIETICIAN_ENDPOINT = BASEURL+"Users/DieticianId={}"
    USER_CONTACT_ENDPOINT = BASEURL+"Users/Contact={}"
    USER_EMAIL_ENDPOINT = BASEURL+"Users/Email={}"
    USER_PUT_ENDPOINT = BASEURL+"Users/DieticianId={}&Userid={}"
    USER_DEL_ENDPOINT = BASEURL+"Users/DieticianId={}&Userid={}"

    RECIPE_ENDPOINT = BASEURL + "Recipes"
    RECIPE_FOODCATG_ENDPOINT = BASEURL+"Recipes/RecipeFoodCategory={}"
    RECIPE_INGR_ENDPOINT = BASEURL + "Recipes/RecipeIngredient={}"
    RECIPE_NUTRI_ENDPOINT = BASEURL + "Recipes/RecipeNutrient={}"
    RECIPE_RTYPE_ENDPOINT = BASEURL + "Recipes/RecipeType={}"

    def read_cvs(payload_path):
        csv_list=[]
        with open(payload_path) as csvfile:
            csvReader = csv.reader(csvfile, delimiter='=')
            for row in csvReader:
                csv_list.append(row)
        return csv_list


    def convert_csv_dict(key_list,value_list):
        Morbidity_list=[]
        for item in enumerate(value_list):
            d = ({k: v for k, v in zip(key_list, item[1])})
            Morbidity_list.append(d)
        return Morbidity_list