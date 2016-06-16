# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

# def test():
#     records = db(db.agg_bird.wdpaid==191).select().first()
#     return dict(record = records)

def hlu():
    # meant to be called via ajax 
    # ===========
    # such as: hlu.json/5004?taxon=amp
    # ===========

    from ccv import get_hlu_by_wdpaid_mk2
    import json

    args = request.args

    # /hlu/<wdpaid>
    if args:
        wdpaid = args[0]

        taxon_dict = request.get_vars

        if not taxon_dict:
            return "meant to be called: hlu.json/5004?taxon=amp"

        # /hlu/<wdpaid>?taxon=<amp>
        if taxon_dict.has_key('taxon'):
            taxon = taxon_dict['taxon']

            try:
                row = get_hlu_by_wdpaid_mk2(wdpaid, taxon)
                # return dict(row=row)
                return json.dumps(row)

            except Exception as e:
                return dict(e=e)

        else:
            return 'Query string should be taxon={amp|bird|coral}; got ' + ';'.join(taxon_dict.keys())
    
    # /hlu/
    else:
        return "meant to be called: hlu.json/5004?taxon=amp"

def sle():
    """exposure, sensitivity and low adaptability
    meant to be called: esl.json/5004?taxon=amp
    constructed specifically for d3js for radar-chart"""
    from ccv import get_hlu_by_wdpaid, sle_components
    import json

    args = request.args
    taxon_dict = request.get_vars

    if args and taxon_dict.has_key('taxon'):
        wdpaid = args[0]
        taxon = taxon_dict['taxon']

        # construct dict for output
        row = get_hlu_by_wdpaid(wdpaid, taxon)

        # if there is data
        if row:
            # Sensitivity, Low-adapt and exposure
            sle_total = [dict(axis=component, value=row[component]['H'] + row[component]['L'] + row[component]['U']) for component in sle_components]
            axes_total = dict(className='Total', axes=sle_total)

            sle_h = [dict(axis=component, value=row[component]['H']) for component in sle_components]
            axes_h = dict(className='High', axes=sle_h)

            result = [axes_h, axes_total]

            # return dict(data=result)
            
            return json.dumps(result)

        # if there is no data
        return json.dumps([])

    else:
        return None

# def site():
#     from ccv import gen_div_taxon
#     args = request.args

#     if args:
#         wdpaid = args[0]

#         return dict(wdpaid=wdpaid)

#         # needs to check if wdpaid is a valid WH site

#         # return dict(wdpaid=wdpaid, 
#         #     amp=gen_div_taxon(wdpaid, 'amp'), 
#         #     bird=gen_div_taxon(wdpaid, 'bird'),
#         #     coral=gen_div_taxon(wdpaid, 'coral'))
#     else:
#         return dict(wdpaid=0)

def site():
    from ccv import get_cv_label

    args = request.args

    if args:
        wdpaid = args[0]
        amp, bird, coral = get_cv_label(wdpaid)
        return dict(amp_label=amp, bird_label=bird, coral_label=coral)

    else:
        return None

def test_spider_chart():
    return dict()