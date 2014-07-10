#!/usr/bin/env python
# -*- coding: latin-1 -*-
# file: make_MC_weekly_L3_wac_website.py

import os
import os.path
import sys
import time
import fileinput


print("\n*******************************************************")
print(" Script \'make_MC_weekly_L3_wac_website.py\' at work... ")
print("*******************************************************\n")

product_IDs = ('chl', 'tsm', 'ys', 'trn', 'sst')

# dictionary of product keys and values
products_dict = { 'chl' : 'Chlorophyll', \
                  'tsm' : 'Total Suspended Matter',\
                  'ys'  : 'Yellow Substance',\
                  'trn' : 'Transparency',\
                  'sst' : 'Sea Surface Temperature'}

def printUsage():
    print("Usage: make_MC_weekly_L3_wac_website.py \'product\' \'backDay\'")
    print("where product is one of the following water constituents:")
    print(product_IDs[0] + " (=" + products_dict[product_IDs[0]] + "), " + product_IDs[1] + " (=" + products_dict[product_IDs[1]] + "),")
    print(product_IDs[2] + " (=" + products_dict[product_IDs[2]] + "), " + product_IDs[3] + " (=" + products_dict[product_IDs[3]] + ")")
    print(product_IDs[4] + " (=" + products_dict[product_IDs[4]] + ")\n")
    print("and backDay is an integer value specifying which day to process:")
    print("1 means yesterday, 2 means the day before yesterday, etc.")
    print("Maximum value is 32767.\n")

try:
    argc=len(sys.argv)
    if (argc < 3):          # the program was called incorrectly
        print("\nToo few parameters passed!")
        printUsage()
        sys.exit(1)
    else:                   # we have also received parameters
        if (sys.argv[1] not in product_IDs):
            print("\nProduct specifier useless!\n")
            sys.exit(1)    
        else:               # incorrect parameter
            product = sys.argv[1]
            try:
                back_days = int(sys.argv[2])
            except:
                print("back_day parameter must be of type integer!")
                printUsage()
                print("\nError in parameters. Now exiting...\n")
                sys.exit(1)
except:
    print("\nError in parameters. Now exiting...\n")
    sys.exit(1)    

if product == 'sst':
    sensor = 'AATSR'
else:
    sensor = 'MERIS'

print(sensor)

# Directories
# bcG5:
#toolsDir           = '/uwe/tools/wac_web/web_resources/'
# bcserver7:
toolsDir           = '/home/uwe/tools/wac_web/web_resources/'
base_dir       = '/fs14/EOservices/OutputPool/quicklooks/WAQS-MC/weekly/'
base_images_dir    = base_dir + 'hires/'
htmlDir            = base_dir + 'html/'
# bcserver7:
webserverImagesDir = '/images/WAQS-MC/weekly/'

# bcG5:
#webserverImagesDir = 'http://www.brockmann-consult.de/images/WAQS-MC/weekly/'
#htmlDir            = '/Volumes/Elephant/Users/uwe/Documents/Development/Python/html/'

monthsDict = { 1 : 'January',   \
               2 : 'February',  \
               3 : 'March',     \
               4 : 'April',     \
               5 : 'May',       \
               6 : 'June',      \
               7 : 'July',      \
               8 : 'August',    \
               9 : 'September', \
              10 : 'October',   \
              11 : 'November',  \
              12 : 'December' }


# Some helper functions:
def get_float_day(day):
    secs_per_day  = 24*60*60
    return time.mktime(time.localtime())-day*secs_per_day

def get_date_string(float_day):
    date  = time.localtime(float_day)
    year  = str(date[0])
    month = str(date[1])
    day   = str(date[2])
    if date[1] <10:
        month = "0" + str(date[1])
    if date[2] <10:
        day   = "0" + str(date[2])
    return year + month + day

def get_year_month_string(month_int):
    date  = time.localtime()
    year  = str(date[0])
    if month_int <10:
        month = "0" + str(month_int)
    else:
        month = str(month_int)
    return year + month

def get_year_from_date_string(_date_string):
    return _date_string[0:4]

def get_month_from_date_string(_date_string):
    return _date_string[4:6]

def get_day_from_date_string(_date_string):
    return _date_string[6:8]

def get_formatted_date(_date_string):
    return get_day_from_date_string(_date_string) + '.' + get_month_from_date_string(_date_string) + '.' + get_year_from_date_string(_date_string)

first_day = get_date_string(get_float_day(back_days + 6))
last_day  = get_date_string(get_float_day(back_days))
current_date_range = last_day + '_' + first_day
print(current_date_range)

_year_first  = get_year_from_date_string(first_day)
_month_first = get_month_from_date_string(first_day)
_day_first   = get_day_from_date_string(first_day)
_year_last   = get_year_from_date_string(last_day)
_month_last  = get_month_from_date_string(last_day)
_day_last    = get_day_from_date_string(last_day)

def get_current_hires_image_names():
    prefix =  webserverImagesDir + 'current_'                                
    if product == 'sst':
        return [prefix + product + '_nos_ipf_max.jpg', prefix + product + '_bas_ipf_max.jpg']            # e.g.: current_sst_bas_ipf_max.jpg
    else:
        return [prefix + product + '_nos_wac_acr_max.jpg', prefix + product + '_bas_wac_acr_max.jpg']    # e.g.: current_chl_bas_wac_acr_max.jpg

def get_current_lores_image_names(): 
    prefix =  webserverImagesDir + 'current_'                                 
    if product == 'sst':
        return [prefix + product + '_nos_ipf_275.jpg', prefix + product + '_bas_ipf_275.jpg']            # e.g.: current_sst_bas_ipf_275.jpg
    else:
        return [prefix + product + '_nos_wac_acr_275.jpg', prefix + product + '_bas_wac_acr_275.jpg']    # e.g.: current_chl_bas_wac_acr_275.jpg

def get_hires_image_names(date_range): 
    prefix = webserverImagesDir + 'hires/'      + date_range + '_' + product
    if product == 'sst':
        return [prefix + '_nos_ipf_1200.jpg', prefix + '_bas_ipf_1200.jpg']               # e.g.: 20060508_20060514_sst_bas_ipf_1200.jpg
    else:
        return [prefix + '_nos_wac_acr_1200.jpg', prefix + '_bas_wac_acr_1200.jpg']       # e.g.: 20060508_20060514_chl_bas_wac_acr_1200.jpg

def get_lores_image_names(date_range):    
    prefix = webserverImagesDir + 'quicklooks/' + date_range + '_' + product
    if product == 'sst':
        return [prefix + '_nos_ipf_1200_ql.jpg', prefix + '_bas_ipf_1200_ql.jpg']         # e.g.: 20060508_20060514_sst_bas_ipf_1200_ql.jpg
    else:
        return [prefix + '_nos_wac_acr_1200_ql.jpg', prefix + '_bas_wac_acr_1200_ql.jpg'] # e.g.: 20060508_20060514_chl_bas_wac_acr_1200_ql.jpg

def get_thumb_image_names(date_range):
    prefix = webserverImagesDir + 'thumbs/'     + date_range + '_' + product             
    if product == 'sst':
        return [prefix + '_nos_ipf_1200_tn.jpg', prefix + '_bas_ipf_1200_tn.jpg']         # e.g.: 20060508_20060514_sst_bas_ipf_1200_tn.jpg
    else:
        return [prefix + '_nos_wac_acr_1200_tn.jpg', prefix + '_bas_wac_acr_1200_tn.jpg'] # e.g.: 20060508_20060514_chl_bas_wac_acr_1200_tn.jpg

def get_table_display_date(date_string):
    return '<b>' + get_formatted_date(date_string[0:8]) + '</b><br><br>to<br><br><b>' + get_formatted_date(date_string[9:17]) + '</b>'

def get_text_display_date(date_string):
    return '<b>' + get_formatted_date(date_string[0:8]) + '</b> to <b>' + get_formatted_date(date_string[9:17]) + '</b>'

def get_text_display_date_reverse(date_string):
    return get_formatted_date(date_string[9:17]) + ' to ' + get_formatted_date(date_string[0:8])

if product == 'sst':
    start_date_of_processed = '200604'    # when the processing of these data started 
else: 
    start_date_of_processed = '200601'

main_page           = htmlDir  + product + '_current.html'

# these files contain constant text and are read by fileinput
main_header         = toolsDir + 'main_header_wac_mc.txt'       # constant header part
main_table_footer   = toolsDir + 'main_table_footer_wac_mc.txt'    # constant table 
months_main_header  = toolsDir + 'months_main_header_wac_mc.txt'   # constant header part
months_list_js_part = toolsDir + 'list_page_js_part_wac_mc.txt'    # constant javascript code part

# File names for output
hires_output_filenames = get_current_hires_image_names() # hires images with legend and text
ql_output_filenames    = get_current_lores_image_names()    # 275 pix height image

headline_tag =  '              <p><font face=\"Verdana, Arial\" size=\"3\"><b>Latest '+ products_dict[product] + ' Images</font></b><br>\n'
headline_tag += '                 <font face=\"Verdana, Arial\" size=\"2\">The images shown here are floating weekly averages of ' + sensor + '-derived ' + products_dict[product] + '<br>that are processed each day. The latest images below contain data from ' + get_text_display_date_reverse(current_date_range) + ':</font></p>\n'

front_images_tag =  '              <table width=\"99%\" border=\"0\" align=\"center\">\n'
front_images_tag += '                <tr>\n'
front_images_tag += '                  <td width=\"43%\">\n'
front_images_tag += '                    <div align=\"center\"><font face=\"Verdana, Arial\" size=\"1\"><a href=\"' + hires_output_filenames[0] + '\" target=\"_blank\"><img src=\"' + ql_output_filenames[0] + '\" width=\"353\" height=\"275\" border=\"0\"></a></font></div>\n'
front_images_tag += '                  </td>\n'
front_images_tag += '                  <td width=\"57%\">\n'
front_images_tag += '                    <div align=\"center\"><font face=\"Verdana, Arial\" size=\"1\"><a href=\"' + hires_output_filenames[1] + '\" target=\"_blank\"><img src=\"' + ql_output_filenames[1] + '\" width=\"466\" height=\"275\" border=\"0\"></a></font></div>\n'
front_images_tag += '                  </td>\n'
front_images_tag += '                </tr>\n'
front_images_tag += '                <tr>\n'
front_images_tag += '                  <td width=\"43%\">\n'
front_images_tag += '                    <div align=\"center\"><font face=\"Verdana, Arial\" size=\"1\">Latest image of ' + products_dict[product] + ', North Sea</font></div>\n'
front_images_tag += '                  </td>\n'
front_images_tag += '                  <td width=\"57%\">\n'
front_images_tag += '                    <div align=\"center\"><font face=\"Verdana, Arial\" size=\"1\">Latest image of ' + products_dict[product] + ', Baltic Sea</font></div>\n'
front_images_tag += '                  </td>\n'
front_images_tag += '                </tr>\n'
front_images_tag += '              </table>\n'

months_headline_tag =  '              <div><img src="images/empty.gif\" width=\"400\" height=\"6\"><br>\n'
months_headline_tag += '                <font face=\"Verdana, Arial\" size=\"3\" color=\"#000000\"><b>\n'
months_headline_tag += '                Archive of ' + products_dict[product] + ' Images<br>\n'
months_headline_tag += '                <img src=\"images/empty.gif\" width=\"400\" height=\"6\"></b></font></div>\n'
months_headline_tag += '             </div>\n'

# Here comes the months table in the html page (is written by write_main_page())

# ('chl', 'tsm', 'ys', 'trn', 'sst')
def get_next_links():
    if product == product_IDs[0]:      # chl
        return ('tsm', 'ys', 'trn', 'sst')
    elif product == product_IDs[1]:    # tsm
        return ('ys', 'trn', 'sst', 'chl')
    elif product == product_IDs[2]:    # ys
        return ('trn', 'sst', 'chl', 'tsm')
    elif product == product_IDs[3]:    # trn
        return ('sst', 'chl', 'tsm', 'ys')
    elif product == product_IDs[4]:    # sst
        return ('chl', 'tsm', 'ys', 'trn')

footer = '\n        <!-- Animations part -->\n'
footer += '        <div align=\"center\"><img src=\"/images/WAQS-MC/misc/empty.gif\" width=\"400\" height=\"6\"><br>\n'
footer += '          <font face=\"Verdana, Arial\" size=\"2\" color=\"#000000\"><b>'+ products_dict[product] + ' Animations <img src=\"/images/WAQS-MC/misc/new.gif\"><br>\n'
footer += '          <img src=\"/images/WAQS-MC/misc/empty.gif\" width=\"400\" height=\"6\"></b></font>\n'
footer += '        </div>\n'
footer += '        <table align=\"center\" width =\"200\" bgcolor=\"#BBDDDD\">\n'
footer += '          <tr>\n'
footer += '            <td width=\"36\" style=\"border-width:1px;border-style:solid;border-color:#F0F2FF;\">\n'
footer += '              <div align=\"center\"><b><font color=\"#000000\" face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\"><a href=\"animations/html/'+ product + '_animations_2006.html\" target=\"_parent\">2006</a></font></b></div>\n'
footer += '            </td>\n'
footer += '            <td width=\"36\" style=\"border-width:1px;border-style:solid;border-color:#F0F2FF;\">\n'
footer += '              <div align=\"center\"><b><font color=\"#000000\" face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\"><a href=\"animations/html/'+ product + '_animations_2007.html\" target=\"_parent\">2007</a></font></b></div>\n'
footer += '            </td>\n'
footer += '            <td width=\"36\" style=\"border-width:1px;border-style:solid;border-color:#F0F2FF;\">\n'
footer += '              <div align=\"center\"><b><font color=\"#000000\" face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\"><a href=\"animations/html/'+ product + '_animations_2008.html\" target=\"_parent\">2008</a></font></b></div>\n'
footer += '            </td>\n'
footer += '          </tr>\n'
footer += '        </table>\n\n'
footer += '        <!-- Navigation -->\n'
footer += '            <div align=\"center\"><img src=\"/images/WAQS-MC/misc/empty.gif\" width=\"400\" height=\"16\"><br>\n'
footer += '            <img src=\"/images/WAQS-MC/misc/sirenj.gif\" width=\"700\" height=\"1\"></div>\n'
footer += '            <table align=\"center\" width=\"735\">\n'
footer += '              <tr>\n'
footer += '                <td style=\"font-family:Verdana; font-size:0.65em;\">\n'
footer += '                   <div align=\"center\">\n'
footer += '                     <span class=\"upper_menu\"> | <a href=\"'+get_next_links()[0]+'_current.html\">' + products_dict[get_next_links()[0]] + '</a>\n'
footer += '                                                 | <a href=\"'+get_next_links()[1]+'_current.html\">' + products_dict[get_next_links()[1]] + '</a>\n'
footer += '                                                 | <a href=\"'+get_next_links()[2]+'_current.html\">' + products_dict[get_next_links()[2]] + '</a>\n'
footer += '                                                 | <a href=\"'+get_next_links()[3]+'_current.html\">' + products_dict[get_next_links()[3]] + '</a> | </span>\n'
footer += '                  </div>\n                </td>\n              </tr>\n            </table>\n          </td>\n        </tr>\n      </table>\n      </body>\n</html>\n'
#footer TODO: make generic for next year

def get_completed_year_table(completed_year):
    completed_year_table = '             <tr>\n                <td width=\"36\" style=\"border-width:1px;border-style:solid;border-color:#F0F2FF;\"> <div align=\"center\"><b><font color=\"#000000\" face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">' + completed_year + '</font></b></font></div><td>\n'
    for imonth in range(1, 13):
        completed_year_table += '                <td width=\"64\" style=\"border-width:1px;border-style:solid;border-color:#F0F2FF;\"> <div align=\"center\"><b><font color=\"#000000\" face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\"><a href=\"' \
                                                    + product + '_' + completed_year + str(imonth).zfill(2) + '.html\" target=\"_parent\">' + monthsDict[imonth] + '</a></font></b></div><td>\n'
    return (completed_year_table + '                </td>\n             </tr>\n')

def write_main_page():                                # here we create the main page
    # Remove main page if it exists:
    if os.path.exists(main_page):
        print("Removing old main page...\n")
        os.remove(main_page)
    
    print("Creating main page...")
    main_html_page = open(main_page, 'a')             # open the file for append
    print("Writing main header part...")
    for line in fileinput.input(main_header):
        main_html_page.write(line)                    # write header part
    print("Writing headline...")
    main_html_page.write(headline_tag)
    print("Writing front image part...")
    main_html_page.write(front_images_tag)             # write the code for the big daily image
    print("Writing months headline part...")
    main_html_page.write(months_headline_tag)
    print("Writing table opener")
    main_html_page.write('             <table width="100%" align="center" bgcolor="#BBDDDD">\n')
    #main_html_page.write('              <td width=\"36\" style=\"border-width:1px;border-style:solid;border-color:#F0F2FF;\">')
    #main_html_page.write(' <div align=\"center\"><b><font color=\"#000000\" face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">')
    
    if _year_last > '2006' :
        year_table_tags = ''
        n_completed = int(_year_last) - 2006
        for iyear in range(1, n_completed+1):
            year_table_tags += get_completed_year_table(str(2006 + n_completed - 1))
    
    main_html_page.write(year_table_tags)
    main_html_page.write('              <td width=\"36\" style=\"border-width:1px;border-style:solid;border-color:#F0F2FF;\"> <div align=\"center\"><b><font color=\"#000000\" face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">' + _year_last + '</font></b></font></div><td>\n')
    
    for i in range(1, 13):                      # loop over all months (1-12), skip 0 
        the_date = get_year_month_string(i)     # e.g. '200605'
        the_month = monthsDict[i]               # e.g. 'May'
        print("\nCreating table for " + the_month + "...")
            
        if (the_date >= start_date_of_processed and the_date <= (_year_first+_month_first)):
            months_table_tags =  '                <td width=\"64\" style=\"border-width:1px;border-style:solid;border-color:#F0F2FF;\">'
            months_table_tags += ' <div align=\"center\"><b><font color=\"#000000\" face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">'
            months_table_tags += '<a href=\"'+product+'_'+the_date+'.html\" target="_parent">'+the_month+'</a></font></b></div><td>\n'
            write_months_pages(the_date, the_month)
        else:
            months_table_tags =  '                <td width=\"64\" style=\"border-width:1px;border-style:solid;border-color:#F0F2FF;\">'
            months_table_tags += ' <div align=\"center\"><font color=\"#AADDAA\"><b><font face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">'
            months_table_tags += 'No data</font></b></font></div><td>\n'
        main_html_page.write(months_table_tags)

    print("Writing table closer")
    main_html_page.write('            </td>\n          </tr>\n        </table>\n')
    
    print("Writing main page footer part...")
    main_html_page.write(footer)
    print("Main page ready. ")
    main_html_page.close()

def write_months_pages(month_date, month_name):        # here we create the monthly pages

    # first we need to retrieve a list of all available images for this month
    src_list = os.listdir(base_images_dir)
    list_size = len( src_list )

    # Remove wrong files from list:
    for a in range( list_size ):
        for item in src_list:
            if not(item.startswith( month_date )) or not(item.endswith( '.jpg' )) or item.find(product)==-1 or item.find('bas')>0 or item.find('est')>0: # comment: we just need all image names that start with the month; we just arbitrarily chose to remove BalticSea and Estland to avoid double entries. We sort them below.
                src_list.remove( item )
                
    list_size = len(src_list)
    
    available_dates =[]
    for item in src_list:
        day_item = item[0:17]
        available_dates.append(day_item)
        
    if len(available_dates) == 0:          # do nothing if there are no available images for this month
        return
    
    available_dates.sort()
    #print '\n', available_dates, '\n'
    
    print('Creating detailed pages for ' + month_name + '...')
    monthly_page           = htmlDir + product + '_' + month_date + '.html'
    
    monthly_main_page_name = product + '_' + month_date + '_main.html'   # main frame
    monthly_main_page      = htmlDir + monthly_main_page_name
    
    monthly_list_page_name = product + '_' + month_date + '_list.html'   # bottom frame
    monthly_list_page      = htmlDir + monthly_list_page_name
    
    page_contents =  '<html>\n<head>\n'
    page_contents += '  <title>MERIS Water Constituents Archive</title>\n'
    page_contents += '  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\">\n'
    page_contents += '</head>\n'
    page_contents += '<frameset rows=\"492,192*\" frameborder=\"NO\" border=\"0\" framespacing=\"0\" cols=\"*\">\n'
    page_contents += '  <frame name=\"mainFrame\" src=\"' + monthly_main_page_name + '\">\n'
    page_contents += '  <frame name=\"bottomFrame\" scrolling=\"YES\" src=\"'+monthly_list_page_name +'\">\n'
    page_contents += '</frameset>\n'
    page_contents += '<noframes><body bgcolor=\"#FFFFFF\">\n'
    page_contents += '</body></noframes></html>\n'
     
    # Remove pages if they exists
    if os.path.exists(monthly_page):
        print("Removing old pages of " + month_name + "...")
        os.remove(monthly_page)
    if os.path.exists(monthly_main_page):
        os.remove(monthly_main_page)
    if os.path.exists(monthly_list_page):
        os.remove(monthly_list_page)
    monthly_html_page = open(monthly_page, 'a')
    monthly_html_page.write(page_contents)
    monthly_html_page.close()
        
    first_hires_image_names = get_hires_image_names(available_dates[0])
    first_lores_image_names = get_lores_image_names(available_dates[0])
    monthly_main_footer =  '         <tr>\n' 
    monthly_main_footer += '          <td> \n'
    monthly_main_footer += '            <div align="center\">\n'
    monthly_main_footer += '              <font face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"3\"><b>' + month_name + ' ' + _year_last + ' ' + products_dict[product] + ' Images</b></font>\n'
    monthly_main_footer += '                <table width=\"99%\" border=\"0\" align=\"center\">\n'
    monthly_main_footer += '                  <tr>\n'
    monthly_main_footer += '                    <td width=\"43%\"> \n'
    monthly_main_footer += '                      <div align=\"center\"><font face=\"Verdana, Arial\" size=\"1\"><a href=\"' + first_hires_image_names[0] + '\" target=\"_blank\"><img src=\"' + first_lores_image_names[0] + '\" width=\"353\" height=\"275\" border=\"0\"></a></font></div>\n'
    monthly_main_footer += '                    </td>\n'
    monthly_main_footer += '                    <td width=\"57%\"> \n'
    monthly_main_footer += '                      <div align=\"center\"><font face=\"Verdana, Arial\" size=\"1\"><a href=\"' + first_hires_image_names[1] + '\" target=\"_blank\"><img src=\"' + first_lores_image_names[1] + '\" width=\"466\" height=\"275\" border=\"0\"></a></font></div>\n'
    monthly_main_footer += '                    </td>\n'
    monthly_main_footer += '                  </tr>\n'
    monthly_main_footer += '                  <tr> \n'
    monthly_main_footer += '                    <td width=\"43%\"> \n'
    monthly_main_footer += '                      <div align=\"center\"><font face=\"Verdana, Arial\" size=\"1\"><b>First North Sea image of '  + products_dict[product] + ' for ' + month_name + '</b><br>' + get_text_display_date(available_dates[0]) + '</font></div>\n'
    monthly_main_footer += '                    </td>\n'
    monthly_main_footer += '                    <td width=\"57%\"> \n'
    monthly_main_footer += '                      <div align=\"center\"><font face=\"Verdana, Arial\" size=\"1\"><b>First Baltic Sea image of ' + products_dict[product] + ' for ' + month_name + '</b><br>' + get_text_display_date(available_dates[0]) + '</font></div>\n'
    monthly_main_footer += '                    </td>\n'
    monthly_main_footer += '                  </tr>\n'
    monthly_main_footer += '                </table>\n'
    monthly_main_footer += '              </div>\n'
    monthly_main_footer += '              <div align=\"center\"><font face=\"Verdana, Arial\" size=\"3\" color=\"#000000\"><b><img src=\"images/empty.gif\" width=\"400\" height=\"12\"><br>' + month_name + ' ' + _year_last + ' Daily ' + products_dict[product] + ' Images Archive </b></font></div>\n'
    monthly_main_footer += '            </td>\n        </tr>\n      </table>\n      </td>\n  </tr>\n</table>\n</body>\n</html>\n'
        
    monthly_main_html_page = open(monthly_main_page, 'a')
    for line in fileinput.input(months_main_header):
        monthly_main_html_page.write(line)                 # write header part
    
    monthly_main_html_page.write(monthly_main_footer)
    monthly_main_html_page.close()
    print("Done writing months main frame page for " + month_name)
    
    # Now the bottom frame page
    monthly_list_const_header ='<html>\n<head>\n<title>MERIS Daily Water Constituents Archive</title>'          + \
                               '\n<meta http-equiv="Content-Type\" content=\"text/html; charset=iso-8859-1\">\n'+ \
                               '</head>\n<body bgcolor=\"#FFFFFF\">\n<div align=\"center\">\n'                  + \
                               '  <table width=\"850\" border=\"0\">\n    <tr>\n      <td width=\"157\">'       + \
                               '<img src=\"images/empty.gif\" width=\"180\" height=\"90\"></td>\n'              + \
                               '      <td width=\"671\">\n        <table width=\"354\" border=\"1\" align=\"center\" bgcolor=\"#F0F2FF\">\n'
    monthly_list_html_page = open(monthly_list_page, 'a')
    monthly_list_html_page.write(monthly_list_const_header)

    # Now the table part
    table_row_opener  =  '          <tr>\n'
    table_row_closer  =  '          </tr>\n'
    table_col_openers = ['            <td width=\"75\" height=\"66\" valign=\"top\">\n', \
                         '            <td width=\"101\" height=\"66\">\n',               \
                         '            <td width=\"156\" height=\"66\">\n']
    table_col_closer =   '            </td>\n'
    
    # write a table with 10 rows and 3 columns
    image_count = 0
    num_days = len(available_dates)
    for row in range(31):
        monthly_list_html_page.write(table_row_opener)
        if (image_count < num_days):
            hires_images = get_hires_image_names(available_dates[image_count])
            thumb_images = get_thumb_image_names(available_dates[image_count])
            
            #print 'list_date_range = ' + list_date_range
            day_entry = table_col_openers[0] + \
                        '              <div align="center\"><font face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">'+ get_table_display_date(available_dates[image_count]) +' </font></div>\n' + \
                        table_col_closer + \
                        table_col_openers[1] + \
                        '              <div align=\"center\"><a href=\"' + hires_images[0] + '\" target=\"_blank\"><img src=\"' + thumb_images[0] + '\" width=\"118\" height=\"92\" border=\"0\"></a></div>\n' + \
                        table_col_closer + \
                        table_col_openers[2] + \
                        '              <div align=\"center\"><a href=\"' + hires_images[1] + '\" target=\"_blank\"><img src=\"' + thumb_images[1] + '\" width=\"155\" height=\"92\" border=\"0\"></a></div>\n' + \
                        table_col_closer
        else:
            day_entry = '            <td width="75\">&nbsp;</td>\n'  + \
                        '            <td width=\"101\">&nbsp;</td>\n' + \
                        '            <td width=\"156\">&nbsp;</td>\n'
        monthly_list_html_page.write(day_entry)
        image_count = image_count + 1
        monthly_list_html_page.write(table_row_closer)

    monthly_list_html_page.write('        </table>\n      </td>\n      <td width="8"><img src="images/empty.gif" width="312" height="90"></td>\n    </tr>\n  </table>\n</div>\n</body>\n</html>\n')
    monthly_list_html_page.close()
    

write_main_page()


print("\n*******************************************************")
print(" Script \'make_MC_weekly_L3_wac_website.py\' finished.  ")
print("*******************************************************\n")

# EOF
