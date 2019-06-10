from selenium import webdriver
import unittest
import random

class CalculatorTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(4)
        self.base_url = "https://www.desmos.com"

    def test_calculator(self):
        expected_page_title = "Desmos | Scientific Calculator"
        num1 = random.randrange(0, 10)
        num2 = random.randrange(0, 10)
        operators = ("Plus", "Minus", "Divide", "Times")
        test_operator = random.choice(operators)

        if test_operator == "Plus":
            expected_result = str(num1 + num2)
        elif test_operator == "Minus":
            expected_result = str(num1 - num2)
        elif test_operator == "Times":
            expected_result = str(num1 * num2)
        else:
            if num2 == 0:
                expected_result = "undefined"
            else:
                expected_result = str(num1 / num2)
                # below covering float rounding by Calc. float results
                # applicable, if number < 10 are used in calculation
                # otherwise need to parse length after period and add to the statement
                if len(expected_result) > 10:
                    x = round(float(expected_result), 10)
                    expected_result = str(x)
                elif len(expected_result) == 3:
                    x = round(float(expected_result))
                    expected_result = str(x)
                # or modify this iteration with: num1 % num2 == 0: do
                else:
                    pass


        driver = self.driver
        driver.get(self.base_url + "/scientific")
        # assert driver.title == ""
        actual_page_title = driver.title
        self.assertEqual(expected_page_title, actual_page_title,
                         "Expected the title of the page {0} to be {1}, but was {2} instead".format(driver.current_url,
                                                                                                    expected_page_title,
                                                                                                    actual_page_title))


        driver.find_element_by_css_selector("span[aria-label = '" + str(num1) + "']").click()
        driver.find_element_by_css_selector("span[aria-label = '" + test_operator + "']").click()
        driver.find_element_by_css_selector("span[aria-label = '" + str(num2) + "']").click()
        driver.find_element_by_css_selector("span[aria-label = 'Enter']").click()



        actual_result = driver.find_elements_by_xpath("//*[@id='main']//div[1]/div[2]/div[1]/div[5]/div[2]/div[1]/span[2]/span[position()>1]")
        value = ""
        for a_r in actual_result:
            a_r = a_r.text
            value = value + str(a_r)


        self.assertEqual(value, expected_result)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
