from UNODC_WebScrapper import searchPage

if __name__ == "__main__":
    searcher = searchPage.SearchPage()
    # urls = searcher.get_page_urls()
    urls = searcher.load_urls("./data/case_urls.csv")
    data = searcher.collect_data(urls)
    print(data)
