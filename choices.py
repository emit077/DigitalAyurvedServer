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

"""gender option"""
DRUG_UNIT = [
    (keys.QTY, keys.QTY),
    (keys.DROP, keys.DROP),
    (keys.ML, keys.ML),
    (keys.GRAM, keys.GRAM),
    (keys.MG, keys.MG),
    (keys.CUP, keys.CUP),
]
TRANSACTION_TYPE_CHOICES = [
    (keys.PURCHASE_ORDER, keys.PURCHASE_ORDER),
    (keys.SALES_ORDER, keys.SALES_ORDER),
    (keys.SHRINK_ITEM, keys.SHRINK_ITEM),
    (keys.ARCHIVE_ITEM, keys.ARCHIVE_ITEM),
    (keys.EXPIRED_ITEM, keys.EXPIRED_ITEM),
]
DISCOUNT_TYPE_CHOICES = [
    (keys.PERCENT_DISCOUNT, keys.PERCENT_DISCOUNT),
    (keys.FLAT_DISCOUNT, keys.FLAT_DISCOUNT)
]
