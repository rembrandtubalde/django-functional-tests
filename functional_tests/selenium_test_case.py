from djangosanetesting.cases import SeleniumTestCase
from django.core.management import call_command
from django.core.cache import cache
import time
try:
    from celery.task.control import discard_all
except:
    pass

class DjangoFunctionalSeleniumTestCase(SeleniumTestCase):
    # selenium_fixtures = []
    
    def setUp(self, *args, **kwargs):
        self.verificationErrors = []

    def tearDown(self, *args, **kwargs):
        if hasattr(self,"verificationErrors"):
            self.assertEqual([], self.verificationErrors)

    def js_refresh(self):
        sel = self.selenium
        sel.get_eval("this.browserbot.getUserWindow().location.href")
        sel.get_eval("this.browserbot.getUserWindow().location.href=window.location.href;")
        time.sleep(4)

    def click_and_wait(self, link):
        sel = self.selenium
        sel.click(link)
        sel.wait_for_page_to_load("30000")
    
    def close(self):
        sel = self.selenium
        sel.get_eval("this.browserbot.getUserWindow().close()")
        try:
            sel.get_confirmation()
        except:
            pass

class DjangoFunctionalConservativeSeleniumTestCase(DjangoFunctionalSeleniumTestCase):


    def tearDown(self, *args, **kwargs):
        try:
            discard_all()
        except:
            pass
        super(DjangoFunctionalConservativeSeleniumTestCase,self).tearDown(*args, **kwargs)
        call_command('flush', interactive=False)
        cache.clear()
        


class DjangoFunctionalUnitTestMixin(object):

    def assertEqualQuerySets(self, q1, q2):
        self.assertEqual(list(q1),list(q2))


class DjangoFunctionalConservativeUnitTestMixin(DjangoFunctionalUnitTestMixin):
    def tearDown(self, *args, **kwargs):
        try:
            discard_all()
        except:
            pass
        super(DjangoFunctionalConservativeUnitTestMixin,self).tearDown(*args, **kwargs)
        call_command('flush', interactive=False)
        cache.clear()