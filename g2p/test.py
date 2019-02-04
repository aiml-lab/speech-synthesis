# encoding: utf-8

import re

from g2p import delete_schwa

test_data_file = open('data/abc.txt', 'rb')
test_data = test_data_file.read().decode('utf-8')

clean_test_data = re.split('[-।,?;.:]|\s', test_data)

write_data = ''

for word in clean_test_data:
    if word != '':
        write_data = write_data + word + ' : ' + str(delete_schwa(word)) + '\n'

write_file = open('data/g2p_output.txt', 'wb')
write_file.write(write_data.encode())

write_file.close()
test_data_file.close()
