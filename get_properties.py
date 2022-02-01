#!/usr/bin/env python
from oauth import authorize_creds, execute_request
import argparse
import httplib2
import requests

from collections import defaultdict
# from dateutil import relativedelta
from googleapiclient.discovery import build
from oauth2client import client
from oauth2client import file
from oauth2client import tools

def get_property_list(webmasters_service):
    '''
    Get a list of validated properties from GSC
    '''
    site_list = webmasters_service.sites().list().execute()

    # Filter for verified websites
    verified_sites_urls = [s['siteUrl'] for s in site_list['siteEntry']
                           if s['permissionLevel'] != 'siteUnverifiedUser'
                           and s['siteUrl'][:4] == 'http']
    return verified_sites_urls


if __name__ == '__main__':
    creds = 'client_secrets.json'
    webmasters_service = authorize_creds(creds)
    verified_sites_urls = get_property_list(webmasters_service)