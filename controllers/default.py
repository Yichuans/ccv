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

    from ccv import get_hlu_by_wdpaid

    # get params
    wdpaid = request.args[0]

    taxon_dict = request.get_vars
    # if query string
    if taxon_dict.has_key('taxon'):
        taxon = taxon_dict['taxon']

        try:
            row = get_hlu_by_wdpaid(wdpaid, taxon)
            return dict(row=row)

        except Exception as e:
            return dict(e=e)

    else:
        return 'Query string should be taxon={amp|bird|coral}; got ' + ';'.join(taxon_dict.keys())
        

def site():
    wdpaid = request.args[0]
    return dict(wdpaid)