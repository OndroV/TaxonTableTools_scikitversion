def calculate_taxonomic_richness(TaXon_table_xlsx, path_to_outdirs, x_tax_rich, y_tax_rich, template, theme):

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
    number_of_taxa_per_level = statistics_set

    fig = go.Figure(data=[go.Bar(x=taxon_levels, y=number_of_taxa_per_level, name="Taxon", textposition="outside", text=number_of_taxa_per_level)])
    fig.update_traces(marker_color=color1, marker_line_color=color2,marker_line_width=1, opacity=opacity_value)
    fig.update_layout(title_text='Taxonomic richness', yaxis_title="# OTUs")
    fig.update_layout(height=int(y_tax_rich), width=int(x_tax_rich), template=template)

    answer = sg.PopupYesNo('Show plot?', keep_on_top=True)
    if answer == "Yes":
        fig.show()
    bar_pdf = Path(str(path_to_outdirs) + "/" + "Taxonomic_richness_plots" + "/" + TaXon_table_file.stem + "_taxonomic_richness_bar.pdf")
    bar_html = Path(str(path_to_outdirs) + "/" + "Taxonomic_richness_plots" + "/" + TaXon_table_file.stem + "_taxonomic_richness_bar.html")
    fig.write_image(str(bar_pdf))
    fig.write_html(str(bar_html))

    closing_text = "\n" + "Taxonomic richness plots are found in: " + str(path_to_outdirs) + "/taxonomic_richness_plots/"
    sg.Popup(closing_text, title="Finished", keep_on_top=True)

    from taxontabletools.create_log import ttt_log
    ttt_log("taxonomic richness", "analysis", TaXon_table_file.name, bar_pdf.name, "nan", path_to_outdirs)
