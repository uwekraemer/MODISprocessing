#!/usr/bin/env python
# -*- coding: latin-1 -*-
# file: make_mosaic_website.py

import os
import os.path
import sys
import time
import fileinput

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

def get_ql_image_name(prefix):
    return prefix + '_mosaic.jpg'

def get_web_image_name(prefix):
    return '/images/daily_mosaics/web_images/' + prefix + '_mosaic_cr.jpg'

def get_thumb_image_name(prefix):
    return '/images/daily_mosaics/thumbs/'     + prefix + '_mosaic_small.jpg'

def get_icon_image_name(prefix):
    return '/images/daily_mosaics/icons/'      + prefix + '_mosaic_icon.jpg'

print("\n********************************************")
print(" Script \'make_mosaic_website.py\' at work... ")
print("********************************************\n")

start_date_of_mosaics = '200605'

# Configure the day to use for the current image relative to the actual date (1 = yesterday, 2 = the day before yesterday...)
back_days = 1

arrival_day=get_date_string(get_float_day(back_days))
_year  = arrival_day[0:4]
_month = arrival_day[4:6]
_day   = arrival_day[6:8]
 
def get_display_date(date_string):
    return date_string[6:8] + '.' + date_string[4:6] + '.' + date_string[0:4]

def get_localised_date():
 return get_display_date(arrival_day)

latest_three_mosaic_days = [get_date_string(get_float_day(back_days+1)), \
                            get_date_string(get_float_day(back_days+2)), \
                            get_date_string(get_float_day(back_days+3))]

# Directories
toolsDir = '/home/uwe/tools/mosaic/web_resources/'
baseDir = '/fs14/EOservices/Repositories/MERIS/RR/DDSrepository/'
srcDir  = baseDir + _year + '/' + _month+ '/'
tempProcDir = '/fs14/temp/'
mosaicsBaseDir = '/fs14/EOservices/OutputPool/quicklooks/daily_mosaics/'
htmlDir = mosaicsBaseDir + 'html/'

#toolsDir = '/Volumes/UWE/tools/mosaic/web_resources/'
#baseDir = '/Volumes/FS14/EOservices/Repositories/MERIS/RR/DDSrepository/'
#srcDir  = baseDir + _year + '/' + _month+ '/'
#tempProcDir = '/Volumes/FS14/temp/'
#mosaicsBaseDir = '/Volumes/FS14/EOservices/OutputPool/quicklooks/daily_mosaics/'

webImagesDir = mosaicsBaseDir + 'web_images/'
rawImagesDir = mosaicsBaseDir + _year + '/' + _month + '/'     # must exist
if not os.path.exists(rawImagesDir):
    print("Creating directory: " + rawImagesDir)
    os.mkdir(rawImagesDir)

main_page           = htmlDir  + 'mosaic.html'
# these files contain constant text and are read by fileinput
main_header         = toolsDir + 'main_header.txt'          # constant header part
main_table_footer   = toolsDir + 'main_table_footer.txt'    # constant table 
months_main_header  = toolsDir + 'months_main_header.txt'   # constant header part
months_list_js_part = toolsDir + 'list_page_js_part.txt'    # constant javascript code part

# File names for output
ql_output_filename    = get_ql_image_name(rawImagesDir  + arrival_day)    # image without watermark and text: + '_mosaic.jpg'
web_output_filename   = get_web_image_name(mosaicsBaseDir  + arrival_day)   # for web: hires image with watermarks and text : + '_mosaic_cr.jpg'
tn_output_filename    = get_thumb_image_name(mosaicsBaseDir + arrival_day) # for web: 10% scaled images: + '_mosaic_small.jpg' 
icn_output_filename   = get_icon_image_name(mosaicsBaseDir  + arrival_day)  # for web:  5% scaled images: + '_mosaic_icon.jpg'

front_image_tag ='\n            <div align=\"center\"><font face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"2\"><a href=\"'+ get_web_image_name(arrival_day)
front_image_tag = front_image_tag +'\"><img src=\"' + get_thumb_image_name(arrival_day)
front_image_tag = front_image_tag + '\" width="810" height="405" border="0"></a><br>MERIS Mosaic Image for ' + get_localised_date() + '</font></div>\n'

latest_three_mosaics_table =                              '            <table width=\"810\" border=\"0\" align=\"center\">\n'
latest_three_mosaics_table = latest_three_mosaics_table + '              <tr> \n                <td><a href=\"'+get_web_image_name(latest_three_mosaic_days[0])
latest_three_mosaics_table = latest_three_mosaics_table + '\"><img src=\"'+get_icon_image_name(latest_three_mosaic_days[0])
latest_three_mosaics_table = latest_three_mosaics_table + '\" width=\"270\" height=\"135\" border=\"0\"></a></td>\n'
latest_three_mosaics_table = latest_three_mosaics_table + '                <td><a href=\"'+get_web_image_name(latest_three_mosaic_days[1])
latest_three_mosaics_table = latest_three_mosaics_table + '\"><img src=\"'+get_icon_image_name(latest_three_mosaic_days[1])
latest_three_mosaics_table = latest_three_mosaics_table + '\" width=\"270\" height=\"135\" border=\"0\"></a></td>\n'
latest_three_mosaics_table = latest_three_mosaics_table + '                <td><a href=\"'+get_web_image_name(latest_three_mosaic_days[2])
latest_three_mosaics_table = latest_three_mosaics_table + '\"><img src=\"'+get_icon_image_name(latest_three_mosaic_days[2])
latest_three_mosaics_table = latest_three_mosaics_table + '\" width=\"270\" height=\"135\" border=\"0\"></a></td>\n'
latest_three_mosaics_table = latest_three_mosaics_table + '              </tr>\n              <tr> \n                <td> \n                  '
latest_three_mosaics_table = latest_three_mosaics_table + '<div align=\"center\"><font face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">MERIS Mosaic Image for '
latest_three_mosaics_table = latest_three_mosaics_table + latest_three_mosaic_days[0][6:8] + '.' + latest_three_mosaic_days[0][4:6] + '.' + latest_three_mosaic_days[0][0:4] 
latest_three_mosaics_table = latest_three_mosaics_table + '</font></div>\n                </td>\n                <td> \n'
latest_three_mosaics_table = latest_three_mosaics_table + '                  <div align=\"center\"><font face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">'
latest_three_mosaics_table = latest_three_mosaics_table + 'MERIS Mosaic Image for '+ latest_three_mosaic_days[1][6:8] + '.' + latest_three_mosaic_days[1][4:6] + '.' + latest_three_mosaic_days[1][0:4] 
latest_three_mosaics_table = latest_three_mosaics_table + '</font></div>\n                </td>\n                <td> \n'
latest_three_mosaics_table = latest_three_mosaics_table + '                  <div align=\"center\"><font face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">'
latest_three_mosaics_table = latest_three_mosaics_table + 'MERIS Mosaic Image for '+ latest_three_mosaic_days[2][6:8] + '.' + latest_three_mosaic_days[2][4:6] + '.' + latest_three_mosaic_days[2][0:4]
latest_three_mosaics_table = latest_three_mosaics_table + '</font></div>\n                </td>\n              </tr>\n            </table>\n'

table_closer =                '                <td width=\"64\" style=\"border-width:1px;border-style:solid;border-color:#F0F2FF;\"> \n'
table_closer = table_closer + '                  <div align=\"center\"><b><font color=\"#000000\" face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">'
table_closer = table_closer + '<a href=\"mosaic_may06.html\">May</a></font></b></div>'      # TODO: add all available months

footer =          '                </td>\n              </tr>\n'
footer = footer + '            </table><img src="../images/empty.gif" width="400" height="8"> \n'
footer = footer + '            </td>\n        </tr>\n      </table>\n      </td>\n  </tr>\n</table>\n</body>\n</html>'
#footer TODO: make generic for next year

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
    print("Writing front image part...")
    main_html_page.write(front_image_tag)             # write the code for the big daily mosaic image
    print("Writing three images table part...")
    main_html_page.write(latest_three_mosaics_table)
    print("Writing main table footer part...")
    for line in fileinput.input(main_table_footer):
        main_html_page.write(line)                    # write table footer part
    
    for i in range(13):                               # loop over all months (1-12), skip 0 
        if i == 0: continue
        else:
            the_date = get_year_month_string(i)       # e.g. '200605'
            the_month = monthsDict[i]                 # e.g. 'May'
            print("\nCreating table for " + the_month + "...")
            
        if (the_date >= start_date_of_mosaics and the_date <= (_year+_month)):
            months_table_tags =                     '                <td width=\"64\" style=\"border-width:1px;border-style:solid;border-color:#F0F2FF;\">'
            months_table_tags = months_table_tags + ' <div align=\"center\"><b><font color=\"#000000\" face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">'
            months_table_tags = months_table_tags + '<a href=\"mosaics_'+the_date+'.html\">'+the_month+'</a></font></b></div><td>\n'
            write_months_pages(the_date, the_month)          # write detailed archive page for each month
        else:
            months_table_tags =                     '                <td width=\"64\" style=\"border-width:1px;border-style:solid;border-color:#F0F2FF;\">'
            months_table_tags = months_table_tags + ' <div align=\"center\"><font color=\"#AADDAA\"><b><font face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">'
            months_table_tags = months_table_tags + 'None</font></b></font></div><td>\n'
        main_html_page.write(months_table_tags)
    
    print("Writing main page footer part...")
    main_html_page.write(footer)
    print("Main page ready. ")
    main_html_page.close()


def write_months_pages(month_date, month_name):        # here we create the monthly pages
    print('Creating detailed pages for ' + month_name + '...')
    monthly_page           = htmlDir + 'mosaics_' + month_date + '.html'
    monthly_main_page_name = 'mosaics_' + month_date + '_main.html'   # main frame
    monthly_main_page      = htmlDir + monthly_main_page_name
    monthly_list_page_name = 'mosaics_' + month_date + '_list.html'   # bottom frame
    monthly_list_page      = htmlDir + monthly_list_page_name
    page_contents =                 '<html>\n<head>\n'
    page_contents = page_contents + '  <title>MERIS DAILY MOSAIC ARCHIVE</title>\n'
    page_contents = page_contents + '  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\">\n'
    page_contents = page_contents + '</head>\n'
    page_contents = page_contents + '<frameset rows=\"580,192*\" frameborder=\"NO\" border=\"0\" framespacing=\"0\" cols=\"*\">\n'
    page_contents = page_contents + '  <frame name=\"mainFrame\" src=\"'+ monthly_main_page_name + '\">\n'
    page_contents = page_contents + '  <frame name=\"bottomFrame\" scrolling=\"YES\" src=\"' + monthly_list_page_name 
    page_contents = page_contents + '\">\n</frameset>\n<noframes>\n'+'  <body bgcolor=\"#FFFFFF\">\n  </body>\n</noframes>\n</html>\n'
    
    # Remove pages if they exists
    if os.path.exists(monthly_page):
        os.remove(monthly_page)
    if os.path.exists(monthly_main_page):
        os.remove(monthly_main_page)
    if os.path.exists(monthly_list_page):
        os.remove(monthly_list_page)
    monthly_html_page = open(monthly_page, 'a')
    monthly_html_page.write(page_contents)
    monthly_html_page.close()
        
    #    here we need to retrieve a list of all available images for this month
    src_list = os.listdir(webImagesDir)
    list_size = len( src_list )

    # Remove wrong files from list:
    for a in range( list_size ):
        for item in src_list:
            if item.startswith( month_date )==0 or item.endswith( '.jpg' )==0:
                print("Removing " + item + " from list.")
                src_list.remove( item )
                
    list_size = len(src_list)
    available_dates =[]
    for item in src_list:
        day_item = item[0:8]
        available_dates.append(day_item)
        
    available_dates.sort()

    monthly_main_footer =                       '        <tr>\n' 
    monthly_main_footer = monthly_main_footer + '          <td>' 
    monthly_main_footer = monthly_main_footer + '            <div align=\"center\"><font face=\"Verdana, Arial\" size=\"2\"><b><font size=\"3\">' + month_name + '\n'
    monthly_main_footer = monthly_main_footer + '              '+ month_date[0:4] + ' MERIS Mosaic Image</font></b></font></div>\n'
    monthly_main_footer = monthly_main_footer + '            <div align=\"center\"><font face=\"Verdana, Arial\" size=\"2\"><a href=\"javascript:parent.bottomFrame.showHugeImage()\"><img name=\"mosaic_810\" src=\"'+ get_thumb_image_name(available_dates[0]) +'\" width=\"810\" height=\"405\" border=\"0\"></a><br>\n'
    monthly_main_footer = monthly_main_footer + '              </font>\n'
    monthly_main_footer = monthly_main_footer + '              <table width=\"810\" border=\"0\">\n'
    monthly_main_footer = monthly_main_footer + '                <tr>\n'
    monthly_main_footer = monthly_main_footer + '                  <td width=\"85\"><b><font face=\"Verdana, Arial\" size=\"1\"><a href=\"javascript:parent.bottomFrame.showPrevious()\">&lt;\n'
    monthly_main_footer = monthly_main_footer + '                    previous</a></font></b></td>\n'
    monthly_main_footer = monthly_main_footer + '                  <td width=\"633\">\n'
    monthly_main_footer = monthly_main_footer + '                    <div align=\"center\">\n'
    monthly_main_footer = monthly_main_footer + '                      <form name=\"form1\" class=\"img_dat_form\">\n'
    monthly_main_footer = monthly_main_footer + '                        <input type=\"text\" id=\"image_datum\" size=\"30\" style=\"font-family:Verdana, Arial; font-size:9px\" value=\"Mosaic Image for ' + get_display_date(available_dates[0]) + '\">\n'
    monthly_main_footer = monthly_main_footer + '                      </form></div>\n'
    monthly_main_footer = monthly_main_footer + '                  </td>\n'
    monthly_main_footer = monthly_main_footer + '                  <td width=\"78\">\n'
    monthly_main_footer = monthly_main_footer + '                    <div align=\"right\"><b><font face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">'
    monthly_main_footer = monthly_main_footer + '                         <a href=\"javascript:parent.bottomFrame.showNext()\">next &gt;</a></font></b></div>\n'
    monthly_main_footer = monthly_main_footer + '                  </td>\n'
    monthly_main_footer = monthly_main_footer + '                </tr>\n'
    monthly_main_footer = monthly_main_footer + '              </table>\n'
    monthly_main_footer = monthly_main_footer + '              <font face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"2\"> </font></div>\n'
    monthly_main_footer = monthly_main_footer + '            <div align=\"center\"><font face=\"Verdana, Arial\" size=\"3\" color=\"#000000\"><b><img src=\"../images/empty.gif\" width=\"400\" height=\"6\"><br>\n'
    monthly_main_footer = monthly_main_footer + '              ' + month_name + ' Daily MERIS Mosaic Images Archive </b></font></div>\n'
    monthly_main_footer = monthly_main_footer + '            </td>\n'
    monthly_main_footer = monthly_main_footer + '        </tr>\n'
    monthly_main_footer = monthly_main_footer + '      </table>\n'
    monthly_main_footer = monthly_main_footer + '      </td>\n'
    monthly_main_footer = monthly_main_footer + '  </tr>\n'
    monthly_main_footer = monthly_main_footer + '</table>\n'
    monthly_main_footer = monthly_main_footer + '</body>\n'
    monthly_main_footer = monthly_main_footer + '</html>\n'
    
    
    monthly_main_html_page = open(monthly_main_page, 'a')
    for line in fileinput.input(months_main_header):
        monthly_main_html_page.write(line)                 # write header part
    
    monthly_main_html_page.write(monthly_main_footer)
    monthly_main_html_page.close()
    print("Done writing months main frame page for " + month_name)
    
    # Now the bottom frame page
    monthly_list_const_header =                            '<html>\n'
    monthly_list_const_header = monthly_list_const_header + '<head>\n'
    monthly_list_const_header = monthly_list_const_header + '<title>MERIS Daily Mosaic Archive</title>\n'
    monthly_list_const_header = monthly_list_const_header + '<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\">\n'
    monthly_list_const_header = monthly_list_const_header + '<script language=\"JavaScript\">\n'
    monthly_list_const_header = monthly_list_const_header + 'Mosaics = new Array();\n'   

    monthly_list_html_page = open(monthly_list_page, 'a')
    monthly_list_html_page.write(monthly_list_const_header)

    num_days = len(available_dates)
    
    for a in range(31):
        if (a < num_days):
            daily_line = 'Mosaics[' + str(a) + '] = \"' + available_dates[a] + '\"\n'    # e.g. Mosaics[0] = "20060505"
        else:
            daily_line = 'Mosaics[' + str(a) + '] = \"no\"\n'                            # e.g. Mosaics[3] = "no"
        monthly_list_html_page.write(daily_line)

    # write constant javascript code
    for line in fileinput.input(months_list_js_part):
        monthly_list_html_page.write(line)                 # write header part

    # Now the table part
    monthly_list_table_header = '<body bgcolor=\"#FFFFFF\" onLoad=\"init();\">\n<div align=\"center\">\n\n  <table width=\"840\" border=\"1\" align=\"center\" bgcolor=\"#F0F2FF\">\n'
    monthly_list_html_page.write(monthly_list_table_header)
    table_row_opener = '    <tr>\n'
    table_row_closer = '    </tr>\n'
    table_col_opener = '      <td>\n'
    table_col_closer = '      </td>\n'
    
    # write a table with 10 rows and 3 columns
    image_count = 0
    for row in range(11):
        monthly_list_html_page.write(table_row_opener)
        for column in range(3):
            monthly_list_html_page.write(table_col_opener)
            if (image_count < num_days):
                day_entry = '        <div align=\"center\"><a href=\"javascript:show810Image(' + str(image_count) +')\"><img src=\"' + get_icon_image_name(available_dates[image_count]) + '\" width=\"270\" height=\"135\" border=\"0\"></a><br><font face=\"Verdana, Arial, Helvetica, sans-serif\" size=\"1\">'+ get_display_date(available_dates[image_count]) +'</font></div>\n'
            else:
                day_entry = '        &nbsp;\n'
            monthly_list_html_page.write(day_entry)
            monthly_list_html_page.write(table_col_closer)
            image_count = image_count + 1
        monthly_list_html_page.write(table_row_closer)

    monthly_list_html_page.write('  </table>\n</div>\n</body>\n</html>')
    monthly_list_html_page.close()
    

write_main_page()


print("\n********************************************")
print(" Script \'make_mosaic_website.py\' finished.  ")
print("********************************************\n")

# EOF
