import pandas as pd
import numpy as np

def create_random_machine():
  prefixes = ['AB', 'CD', 'EF', 'XZ']
  prefix = np.random.choice(prefixes)
  suffix = np.random.randint(99999)
  machine = '{pre:}-{suf:05d}'.format(pre=prefix, suf=suffix)
  return machine

# Create 50 machines
machines = [create_random_machine() for i in range(50)]

devices = ['kingston usb', 'panasonic dvd', 'iphone', 'mspro usb']
probabilities = [0.2, 0.1, 0.05, 0.65]

data = {
  'machine': [np.random.choice(machines) for i in range(1000)],
  'device': [np.random.choice(devices, p=probabilities) for i in range(1000)],
  'dummy': [1 for i in range(1000)]
}

df = pd.DataFrame(data)
df.to_csv('sample.csv', index=False)
