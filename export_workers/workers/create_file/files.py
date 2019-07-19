"""Functions to creating csv, pdf, xls files"""
import csv
import os
import random

import xlsxwriter
from fpdf import FPDF

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
    file_name = PATH_TO_EXPORT_FILES + '/{0}.xls'.format(name)
    try:
        workbook = xlsxwriter.Workbook(file_name)
        worksheet = workbook.add_worksheet()
        row = 0
        col = 0
        user_id = random.choice(list(answers))
        field_titles = answers[user_id].keys()
        for title in field_titles:
            worksheet.write(0, col, title)
            col += 1
        for _, user_id in enumerate(answers):
            row += 1
            for col, value in enumerate(answers[user_id]):
                worksheet.write(row, col, answers[user_id][value])
        workbook.close()
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
    file_name = PATH_TO_EXPORT_FILES + '/{0}.csv'.format(name)
    try:
        with open(file_name, 'w') as file:
            user_id = random.choice(list(answers))
            field_titles = answers[user_id].keys()
            writer = csv.DictWriter(file, fieldnames=field_titles)
            writer.writeheader()
            for user in answers:
                writer.writerow(answers[user])
            status = True
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
    file_name = PATH_TO_EXPORT_FILES + '/{0}.pdf'.format(name)
    try:
        user_id = random.choice(list(answers))
        field_titles = answers[user_id].keys()
        col_count = len(field_titles) + 0.5
        pdf = FPDF()
        pdf.set_font("Arial", size=6)
        pdf.add_page()

        col_width = pdf.w / col_count
        row_height = pdf.font_size

        for title in field_titles:
            pdf.cell(col_width, row_height * 3,
                     txt=title, border=1)

        for user_answers in answers:
            pdf.ln(row_height * 3)
            for field_title in answers[user_answers]:
                pdf.cell(col_width, row_height * 3,
                         txt=answers[user_answers][field_title], border=1)
        pdf.output(file_name)
        status = True
    except TypeError as error:
        print(error)
        status = False
    return status
