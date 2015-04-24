from util.excel_reader import get_excel_data
from booking.models import Company, Activity, TimeTable, Location
import re
from decimal import Decimal

class Init_DB(object):

    def __init__(self, resource_file):

        self.ac_list = get_excel_data(resource_file)
        self.parse_company = lambda string: re.match(r"(?P<company>.+)\s?(?P<website>https?://[\w\-\.]+[/|\s])(?P<comment>.*)?", string)

    def init_location(self):
        for item in self.ac_list:
            location = item['location']
            Location.objects.get_or_create(name=location)

    def init_company(self):
        company = None
        for item in self.ac_list:
            act_list = item['act_list']
            for act in act_list:
                print act['company']
                m = self.parse_company(act['company'])
                if m.group('company') != company:
                    company = m.group('company')
                    updated_values = {'website': m.group('website'),
                                    'comment': m.group('comment').strip()}
                    obj, created = Company.objects.update_or_create(name=company,
                                                                    defaults=updated_values)

    def init_activity(self):
        for item in self.ac_list:
            location = Location.objects.get(name=item['location'])
            for act in item['act_list']:
                deposit = False if act['pay_deposit_ad'] == '' else True
                m = self.parse_company(act['company'])
                company = Company.objects.get(name=m.group('company'))
                print act['activity']
                updated_values = {
                                'during_time': act['time'],
                                'web_adult': self.parse_decimal(act['web_adult']),
                                'web_child': self.parse_decimal(act['web_child']),
                                'KTL_adult': self.parse_decimal(act['KTL_adult']),
                                'KTL_child': self.parse_decimal(act['KTL_child']),
                                'deposit': deposit,
                                'deposit_adult': self.parse_decimal(act['pay_deposit_ad']),
                                'deposit_child': self.parse_decimal(act['pay_deposit_ch']),
                                'location': location,
                                'company': company
                                }
                Activity.objects.update_or_create(name=act['activity'], during_time=act['time'],
                                                  defaults=updated_values)

    def parse_decimal(self, x):
        try:
            return Decimal(x)
        except:
            print x
            return Decimal('0.00')



