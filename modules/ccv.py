from gluon import current
from gluon.html import *

# def get_hlu_by_wdpaid(wdpaid, taxon, target_field='FINAL_SCORE'):
# 	# it cannot be global
# 	db = current.db

# 	if taxon not in ['amp', 'bird', 'coral']:
# 		raise Exception('taxon: {}, not in amp, bird and coral'.format(taxon))

# 	agg_table = 'agg_' + taxon

# 	# for wh and category
# 	# whereclause = (db[agg_table].wdpaid == wdpaid) & (db[agg_table].category.upper() == target_field.upper())
# 	whereclause = (db[agg_table].wdpaid == wdpaid) & (db[agg_table].category == target_field)

# 	# there should only be one row. this could be empty
# 	record = db(whereclause).select().first()

# 	if record:
# 		return record.as_dict()
# 	return None
sle_components = ['SENSITIVITY','LOW_ADAPTABILITY','EXPOSURE']


def get_hlu_by_wdpaid(wdpaid, taxon):
	# it cannot be global
	db = current.db

	if taxon not in ['amp', 'bird', 'coral']:
		raise Exception('taxon: {}, not in amp, bird and coral'.format(taxon))

	agg_table = 'agg_' + taxon

	# for wh and category
	# whereclause = (db[agg_table].wdpaid == wdpaid) & (db[agg_table].category.upper() == target_field.upper())
	whereclause = (db[agg_table].wdpaid == wdpaid) 

	# there should only be one row. this could be empty
	records = db(whereclause).select()

	result = {record.category: {'H': record.H, 'L': record.L, 'U': record.U, 'per_H': record.per_H} for record in records}

	return result


def get_wh_species_by_wdpaid(wdpaid, taxon):
	db = current.db

	if taxon not in ['amp', 'bird', 'coral']:
		raise Exception('taxon: {}, not in amp, bird and coral'.format(taxon))

	species_table = 'wh_' + taxon
	whereclause = (db[species_table].wdpaid == wdpaid) 

	# there should only be one row. this could be empty
	records = db(whereclause).select()

	return records

def gen_div_taxon(wdpaid, taxon):
	div_list = []

	records = get_hlu_by_wdpaid(wdpaid, taxon)

	if not records:
		return DIV(_class=taxon)

	keys = records.keys()

	def gen_div_com(com_key, _class):
		""" sort each component to

		<div> 
		<h2>name</h2>
		<h3>High</h3><p>xxxx</p>
		<h3>Low</h3><p>xxxx<p>
		...

		</div>

		# COM_KEY: e.g. FINAL_SCORE
		"""
		return DIV(H2(com_key), H3('High'), P(records[com_key]['H']),
			H3('Low'), P(records[com_key]['L']),
			H3('Unknown'), P(records[com_key]['U']),
			H3('Percentage of those highly vulnerable'), P(records[com_key]['per_H']), _class=_class)

	# final 
	final_div = gen_div_com('FINAL_SCORE', 'final')

	# separate aggregate
	sle_div_list = [gen_div_com(component, 'sle') for component in sle_components]

	div_list.append(final_div)
	div_list.extend(sle_div_list)

	# remove those already generated
	keys.remove('FINAL_SCORE')
	for component in sle_components:
		keys.remove(component)

	# add the rest
	keys.sort()
	for key in keys:
		div_list.append(gen_div_com(key, 'other'))

	return DIV(*div_list, _class=taxon)




