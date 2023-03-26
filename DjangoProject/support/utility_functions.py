
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
import json
from io import BytesIO as IO
import pandas as pd





def returnExcelResponse(dataframe,sheet='default',file_name='excelfile'):
    response = ''
    try:
        byteStream = IO()
        # Assign the memory buffer to the excel byte stream so  excelwriter can know where and what is it is writing to IO can know how to represent it in memory
        xls_bytestream = pd.ExcelWriter(byteStream, engine='xlsxwriter')
        #write excel file to memory which is the XLS Bytestream
        dataframe.to_excel(xls_bytestream,sheet_name=sheet)
        xls_bytestream.close()
        #Byte stream is finished writing to memory but the cursor is at the end of the stream. Seek back to beginning so User can download from beginning.
        byteStream.seek(0)
        # create an HTTP response with the bytestream to be downloaded by the user. Content Type
        response = HttpResponse(byteStream)
        response["Content-Type"] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response['Content-Disposition'] = 'attachment; filename={r}.xlsx'.format(r=file_name)
    except (Exception) as error:
        print(error)
    return response