from decimal import Decimal
from gettext import install
from operator import is_
from faker import Faker
from pydantic import HttpUrl
from iso4217 import Currency

from product_feed.model import GoogleProduct
from product_feed.model.google import Availability

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
        size_type='regular',
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

        print(self.full_product.tax)

