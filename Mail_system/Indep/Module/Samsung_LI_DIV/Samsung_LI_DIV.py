# -*- coding: euc-kr -*-
__author__ = "Goobin"

import pandas as pd
#import gmail
import pandas.io.sql as psql
import os
import datetime
import Authentication
import xlsxwriter
import email_logger
#import win32com.client
import smtp_fnguide2


##Real mode
mail_sender = 'index@fnguide.com'
emails = 'bhkeen.kim@samsung.com; yh8426.kim@samsung.com; hs_brian.kim@samsung.com; keenbh@naver.com; yukyoung.won@samsung.com; sh90.gwon@samsung.com; compliance.risk.kr@barings.com; equity.kr@barings.com; Institutional.kr@barings.com; jasmine.kim@barings.com; hong.kim@barings.com; lindsey.chang@barings.com; hwajin@syfund.co.kr; minah.choi@syfund.co.kr; risk@syfund.co.kr; kukdae@truefriend.com; kdyoo@truefriend.com; young88@truefriend.com; yopark@midasasset.com; seongcheol.hong@midasasset.com; phj@midasasset.com; ylkim@midasasset.com; kimung@midasasset.com; kunhee.ko@samsung.com'
cc = 'index@fnguide.com; hskim@fnguide.com'

## Test Mode
#mail_sender = 'jinwoo6627@fnguide.com'
#emails = 'jinwoo6627@fnguide.com'
#cc = 'jinwoo6627@fnguide.com'

engine_oracle = Authentication.oracle_db()
file_path = 'C:\\Users\\user\\PycharmProjects\\Project2017\\Mail_system\\Indep\\Module\\Samsung_LI_DIV\\log\\'

if not os.path.exists(file_path):
    file_path = ''
file_name = file_path + 'FnGuide_SLV_DIV_' + str(datetime.date.today()).replace("-", "") + '.xlsx'

num = 0
while os.path.isfile(file_name):
    num += 1
    file_name = file_path + 'FnGuide_SLV_DIV_' + str(datetime.date.today()).replace("-", "") + '_' + str(num) + '.xlsx'


def portfolio_info ():
    sql_text = """
        SELECT  A.GICODE "종목코드", B.ITEMCD "KR코드", B.ITEMABBRNM "종목명", A.CLS_CAP/SUM(A.CLS_CAP)OVER(PARTITION BY A.TRD_DT) "편입비중", C.U_NM "FICS 대분류", D.U_NM "FICS 중분류", E.U_NM "FICS 소분류", DECODE (B.MKT_GB, 1, DECODE (B.MKT_CAP_SIZE, 2, '대형주', DECODE (B.MKT_CAP_SIZE, 3, '중형주', '소형주')), 2, 'KOSDAQ', 0) "SIZE_GB"
        FROM JISUDEV.RES_J_CAP_HIST A, FNS_J_MAST_HIST B, FNS_U_MAST C, FNS_U_MAST D, FNS_U_MAST E
        WHERE A.U_CD = 'FI00.WLT.SLD'
        AND A.TRD_DT = TO_CHAR(SYSDATE, 'YYYYMMDD')
        AND A.GICODE = B.GICODE
        AND A.TRD_DT = B.TRD_DT
        AND SUBSTR(B.FGSC_CD,1,7) = C.U_CD
        AND SUBSTR(B.FGSC_CD,1,10) = D.U_CD
        AND B.FGSC_CD = E.U_CD
        ORDER BY 편입비중 DESC
   """
    df_portfolio = psql.read_sql(sql_text, engine_oracle)
    df_portfolio.index += 1
    print(df_portfolio)

    return df_portfolio


def calendar_info ():
    sql_text_cal = """
        select open_gb_stock
        from fnc_calendar
        where 1 = 1
        AND trd_dt = to_char(sysdate  , 'YYYYMMDD')
    """
    df_holiday = psql.read_sql(sql_text_cal, engine_oracle)

    return int(df_holiday['OPEN_GB_STOCK'][0])


def index_info ():
    sql_text_index = """
        SELECT DT2(A.TRD_DT) "기준일", A.CLS_PRC "기준일종가", B.CLS_PRC "전일종가", A.CLS_PRC/B.CLS_PRC - 1 "수익률"
        FROM FNS_UD A, FNS_UD B, FNC_CALENDAR C
        WHERE A.U_CD = 'FI00.WLT.SLD'
        AND A.U_CD = B.U_CD
        AND A.TRD_DT = TO_CHAR(SYSDATE  , 'YYYYMMDD')
        AND A.TRD_DT = C.TRD_DT
        AND B.TRD_DT = C.TRD_DT_PDAY
    """
    df_index = psql.read_sql(sql_text_index, engine_oracle)

    return df_index



def to_excel(portfolio, index):
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet('Portfolio_Information')
    bold_bottomline = workbook.add_format({'bold': True, 'bottom': 6, 'align': 'center', 'font_size': 10, 'bg_color': 'silver'})
    number = workbook.add_format({'num_format': '#,##0.00', 'font_size': 10})
    percent = workbook.add_format({'num_format': '0.0000%', 'font_size': 10})
    text = workbook.add_format({'align': 'center', 'font_size': 10})

    worksheet.write('A1', '#', bold_bottomline)
    worksheet.write('B1', '종목코드', bold_bottomline)
    worksheet.write('C1', 'KR코드', bold_bottomline)
    worksheet.write('D1', '종목명', bold_bottomline)
    worksheet.write('E1', '편입비중', bold_bottomline)
    worksheet.write('F1', 'FICS 대분류', bold_bottomline)
    worksheet.write('G1', 'FICS 중분류', bold_bottomline)
    worksheet.write('H1', 'FICS 소분류', bold_bottomline)
    worksheet.write('I1', 'SIZE 구분', bold_bottomline)

    worksheet.write('K1', '기준일', bold_bottomline)
    worksheet.write('L1', '기준일종가', bold_bottomline)
    worksheet.write('M1', '전일종가', bold_bottomline)
    worksheet.write('N1', '수익률', bold_bottomline)

    worksheet.set_column('A:A', 6)
    worksheet.set_column('B:B', 10)
    worksheet.set_column('C:C', 13)
    worksheet.set_column('D:D', 20)
    worksheet.set_column('E:E', 12)
    worksheet.set_column('F:H', 18)
    worksheet.set_column('I:I', 9)
    worksheet.set_column('K:N', 10)


    worksheet.write_column(1, 0, portfolio.index, text)
    worksheet.write_column(1, 1, portfolio['종목코드'], text)
    worksheet.write_column(1, 2, portfolio['KR코드'], text)
    worksheet.write_column(1, 3, portfolio['종목명'], text)
    worksheet.write_column(1, 4, portfolio['편입비중'], percent)
    worksheet.write_column(1, 5, portfolio['FICS 대분류'], text)
    worksheet.write_column(1, 6, portfolio['FICS 중분류'], text)
    worksheet.write_column(1, 7, portfolio['FICS 소분류'], text)
    worksheet.write_column(1, 8, portfolio['SIZE_GB'], text)

    worksheet.write(1, 10, index['기준일'][0], text)
    worksheet.write(1, 11, index['기준일종가'][0], number)
    worksheet.write(1, 12, index['전일종가'][0], number)
    worksheet.write(1, 13, index['수익률'][0], percent)


    workbook.close()
    engine_oracle.close()


#if __name__ == '__main__':
def main():
    email_logger.write_filename(__file__)

    if calendar_info() == 0:
        print('KRX is open today!\n\n')

        try:
            to_excel(portfolio_info(), index_info())
            title = "[FnGuide] FnGuide SLV 배당주형 지수 - 구성종목내역 " + str(datetime.date.today())

            #input_text = "C:\\Users\\user\\PycharmProjects\\Project2017\\Mail_system\\Samsung_LI_DIV\\email_body_Samsung_LI_DIV.txt"
            input_text = "C:\\Users\\user\\PycharmProjects\\Project2017\\Mail_system\\Indep\\Module\\Samsung_LI_DIV\\email_body_Samsung_LI_DIV.txt"

            f = open(input_text, "r")
            text = f.read()
            f.close()
            text = text.replace(':dt', str(datetime.date.today()))


            email_logger.write_recipients(emails + ', ' + cc)
            smtp_fnguide2.email_send(mail_sender, emails, cc, title, text, None, file_name)
            email_logger.write_completion()
            return True

        except (KeyError, IndexError) as e:
            print(e)
            email_logger.write_exception(str(e))
            return False

    else:
        email_logger.write_holiday()
        print('NOT OPEN')
        return False

if __name__ == '__main__':
    #from imp import reload
    #smtp_fnguide2 = reload(smtp_fnguide2)
    main()