#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Library to create visualizations about the features used in the project

@author: ucaiado

Created on 04/12/2016
"""
# load required libraries
import seaborn as sns


# function to plot bar chart
def bar_chart(student_data, i_plotGroup):
    '''
    Return 3 nomalized bar charts showing the proportion of students that
    passed by feature
    :param student_data: DataFrame. dataframe with 31 columns
    :param i_plotGroup: integer. Group to be ploted (1,2 or 3)
    '''
    if i_plotGroup not in [1, 2, 3]:
        print "The i_plotGroup attribute should be 1, 2 or 3"
        return None
    # Reshape the data
    df_y = student_data.passed
    df = student_data.copy()
    df.drop("passed", axis=1, inplace=True)
    df = df.unstack().reset_index()
    df.columns = ["FEATURE", "IDX", "VALUE"]
    df.drop("IDX", axis=1, inplace=True)
    df["PASSED"] = None
    df["PASSED"] = list(df_y.values) * (student_data.shape[1]-1)
    df["COUNT"] = 1
    # counting occurance of each combination of feature
    df2 = df.groupby(["FEATURE", "VALUE", "PASSED"]).count()
    df3 = df.groupby(["FEATURE", "VALUE"]).count()
    # split the features in each type
    l_c = [[u'Mjob', u'Fjob', u'reason', u'guardian'],
           [u'age', u'Medu', u'Fedu', u'traveltime', u'studytime', u'failures',
            u'famrel', u'freetime', u'goout', u'Dalc', u'Walc', u'health',
            u'absences'],
           [u'school', u'sex', u'address', u'famsize', u'Pstatus', u'paid',
            u'famsup', u'schoolsup', u'activities',
            u'nursery', u'higher', u'internet', u'romantic']]
    # split the data for each feature type
    l_col = l_c[i_plotGroup-1]
    df_plot = df2.loc[l_col].reset_index()
    # normalize the count to be between 0 and 1
    for o in df_plot.iterrows():
        if o[1]['PASSED'] == 'yes':
            df_plot.ix[o[0], "COUNT"] = 1.
        else:
            f_tot = df3.loc[(o[1]["FEATURE"], o[1]["VALUE"])]['COUNT'] * 1.
            df_plot.ix[o[0], "COUNT"] = o[1]['COUNT']/f_tot
    # define the title
    if i_plotGroup == 1:
        s_title = 'Distribution of Categorical Features by Passed Status'
    elif i_plotGroup == 2:
        s_title = 'Distribution of Ordered Categorical Features by Passed'
        s_title += ' Status'
    elif i_plotGroup == 3:
        s_title = 'Distribution of Binary Features by Passed Status'
    # plot data
    g = sns.FacetGrid(df_plot, col="FEATURE", hue="PASSED", col_wrap=5,
                      hue_order=["yes", "no"], margin_titles=True,
                      sharex=False)
    g.map(sns.barplot, "VALUE", "COUNT")
    g.fig.suptitle(s_title, fontsize=18, y=1.03)
    g.despine(left=True).add_legend(title="passed")

    return g
