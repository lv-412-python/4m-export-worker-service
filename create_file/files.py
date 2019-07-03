"""Functions to creating csv, pdf, xls files"""
import os
import pandas as pd
import pdfkit as pdf
from delete_files import PATH

def file_name(dic):
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
        dataframe.to_excel(PATH + "/{}.xls".format(name))
    except ValueError as error:
        print("ValueError error - ({0})".format(error))

def csv_file(answers, name):
    """
    Creates csv file with answers for particular form.
    :param answers: dict: Answers for form.
    :param name: str: File name for new file.
    :return: None
    """
    try:
        dataframe = pd.DataFrame(answers).T
        dataframe.to_csv(PATH + "/{}.csv".format(name))
    except ValueError as error:
        print("ValueError error - ({0})".format(error))

def pdf_file(answers, name):
    """
    Creates pdf file with answers for particular form.
    :param answers: dict: Answers for form.
    :param name: str: File name for new file.
    :return: None
    """
    try:
        dataframe = pd.DataFrame(answers).T
        html_file = PATH + '/{}.html'.format(name)
        file_pdf = PATH + '/{}.pdf'.format(name)
        dataframe.to_html(html_file)
        pdf.from_file(html_file, file_pdf)
        os.remove(html_file)
    except ValueError as error:
        print("ValueError error - ({0})".format(error))


FILE_MAKERS = {'xls': xls_file,
               'csv': csv_file,
               'pdf': pdf_file
              }
