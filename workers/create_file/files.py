"""Functions to creating csv, pdf, xls files"""
import os

import pandas as pd
import pdfkit as pdf

PATH_TO_EXPORT_FILES = os.environ.get('PATH_TO_EXPORT_FILES')


def create_file_name(dic):
    """
    Create unique filename.
    :param dic: Dictionary has particular form_id and groups.
    Based on that request info this function creates logic name
    for file.
    :return: str : File name.
    """
    name = f"Answers_for_form:{dic['form_id']}_groups:{dic['groups']}"
    return name


def xls_file(answers, name):
    """
    Creates xls file with answers for particular form.
    :param answers: dict: Answers for form.
    :param name: str: File name for new file.
    :return: None
    """
    try:
        dataframe = pd.DataFrame(answers).T
        dataframe.to_excel(PATH_TO_EXPORT_FILES + "/{}.xls".format(name))
        status = True
    except TypeError as error:
        print(error)
        status = False
    return status


def csv_file(answers, name):
    """
    Creates csv file with answers for particular form.
    :param answers: dict: Answers for form.
    :param name: str: File name for new file.
    :return: status: bool: returns True if file was created successfully, otherwise - False.
    """
    try:
        dataframe = pd.DataFrame(answers).T
        name = PATH_TO_EXPORT_FILES + "/{}.csv".format(name)
        dataframe.to_csv(name)
        status = name
    except TypeError as error:
        print(error)
        status = False
    return status


def pdf_file(answers, name):
    """
    Creates pdf file with answers for particular form.
    :param answers: dict: Answers for form.
    :param name: str: File name for new file.
    :return: status: bool: returns True if file was created successfully, otherwise - False.
    """
    try:
        dataframe = pd.DataFrame(answers).T
        html_file = PATH_TO_EXPORT_FILES + '/{}.html'.format(name)
        file_pdf = PATH_TO_EXPORT_FILES + '/{}.pdf'.format(name)
        dataframe.to_html(html_file)
        pdf.from_file(html_file, file_pdf)
        os.remove(html_file)
        status = True
    except TypeError as error:
        print(error)
        status = False
    return status
