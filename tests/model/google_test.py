from datetime import datetime
from decimal import Decimal
from gettext import install
from operator import is_
from typing import Tuple
from faker import Faker
from iso3166 import countries_by_alpha2
from pydantic import HttpUrl
from iso4217 import Currency 

from product_feed.model import GoogleProduct
from product_feed.model.google import AgeGroup, Availability, Condition, Destination, EnergyEfficiency, Gender, Installment, LenUnit, LoyaltyPoints, Pause, ProductDetail, Shipping, SizeSystem, SizeType, SubscriptionCost, Tax, Unit, WeightUnit

f = Faker()

class TestGoogleProduct:
    base_product = GoogleProduct(
        id='1',
        title=f.word(),
        description=f.sentence(),
        link=f.url(),
        image_link=f.image_url(),
        price='1.99 TWD',
        availability='in stock'
    )

    full_product = GoogleProduct(
        id='2',
        title=f.word(),
        description=f.sentence(),
        link=f.url(),
        image_link=f.image_url(),
        additional_image_link=','.join([f.image_url() for _ in range(10)]),
        mobile_link=f.url(),
        availability='in stock',
        availability_date=f.date_time().strftime('%Y-%m-%dT%H:%M%z'),
        cost_of_goods_sold='0.99 TWD',
        expiration_date=f.date_time().strftime('%Y-%m-%dT%H:%M%z'),
        price='1.99 TWD',
        sale_price='1.49 TWD',
        sale_price_effective_date=f'{f.date_time().strftime("%Y-%m-%dT%H:%M%z")}/{f.date_time().strftime("%Y-%m-%dT%H:%M%z")}',
        unit_pricing_measure='g',
        unit_pricing_base_measure='4g',
        installment='3:0.5 TWD',
        subscription_cost='month:12:0.99 TWD',
        loyalty_points='Plan A:100:0.1',
        google_product_category='Apparel & Accessories > Clothing > Shirts & Tops',
        product_type='Shirts,Tops & Blouses,Blouses & Button-Down Shirts',
        brand='Google',
        gtin='3234567890126',
        mpn='GO12345OOGLE',
        identifier_exists='no',
        condition='new',
        adult='yes',
        multipack=6,
        is_bundle='yes',
        energy_efficiency_class='A++',
        min_energy_efficiency_class='A',
        max_energy_efficiency_class='A+++',
        age_group='kids',
        color='red/pink',
        gender='unisex',
        material='leather',
        pattern='striped',
        size='S',
        size_type='regular,petite',
        size_system='US',
        item_group_id='123456',
        product_length='20 in',
        product_width='20 cm',
        product_height='20 in',
        product_weight='3.5 lbs',
        product_detail='General:Product Type:Digital player,General:Digital Player Type:Flash based,Display:Resolution:432 x 240,Display:Diagonal Size:2.5"',
        product_hightlight='Supports thousands of apps',
        ads_redirect=f.url(),
        custom_label_0='Seasonal',
        custom_label_1='Clearance',
        custom_label_2='Holiday',
        custom_label_3='Sale',
        custom_label_4='Price range',
        promotion_id='ABC123',
        excluded_destination='Shopping_ads,Buy_on_Google_listings',
        included_destination='Display_ads,Local_inventory_ads',
        shopping_ads_excluded_country='US,DE',
        pause='ads',
        shipping='US::Fedex:1.99 USD',
        shipping_label='Only Fedex',
        shipping_weight='3.5 kg',
        shipping_length='20.5 in',
        shipping_width='20 cm',
        shipping_height='20.5 in',
        ships_from_country='US',
        transit_time_label='3-5 days',
        max_handling_time=3,
        min_handling_time=1,
        tax='US:CA:5.0:yes',
        tax_category='Clothing & Accessories',
    )

    def test_required_fields(self):
        assert self.base_product is not None

        assert isinstance(self.base_product.link, HttpUrl)
        assert isinstance(self.base_product.image_link, HttpUrl)
        
        assert self.base_product.price[0] == Decimal('1.99')
        assert self.base_product.price[1] == Currency.twd
        assert self.base_product.availability == Availability.IN_STOCK
    
    def test_full_fields(self):
        assert self.full_product is not None

        assert isinstance(self.full_product.availability_date, datetime)
        assert isinstance(self.full_product.cost_of_goods_sold[0], Decimal)
        assert isinstance(self.full_product.cost_of_goods_sold[1], Currency)
        assert isinstance(self.full_product.expiration_date, datetime)
        assert isinstance(self.full_product.price[0], Decimal)
        assert isinstance(self.full_product.price[1], Currency)
        assert isinstance(self.full_product.sale_price[0], Decimal)
        assert isinstance(self.full_product.sale_price[1], Currency)
        assert isinstance(self.full_product.sale_price_effective_date[0], datetime)
        assert isinstance(self.full_product.sale_price_effective_date[1], datetime)
        assert isinstance(self.full_product.unit_pricing_measure, Unit)
        assert isinstance(self.full_product.unit_pricing_base_measure[0], int)
        assert isinstance(self.full_product.unit_pricing_base_measure[1], Unit)
        assert isinstance(self.full_product.ads_redirect, HttpUrl)


        assert len(self.full_product.additional_image_link) == 10
        assert self.full_product.installment == Installment(months=3, amount=(Decimal('0.5'), Currency.twd))
        assert self.full_product.subscription_cost == SubscriptionCost(period='month', period_length=12, amount=(Decimal('0.99'), Currency.twd))
        assert self.full_product.loyalty_points == LoyaltyPoints(name='Plan A', points_value=100, ratio=Decimal('0.1'))
        assert len(self.full_product.product_type) == 3
        assert self.full_product.identifier_exists == False
        assert self.full_product.condition == Condition.NEW
        assert self.full_product.adult == True
        assert self.full_product.multipack == 6
        assert self.full_product.is_bundle == True
        assert self.full_product.energy_efficiency_class == EnergyEfficiency.APP
        assert self.full_product.min_energy_efficiency_class == EnergyEfficiency.A
        assert self.full_product.max_energy_efficiency_class == EnergyEfficiency.APPP
        assert self.full_product.age_group == AgeGroup.KIDS
        assert self.full_product.color == ['red', 'pink']
        assert self.full_product.gender == Gender.UNISEX
        assert self.full_product.material == 'leather'
        assert self.full_product.pattern == 'striped'
        assert self.full_product.size == 'S'
        assert self.full_product.size_type == [SizeType.REGULAR, SizeType.PETITE]
        assert self.full_product.size_system == SizeSystem.US
        assert self.full_product.product_length == ('20', LenUnit.IN)
        assert self.full_product.product_width == ('20', LenUnit.CM)
        assert self.full_product.product_height == ('20', LenUnit.IN)
        assert self.full_product.product_weight == ('3.5', WeightUnit.LB)
        assert len(self.full_product.product_detail) == 4
        assert self.full_product.product_detail == [
            ProductDetail('General', 'Product Type', 'Digital player'),
            ProductDetail('General', 'Digital Player Type', 'Flash based'),
            ProductDetail('Display', 'Resolution', '432 x 240'),
            ProductDetail('Display', 'Diagonal Size', '2.5"'),
        ]
        assert self.full_product.product_hightlight == ['Supports thousands of apps']
        assert self.full_product.promotion_id == ['ABC123']
        assert self.full_product.excluded_destination == [Destination.SHOPPING_ADS, Destination.BUY_ON_GOOGLE_LISTINGS]
        assert self.full_product.included_destination == [Destination.DISPLAY_ADS, Destination.LOCAL_INVENTORY_ADS]
        assert self.full_product.shopping_ads_excluded_country == [countries_by_alpha2['US'], countries_by_alpha2['DE']]
        assert self.full_product.pause == Pause.ADS
        assert self.full_product.shipping == [Shipping(country=countries_by_alpha2['US'], service='Fedex', price=(Decimal('1.99'), Currency.usd))]
        assert self.full_product.shipping_label == 'Only Fedex'
        assert self.full_product.shipping_weight == ('3.5', WeightUnit.KG)
        assert self.full_product.shipping_length == ('20.5', LenUnit.IN)
        assert self.full_product.shipping_width == ('20', LenUnit.CM)
        assert self.full_product.shipping_height == ('20.5', LenUnit.IN)
        assert self.full_product.ships_from_country == countries_by_alpha2['US']
        assert self.full_product.tax == [Tax(country='US', region='CA', rate=Decimal('5.0'), tax_ship=True)]
