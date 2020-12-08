def calculate_taxonomic_resolution(TaXon_table_xlsx, path_to_outdirs, x_tax_res, y_tax_res, figure_type, template, theme):

    # TaXon_table_xlsx = "/Users/tillmacher/Desktop/Projects/TTT_Projects/Projects/Tutorial/TaXon_tables/TTT_cons_derep_arthropoda_no_NC.xlsx"
    # path_to_outdirs = "/Users/tillmacher/Desktop/Projects/TTT_Projects/Projects/Tutorial/"
    # x_tax_res = "1000"
    # y_tax_res = "1000"
    # figure_type = "a"
    # template= "seaborn"
    # theme = ["Blue", "Black", 1]

    import glob
    import PySimpleGUI as sg
    import pandas as pd
    from pandas import DataFrame
    import numpy as np
    import plotly.graph_objects as go
    from pathlib import Path

    color1 = theme[0]
    color2 = theme[1]
    opacity_value = theme[2]

    TaXon_table_file =  Path(TaXon_table_xlsx)

    taxonomic_levels = ["Phylum", "Class", "Order", "Family", "Genus", "Species"]

    TaXon_table_xlsx = pd.ExcelFile(TaXon_table_xlsx)
    df = pd.read_excel(TaXon_table_xlsx, 'TaXon table', header=0)
    statistics_list, statistics_set, statistics_dict, highest_level_dict = [], [], {}, {}
    writer = pd.ExcelWriter(TaXon_table_xlsx, engine = 'xlsxwriter')

    for taxon_to_evaluate in taxonomic_levels:
        taxa_list = [x for x in df[taxon_to_evaluate].values.tolist() if str(x) != 'nan']
        statistics = taxon_to_evaluate, len(taxa_list)
        statistics_set.append(len(set(taxa_list)))
        statistics_list.append(list(statistics))
        statistics_dict[taxon_to_evaluate] = len(taxa_list)

    highest_level_dict["Phylum"] = statistics_dict["Phylum"] - statistics_dict["Class"]
    highest_level_dict["Class"] = statistics_dict["Class"] - statistics_dict["Order"]
    highest_level_dict["Order"] = statistics_dict["Order"] - statistics_dict["Family"]
    highest_level_dict["Family"] = statistics_dict["Family"] - statistics_dict["Genus"]
    highest_level_dict["Genus"] = statistics_dict["Genus"] - statistics_dict["Species"]
    highest_level_dict["Species"] = statistics_dict["Species"]

    taxon_levels = list(highest_level_dict.keys())
    highest_level_OTUs = list(highest_level_dict.values())
    total_OTUs = list(statistics_dict.values())

    # create plot
    # option A: scatter plot
    if figure_type == "a":

        fig = go.Figure(data=[go.Bar(x=taxon_levels, y=highest_level_OTUs, name="Taxon", textposition="outside", text=highest_level_OTUs)])
        fig.update_traces(marker_color=color1, marker_line_color=color2,marker_line_width=1, opacity=opacity_value)
        fig.update_layout(title_text='Taxonomic resolution (highest taxonomic level)', yaxis_title="# OTUs")
        fig.update_layout(height=int(y_tax_res), width=int(x_tax_res), template=template)

        answer = sg.PopupYesNo('Show plot?', keep_on_top=True)
        if answer == "Yes":
            fig.show()
        bar_pdf = Path(str(path_to_outdirs) + "/" + "Taxonomic_resolution_plots" + "/" + TaXon_table_file.stem + "_taxonomic_resolution_a.pdf")
        bar_html = Path(str(path_to_outdirs) + "/" + "Taxonomic_resolution_plots" + "/" + TaXon_table_file.stem + "_taxonomic_resolution_a.html")
        fig.write_image(str(bar_pdf))
        fig.write_html(str(bar_html))

        from taxontabletools.create_log import ttt_log
        ttt_log("taxonomic resolution", "analysis", TaXon_table_file.name, bar_pdf.name, "plot a", path_to_outdirs)

    # option B: bar plot
    else:

        fig = go.Figure(data=[go.Bar(x=taxon_levels, y=total_OTUs, name="Taxon", textposition="outside", text=total_OTUs)])
        fig.update_traces(marker_color=color1, marker_line_color=color2,marker_line_width=1, opacity=opacity_value)
        fig.update_layout(title_text='Taxonomic resolution (total number of OTUs)', yaxis_title="# OTUs")
        fig.update_layout(height=int(y_tax_res), width=int(x_tax_res), template=template)

        answer = sg.PopupYesNo('Show plot?', keep_on_top=True)
        if answer == "Yes":
            fig.show()
        bar_pdf = Path(str(path_to_outdirs) + "/" + "Taxonomic_resolution_plots" + "/" + TaXon_table_file.stem + "_taxonomic_resolution_b.pdf")
        bar_html = Path(str(path_to_outdirs) + "/" + "Taxonomic_resolution_plots" + "/" + TaXon_table_file.stem + "_taxonomic_resolution_b.html")
        fig.write_image(str(bar_pdf))
        fig.write_html(str(bar_html))

        from taxontabletools.create_log import ttt_log
        ttt_log("taxonomic resolution", "analysis", TaXon_table_file.name, bar_pdf.name, "plot b", path_to_outdirs)

    closing_text = "\n" + "Taxonomic resolution plots are found in: " + str(path_to_outdirs) + "/taxonomic_resolution_plots/"
    sg.Popup(closing_text, title="Finished", keep_on_top=True)
