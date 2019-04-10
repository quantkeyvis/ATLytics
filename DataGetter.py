from UNODC_WebScrapper import searchPage

if __name__ == "__main__":
    searcher = searchPage.SearchPage()
    # urls = searcher.get_page_urls()
    # with open("./all_urls.csv", "w") as f:
    #     for url in urls:
    #         f.write(url[0])
    #         f.write("\n")
    urls = searcher.load_urls("./all_urls.csv")
    data, new_urls = searcher.collect_data(urls)
    with open("./all_urls_fixed.csv", "w") as f:
        for url in new_urls:
            f.write(url)
            f.write("\n")
    print(data)
    data.to_csv("./unodc_export_full.csv", index=False)
    data.to_pickle("./unodc_export_full.pkl")
