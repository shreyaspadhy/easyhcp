#!/usr/bin/python
# -*- coding: utf-8 -*-

import boto3
import os
import json
import subprocess
import sklearn as sk
import numpy as np
from typing import Tuple


def setup_credentials():
    """
    Set Up AWS credentials from access keys into a credentials file
    Inputs
    ----------
    access_key : str
        AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXX
    secret_access_key : str
        AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXX
    Notes
    ------
    This function will open/create a file '~/.aws/credentials', that
    will then include a section:
    [hcp]
    AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXX
    AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXX
    The keys are credentials that you can get from HCP
    (see https://wiki.humanconnectome.org/display/PublicData/How+To+Connect+to+Connectome+Data+via+AWS)
    """
    access_key = input('Enter your HCP ACCESS KEY ID : ')
    secret_access_key = input('Enter your HCP SECRET ACCESS KEY : ')

    if not os.path.isdir(os.path.expanduser('~') + '/.aws'):
        print("test")
        os.makedirs(os.path.expanduser('~') + '/.aws')

    cred_file = open(os.path.expanduser('~') + '/.aws/credentials', "w+")
    if '[hcp]' in cred_file.read():
        update = input(
            "You have 'hcp' credentials set up already! Do you wish to update? [y/n] \n")
        if update == 'y:
            pass
    else:
        line1 = '[hcp]' + '\n'
        line2 = 'aws_access_key_id = ' + access_key + '\n'
        line3 = 'aws_secret_access_key = ' + secret_access_key + '\n'
        cred_file.writelines([line1, line2, line3])


def explain_HCP():
    """
    Lists all the files in a folder for a subject and explains what they are.
    Returns
    -------
    A dictionary with a filename and function
    Notes
    -----
    This function prints out a directory structure tree for an HCP subject
    with a simple description of what each file is.
    """


def get_subjects(get_all=True, get_random=1):
    """
    Fetch a list of HCP subjects
    Parameters
    ----------
    get_all : bool
       Gets a list of all the subjects
    get_random : int
        Gets a random subset of subjects
    Returns
    -------
    A list of UIDs for subjects in HCP
    Notes
    -----
    ...
    """
    pass


def get_structural_data(subject_list, scan_type, preprocessed=True, MNISpace=True, out_dir='.'):
    """
    Gets data of a specific type of modality for a list of subjects, and stores
    them in BIDS-like format in the specified output directory
    Parameters
    ----------
    subject_list : list
        List of subjects to get data for
    processed : bool
        Gets processed data in MNI Space
    type : list
        A list of identifiers for the type of data to scrape
    out_dir : str
        Path to output directory
    Notes
    -----
    """
    if preprocessed and MNISpace:
        output_dir = "{}/hcp/".format(out_dir)

        for subject in subject_list:
            subprocess.check_output(
                "mkdir -p {}{}/".format(output_dir, subject), shell=True)

            for scan in scan_type:
                subprocess.check_output("aws s3 cp \
               s3://hcp-openaccess-temp/HCP_1200/{}/MNINonLinear/{}_restore_brain.nii.gz \
               {}{}/".format(subject, scan, output_dir, subject), shell=True)


def get_rest_data(subject_list: list,
                  scan_run: tuple(["rfMRI_REST1_LR", "rfMRI_REST2_LR", "rfMRI_REST1_RL", "rfMRI_REST2_RL"]),
                  preprocessed: bool=True,
                  MNISpace: bool=True,
                  out_dir: str='.'):
    """
    Gets resting state fMRI data for different runs for a list of subjects,
     and stores them in the specified output directory
    Parameters
    ----------
    subject_list : list
        List of subjects to get data for
    processed : bool
        Gets processed data in MNI Space
    type : list
        A list of identifiers for the type of data to scrape
    out_dir : str
        Path to output directory
    Notes
    -----
    """
    if preprocessed and MNISpace:
        output_dir = "{}/hcp/".format(out_dir)

        for subject in subject_list:
            subprocess.check_output(
                "mkdir -p {}{}/".format(output_dir, subject), shell=True)

            for scan in scan_run:
                subprocess.check_output("aws s3 cp \
               s3: //hcp-openaccess-temp/HCP_1200/{}/MNINonLinear/Results/{}/{}_Atlas_MSMAll.dtseries.nii{}{} /".format(subject, scan, scan, output_dir, subject), shell=True)


def train_test_split(root: str,
                     split_folds: tuple([.7, .2, .1]),
                     scan_type: list,
                     convert_to_npy: bool=False) -> None:
    """
    splits an hcp dataset into train, test, val and converts the .nii.gz 
    files to .npy for easier processing checks shape to ensure t1 and t2
    are same dim
    Parameters
    ----------
    root: str
        root directory where raw files are stored
    split_folds: tuple(float, float, float)
        What fraction to divide data in for train, test, val
    scan_type: list
        What scans to divive into train - test splits
    Notes
    -----
    """
    os.chdir(root)
    subject_list = glob.glob('*')
    shuffled_list = sk.utils.shuffle(subject_list, random_state=42)
    n_subjects = len(shuffled_list)
    train_list = subject_list[0:np.floor(n_subjects) * split_folds[0]]
    train_list = subject_list[np.floor(
        n_subjects) * split_folds[0]:np.floor(n_subjects) * split_folds[1]]
    train_list = subject_list[np.floor(
        n_subjects) * split_folds[1]:np.floor(n_subjects) * split_folds[2]]
    data_splits = [train_list, test_list, val_list]
    split_names = ['train', 'test', 'val']
    for num, split in enumerate(split_names):
        train_list = data_splits[num]
        for subject in train_list:
            for type in scan_type:
                name = '/{}_restore_brain.nii.gz'.format(type)
                os.rename(root + '/' + name, root + '/' +
                          split + '/' + subject + name)
                if convert_to_npy:
                    t1_np = np.array(
                        nib.load(root + subject + '/' + t1_name).dataobj)
                    t2_np = np.array(
                        nib.load(root + subject + '/' + t2_name).dataobj)
                    t1_np = t1_np[2:-2, 27:-28, 40:-45]
                    t2_np = t2_np[2:-2, 27:-28, 40:-45]
                    for i in range(t1_np.shape[2]):
                        assert(t1_np.shape == t2_np.shape)


def fetch_hcp_diffusion(subjects, out_dir='.'):
    """
    Fetch HCP diffusion data and arrange it in a manner that resembles the
    BIDS[1]_ specification.
    Parameters
    ----------
    subjects: list
       Each item is an integer, identifying one of the HCP subjects
    Returns
    -------
    dict with remote and local names of these files.
    Notes
    -----
    To use this function, please setup credentials either manually,
    or by running `setup_credentials()`
    Local filenames are changed to match our expected conventions.
    .. [1] Gorgolewski et al. (2016). The brain imaging data structure,
           a format for organizing and describing outputs of neuroimaging
           experiments. Scientific Data, 3:: 160044. DOI: 10.1038/sdata.2016.44.
    """
    boto3.setup_default_session(profile_name='hcp')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('hcp-openaccess-temp')
    base_dir = op.join(out_dir, "hcp")
    if not os.path.exists(base_dir):
        os.makedirs(base_dir, exist_ok=True)

    data_files = {}
    for subject in subjects:
        # We make a single session folder per subject for this case, because
        # AFQ api expects session structure:
        sub_dir = op.join(base_dir, 'sub-%s' % subject)
        sess_dir = op.join(sub_dir, "sess-01")
        if not os.path.exists(sub_dir):
            os.mkdir(sub_dir)
            os.mkdir(sess_dir)
            os.mkdir(os.path.join(sess_dir, 'dwi'))
            os.mkdir(os.path.join(sess_dir, 'anat'))
        data_files[op.join(sess_dir, 'dwi', 'sub-%s_dwi.bval' % subject)] =\
            'HCP/%s/T1w/Diffusion/bvals' % subject
        data_files[op.join(sess_dir, 'dwi', 'sub-%s_dwi.bvec' % subject)] =\
            'HCP/%s/T1w/Diffusion/bvecs' % subject
        data_files[op.join(sess_dir, 'dwi', 'sub-%s_dwi.nii.gz' % subject)] =\
            'HCP/%s/T1w/Diffusion/data.nii.gz' % subject
        data_files[op.join(sess_dir, 'anat', 'sub-%s_T1w.nii.gz' % subject)] =\
            'HCP/%s/T1w/T1w_acpc_dc.nii.gz' % subject
        data_files[op.join(sess_dir, 'anat',
                           'sub-%s_aparc+aseg.nii.gz' % subject)] =\
            'HCP/%s/T1w/aparc+aseg.nii.gz' % subject

    for k in data_files.keys():
        if not op.exists(k):
            bucket.download_file(data_files[k], k)
    # Create the BIDS dataset description file text
    dataset_description = {
         "BIDSVersion": "1.0.0",
         "Name": "HCP",
         "Acknowledgements": """Data were provided by the Human Connectome 
         Project, WU-Minn Consortium (Principal Investigators: David Van 
        Essen and Kamil Ugurbil; 1U54MH091657) funded by the 16 NIH Institutes
        and Centers that support the NIH Blueprint for Neuroscience Research;
       and by the McDonnell Center for Systems Neuroscience at Washington University.""",  # noqa
         "Subjects": subjects}

    with open(op.join(base_dir, 'dataset_description.json'), 'w') as outfile:
        json.dump(dataset_description, outfile)

    return data_files
