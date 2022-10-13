from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Tuple
import re

from pydantic import BaseModel, validator, HttpUrl
import dateutil.parser
from iso4217 import Currency
from iso3166 import Country, countries_by_alpha2

Amount = Tuple[Decimal, Currency]

class Tax(BaseModel):
    country: str | None
    
    region: str | None
    postal_code: str | None
    location_id: str | None

    rate: Decimal

    tax_ship: bool | None

class Shipping(BaseModel):
    country: Country

    region: str | None
    postal_code: str | None
    location_id: str | None
    location_group_name: str | None

    service: str | None
    price: Amount | None

    min_handling_time: int | None
    max_handling_time: int | None

    min_transit_time: int | None
    max_transit_time: int | None

class Pause(Enum):
    ADS = 'ads'
    ALL = 'all'

class Destination(Enum):
    SHOPPING_ADS = 'Shopping_ads'
    BUY_ON_GOOGLE_LISTING = 'Buy_on_Google_listings'
    DISPLAY_ADS = 'Display_ads'
    LOCAL_INVENTORY_ADS = 'Local_inventory_ads'
    FREE_LISTINGS = 'Free_listings'
    FREE_LOCAL_LISTINGS = 'Free_local_listings'

class ProductDetail(BaseModel):
    section_name: str | None
    attribute_name: str
    attribute_value: str

    def __init__(self, section_name: str, attribute_name: str, attribute_value: str):
        super().__init__(
            section_name=None if section_name == '' else section_name,
            attribute_name=attribute_name,
            attribute_value=attribute_value
        )

class SizeSystem(Enum):
    AU = 'AU'
    BR = 'BR'
    CN = 'CN'
    DE = 'DE'
    EU = 'EU'
    FR = 'FR'
    IT = 'IT'
    JP = 'JP'
    MEX = 'MEX'
    UK = 'UK'
    US = 'US'

class SizeType(Enum):
    REGULAR = 'regular'
    PETITE = 'petite'
    PLUS = 'plus'
    TALL = 'tall'
    BIG = 'big'
    MATERNITY = 'maternity'

class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'
    UNISEX = 'unisex'

class AgeGroup(Enum):
    NEWBORN = "newborn"
    INFANT = "infant"
    TODDLER = "toddler"
    KIDS = "kids"
    ADULT = "adult"

class EnergyEfficiency(Enum):
    APPP = 'A+++'
    APP = 'A++'
    AP = 'A+'
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'

class Condition(Enum):
    NEW = 'new'
    REFURBISHED = 'refurbished'
    USED = 'used'

class Installment(BaseModel):
    months: int
    amount: Amount

class SubscriptionCost(BaseModel):
    class Period(Enum):
        MONTH = 'month'
        YEAR = 'year'

    period: Period
    period_length: int
    amount: Amount

class LoyaltyPoints(BaseModel):
    name: str | None
    points_value: int
    ratio: Decimal = Decimal(1.0)

    def __init__(self, name: str, points_value: str, ratio: str):
        super().__init__(
            name=None if name == '' else name,
            points_value=points_value,
            ratio=Decimal(1.0) if ratio == '' else Decimal(ratio)
        )
        

class Availability(Enum):
    IN_STOCK = 'in stock'
    OUT_OF_STOCK = 'out of stock'
    PREORDER = 'preorder'
    BACKORDER = 'backorder'

class LenUnit(Enum):
    CM = 'cm'
    IN = 'in'

class WeightUnit(Enum):
    LB = 'lb'
    LBS = 'lbs'
    OZ = 'oz'
    G = 'g'
    KG = 'KG'

class Unit(Enum):
    # Weight
    OZ = 'oz'
    LB = 'lb'
    LBS = 'lbs'
    MG = 'mg'
    G = 'g'
    KG = 'kg'

    # Volume (US imperial)
    FLOZ = 'floz'
    PT = 'pt'
    QT = 'qt'
    GAL = 'gal'

    # Volume (metric)
    ML = 'ml'
    CL = 'cl'
    L = 'l'
    CBM = 'cbm'

    # Length
    IN = 'in'
    FT = 'ft'
    YD = 'yd'
    CM = 'cm'
    M = 'm'

    # Area
    SQFT = 'sqft'
    SQM = 'sqm'

    # Per unit
    CT = 'ct'


class Google(BaseModel):
    # Basic product data
    id: str
    @validator('id')
    def id_len(cls, v):
        assert len(v) <= 50, 'id must be less than 50 characters'
        return v

    title: str
    @validator('title')
    def title_len(cls, v):
        assert len(v) <= 150, 'title must be less than 150 characters'
        return v

    description: str
    @validator('description')
    def description_len(cls, v):
        assert len(v) <= 5000, 'description must be less than 5000 characters'
        return v

    link: HttpUrl
    @validator('link')
    def link_len(cls, v):
        assert len(v) <= 2000, 'link must be less than 2000 characters'
        return v

    image_link: HttpUrl
    @validator('image_link')
    def image_link_len(cls, v):
        assert len(v) <= 2000, 'image_link must be less than 2000 characters'
        return v

    additional_image_link: list[str] | None
    @validator('additional_image_link', pre=True)
    def additional_image_link_format(cls, v):
        if v:
            assert len(v) <= 2000, 'additional_image_link must be less than 2000 characters'
            # When it is from CSV, it is a string and should be converted to a list by splitting on commas
            # The list is then validated to ensure it is less than 10 items
            v = v.split(',', 10)[:10]
        return v

    mobile_link: HttpUrl | None
    @validator('mobile_link')
    def mobile_link_len(cls, v):
        if v:
            assert len(v) <= 2000, 'mobile_link must be less than 2000 characters'
        return v

    # Price and availability
    availability: Availability
    availability_date: datetime | None
    @validator('availability_date', pre=True)
    def availability_date_format(cls, v):
        if v:
            assert len(v) <= 25, 'availability_date must be less than 25 characters'
            v = dateutil.parser.parse(v)
        return v

    cost_of_goods_sold: Tuple[Decimal, Currency] | None
    @validator('cost_of_goods_sold', pre=True)
    def cost_of_goods_sold_format(cls, v):
        if v:
            parsed = v.split(' ', 1)
            assert len(parsed) == 2, 'cost_of_goods_sold must be in the format "0.00 USD"'
            v = (Decimal(parsed[0]), Currency(parsed[1]))
        return v

    expiration_date: datetime | None
    @validator('expiration_date', pre=True)
    def expiration_date_format(cls, v):
        if v:
            assert len(v) <= 25, 'expiration_date must be less than 25 characters'
            v = dateutil.parser.parse(v)
        return v

    price: Amount
    @validator('price', pre=True)
    def price_format(cls, v):
        parsed = v.split(' ', 1)
        assert len(parsed) == 2, 'price must be in the format "0.00 USD"'
        return (Decimal(parsed[0]), Currency(parsed[1]))

    sale_price: Amount | None
    @validator('sale_price', pre=True)
    def sale_price_format(cls, v):
        if v:
            parsed = v.split(' ', 1)
            assert len(parsed) == 2, 'sale_price must be in the format "0.00 USD"'
            v = (Decimal(parsed[0]), Currency(parsed[1]))
        return v

    sale_price_effective_date: Tuple[datetime, datetime] | None
    @validator('sale_price_effective_date', pre=True)
    def sale_price_effective_date_format(cls, v):
        if v:
            parsed = v.split('/', 1)
            assert len(parsed) == 2, 'sale_price_effective_date must be in the format "2020-01-01/2020-01-31"'
            v = (dateutil.parser.parse(parsed[0]), dateutil.parser.parse(parsed[1]))
        return v

    unit_pricing_measure: Unit | None
    @validator('unit_pricing_measure', pre=True)
    def unit_pricing_measure_format(cls, v):
        if v:
            v = Unit(v)
        return v

    unit_pricing_base_measure: Tuple[int, Unit] | None
    @validator('unit_pricing_base_measure', pre=True)
    def unit_pricing_base_measure_format(cls, v):
        if v:
            p = re.compile(r"^(\d+)(\w+)$")
            m = p.match(v)
            assert m, 'unit_pricing_base_measure must be in the format "[integer][unit]" such as "15kg"'
            g = m.groups()
            assert len(g) == 2, 'unit_pricing_base_measure must be in the format "[integer][unit] such as "15kg"'
            v = (int(g[0]), Unit(g[1]))
        return v

    installment: Installment | None
    @validator('installment', pre=True)
    def installment_format(cls, v):
        if v and isinstance(v, str):
            parsed = v.split(':', 1)
            assert len(parsed) == 2, 'installment must be in the format "3:10.00 USD"'
            amount = parsed[1].split(' ', 1)
            assert len(amount) == 2, 'amount of installment must be in the format "10.00 USD"'
            v = Installment(
                months=int(parsed[0]),
                amount=(Decimal(amount[0]), Currency(amount[1]))
            )
        return v

    subscription_cost: SubscriptionCost | None
    @validator('subscription_cost', pre=True)
    def subscription_cost_format(cls, v):
        if v and isinstance(v, str):
            parsed = v.split(':', 2)
            assert len(parsed) == 3, 'subscription_cost must be in the format "month:12:10.00 USD"'
            amount = parsed[2].split(' ', 1)
            assert len(amount) == 2, 'amount of subscription_cost must be in the format "10.00 USD"'
            v = SubscriptionCost(
                period=SubscriptionCost.Period(parsed[0]),
                period_length=int(parsed[1]),
                amount=(Decimal(amount[0]), Currency(amount[1]))
            )
        return v

    loyalty_points: LoyaltyPoints | None
    @validator('loyalty_points', pre=True)
    def loyalty_points_format(cls, v):
        if v and isinstance(v, str):
            parsed = v.split(':', 2)
            assert len(parsed) == 3, 'loyalty_points must be in the format "Plan A:100:0.5"'
            v = LoyaltyPoints(
                name=parsed[0],
                points=parsed[1],
                ratio=parsed[2]
            )
        return v

    # Product category
    google_product_category: str | None
    product_type: list[str] | None
    @validator('product_type', pre=True)
    def product_type_format(cls, v):
        if v:
            assert len(v) <= 750, 'product_type must be less than 750 characters'
            v = v.split(',', 5)[:5]
        return v

    # Product identifiers 
    brand: str | None
    @validator('brand')
    def brand_len(cls, v):
        if v:
            assert len(v) <= 70, 'brand must be less than 70 characters'
        return v

    gtin: list[str] | None
    @validator('gtin', pre=True)
    def gtin_format(cls, v):
        pass

    mpn: str | None
    @validator('mpn')
    def mpn_len(cls, v):
        if v:
            assert len(v) <= 70, 'mpn must be less than 70 characters'
        return v

    identifier_exists: bool | None


    # Detailed product description
    condition: Condition | None
    adult: bool | None
    multipack: int | None
    is_bundle: bool | None
    energy_efficiency_class: EnergyEfficiency | None
    min_energy_efficiency_class: EnergyEfficiency | None
    max_energy_efficiency_class: EnergyEfficiency | None
    age_group: AgeGroup | None
    color: list[str] | None
    @validator('color')
    def color_format(cls, v):
        if v:
            assert len(v) <= 100, 'color must be less than 100 characters'
            v = v.split('/', 3)[:3]
        return v

    gender: Gender | None
    material: str | None
    @validator('material')
    def material_len(cls, v):
        if v:
            assert len(v) <= 200, 'material must be less than 200 characters'
        return v

    pattern: str | None
    @validator('pattern')
    def pattern_len(cls, v):
        if v:
            assert len(v) <= 100, 'pattern must be less than 100 characters'
        return v

    size: str | None
    @validator('size')
    def size_len(cls, v):
        if v:
            assert len(v) <= 100, 'size must be less than 100 characters'
        return v

    size_type: list[SizeType] | None
    @validator('size_type', pre=True)
    def size_type_format(cls, v):
        if v and isinstance(v, str):
            v = v.split(',', 2)[:2]
        return v

    size_system: SizeSystem | None
    item_group_id: str | None
    @validator('item_group_id')
    def item_group_id_len(cls, v):
        if v:
            assert len(v) <= 50, 'item_group_id must be less than 50 characters'
        return v

    product_length: Tuple[str, LenUnit] | None
    product_width: Tuple[str, LenUnit] | None
    product_height: Tuple[str, LenUnit] | None
    @validator('product_length', 'product_width', 'product_height', pre=True)
    def product_dimension_format(cls, v):
        if v:
            parsed = v.split(' ', 1)
            assert len(parsed) == 2, 'product_length, product_width, product_height must be in the format "15 cm"'
            assert parsed[0] >= 1 and parsed[0] <= 3000, 'product_length, product_width, product_height must be between 1 and 3000'
            v = (parsed[0], LenUnit(parsed[1]))
        return v

    product_weight: Tuple[str, WeightUnit] | None
    @validator('product_weight', pre=True)
    def product_weight_format(cls, v):
        if v:
            parsed = v.split(' ', 1)
            assert len(parsed) == 2, 'product_weight must be in the format "15 kg"'
            assert parsed[0] >= 0 and parsed[0] <= 2000, 'product_weight must be between 1 and 3000'
            v = (parsed[0], WeightUnit(parsed[1]))
        return v

    product_detail: list[ProductDetail] | None
    @validator('product_detail', pre=True)
    def product_detail_format(cls, v):
        if v and isinstance(v, str):
            details = v.split(',', 1000)[:1000]
            v = []
            for detail in details:
                parsed = detail.split(':', 2)
                assert len(parsed) == 3, 'product_detail must be in the format "section_name:attribute_name:attribute_value"'
                v.append(ProductDetail(
                    section_name=parsed[0],
                    attribute_name=parsed[1],
                    attribute_value=parsed[2]
                ))
        return v

    product_hightlight: list[str] | None
    @validator('product_hightlight', pre=True)
    def product_hightlight_format(cls, v):
        if v and isinstance(v, str):
            v = v.split(',', 10)[:10]
        return v

    # Shopping campaigns and other configurations
    ads_redirect: HttpUrl | None
    @validator('ads_redirect')
    def ads_redirect_len(cls, v):
        if v:
            assert len(v) <= 2000, 'ads_redirect must be less than 2000 characters'
        return v

    custom_label_0: str | None
    custom_label_1: str | None
    custom_label_2: str | None
    custom_label_3: str | None
    custom_label_4: str | None
    @validator('custom_label_0', 'custom_label_1', 'custom_label_2', 'custom_label_3', 'custom_label_4')
    def custom_label_len(cls, v):
        if v:
            assert len(v) <= 100, 'custom_label_0, custom_label_1, custom_label_2, custom_label_3, custom_label_4 must be less than 100 characters'
        return v

    promotion_id: list[str] | None
    @validator('promotion_id')
    def promotion_id_len(cls, v):
        if v:
            assert len(v) <= 10, 'promotion_id must be less than 10 items'

    # Destinations
    excluded_destination: list[Destination] | None
    included_destination: list[Destination] | None
    @validator('excluded_destination', 'included_destination', pre=True)
    def destination_format(cls, v):
        if v and isinstance(v, str):
            v = v.split(',', 6)[:6]
        elif v and isinstance(v, list):
            ret = []
            for dest in v:
                ret.append(Destination(dest))
            v = ret[:6]
        return v

    shopping_ads_excluded_country: list[Country] | None
    @validator('shopping_ads_excluded_country', pre=True)
    def shopping_ads_excluded_country_format(cls, v):
        if v and isinstance(v, str):
            v = v.split(',', 100)[:100]
        elif v and isinstance(v, list):
            ret = []
            for country in v:
                ret.append(countries_by_alpha2(country))
            v = ret[:100]
        return v
    pause: Pause | None

    # Shipping
    shipping: list[Shipping] | None
    shipping_label: str | None
    @validator('shipping_label')
    def shipping_label_len(cls, v):
        if v:
            assert len(v) <= 100, 'shipping_label must be less than 100 characters'
        return v

    shipping_weight: Tuple[str, WeightUnit] | None
    @validator('shipping_weight', pre=True)
    def shipping_weight_format(cls, v):
        if v:
            parsed = v.split(' ', 1)
            assert len(parsed) == 2, 'shipping_weight must be in the format "15 kg"'
            if parsed[1] == 'lb' or parsed[1] == 'lbs':
                assert parsed[0] >= 0 and parsed[0] <= 2000, 'shipping_weight must be between 1 and 3000 lbs'
            if parsed[1] == 'kg':
                assert parsed[0] >= 0 and parsed[0] <= 1000, 'shipping_weight must be between 1 and 1000 kg'
            v = (parsed[0], WeightUnit(parsed[1]))
        return v

    shipping_length: Tuple[str, LenUnit] | None
    shipping_width: Tuple[str, LenUnit] | None
    shipping_height: Tuple[str, LenUnit] | None
    @validator('shipping_length', 'shipping_width', 'shipping_height', pre=True)
    def shipping_dimension_format(cls, v):
        if v:
            parsed = v.split(' ', 1)
            assert len(parsed) == 2, 'shipping_length, shipping_width, shipping_height must be in the format "15 cm"'
            if parsed[1] == 'in':
                assert parsed[0] <= 150, 'shipping_length, shipping_width, shipping_height must be less than 150 inch'
            if parsed[1] == 'cm':
                assert parsed[0] <= 400, 'shipping_length, shipping_width, shipping_height must be less than 400 cm'
            v = (parsed[0], LenUnit(parsed[1]))
        return v

    ships_from_country: Country | None
    @validator('ships_from_country', pre=True)
    def ships_from_country_format(cls, v):
        if v:
            v = countries_by_alpha2(v)
        return v

    transit_time_label: str | None
    @validator('transit_time_label')
    def transit_time_label_len(cls, v):
        if v:
            assert len(v) <= 100, 'transit_time_label must be less than 100 characters'
        return v

    max_handling_time: int | None
    min_handling_time: int | None
    @validator('max_handling_time', 'min_handling_time')
    def handling_time_limit(cls, v):
        if v:
            assert v >= 0, 'max_handling_time must be greater than 0'
        return v

    # Tax
    tax: list[Tax] | None
    tax_category: str | None
    @validator('tax_category')
    def tax_category_len(cls, v):
        if v:
            assert len(v) <= 100, 'tax_category must be less than 100 characters'
        return v

    @validator('adult', 'identifier_exists', 'is_bundle', pre=True)
    def bool_format(cls, v):
        if v:
            if v == 'yes' or v == 'true':
                v = True
            elif v == 'no' or v == 'false':
                v = False
            else:
                v = None
        return v

