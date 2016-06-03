from gluon import current


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
