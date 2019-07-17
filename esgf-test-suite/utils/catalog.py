import re
import urllib.request, urllib.error, urllib.parse
from lxml import etree
import multiprocessing
from io import BytesIO

import random
import re
import utils.configuration as config

class ThreddsUtils(object):
  
  CATALOG_REF_NUM_LIMIT = 100
  
  catalog_ns = '{http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0}'
  # catalog.py experienced memory problem when computing more than twice the
  # endpoints of a data node. So this variable is sort of singleton of the 
  # endpoints of the data node.
  endpoints = None

  def __init__(self):
    # init
    self.in_queue = multiprocessing.JoinableQueue()
    self.out_queue = multiprocessing.Queue()
    self.data_node = config.get(config.NODES_SECTION, config.DATA_NODE_KEY)

  def chunk_it(self, seq, num):
    avg = len(seq) / float(num)
    res = []
    last = 0.0

    while last < len(seq):
      res.append(seq[int(last):int(last + avg)])
      last += avg

    return res

  def get_dataset_services(self, dataset, services_def):
    ds_services = []

    # Collecting available services from <serviceName>some_service</serviceName>
    for sv in dataset.iterchildren(tag=ThreddsUtils.catalog_ns + 'serviceName'):
      ds_services.append(services_def[sv.text])
    # Collecting available services from <access serviceName="some_service">
    for acc in dataset.iterchildren(tag=ThreddsUtils.catalog_ns + 'access'):
      try:
        ds_services.append(services_def[acc.get('serviceName')])
      except:
        continue

    return ds_services

  def get_dataset_size(self, dataset):
    # Set aggregations size to inf
    if "aggregation" in dataset.get('urlPath'):
      size = float('inf')
    else:
      for si in dataset.iterchildren(tag=ThreddsUtils.catalog_ns + 'dataSize'):
        units = si.get('units')
        if units == 'Kbytes':
          size = float(si.text) / 1024
        elif units == 'Mbytes':
          size = float(si.text)
        elif units == 'Gbytes':
          size = float(si.text) * 1024
        else:
          size = float('inf')

    return size

  def get_datasets_list(self, data, services_def):
    datasets_list = []

    # Parsing datasets XML document
    for events, ds in etree.iterparse(BytesIO(data), tag=ThreddsUtils.catalog_ns + 'dataset'):
      # Only interested in datasets which have an URL
      if ds.get('urlPath'):
        # Building dataset entry with URL, size and available services
        dataset = []
        dataset.append(ds.get('urlPath'))
        dataset.append(self.get_dataset_size(ds))
        dataset.append(self.get_dataset_services(ds, services_def))
        datasets_list.append(dataset)

    return datasets_list

  def get_services_definition(self, data):
    services_def = {}

    for events, sv in etree.iterparse(BytesIO(data), tag=ThreddsUtils.catalog_ns + 'service'):
      if sv.get('serviceType') != 'Compound':
        services_def.update({sv.get('name'): sv.get('serviceType')})

    return services_def

  def worker(self, catalogrefs):
    datasets_list = []

    for cr in catalogrefs:
      try:
        content = urllib.request.urlopen(cr)
        data = content.read()
      except:
        continue

      # Parsing services definition
      services_def = self.get_services_definition(data)
      # Parsing datasets
      datasets_list = self.get_datasets_list(data, services_def)

    return datasets_list

  def queue_manager(self):
    for item in iter(self.in_queue.get, None):
      self.out_queue.put(self.worker(item))
      self.in_queue.task_done()
    self.in_queue.task_done()

  def map_processes(self, chunks):
    processes = []

    # Starting nb_chunk processes calling the queue manager
    for i in chunks:
      processes.append(multiprocessing.Process(target=self.queue_manager))
      processes[-1].daemon = True
      processes[-1].start()

    # Feeding the input queue with chunks
    for cr in chunks:
      self.in_queue.put(cr)

    # Waiting for every chunk to be processed
    self.in_queue.join()

    # Feeding the input queue with None to be sure
    for p in processes:
      self.in_queue.put(None)

    # Collecting results from output queue
    datasets_list = []
    for p in processes:
      datasets_list.extend(self.out_queue.get())

    self.in_queue.join()

    for p in processes:
      p.join()

    return datasets_list

  def filter_catalogrefs(self, proj_url, matcher, content):
    filtered = list()
    unfiltered = list()

    tag=ThreddsUtils.catalog_ns + 'catalogRef'
    root = etree.parse(content).getroot()
    
    pattern = re.compile(matcher)
    for node in root.findall(tag):
      path = node.attrib['{http://www.w3.org/1999/xlink}href']
      url = re.sub('catalog.xml', '', proj_url) + path
      if pattern.search(path):
        filtered.append(url)
      else:
        unfiltered.append(url)

    print(f"[DEBUG] len of filtered: {len(filtered)}")
    print(f"[DEBUG] len of unfiltered: {len(unfiltered)}")
    return (filtered, unfiltered)

  def get_catalogrefs(self, projects):
    print("[DEBUG] starting get_catalogrefs")
    filtered   = list()
    unfiltered = list()

    for proj_url in projects:
      print(f"[DEBUG] fetching content of project '{proj_url}'")
      try:
        content = urllib.request.urlopen(proj_url)
      except:
        continue
      print(f"[DEBUG] parsing the content of project '{proj_url}'")
      # Parsing catalogRef xml entries
      local_filtered, local_unfiltered = self.filter_catalogrefs(proj_url, '(.fx.)|(.mon.)', content)
      filtered.extend(local_filtered)
      unfiltered.extend(local_unfiltered)      
    
    filtered_size = len(filtered)

    delta = ThreddsUtils.CATALOG_REF_NUM_LIMIT - filtered_size

    if delta > 0:
      unfiltered_size = len(unfiltered)
      if delta > unfiltered_size:
        last_index = unfiltered_size - 1
      else:
        last_index = delta - 1
      filtered.extend(unfiltered[0:last_index])
    else:
      filtered = random.sample(filtered, ThreddsUtils.CATALOG_REF_NUM_LIMIT)
    print("[DEBUG] end of get_catalogrefs")
    return filtered

  def get_projects(self):
    projects = []
    main_url = "http://{0}/thredds/catalog/catalog.xml".format(self.data_node);

    try:
      content = urllib.request.urlopen(main_url)
    except Exception as e:
      err_msg = "unable to get the catalog at '{0}' (reason: {1})"\
        .format(main_url, e)
      assert(False), err_msg

    for event, cr in etree.iterparse(content, events=('end',), tag=ThreddsUtils.catalog_ns + 'catalogRef'):
      path = cr.get('{http://www.w3.org/1999/xlink}href')
      # Exclude DatasetScans
      if 'thredds' not in path:
        projects.append(re.sub('catalog.xml', '', main_url) + path)

    return projects

  def get_endpoints(self):
    if ThreddsUtils.endpoints is None:
      print("[DEBUG] starting get_endpoints")
      endpoints = []

      # Determining number of processes and chunks
      nb_chunks = multiprocessing.cpu_count()
      print(f"[DEBUG] number of chunks: {nb_chunks}")

      print("[DEBUG] getting projects")      
      # Getting projects href links from main catalog (http://data_node/thredds/catalog/catalog.xml)
      # !!!
      projects = self.get_projects()
      #projects = ["http://vesg.ipsl.upmc.fr/thredds/catalog/esgcet/catalog.xml"]
      print(f"[DEBUG] projects: {projects}")

      # Getting and chunking catalogrefs href links from project catalogs (ex: http://data_node/thredds/geomip/catalog.xml)
      print("[DEBUG] getting catalogrefs")
      catalogrefs = self.get_catalogrefs(projects)
      print(f"[DEBUG] len of catalogrefs: {len(catalogrefs)}")

      print(catalogrefs[0])
      print("[DEBUG] chunking catalogrefs")
      chunked_catalogrefs = self.chunk_it(catalogrefs, nb_chunks)
      print(f"[DEBUG] len of chunked_catalogrefs: {len(chunked_catalogrefs)}")

      # Starting multiprocessed work
      print("[DEBUG] starting multiprocess work")
      endpoints = self.map_processes(chunked_catalogrefs)
      ThreddsUtils.endpoints = endpoints

      print("[DEBUG] end of get_endpoints")
    return ThreddsUtils.endpoints
