import os
import nimare as nim
from nimare.dataset import Dataset
from datetime import date

today = date.today().strftime('%d_%m_%Y')

constructs = ['Affiliation', 'Others', 'Self', 'Soc_Comm']
root_dir = '/Users/kbottenh/Dropbox/Projects/metas/ro-flux'

all_dat = [f'{root_dir}/data/ALL_Talairach.txt', f'{root_dir}/data/ALL_MNI.txt']

all_dset = nim.io.convert_sleuth_to_dataset(all_dat)

for construct in constructs:
    print(construct)
    con_dat = [os.path.join(root_dir, 'data', f'{construct}_Pure_Talairach.txt'), 
               os.path.join(root_dir, 'data', f'{construct}_Pure_MNI.txt')]

    con_dset = nim.io.convert_sleuth_to_dataset(con_dat)
    con_dset.save(f'{root_dir}/data/{construct}_all.pkl.gz')

    non_construct_ids = list(set(all_dset.ids) - set(con_dset.ids))
    non_construct_dset = all_dset.slice(non_construct_ids)

    non_construct_dset.save(f'{root_dir}/data/Not_{construct}_all.pkl.gz')

    #non_construct_ids = list(set(tal_dset.ids) - set(tal_construct.ids))
    #tal_non_construct = mni_dset.slice(non_construct_ids)

    #tal_non_construct.save(f'{root_dir}/data/Not_{construct}_Talairach.pkl', compress=False)

