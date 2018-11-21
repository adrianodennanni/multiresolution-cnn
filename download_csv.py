from __future__ import print_function
import os
import sys
from six.moves.urllib.request import urlretrieve

data_root = './dataset'

last_percent_reported = None

def download_progress_hook(count, blockSize, totalSize):
  """A hook to report the progress of a download. This is mostly intended for users with
  slow internet connections. Reports every 5% change in download progress.
  """
  global last_percent_reported
  percent = int(count * blockSize * 100 / totalSize)

  if last_percent_reported != percent:
    if percent % 5 == 0:
      sys.stdout.write("%s%%" % percent)
      sys.stdout.flush()
    else:
      sys.stdout.write(".")
      sys.stdout.flush()

    last_percent_reported = percent

def maybe_download(url, filename, force=False):
  """Download a file if not present, and make sure it's the right size."""
  directory = '/'.join(filename.split('/')[:-1])
  if not os.path.exists(directory):
    os.makedirs(directory, exist_ok=True)
  if force or not os.path.exists(filename):
    try:
      print("Downloading "+filename)
      urlretrieve(url, filename, reporthook=download_progress_hook)
      print('Finished download')
    except:
      os.removedirs(filename)
  else:
    print('File: ' + filename + ' already exists!')

csv_files = {
  'train_labels'     : 'train/train-annotations-human-imagelabels.csv',
  'validation_labels': 'validation/validation-annotations-human-imagelabels.csv',
  'train_ids'        : 'train/train-images-with-labels-with-rotation.csv',
  'validation_ids'   : 'validation/validation-images-with-rotation.csv',
}

# First download the csv
url = 'https://storage.googleapis.com/openimages/2018_04/' # url from where we get the dataset
csv_dir = os.path.join(data_root, 'csv_files')
maybe_download(url + csv_files['train_labels'],      os.path.join(csv_dir, csv_files['train_labels']))
maybe_download(url + csv_files['validation_labels'], os.path.join(csv_dir, csv_files['validation_labels']))
maybe_download(url + csv_files['train_ids'],         os.path.join(csv_dir, csv_files['train_ids']))
maybe_download(url + csv_files['validation_ids'],    os.path.join(csv_dir, csv_files['validation_ids']))
