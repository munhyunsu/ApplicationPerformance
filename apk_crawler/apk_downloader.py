from selenium import webdriver


class APKDownloader(object):
    def __init__(self, driver, data_path):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {
            'download.default_directory': data_path,
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True})
        self.driver = webdriver.Chrome(driver, chrome_options=options)
        self.driver.set_window_size(1366, 768)

    def download_apk(self, package):
        search_url = 'http://apkpure.com/search?q={0}'.format(package)
        self.driver.get(search_url)
        self.driver.implicitly_wait(10)

        try:
            search_title = self.driver.find_element_by_class_name('search-title')
            a_tag = search_title.find_element_by_tag_name('a')
            apk_page = a_tag.get_attribute('href')
        except selenium.common.exceptions.NoSuchElementException:
            return None

        self.driver.get(apk_page)
        self.driver.implicitly_wait(10)

        try:
            download_button = self.driver.find_element_by_class_name('da')
            apk_link = download_button.get_arrtibute('href')
        except selenium.common.exceptions.NoSuchElementException:
            return None

        
