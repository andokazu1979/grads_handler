#! /usr/bin/env python

class ScriptMakerGrADS(object):
    """ScriptMakerGrADS"""

    def __init__(self, calc, filepath, lev=None, varname=None):
        """__init__ """
        self.str_parameters = ""
        self.str_global_settings = ""
        self.str_open_files = ""
        self.str_setting_after_open = ""
        self.str_draw_variables = ""
        self.str_draw_landform = ""
        self.str_draw_colorbar = ""
        self.str_draw_title = ""
        self.str_string = ""
        self.str_output_figures = ""
        self.str_finalize = ""

        self.calc = calc
        figure_cond = calc['figure_cond']
        self.figure_cond = figure_cond
        self.filepath = filepath
        self.cbar_drawed = False

        if lev is None:
            self.lev = figure_cond['lev']
        else:
            self.lev = lev

        if varname is None:
            self.lst_var = figure_cond['var']
        else:
            if lev == '0':
                self.lst_var = figure_cond[varname]
            else:
                self.lst_var = figure_cond[lev][varname]

        if varname is None:
            self.title = figure_cond['title']
        else:
            if lev == '0':
                self.title = figure_cond[varname][0]['title']
            else:
                self.title = figure_cond[lev][varname][0]['title']

        if varname is None:
            self.header = figure_cond['header']
        else:
            if lev == '0':
                self.header = figure_cond[varname][0]['header']
            else:
                self.header = figure_cond[lev][varname][0]['header']

    def set_str_parameters(self):
        self.str_parameters += """
****************************************
* Function definition for main
****************************************

"""[1:]

        for index, var in enumerate(self.lst_var):
            if 'dirpath' in var:
                path = var['dirpath']
            else:
                path = self.ipath
            self.str_parameters += "fpath_var{0}='{1}/{2}'\n".format(
                    index + 1,
                    path,
                    var['fname'],
                    )
            self.str_parameters += "name_var{0}='{1}'\n".format(index + 1, var['vname'])
            if 'fname_mask' in var:
                if 'dirpath_mask' in var:
                    path = var['dirpath_mask']
                else:
                    path = self.ipath
                self.str_parameters += "fpath_var_mask{0}='{1}/{2}'\n".format(
                        index + 1,
                        path,
                        var['fname_mask'],
                        )
                self.str_parameters += "name_var_mask{0}='{1}'\n".format(index + 1, var['vname_mask'])
        self.str_parameters += "title='{0}'\n".format(self.title)
        self.str_parameters += "header='{0}'\n".format(self.header)
        # if(self.figure_cond['coord'] == 'xy'):
            # self.str_parameters += "fpath_land='{0}'\n".format(self.figure_cond['filepath_topo'])
        self.str_parameters += "xmin='{0}'\n".format(self.figure_cond['xmin'])
        self.str_parameters += "xmax='{0}'\n".format(self.figure_cond['xmax'])
        self.str_parameters += "ymin='{0}'\n".format(self.figure_cond['ymin'])
        self.str_parameters += "ymax='{0}'\n".format(self.figure_cond['ymax'])
        self.str_parameters += "t_='{0}'\n".format(self.index_t)
        self.str_parameters += "t__='{0}'\n".format(self.index_t2)
        self.str_parameters += "tstr='{0}'\n".format(self.tstr)
        self.str_parameters += "\n"

    def set_str_global_settings(self):
        self.str_global_settings += """
****************************************
* Initial setting
****************************************

* Set background color to white
'set display color white'

* Font of label for x-direction (color thickness size)
'set xlopts {0} {1} {2}' 

* Font of label for y-direction (color thickness size)
'set ylopts {3} {4} {5}' 

* Set as grfill
'set gxout grfill'

* Clear screen
'c'

* Set rectangle area for figure
'set parea {6} {7} {8} {9}'

* Remove logo of GrADS
'set grads off'
"""[1:].format(
        self.figure_cond['font_x_color'],
        self.figure_cond['font_x_thickness'],
        self.figure_cond['font_x_size'],
        self.figure_cond['font_y_color'],
        self.figure_cond['font_y_thickness'],
        self.figure_cond['font_y_size'],
        self.figure_cond['parea_xmin'],
        self.figure_cond['parea_xmax'],
        self.figure_cond['parea_ymin'],
        self.figure_cond['parea_ymax'],
        )

        if(self.figure_cond['coord'] == 'xy'):
            self.str_global_settings += """
'set mproj off'
"""[1:]
        elif(self.figure_cond['coord'] == 'latlon'):
            self.str_global_settings += """
'set mproj latlon'
'set map 1 1 7.5'
'set mpdset hires'
"""[1:]

        self.str_global_settings += """
* Set interval for label and auxiliary line for x-direction
'set xlint {0}'

* Set interval for label and auxiliary line for y-direction
'set ylint {1}'


"""[1:].format(
        self.figure_cond['xlint'],
        self.figure_cond['ylint'],
        )

    def set_str_open_files(self):
        self.str_open_files += """
****************************************
* Open files
****************************************

"""[1:]#.format()

        for index, var in enumerate(self.lst_var):
            self.str_open_files += "'open 'fpath_var{0}\n".format(index + 1)
            if 'fname_mask' in var:
                self.str_open_files += "'open 'fpath_var_mask{0}\n".format(index + 1)
        # if(self.figure_cond['coord'] == 'xy'):
            # self.str_open_files += "'open 'fpath_land\n"
        self.str_open_files += "\n"

    def set_str_setting_after_open(self):
        if self.tstr is None:
            self.str_setting_after_open = """
* Set lon and lat
'set lon 'xmin' 'xmax
'set lat 'ymin' 'ymax

* Set time
'set t 't_

"""[1:]
        else:
            self.str_setting_after_open = """
* Set lon and lat
'set lon 'xmin' 'xmax
'set lat 'ymin' 'ymax

* Set time
'set time 'tstr

"""[1:]

        if self.lev is not None:
            self.str_setting_after_open += """
* Set level of z-direction
'set lev {0}'


"""[1:].format(self.lev)

    def set_str_draw_variables(self):
        self.str_draw_variables += """
****************************************
* Draw variables
****************************************

"""[1:]#.format()

        flag = False
        index_var = -1
        index_file = 0
        for var in self.lst_var:
            index_var += 1
            index_file += 1
            if flag:
                flag = False
                continue
            self.str_draw_variables += "'set gxout {0}'\n".format(var['type'])
            if 'ccolor' in var:
                self.str_draw_variables += """
'set ccolor {0}'
"""[1:].format(var['ccolor'])

            if 'clevs' in var:
                self.str_draw_variables += "'set clevs {0}'\n".format(" ".join(var['clevs']))
            elif 'cint' in var:
                self.str_draw_variables += "'set cint {0}'\n".format(var['cint'])

            if 'clab' in var:
                self.str_draw_variables += "'set clab {0}'\n".format(var['clab'])

            if 'clskip' in var:
                self.str_draw_variables += "'set clskip {0}'\n".format(var['clskip'])

            if 'rgb' in var:
                self.str_draw_variables += """
'set rgb {0}'
"""[1:].format(var['rgb'])

            if 'rgb1' in var:
                self.str_draw_variables += """
'set rgb {0}'
"""[1:].format(var['rgb1'])

            if 'rgb2' in var:
                self.str_draw_variables += """
'set rgb {0}'
"""[1:].format(var['rgb2'])

            if 'ccols' in var:
                self.str_draw_variables += """
'set ccols  {0}'
"""[1:].format(var['ccols'])

            if 'factor' in var:
                factor = var['factor']
            else:
                factor = 1

            if 'skip_interval' in var:
                skip_interval = var['skip_interval']
            else:
                skip_interval = 1

            if 'cmin' in var:
                self.str_draw_variables += "'set cmin {0}'\n".format(var['cmin'])

            if 'arrscl' in var:
                self.str_draw_variables += "'set arrscl {0} {1}'\n".format(var['arrscl'][0], var['arrscl'][1])

            if 'vector' == var['type']:
                if 'use_second_time' in var:
                    self.str_draw_variables += "'d skip('name_var{0}'.{0}(t='t__'),{2},{2});'name_var{1}'.{1}'\n".format(index_var + 1, index_var + 2, skip_interval)
                else:
                    if 'diff' in var:
                        self.str_draw_variables += "'d skip('name_var{0}'.{2} - 'name_var_mask{0}'.{3},{6},{6});'name_var{1}'.{4} - 'name_var_mask{1}'.{5}'\n".format(index_var + 1, index_var + 2, index_file,  index_file + 1, index_file + 2, index_file + 3, skip_interval)
                        self.str_draw_variables += "\n"
                        break
                    elif 'lterp' in var:
                        self.str_draw_variables += "'d skip(lterp('name_var{0}'.{2}, 'name_var_mask{0}'.{3}) - 'name_var_mask{0}'.{3},{6},{6});lterp('name_var{1}'.{4}, 'name_var_mask{1}'.{5}) - 'name_var_mask{1}'.{5}'\n".format(index_var + 1, index_var + 2, index_file,  index_file + 1, index_file + 2, index_file + 3, skip_interval)
                        self.str_draw_variables += "\n"
                        break
                    else:
                        self.str_draw_variables += "'d skip('name_var{0}'.{0},{2},{2});'name_var{1}'.{1}'\n".format(index_var + 1, index_var + 2, skip_interval)
                flag = True
            else:
                if 'use_second_time' in var:
                    self.str_draw_variables += "'d 'name_var{0}'.{0}(t='t__') * {1}'\n".format(index_var + 1, factor)
                else:
                    if 'fname_mask' in var:
                        if 'diff' in var:
                            self.str_draw_variables += "'d ('name_var{0}'.{1} - 'name_var_mask{0}'.{2}) * {3}'\n".format(index_var + 1, index_file, index_file + 1, factor)
                        elif 'lterp' in var:
                            # self.str_draw_variables += "'d (lterp('name_var_mask{0}'.{2}, 'name_var{0}'.{1}) - 'name_var{0}'.{1}) * {3}'\n".format(index_var + 1, index_file, index_file + 1, factor)
                            self.str_draw_variables += "'d (lterp('name_var{0}'.{1}, 'name_var_mask{0}'.{2}) - 'name_var_mask{0}'.{2}) * {3}'\n".format(index_var + 1, index_file, index_file + 1, factor)
                        else:
                            self.str_draw_variables += "'d maskout('name_var{0}'.{1},'name_var_mask{0}'.{2}) * {3}'\n".format(index_var + 1, index_file, index_file + 1, factor)
                        index_file += 1
                    else:
                        self.str_draw_variables += "'d 'name_var{0}'.{1} * {2}'\n".format(index_var + 1, index_file, factor)

            if 'cbar' in var:
                if 'on' == var['cbar']:
                    self.str_draw_variables += "'cbarn'\n"
                    self.cbar_drawed = True

            self.str_draw_variables += "\n"

    def set_str_draw_landform(self):
        # if(self.figure_cond['coord'] == 'xy'):
            # self.str_draw_landform += """
# ****************************************
# * Draw land form (contour)
# ****************************************

# * Enable contour
# 'set gxout contour'

# 'set clevs {0}'
# 'set cthick {1}'

# * Unset label for contour
# 'set clab off'

# 'set ccolor {2}'

# 'd lsmask.{3}(t=1)'

# """[1:].format(
        # self.figure_cond['land_clevs'],
        # self.figure_cond['land_cthick'],
        # self.figure_cond['land_ccolor'],
        # len(self.lst_var) + 1,
        # )
        pass

    def set_str_draw_colorbar(self):
        self.str_draw_colorbar += """
****************************************
* Color bar
****************************************

* Show color-bar
'cbarn'

"""[1:]

    def set_str_draw_title(self):
        self.str_draw_title += """
****************************************
* Title
****************************************

* Draw title
'q time'
var = result
time_ = subwrd(var,3)

'draw title 'title' 'time_

"""[1:]

    def set_str_string(self):
        self.str_string += """
****************************************
* String
****************************************

* Draw string
'set string 1'
'draw string {0} {1} {2}'

"""[1:].format(self.figure_cond['string'][0], self.figure_cond['string'][1], self.string)

    def set_str_output_figures(self):
        self.str_output_figures += """
****************************************
* Output figure
****************************************

* Output figure as file
'printim {0}/{1}_'time_'.png'

"""[1:].format(
        self.opath,
        self.header,
        )

    def set_str_finalize(self):
        self.str_finalize += """
* Clear screen
'c'

"""[1:]

        # if(self.figure_cond['coord'] == 'xy'):
            # self.str_finalize += "'close {0}'\n".format(len(self.lst_var) + 1)
        num = 0
        for index, var in enumerate(self.lst_var):
            if 'fname_mask' in var:
                num += 1
        for index in range(len(self.lst_var) + num, 0, -1):
            self.str_finalize += "'close {0}'\n".format(index)
        self.str_finalize += "\n"

        self.str_finalize += """
'quit'

"""[1:]


    def get_str(self):
        """get_str"""
        self.str_parameters = ""
        self.str_global_settings = ""
        self.str_open_files = ""
        self.str_setting_after_open = ""
        self.str_draw_variables = ""
        self.str_draw_landform = ""
        self.str_draw_colorbar = ""
        self.str_draw_title = ""
        self.str_string = ""
        self.str_output_figures = ""
        self.str_finalize = ""

        self.set_str_parameters()
        self.set_str_global_settings()
        self.set_str_open_files()
        self.set_str_setting_after_open()
        self.set_str_draw_variables()
        self.set_str_draw_landform()
        if self.cbar_drawed == False:
            self.set_str_draw_colorbar()
        self.set_str_draw_title()
        if 'string' in self.figure_cond:
            self.set_str_string()
        self.set_str_output_figures()
        self.set_str_finalize()

        str_script = ""\
            + self.str_parameters \
            + self.str_global_settings \
            + self.str_open_files \
            + self.str_setting_after_open \
            + self.str_draw_variables \
            + self.str_draw_landform \
            + self.str_draw_colorbar \
            + self.str_draw_title \
            + self.str_string \
            + self.str_output_figures \
            + self.str_finalize

        return str_script

    def output(self, ipath, opath, index_t = -1, index_t2 = -1, string = None, tstr = None):
        self.ipath = ipath
        self.opath = opath
        self.index_t = index_t
        self.index_t2 = index_t2
        self.string = string
        self.tstr = tstr
        with open(self.filepath, "w") as f:
            f.write(self.get_str())


