import keys

""" user account type """
ACCOUNT_TYPE_CHOICES = [
    (keys.ACCOUNT_DOCTOR, keys.ACCOUNT_DOCTOR),
    (keys.ACCOUNT_DISTRIBUTOR, keys.ACCOUNT_DISTRIBUTOR),
    (keys.ACCOUNT_PATIENTS, keys.ACCOUNT_PATIENTS),
    (keys.ACCOUNT_SUPER_ADMIN, keys.ACCOUNT_SUPER_ADMIN),
]

"""gender option"""
GENDER_CHOICE = [
    (keys.GENDER_MALE, keys.GENDER_MALE),
    (keys.GENDER_FEMALE, keys.GENDER_FEMALE),
    (keys.GENDER_TRANSGENDER, keys.GENDER_TRANSGENDER),
    (keys.GENDER_OTHER, keys.GENDER_OTHER),
]

"""DRUG_UNIT"""
DRUG_UNIT = [
    (keys.QTY, keys.QTY),
    (keys.DROP, keys.DROP),
    (keys.ML, keys.ML),
    (keys.GRAM, keys.GRAM),
    (keys.MG, keys.MG),
    (keys.CUP, keys.CUP),
]

"""DRUG_TYPE"""
DRUG_TYPE = [
    (keys.QTY, keys.QTY),
    (keys.DROP, keys.DROP),
]

ITEM_CATEGORY = [
    (keys.DRUG, keys.DRUG),
    (keys.INSTRUMENT, keys.INSTRUMENT),
]
