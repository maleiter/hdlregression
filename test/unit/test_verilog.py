# ================================================================================================================================
#  Copyright 2021 Bitvis
#  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 and in the provided LICENSE.TXT.
#
#  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
#  an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and limitations under the License.
# ================================================================================================================================
#  Note : Any functionality not explicitly described in the documentation is subject to change at any time
# --------------------------------------------------------------------------------------------------------------------------------

import pytest
import sys
import os
import shutil

from hdlregression import HDLRegression


exp_modules = ['top',
               'fifo',
               'port_fsm',
               'switch',
               'simple_module',
               'mydesignsub',
               'tb_top',
               'half_adder',
               'half_adder_tb',
               'tb',
               'dff',
               'd_ff']

if len(sys.argv) >= 2:
    '''
    Remove pytest from argument list
    '''
    sys.argv.pop(1)


def get_file_path(path) -> str:
    '''
    Adjust file paths to match running directory.
    '''
    TEST_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(TEST_DIR, path)


def clear_output():
    if os.path.isdir('./hdlregression'):
        shutil.rmtree('./hdlregression')


def setup_function():
    if os.path.isdir('./hdlregression'):
        print('WARNING! hdlregression folder already exist!')


def tear_down_function():
    if os.path.isdir('./hdlregression'):
        shutil.rmtree('./hdlregression')


def test_verilog_modules():
    clear_output()
    hr = HDLRegression()

    filename = '../tb/verilog/half_adder*.v'
    filename = get_file_path(filename)
    hr.add_files(filename, 'verilog_lib')

    hr.start()

    library = hr._get_library_object('verilog_lib')
    file_list = library.get_hdlfile_list()

    assert len(file_list) == 2, "check verilog files in project"


def test_compile_order():
    clear_output()
    hr = HDLRegression()

    filename = '../tb/verilog/half_adder*.v'
    filename = get_file_path(filename)
    hr.add_files(filename, 'verilog_lib')

    hr.start()

    library = hr._get_library_object('verilog_lib')
    file_list = library.get_hdlfile_list()

    assert 'half_adder.v' in file_list[0].get_filename_with_path(), "check compile order"
    assert 'half_adder_tb.v' in file_list[1].get_filename_with_path(
    ), "check compile order"


def test_module_name():
    clear_output()
    hr = HDLRegression()

    filename = '../tb/verilog/half_adder*.v'
    filename = get_file_path(filename)
    hr.add_files(filename, 'verilog_lib')

    hr.start()

    library = hr._get_library_object('verilog_lib')
    file_list = library.get_hdlfile_list()

    assert 'half_adder' in file_list[0].get_name(), "check module name"
    assert 'half_adder_tb' in file_list[1].get_name(), "check module name"


def test_testbench_pragma():
    clear_output()
    hr = HDLRegression()

    filename = '../tb/verilog/half_adder*.v'
    filename = get_file_path(filename)
    hr.add_files(filename, 'verilog_lib')

    hr.start()

    library = hr._get_library_object('verilog_lib')
    file_list = library.get_hdlfile_list()

    assert file_list[1].get_is_tb() == True, "check testbench pragma %s" % (file_list)


def test_number_of_module_detected():
    clear_output()
    hr = HDLRegression()

    filename = '../tb/verilog/*.v'
    filename = get_file_path(filename)
    hr.add_files(filename, 'verilog_lib')
    hr.set_result_check_string('Simulation end')

    hr.start()

    library = hr._get_library_object('verilog_lib')

    modules = library._get_list_of_lib_modules()
    
    names = [module.get_name() for module in modules]

    assert len(modules) == len(exp_modules), "check number of detected verilog modules %s" % (names)


def test_modules_detected():
    clear_output()
    hr = HDLRegression()

    filename = '../tb/verilog/*.v'
    filename = get_file_path(filename)
    hr.add_files(filename, 'verilog_lib')
    hr.set_result_check_string('Simulation end')

    hr.start()

    library = hr._get_library_object('verilog_lib')

    modules = library._get_list_of_lib_modules()

    act_modules = [module.get_name() for module in modules]

    for act_module in act_modules:
        assert act_module in exp_modules, "check %s module" % (act_module)

