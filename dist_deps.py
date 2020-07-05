# Author: Artemie Jurgenson
# Angular Distribution Dependency Parser
# This is a python script that is placed into an Angular project directory and is run to obtain a list
# of unique npmjs package directories.  It parsed the vendor source map header that contains the paths
# to all the files that are pulled in from the node_modules directory by the embedded Angular webpack.

import glob, os

# finds the vendor map in the dist directory when inside the angular project folder (w/ some arbitrary names)
# if there's no vendor map it parses the main source map
try:
    path = glob.glob('./dist/*/vendor.*.map')[0]
except IndexError:
    print('Vendor source map not found, using main source map.')
    try:
        path = glob.glob('./dist/*/main.*.map')[0]
    except IndexError:
        print('No valid source map found.')
        quit()

# reads in the file
with open(path, 'r') as f:
    vendor_paths = f.read().replace('\n', '')

# chops off the end of the source map header with the vendor directories
vendor_paths = vendor_paths.split(']')[0]
# chops off the opener to give all the paths dilimited by commas
vendor_paths = vendor_paths.split('[')[1]
# splits by commas
vendor_paths = vendor_paths.split(',')

package_dirs = set()

for path in vendor_paths:
    # further cuts to include only the relative path starting with the node_modules directory
    path = path[12:-1]
    print(path)
    
    # running ng build with the --build-optimizer flag appends this to the end of the file in the source map
    if path.endswith('.pre-build-optimizer.js'):
        path = path.replace('.pre-build-optimizer.js','')

    # checks if the file actually exists
    if not os.path.isfile(path):
        print('The following file was not found: ', path)
        continue
    
    # gets directory containing the source map file
    parent_dir = os.path.dirname(path)
    
    # loop to traverse up the path terminating at the node_modules directory
    while(parent_dir != './node_modules'):
        # checks to prevent infinite loop if the path doesn't have a node_modules directory
        if parent_dir == '.' or parent_dir == '':
            print('The following path is not in a node_modules directory: ', path)
            break
        # checks if a package.json exists in the directory, adds to the set of package directorys, and breaks
        if os.path.isfile(parent_dir + '/package.json'):
            package_dirs.add(parent_dir)
            #print(parent_dir)
            break
        # progresses the loop by getting the next parent directory
        parent_dir = os.path.dirname(parent_dir)
    # checks if the loops terminates with no breaks (it hit the node_modules)
    else:
        print('No package.json file was found anywhere in the following path: ', path)

# opens/overwrites output file to be passed into the iq server cli
out_file = open('package_dirs.txt', 'w+')

# prints package directories and writes to file
print('This is the set of unique package directories for files defined in the vendor source map: ')
for package_path in package_dirs:
    out_file.write(package_path + '\n')
    print(package_path)

out_file.close()
