import decimal
import os
import csv
import io
from decimal import Decimal

STORE_LOCATION = os.path.join(os.getcwd(), "read_files")
WIX_STORE_LOCATION = os.path.join(STORE_LOCATION, "wix_products.csv")
SHOPIFY_STORE_LOCATION = os.path.join(STORE_LOCATION, "shopify_products.csv")

# ALL THESE FIELDS MUST BE ADDRESSED IN ONE WAY OR ANOTHER [IN SHOPIFY]
HANDLE = 'Handle'
TITLE = 'Title'
BODY = 'Body (HTML)'
VENDOR = 'Vendor'
TAGS = 'Tags'
SKU = 'Variant SKU'
PUBLISHED = 'Published'
OPTION1NAME = 'Option1 Name'
OPTION1VALUE = 'Option1 Value'
OPTION2NAME = 'Option2 Name'
OPTION2VALUE = 'Option2 Value'
VARIANT_GRAMS = 'Variant Grams'
VARIANT_QTY = 'Variant Inventory Qty'
VARIANT_PRICE = 'Variant Price'
IMAGE_SOURCE = 'Image Src'
IMAGE_POSITION = 'Image Position'
GIFT_CARD = 'Gift Card'
STATUS = 'Status'

VARIANT_WEIGHT = 'Variant Weight Unit'
VARIANT_POLICY = 'Variant Inventory Policy'              # Entire Column fills out to 'deny'
VARIANT_FULFILMENT = 'Variant Fulfillment Service'       # Entire Column fills out to 'manual'
VARIANT_SHIPPING = 'Variant Requires Shipping'           # Entire Column fills out to 'TRUE'
VARIANT_TAXABLE = 'Variant Taxable'                      # Entire Column fills out to 'TRUE'
VARIANT_TRACKER = 'Variant Inventory Tracker'            # Entire Column fills out to 'shopify'

# Translates Shopify headers to wix
TOWIX = {
    TITLE: 'name',
    BODY: 'description',
    IMAGE_SOURCE: 'productImageUrl',
    TAGS: 'collection',
    SKU: 'sku',
    VARIANT_PRICE: 'price',
    PUBLISHED: 'visible',
    VARIANT_QTY: 'inventory',
    VARIANT_GRAMS: 'weight',
    OPTION1NAME: 'productOptionName1',
    OPTION1VALUE: 'productOptionDescription1',
    OPTION2NAME: 'productOptionName2',
    OPTION2VALUE: 'productOptionDescription2',
}


# PARAMS: [csv_file] - file to get headers from
# RETURNS: Dictionary instantiated with column-headers as the keys.
def get_headers(csv_file):
    template_headers = []
    with open(csv_file, 'r') as header_template:
        for header in csv.DictReader(header_template).fieldnames:
            template_headers.append(header)

    return template_headers


# PARAMS: [raw_handle] - Item Titles'
# RETURNS: String stripped of invalid characters
# Translates TITLE into a Shopify HANDLE
def translate_handle(raw_handle):
    new_handle = str(raw_handle).lower().strip()

    characters_to_remove = [
        '\'', '\"', '\\', '®', '?', '\''
    ]

    universal_char = '-'
    characters_to_replace = {
        'ö': 'o',
        '.': universal_char,
        '/': universal_char,
        '(': universal_char,
        ')': universal_char,
        '+': universal_char,
        ' ': universal_char,
        '---': universal_char,
        '--': universal_char,
    }

    for remove_char in characters_to_remove:
        new_handle = new_handle.replace(remove_char, '')

    for replace_char in characters_to_replace.keys():
        new_handle = new_handle.replace(replace_char, characters_to_replace[replace_char])

    return new_handle


# RETURNS: Default Shopify item-dictionary with instantiated default cells
# With the exception of "Single-Item Image Rows" all other rows have
# static cell values. Thus, we have a default Shopify item.
def get_shopify_default_item():
    shopify_blank = {
        VARIANT_WEIGHT: 'ib',
        VARIANT_POLICY: 'deny',
        VARIANT_FULFILMENT: 'manual',
        VARIANT_SHIPPING: 'TRUE',
        VARIANT_TAXABLE: 'TRUE',
        VARIANT_TRACKER: 'shopify'
        }

    return shopify_blank


# PARAMS: [raw_string] - string to search for key string values
# RETURNS: Vendor Name as UTF-8 equivalent string
# Searches for Vendor strings contained in raw_string and translates
# Vendor names into UTF-8 equivalent
def identify_vendor(raw_string):
    vendor_list = [
        'Aztec Innovation',
        'Black Diamond',
        'Ettore',
        'Moerman',
        # Sörbo Tags
        'Sörbo',
        'Sorbo',
        'Wagtail',
        'Maykker',
        'Triumph',
        'Tucker',
        'Winsol',
        'Xero',
        'Genlabs',
        'Glass Gleam',
        'A-1',
        # IPC Pulex tags
        'IPC Pulex',
        'IPC',
        'Pulex',
        'Unger',
        'The Ledger',
        'Titan Labs',
        'Cement Off',
        'Oil Flo',
        'Titan Green',
    ]

    # try and find a vendor in the title
    vendor_found = False
    for vendor in vendor_list:
        if vendor.lower() in raw_string.lower():
            if vendor == 'Pulex' or vendor == 'IPC':
                return 'IPC Pulex'
            elif vendor == 'Sorbo':
                return 'Sörbo'

            elif vendor == 'Glass Gleam' or vendor == 'A-1' or vendor == 'Cement Off' or vendor == 'Cement Off' or vendor == 'Oil Flo' or vendor == 'Titan Green':
                return 'Titan Labs'

            return vendor

        else:
            vendor_found = False

    if not vendor_found:
        return ''


def translate_qty(qty_string):
    if len(qty_string):
        if not str(qty_string).isnumeric():
            return 0

        return qty_string
    else:
        return 0


def translate_weight(weight_string, optional_name='none'):
    try:
        weight_num = float(weight_string)
        gram_const = 453.5924

        return weight_num * gram_const
    except ValueError:
        print('ERROR: ' + optional_name + ' WEIGHT FAILED TO CONVERT FROM -> ' + weight_string)
        return 0


# PARAMS: [tag_cell] - Category cell from Wix item
#         [additional_tags] - Any other tag that should be included into the tag cell of Shopify item
# RETURNS: Single string with formatted as Shopify tags
def translate_tags(tag_cell, additional_tags=[]):
    tags = ''
    if len(tag_cell):
        tags = str(tag_cell).replace(' and ', ' ')
        tags = tags.strip(' 1')
        tags = tags.replace(' ', ', ')
        tags = tags.replace(';', ', ')
        tags = tags.lower()

        for tag in additional_tags:
            tags = tags + ', ' + tag

    return tags


# PARAMS: [image_string] - raw wix image url
# RETURNS: a single image location url
# EXAMPLE:
# From: eea7b6_acbbbbda0aac4c828f42329ee101f1bc~mv2.jpg
# To: https://static.wixstatic.com/media/eea7b6_acbbbbda0aac4c828f42329ee101f1bc~mv2.jpg
def convert_image(image_string):
    static_img_key = 'https://static.wixstatic.com/media/'
    if len(image_string):
        return static_img_key + image_string
    else:
        return ''


def translate_title(title_string):
    return title_string.replace('Sorbo', 'Sörbo')


# ------------------ MAIN ------------------
wix_store = io.open(WIX_STORE_LOCATION, 'r', encoding="utf-8")
try:
    wix_store_items = csv.DictReader(wix_store)

    # Create Shopify store
    shopify_headers = get_headers(os.path.join(STORE_LOCATION, 'shopify_template.csv'))
    with open(SHOPIFY_STORE_LOCATION, 'w', newline='', encoding="utf-8") as shopify_store:
        writer = csv.DictWriter(shopify_store, fieldnames=shopify_headers)
        writer.writeheader()

        # Traverse all items in wix store and identify product variations and single products
        for wix_item in wix_store_items:
            # Gather key data for any succeeding rows
            variant_cell = wix_item[TOWIX[OPTION1VALUE]]
            image_strings = str(wix_item[TOWIX[IMAGE_SOURCE]]).split(';')

            # PRODUCT VARIATION
            # Product variation header
            if len(variant_cell) > 0 and wix_item['fieldType'] != 'Variant':
                # Gather THIS item's variations
                variant_list = str(variant_cell).split(';')
                shopify_variation_block = []

                price_adjustment = 0
                price_cell = str(wix_item[TOWIX[VARIANT_PRICE]])
                if price_cell != '0.0':
                    try:
                        price_adjustment = Decimal(price_cell)
                    except decimal.InvalidOperation:
                        print("ERROR: PRICE CONVERSION FAILED: " + wix_item[TOWIX[HANDLE]])

                i = 0
                variant_list_length = len(variant_list)
                while i < variant_list_length:
                    variant_item = wix_store_items.__next__()
                    new_shopify_item = get_shopify_default_item()

                    # Fill Shopify header data
                    if i == 0:
                        new_shopify_item[TITLE] = translate_title(wix_item[TOWIX[TITLE]])
                        new_shopify_item[BODY] = wix_item[TOWIX[BODY]]
                        new_shopify_item[VENDOR] = identify_vendor(wix_item[TOWIX[TITLE]])
                        new_shopify_item[TAGS] = translate_tags(wix_item[TOWIX[TAGS]])
                        new_shopify_item[OPTION1NAME] = wix_item[TOWIX[OPTION1NAME]]
                        new_shopify_item[PUBLISHED] = wix_item[TOWIX[PUBLISHED]]
                        new_shopify_item[GIFT_CARD] = 'FALSE'
                        new_shopify_item[STATUS] = 'active'

                        identify_vendor(wix_item[TOWIX[TITLE]])

                        # Image Munips
                        if len(image_strings) >= 1:
                            new_shopify_item[IMAGE_POSITION] = 1
                            new_shopify_item[IMAGE_SOURCE] = convert_image(image_strings.pop())

                    # Verify Price
                    if price_adjustment > 0:
                        try:
                            if len(variant_item['surcharge']) > 0:
                                surcharge = Decimal(variant_item['surcharge'])
                                new_shopify_item[VARIANT_PRICE] = surcharge + price_adjustment

                            else:
                                new_shopify_item[VARIANT_PRICE] = price_adjustment

                        except decimal.InvalidOperation:
                            print("ERROR: SURCHARGE FAILED TO CONVERT: " + str(wix_item[TOWIX[TITLE]]) + ' -> ' + variant_item['surcharge'])
                    else:
                        new_shopify_item[VARIANT_PRICE] = variant_item['surcharge']

                    # Fill variation data
                    variant_list.pop()
                    new_shopify_item[HANDLE] = translate_handle(wix_item[TOWIX[TITLE]])
                    new_shopify_item[OPTION1VALUE] = variant_item[TOWIX[OPTION1VALUE]]
                    new_shopify_item[SKU] = variant_item[TOWIX[SKU]]
                    new_shopify_item[VARIANT_QTY] = translate_qty(variant_item[TOWIX[VARIANT_QTY]])
                    new_shopify_item[VARIANT_GRAMS] = translate_weight(variant_item[TOWIX[VARIANT_GRAMS]], new_shopify_item[HANDLE])

                    # Only enter on the second iteration of this loop
                    if i >= 1 and len(image_strings):
                        new_shopify_item[IMAGE_POSITION] = i+1
                        new_shopify_item[IMAGE_SOURCE] = convert_image(image_strings.pop())

                    i = i+1
                    shopify_variation_block.append(new_shopify_item)

                writer.writerows(shopify_variation_block)

            # SINGLE PRODUCT
            # Regular Product with no variations
            elif wix_item['fieldType'] == 'Product':
                new_shopify_item = get_shopify_default_item()
                new_shopify_item[TITLE] = translate_title(wix_item[TOWIX[TITLE]])
                new_shopify_item[BODY] = wix_item[TOWIX[BODY]]
                new_shopify_item[VENDOR] = identify_vendor(wix_item[TOWIX[TITLE]])
                new_shopify_item[TAGS] = translate_tags(wix_item[TOWIX[TAGS]])
                new_shopify_item[OPTION1NAME] = wix_item[TOWIX[OPTION1NAME]]
                new_shopify_item[PUBLISHED] = wix_item[TOWIX[PUBLISHED]]
                new_shopify_item[GIFT_CARD] = 'FALSE'
                new_shopify_item[STATUS] = 'active'

                identify_vendor(wix_item[TOWIX[TITLE]])

                # Fill variation data
                new_shopify_item[HANDLE] = translate_handle(wix_item[TOWIX[TITLE]])
                new_shopify_item[OPTION1NAME] = 'Title'
                new_shopify_item[OPTION1VALUE] = 'Default Title'
                new_shopify_item[SKU] = wix_item[TOWIX[SKU]]
                new_shopify_item[VARIANT_PRICE] = wix_item[TOWIX[VARIANT_PRICE]]
                new_shopify_item[VARIANT_QTY] = translate_qty(wix_item[TOWIX[VARIANT_QTY]])
                new_shopify_item[VARIANT_GRAMS] = translate_weight(wix_item[TOWIX[VARIANT_GRAMS]], new_shopify_item[TITLE])

                # Image Munips
                new_img_bloc = []
                if len(image_strings) > 0 and image_strings[0] != '':
                    new_shopify_item[IMAGE_POSITION] = 1
                    new_shopify_item[IMAGE_SOURCE] = convert_image(image_strings.pop())

                    j = 1
                    for imgs in image_strings:
                        j = j+1
                        img_line = {}
                        img_line[HANDLE] = new_shopify_item[HANDLE]
                        img_line[IMAGE_POSITION] = j
                        img_line[IMAGE_SOURCE] = convert_image(imgs)
                        new_img_bloc.append(img_line)

                writer.writerow(new_shopify_item)
                if len(new_img_bloc) > 0:
                    writer.writerows(new_img_bloc)

finally:
    wix_store.close()
