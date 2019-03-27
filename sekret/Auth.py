from controller.DB import Poswiadczenia
sekretneDane = {'db':'nbp', 'host': 'localhost'}
poswiadczeniaTestAdmin = Poswiadczenia(user='admin_test_NBP', haslo='admin_test_378th21', zaszyfrowaneHaslo=False)
poswiadczeniaTestUser = Poswiadczenia(user='user_test_NBP', haslo='user_test_7fr53', zaszyfrowaneHaslo=False)
