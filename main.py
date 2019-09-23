from ceneo import ceneo
from datetime import datetime

start = datetime.now()
print('start')
ceneo.findAllPaginationLinks('/Maszyny_do_szycia', 'Maszyny_do_szycia')

for page in ceneo.CeneoPaginationLink.page_urls:
    ceneo.findAllProducts(page)
i = 1
for item in ceneo.Product.product_list:
    data = ceneo.getInfoFromProductCard(item.ceneo_number, item.product_code)
    with open('data.csv', 'a+') as file:
        for line in data:
            file.write(line)
    print('{} loop done'.format(i))
    i += 1


end = datetime.now()
print('Job was finished after {}'.format(end-start))