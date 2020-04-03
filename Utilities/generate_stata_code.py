#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: generate_stata_code
# @Date: 2020/4/3
# @Author: Mark Wang
# @Email: wangyouan@gamil.com


def generate_foreach2_dep_ind_code(dep, ind, ctrl, fe_option, cluster_option, output_path, text_option,
                                   data_description, condition=''):
    return ['foreach dep_var in {}{{'.format(dep),
            'foreach ind_var in {}{{'.format(ind),
            "capture qui reghdfe `dep_var' `ind_var' {ctrl} {condition}, absorb({fe}) cl({cl})".format(
                dep=dep, ctrl=ctrl, fe=fe_option, cl=cluster_option, condition=condition),
            'qui outreg2 using "{output_file}", addtext({output_text}) {dataconfig} nolabel append'.format(
                output_file=output_path, output_text=text_option,
                dataconfig=data_description),
            '}\n}\n']


def generate_foreach_dep_code(dep, ind, ctrl, fe_option, cluster_option, output_path, text_option,
                              data_description, condition=''):
    return ['foreach dep_var in {}{{'.format(dep),
            "capture qui reghdfe `dep_var' {ind} {ctrl} {condition}, absorb({fe}) cl({cl})".format(
                dep=dep, ctrl=ctrl, fe=fe_option, cl=cluster_option, condition=condition, ind=ind),
            'qui outreg2 using "{output_file}", addtext({output_text}) {dataconfig} nolabel append'.format(
                output_file=output_path, output_text=text_option,
                dataconfig=data_description),
            '}\n']


def generate_regression_code(dep, ind, ctrl, fe_option, cluster_option, output_path, text_option, data_description,
                             condition=''):
    return ['capture qui reghdfe {dep} {ind} {ctrl} {condition}, absorb({fe}) cl({cl})'.format(
        dep=dep, ind=ind, ctrl=ctrl, fe=fe_option, cl=cluster_option, condition=condition),
        'outreg2 using "{output_file}", addtext({output_text}) {dataconfig} nolabel append'.format(
            output_file=output_path, output_text=text_option,
            dataconfig=data_description), '']
