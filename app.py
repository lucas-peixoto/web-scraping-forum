from datetime import datetime
from core import load_subcategories

start_time = datetime.now()
subcategories = load_subcategories()
end_time = datetime.now()
print('Duração: {}'.format(end_time - start_time))
