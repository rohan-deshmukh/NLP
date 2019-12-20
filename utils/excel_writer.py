import xlsxwriter
import os
import datetime


class Excelwrite(object):
    def __init__(self, path, input_list):
        self.destination_path = path
        self.ans_list = input_list

    def writedata(self):
        """Takes a list and writes to an excel file"""
        filename = 'Completed_questionnaire.xlsx'
        workbook = xlsxwriter.Workbook(os.path.join(self.destination_path, filename))

        worksheet1 = workbook.add_worksheet("Completed Questionnaire")

        cell_format = workbook.add_format()
        conf_score_cell_format = workbook.add_format()
        cell_format.set_font_size(11)
        cell_format.set_text_wrap()
        cell_format.set_align('left')
        cell_format.set_align('top')
        conf_score_cell_format.set_align('center')
        conf_score_cell_format.set_align('vcenter')
        header_style = workbook.add_format({'bold': True})
        header_style.set_font_size(12)
        header_style.set_align('left')
        header_style.set_align('vcenter')
        worksheet1.set_row(0, 30)
        worksheet1.set_column('A:A', 50)
        worksheet1.set_column('B:B', 40)
        worksheet1.set_column('C:C', 40)
        worksheet1.set_column('D:D', 20)

        worksheet1.write('A1', "Question", header_style)
        worksheet1.write('B1', "Response", header_style)
        worksheet1.write('C1', 'Similar Question from Previous Qs', header_style)
        worksheet1.write('D1', 'Confidence Score(%)', header_style)

        row = 0
        col = 0
        first_row = 1
        first_col = 3
        last_row = len(self.ans_list)
        last_col = 3

        for item in self.ans_list:
            row += 1
            worksheet1.write(row, col, str(item[0]), cell_format)
            worksheet1.write(row, col + 1, str(item[1]), cell_format)
            worksheet1.write(row, col + 2, str(item[2]), cell_format)
            worksheet1.write(row, col + 3, item[3]*100, conf_score_cell_format)

        # Light red fill with dark red text.
        format1 = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})

        # Light yellow fill with dark yellow text.
        format2 = workbook.add_format({'bg_color': '#FFEB9C', 'font_color': '#9C6500'})

        # Green fill with dark green text.
        format3 = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})

        worksheet1.conditional_format(first_row, first_col, last_row, last_col, {'type': 'cell', 'criteria': '<=', 'value': 50, 'format': format1})
        worksheet1.conditional_format(first_row, first_col, last_row, last_col, {'type': 'cell', 'criteria': 'between', 'minimum': 50, 'maximum': 80, 'format': format2})
        worksheet1.conditional_format(first_row, first_col, last_row, last_col, {'type': 'cell', 'criteria': '>', 'value': 80, 'format': format3})

        worksheet2 = workbook.add_worksheet("File metadata")
        worksheet2.set_column('A:A', 20)

        current_time = datetime.datetime.now()
        customized_timestamp = current_time.strftime("%m/%d/%Y %H:%M:%S")
        metadata = ["File Created at: " + str(customized_timestamp)]
        worksheet2.write('A1', 'File Details', header_style)

        row = 0
        for item in metadata:
            row += 1
            worksheet2.write(row, 0, item, cell_format)

        workbook.close()

