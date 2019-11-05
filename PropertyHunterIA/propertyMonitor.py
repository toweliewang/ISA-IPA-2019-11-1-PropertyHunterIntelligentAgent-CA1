import tagui as t
import pandas as pd
from pandas import DataFrame
from propertySearcher_util import *
from threading import Timer


def propertydata(project_name):

    t.close()
    t.init()
    project_url = f'https://www.propertyguru.com.sg/property-for-sale?market=residential&freetext={project_name}&newProject=all'
    t.url(project_url)
    wait_for_pageload('//div[@class="header-wrapper"]')
    num_result_ad = 3

    # load main page, get detail page url link
    url = [''] * num_result_ad
    for n in [x for x in range(1, num_result_ad + 1) if x != 4 and x != 8]:  # skip 4th and 8th advertisement
        wait_for_pageload(
            f'(//div[@class="listing-widget-new"]/div[{n}]/div[1]/div[2]/div[1]/div[1]/h3/a/@href)')
        url[n - 1] = read_if_present(
            f'(//div[@class="listing-widget-new"]/div[{n}]/div[1]/div[2]/div[1]/div[1]/h3/a/@href)')
        print(f"{n}. url = " + url[n - 1])

    property_title = [''] * num_result_ad
    id = [''] * num_result_ad
    pdf = [''] * num_result_ad
    pdf_link = [''] * num_result_ad

    for n in [x for x in range(1, num_result_ad + 1) if x != 4 and x != 8]:
        t.url("https://www.propertyguru.com.sg" + url[n - 1])

        wait_for_pageload(
            '//h1[@class="h2"]')

        property_title[n - 1] = read_if_present(
            '//h1[@class="h2"]')
        print(f"{n}. property_title = " + property_title[n - 1])

        id[n - 1] = read_if_present(
            '//*[@id="details"]/div/div[1]/div[2]/div[10]/div/div[2]')
        print(f"{n}. id = " + id[n - 1])

        pdf[n - 1] = read_if_present(
            '//*[@id="sticky-right-col"]/div[3]/a[2]/@href')
        pdf_link[n - 1] = 'https://www.propertyguru.com.sg' + pdf[n - 1]
        print(f"{n}. pdf_link = " + pdf_link[n - 1])



    property_info = {'property_title': property_title,
                     'url': ['https://www.propertyguru.com.sg' + x for x in url],
                     'id': id,
                     'pdf_link': pdf_link,
                     }

    df = DataFrame(property_info, columns=['property_title', 'id', 'url', 'pdf_link'])
    df.to_excel('Property Monitor.xlsx', encoding='utf8', index=None)
    print('======== Property Monitor.xlsx saved ==========')
    print(f'======== Monitoring every {interval} second ==========')

def propertydata_update(project_name):

    df1 = pd.read_excel('Property Monitor.xlsx')

    t.close()
    t.init()
    project_url = f'https://www.propertyguru.com.sg/property-for-sale?market=residential&freetext={project_name}&newProject=all'
    print(project_url)
    t.url(project_url)
    wait_for_pageload('//div[@class="header-wrapper"]')
    num_result_ad = 3

    # load main page, get detail page url link
    url = [''] * num_result_ad
    id = [''] * num_result_ad

    for n in [x for x in range(1, num_result_ad + 1) if x != 4 and x != 8]:  # skip 4th and 8th advertisement
        wait_for_pageload(
            f'(//div[@class="listing-widget-new"]/div[{n}]/div[1]/div[2]/div[1]/div[1]/h3/a/@href)')
        url[n - 1] = read_if_present(
            f'(//div[@class="listing-widget-new"]/div[{n}]/div[1]/div[2]/div[1]/div[1]/h3/a/@href)')
        print(f"{n}. url = " + url[n - 1])
        id[n - 1] = read_if_present(
            f'(//*[@id="wrapper-inner"]/section[1]/div[2]/div[1]/div[2]/div[2]/section/div[2]/div[{n}]/@data-listing-id)')

    print(f'searching: {id}')  # ['22036842', '21725956', '20648962']
    id_int = list(df1['id'])
    id_str = list()
    for n in id_int:
        id_str.append(str(n))
    print(id_str)

    new_url = list()
    for n in id:
        if n not in id_str:
            print(f'new property found: {n}')
            u = f"https://www.propertyguru.com.sg/listing/{n}/for-sale-{project_name}"
            new_url.append(u)
    if new_url == []:
        return print(f'======== no new property found! ==========')

    print(f'======== new property found==========')
    property_title = [''] * len(new_url)
    pdf = [''] * len(new_url)
    pdf_link = [''] * len(new_url)

    for (n,i) in zip(new_url,range(1,len(new_url)+1)):
        t.url(n)
        wait_for_pageload(
            '//h1[@class="h2"]')
        property_title[i - 1] = read_if_present(
            '//h1[@class="h2"]')
        print(f"{i}. property_title = " + property_title[i - 1])
        pdf[i - 1] = read_if_present(
            '//*[@id="sticky-right-col"]/div[3]/a[2]/@href')
        pdf_link[i - 1] = 'https://www.propertyguru.com.sg' + pdf[i - 1]
        print(f"{i}. pdf_link = " + pdf_link[i - 1])

    property_info = {'property_title': property_title,
                     'url': ['https://www.propertyguru.com.sg' + x for x in url],
                     'id': id,
                     'pdf_link': pdf_link,
                     }
    df2= DataFrame(property_info, columns=['property_title', 'id', 'url', 'pdf_link'])

    new_df = pd.concat([df1,df2])
    new_df.to_excel('Property Monitor.xlsx', encoding='utf8', index=None)
    print('======== Property Monitor.xlsx update ==========')

    pdf_filename = download_pdf(property_title, pdf_link, id)
    mail_subscription(input_email, input_name, pdf_filename)


if __name__ == "__main__":


    # input from chatbot
    df = pd.read_csv('user_appointment_detail.csv')
    input_email = df['Email'][0]
    print(input_email)
    input_name = df['Client Name'][0]
    print(input_name)
    project_name = df['Project Name'][0]
    print(project_name)
    interval = 60                      # 60 second searching interval

    # first run, get Property Monitor.xlsx database
    propertydata(project_name)

    # loop
    def scheduler():
        propertydata_update(project_name)        # for real case
        # propertydata_update('seaside residences') # for demo
        print(f'======== Monitoring every {interval} second ==========')
        Timer(interval, scheduler).start()

    schedule = Timer(interval, scheduler)
    schedule.start()
