# main
import tagui as t
# import pandas as pd
from pandas import DataFrame
from propertySearcher_util import *

def get_property(input_email, input_name, prefer1, prefer2, prefer3,input_loc, input_size, input_price, input_bed, input_floor):
	"""
	:param input_email: user email
	:param input_name: user name
	:param prefer1:
	:param prefer2:
	:param prefer3:
	:param input_loc: location name input_loc = ['Orchard', 'River Valley','Eunos']
	:param input_size: square feet
	:param input_price:
	:param input_bed:
	:param input_floor:
	:return:
	"""
	# chatbot input
	input_area = list()
	if input_loc in ['Cecil' , 'Raffles Place' , 'Marina']:
		input_area.append('D01')
	elif input_loc in ['Chinatown' , 'Tanjong Pagar']:
		input_area.append('D02')
	elif input_loc in ['Alexandra' , 'Queenstown', 'Tiong Bahru']:
		input_area.append('D03')
	elif input_loc in ['Harbourfront' , 'Telok Blangah', 'Mount Faber']:
		input_area.append('D04')
	elif input_loc in ['Buona Vista' , 'Pasir Panjang' , 'Clementi']:
		input_area.append('D05')
	elif input_loc in ['City Hall' , 'Clarke Quay']:
		input_area.append('D06')
	elif input_loc in ['Beach Road' , 'Bugis' , 'Golden Mile']:
		input_area.append('D07')
	elif input_loc in ['Farrer Park' , 'Little India']:
		input_area.append('D08')
	elif input_loc in ['Orchard' , 'River Valley']:
		input_area.append('D09')
	elif input_loc in ['Balmoral' , 'Holland' , 'Bukit Timah']:
		input_area.append('D10')
	elif input_loc in ['Newton' , 'Novena', 'Thomson']:
		input_area.append('D11')
	elif input_loc in ['Balestier' , 'Toa Payoh', 'Serangoon']:
		input_area.append('D12')
	elif input_loc in ['Macpherson' , 'Braddell']:
		input_area.append('D13')
	elif input_loc in ['Sims' , 'Geylang' , 'Paya Lebar']:
		input_area.append('D14')
	elif input_loc in ['Joo Chiat' , 'Marine Parade', 'Katong']:
		input_area.append('D15')
	elif input_loc in ['Bedok' , 'Upper East Coast', 'Siglap']:
		input_area.append('D16')
	elif input_loc in ['Flora' , 'Changi', 'Loyang']:
		input_area.append('D17')
	elif input_loc in ['Pasir Ris' , 'Tampines']:
		input_area.append('D18')
	elif input_loc in ['Serangoon Gardens' , 'Punggol' , 'Sengkang']:
		input_area.append('D19')
	elif input_loc in ['Ang Mo Kio' , 'Bishan' , 'Thomson']:
		input_area.append('D20')
	elif input_loc in ['Clementi Park' , 'Upper Bukit Timah', 'Ulu Pandan']:
		input_area.append('D21')
	elif input_loc in ['Boon Lay' , 'Jurong', 'Tuas']:
		input_area.append('D22')
	elif input_loc in ['Dairy Farm' , 'Bukit Panjang' , 'Choa Chu Kang', 'Hillview', 'Bukit Batok']:
		input_area.append('D23')
	elif input_loc in ['Lim Chu Kang' , 'Tengah', 'Kranji']:
		input_area.append('D24')
	elif input_loc in ['Admiralty' , 'Woodlands']:
		input_area.append('D25')
	elif input_loc in ['Mandai' , 'Upper Thomson']:
		input_area.append('D26')
	elif input_loc in ['Sembawang' , 'Yishun']:
		input_area.append('D27')
	elif input_loc in ['Seletar' , 'Yio Chu Kang']:
		input_area.append('D28')
	print(input_area)

	input_type = ['condo']  # HDB, condo, landed (only single choice is supported in propertyguru)
	input_minsize = [str(input_size*0.8)]  # square feet   @ modified
	input_maxsize = [str(input_size*1.2)]  # square feet   @ modified
	input_minprice = [str(input_price*0.5)]  # $    @ modified
	input_maxprice = [str(input_price*1.5)]  # $    @ modified
	input_bed = [str(input_bed)]  # 0 to 5 bedroom, 0 stands for studio,  @
	input_floor = [str(input_floor)]  # ground, low, mid, high, penthouse (only single choice is supported in propertyguru   @

	# url transfer
	def url_area():
		url_area = ''
		for n in input_area:
			url_area += f'district_code%5B%5D={n}&'
		return url_area

	def url_type():
		if 'HDB' in input_type:
			url_type = 'property_type=H&'
		if 'condo' in input_type:
			url_type = 'property_type=N&'
		if 'landed' in input_type:
			url_type = 'property_type=L&'
		return url_type

	def url_minsize():
		url_minsize = ''.join(input_minsize)
		return f'minsize={url_minsize}&'

	def url_maxsize():
		url_maxsize = ''.join(input_maxsize)
		return f'maxsize={url_maxsize}&'

	def url_minprice():
		url_minprice = ''.join(input_minprice)
		return f'minprice={url_minprice}&'

	def url_maxprice():
		url_maxprice = ''.join(input_maxprice)
		return f'maxprice={url_maxprice}&'

	def url_bed():
		url_bed = ''
		for n in input_bed:
			url_bed += f'beds%5B%5D={n}&'
		return url_bed

	def url_floor():
		url_floor = ''
		if 'ground' in input_floor:
			url_floor = 'floor_level=GND&'
		if 'low' in input_floor:
			url_floor = 'floor_level=LOW&'
		if 'mid' in input_floor:
			url_floor = 'floor_level=MID&'
		if 'high' in input_floor:
			url_floor = 'floor_level=HIGH&'
		if 'penthouse' in input_floor:
			url_floor = 'floor_level=PENT&'
		return url_floor

	url_main = f'https://www.propertyguru.com.sg/property-for-sale?market=residential&{url_type()}{url_area()}{url_minprice()}{url_maxprice()}{url_bed()}{url_minsize()}{url_maxsize()}{url_floor()}newProject=all'
	print('main page url link: ' + url_main)

	# tagui scrape
	t.init()
	t.url(url_main)
	result = wait_for_mainpageload('//div[@class="header-wrapper"]')
	if result ==0:
		print(' no result found')
		mail_notfound(input_email, input_name, input_loc, input_size, input_price, input_bed, input_floor)
		# restart BuyerAgent.py
		python = sys.executable
		os.execl(python, python, *sys.argv)
	num_result = t.count('//div[@class="header-wrapper"]')
	num_result_ad = num_result + 2
	# num_result_ad = 6  # for test
	print("num of property in this page without ad = ", num_result)
	print("num of property in this page including ad = ", num_result_ad)

	# load main page, get detail page url link
	url = [''] * num_result_ad
	for n in [x for x in range(1, num_result_ad + 1) if x != 4 and x != 8]:  # skip 4th and 8th advertisement
		wait_for_pageload(
			f'(//div[@class="listing-widget-new"]/div[{n}]/div[1]/div[2]/div[1]/div[1]/h3/a/@href)')
		url[n - 1] = read_if_present(
			f'(//div[@class="listing-widget-new"]/div[{n}]/div[1]/div[2]/div[1]/div[1]/h3/a/@href)')
		print(f"{n}. url = " + url[n - 1])

	# load detail page
	property_title = [''] * num_result_ad
	type = [''] * num_result_ad
	area = [''] * num_result_ad
	bedroom = [''] * num_result_ad
	bathroom = [''] * num_result_ad
	price = [''] * num_result_ad
	total = [''] * num_result_ad
	address = [''] * num_result_ad
	postcode = [''] * num_result_ad
	region = [''] * num_result_ad
	floor = [''] * num_result_ad
	furnish = [''] * num_result_ad
	description = [''] * num_result_ad
	feature = [''] * num_result_ad
	image1 = [''] * num_result_ad
	image2 = [''] * num_result_ad
	image3 = [''] * num_result_ad
	id = [''] * num_result_ad
	pdf = [''] * num_result_ad
	pdf_link = [''] * num_result_ad

	for n in [x for x in range(1, num_result_ad + 1) if x != 4 and x != 8]:

		t.url("https://www.propertyguru.com.sg"+url[n-1])
		wait_for_pageload(
		'//h1[@class="h2"]')
		property_title[n - 1] = read_if_present(
		'//h1[@class="h2"]')
		print(f"{n}. property_title = " + property_title[n - 1])
		type[n - 1] = read_if_present(
		'//*[@id="condo-profile"]/div/div/div/div/div[1]/div/div/div[1]/div/div[2]')
		print(f"{n}. type = " + type[n - 1])
		area[n - 1] = read_if_present(
		'//*[@id="details"]/div/div[1]/div[2]/div[3]/div/div[2]')
		print(f"{n}. area = " + area[n - 1])
		bedroom[n - 1] = read_if_present(
		'//*[@id="overview"]/div/div/div/section/div[1]/div[2]/div[1]/span')
		print(f"{n}. bedroom = " + bedroom[n - 1])
		bathroom[n - 1] = read_if_present(
		'//*[@id="overview"]/div/div/div/section/div[1]/div[2]/div[2]/span')
		print(f"{n}. bathroom = " + bathroom[n - 1])
		total[n - 1] = read_if_present(
		'//*[@id="overview"]/div/div/div/section/div[1]/div[1]/div[1]/span[2]')
		print(f"{n}. total price = " + total[n - 1])
		price[n - 1] = read_if_present(
		'//*[@id="overview"]/div/div/div/section/div[1]/div[2]/div[4]/div/span[2]')
		print(f"{n}. price = " + price[n - 1])
		address[n - 1] = read_if_present(
		'//*[@id="overview"]/div/div/div/section/div[1]/div[3]/div/div[2]/div[1]/span[1]')
		print(f"{n}. address = " + address[n - 1])
		postcode[n - 1] = read_if_present(
		'//*[@id="overview"]/div/div/div/section/div[1]/div[3]/div/div[2]/div[1]/span[2]')
		print(f"{n}. postalcode = " + postcode[n - 1])
		region[n - 1] = read_if_present(
		'//*[@id="overview"]/div/div/div/section/div[1]/div[3]/div/div[2]/div[1]/span[3]')
		print(f"{n}. region = " + region[n - 1])
		floor[n - 1] = read_if_present(
		'//*[@id="details"]/div/div[1]/div[2]/div[9]/div/div[2]')
		print(f"{n}. floor = " + floor[n - 1])
		furnish[n - 1] = read_if_present(
		'//*[@id="details"]/div/div[1]/div[2]/div[7]/div/div[2]')
		print(f"{n}. furnish = " + furnish[n - 1])
		description[n - 1] = read_if_present(
			'//*[@id="details"]/div/div[2]')
		print(f"{n}. description = " + description[n - 1])
		feature[n - 1] = read_if_present(
			'//*[@id="facilities"]')
		print(f"{n}. feature = " + feature[n - 1])
		image1[n - 1] = read_if_present(
			'//*[@id="carousel-photos"]/div[2]/div/div[1]/span/img/@src')
		print(f"{n}. image1 = " + image1[n - 1])
		image2[n - 1] = read_if_present(
			'//*[@id="carousel-photos"]/div[2]/div/div[2]/span/img/@src')
		print(f"{n}. image2 = " + image2[n - 1])
		image3[n - 1] = read_if_present(
			'//*[@id="carousel-photos"]/div[2]/div/div[3]/span/img/@src')
		print(f"{n}. image3 = " + image3[n - 1])
		pdf[n - 1] = read_if_present(
			'//*[@id="sticky-right-col"]/div[3]/a[2]/@href')
		pdf_link[n - 1] = 'https://www.propertyguru.com.sg' + pdf[n - 1]
		print(f"{n}. pdf_link = " + pdf_link[n - 1])
		id[n - 1] = read_if_present(
			'//*[@id="details"]/div/div[1]/div[2]/div[10]/div/div[2]')
		print(f"{n}. id = " + id[n - 1])

	property_info = {'property_title': property_title,
					 'url': ['https://www.propertyguru.com.sg'+x for x in url],
					 'type': type,
					 'area': area,
					 'total price': total,
					 'price': price,
					 'bedroom': bedroom,
					 'bathroom': bathroom,
					 'address': address,
					 'postcode': postcode,
					 'region': region,
					 'floor': floor,
					 'furnish': furnish,
					 'description': description,
					 'feature': feature,
					'image1': image1,
					'image2': image2,
					'image3': image3,
					'id': id,
					'pdf_link': pdf_link,
					 }

	df = DataFrame(property_info, columns=[ 'property_title',
										    'id',
										    'pdf_link',
											'type',
											'area',
											'total price',
											'price',
											'bedroom',
											'bathroom',
											'address',
											'postcode',
											'region',
											'floor',
											'furnish',
											'description',
											'feature',
											'url',
											'image1',
											'image2',
											'image3'
											])

	df.to_excel('property_info.xlsx', encoding='utf8', index=None)
	print('======== property_info.xlsx saved ==========')


	# from propertySearcher_util import download_image
	download_image(id, image1, image2, image3)

	# from propertySearcher_util import classify_image
	filtered_id, filtered_cluster = classify_image(df, prefer1, prefer2, prefer3)

	print(df)
	# generate image filtered df, sorted by filtered_id
	filtered_df = df[df['id'].isin(filtered_id)]
	# write image cluster column into df
	filtered_df['image'] = filtered_cluster
	print(filtered_df)
	# save to excel
	filtered_df.to_excel('property_info_image.xlsx', encoding='utf8', index=None)

	print('======== generate data for pdf downloader ==========')
	property_title = filtered_df['property_title']  # filtered_df = pd.read_excel('property_info_filtered.xlsx')
	print(list(property_title))
	pdf_link = filtered_df['pdf_link']
	print(list(pdf_link))
	pdf_id = filtered_df['id']
	print(list(pdf_id))

	# from propertySearcher_util import download_pdf
	pdf_filename = download_pdf(property_title, pdf_link,pdf_id)  #  pdf_filename =  property_title + pdf_id, pdf_filename for email attachment

	# from propertySearcher_util import classify_text
	features_selected = classify_text(filtered_df, 3, 6)
	# edit dataframe
	filtered_df['Key Features'] = features_selected
	filtered_df = filtered_df.drop(columns=['pdf_link', 'description', 'feature', 'image1','image2', 'image3'])
	# save to excel
	filtered_df.to_excel('Property_info_text.xlsx', encoding='utf8', index=None)

	# from propertySearcher_util import edit_excel
	edit_excel('Property_info_text.xlsx')
	print('============ excel saved ============')

	# from propertySearcher_util import mail_shortlist
	mail_shortlist(input_email, input_name, pdf_filename)




