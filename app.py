import arcgis
import csv
import time
import pandas as pd
import click
from arcgis.features import FeatureLayerCollection
from tqdm import tqdm

@click.command()
@click.argument('fs_url')
@click.option('--waittime', default=-1.0,
            help='Wait time to call get attachment api for a specific feature object Id')
@click.argument('output', type=click.File('w'),default='-',required=False)
def cli(fs_url,output,waittime):
    """Process the Fire Structure Damage ESRI Feature Service to generate CSV file with location, structure status and attachments Web URLs"""
  # fs_url = 'https://services1.arcgis.com/jUJYIo9tSA7EHvfZ/ArcGIS/rest/services/Camp2018_DINS_Public_View_Pictures/FeatureServer'
    flc = FeatureLayerCollection(fs_url)
    fl = flc.layers[0]
    rs = fl.query(where='1=1')
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['id','damage','structuretype','Y','X','weburl'])
    for feature in tqdm(rs.features):
        aId = None
        aUrl = None
        objId = feature.attributes['OBJECTID']
        attachs = fl.attachments.get_list(objId)
        if (len(attachs) > 0):
            aId = attachs[0]['id']
            aUrl = fs_url + '/0/' + str(objId) + '/attachments/' + str(aId)
        tup =feature.attributes['OBJECTID'],feature.attributes['DAMAGE'],feature.attributes['STRUCTURETYPE'],feature.geometry['y'],feature.geometry['x'],aUrl
        if (waittime > 0):
            time.sleep(waittime)
        writer.writerow(tup)

