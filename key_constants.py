MORBIDITY_PK_PREFIX = 'MR#'
MORBIDITY_SK_PREFIX = 'TEST#'
RECIPE_PK_PREFIX = 'RECIPE#'
RECIPE_SK_PREFIX = 'RID#'
MORBIDITY_INFO='Morbidity'
USER_PREFIX={'PK':'LOGIN#', 'SK':'USER#'}
INFO_TYPE = {'MORBIDITY':'Morbidity','USER':'User'}
USER_TYPE_PREFIX = {'Dietician':'DT','Patient':'PT'}


REQUIRE_USER_DATA = ['UserType', 'FirstName', 'LastName', 'Address',
                     'Contact', 'Email', 'DieticianId', 'LoginUsername', 'Password','FoodCategory','Allergy']

REQUIRE_MORB_DATA = ['MorbidityName', 'MorbidityTestName', 'MorbidityMarkerRef', 'MorbidityTestUnit']

