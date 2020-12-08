def alpha_diversity_scatter_plot(TaXon_table_xlsx, meta_data_to_test, width, heigth, scatter_size, path_to_outdirs, template):

    import PySimpleGUI as sg
    import pandas as pd
    import numpy as np
    from pathlib import Path
    import plotly.graph_objects as go

    TaXon_table_xlsx =  Path(TaXon_table_xlsx)
    Meta_data_table_xlsx = Path(str(path_to_outdirs) + "/" + "Meta_data_table" + "/" + TaXon_table_xlsx.stem + "_metadata.xlsx")

    TaXon_table_df = pd.read_excel(TaXon_table_xlsx, header=0)
    TaXon_table_samples = TaXon_table_df.columns.tolist()[10:]
    Meta_data_table_df = pd.read_excel(Meta_data_table_xlsx, header=0)
    Meta_data_table_samples = Meta_data_table_df['Samples'].tolist()
    categories = Meta_data_table_df[meta_data_to_test].tolist()

    if len(set(Meta_data_table_df[meta_data_to_test])) == 1:
        sg.PopupError("The meta data has to differ between samples!", title="Error")
        raise RuntimeError

    if sorted(TaXon_table_samples) == sorted(Meta_data_table_samples):

        samples = Meta_data_table_samples
        OTU_abundances_dict = {}
        samples_metadata_list = []

        # remove samples that do not fit the format
        for i, sample in enumerate(samples):
            meta_data = str(Meta_data_table_df.loc[i][meta_data_to_test])
            samples_metadata_list.append(meta_data)

        #################################
        # Calculate Alpha diversity measurements (= observed_otus)

        observed_otus_dict = {}
        samples_dict = {}

        for i, sample in enumerate(samples):
            observed_otus = len([taxon for taxon in TaXon_table_df[sample].values.tolist() if taxon != 0])
            category = samples_metadata_list[i]
            if category not in observed_otus_dict.keys():
                observed_otus_dict[category] = [observed_otus]
                samples_dict[category] = [sample]
            else:
                observed_otus_dict[category] = observed_otus_dict[category] + [observed_otus]
                samples_dict[category] = samples_dict[category] + [sample]

        ########################################
        # create the plot

        fig = go.Figure()
        for category in set(categories):
            fig.add_trace(go.Scatter(x=samples_dict[category], y=observed_otus_dict[category], mode='markers', name=category, marker=dict(size=int(scatter_size))))
        fig.update_layout(height=int(heigth), width=int(width), template=template, yaxis_title="# OTUs", showlegend=True)

        # finish script
        answer = sg.PopupYesNo('Show plot?', keep_on_top=True)
        if answer == "Yes":
            fig.show()

        bar_pdf = Path(str(path_to_outdirs) + "/" + "Alpha_diversity" + "/" + TaXon_table_xlsx.stem + "_" + meta_data_to_test + "_scatter_plot.pdf")
        bar_html = Path(str(path_to_outdirs) + "/" + "Alpha_diversity" + "/" + TaXon_table_xlsx.stem + "_" + meta_data_to_test + "_scatter_plot.html")
        fig.write_image(str(bar_pdf))
        fig.write_html(str(bar_html))

        sg.Popup("Alpha diversity estimate are found in", path_to_outdirs, "/Alpha_diversity/", title="Finished", keep_on_top=True)
        from taxontabletools.create_log import ttt_log
        ttt_log("alpha diversity scatter", "analysis", TaXon_table_xlsx.name, bar_pdf.name, meta_data_to_test, path_to_outdirs)

    else:
        sg.PopupError("Error: The samples between the taxon table and meta table do not match!", keep_on_top=True)

def alpha_diversity_boxplot(TaXon_table_xlsx, meta_data_to_test, width, heigth, scatter_size, path_to_outdirs, template, theme):

    import PySimpleGUI as sg
    import pandas as pd
    import numpy as np
    from pathlib import Path
    import plotly.graph_objects as go

    color1 = theme[0]
    color2 = theme[1]
    opacity_value = theme[2]

    TaXon_table_xlsx =  Path(TaXon_table_xlsx)
    Meta_data_table_xlsx = Path(str(path_to_outdirs) + "/" + "Meta_data_table" + "/" + TaXon_table_xlsx.stem + "_metadata.xlsx")

    TaXon_table_df = pd.read_excel(TaXon_table_xlsx, header=0)
    TaXon_table_samples = TaXon_table_df.columns.tolist()[10:]
    Meta_data_table_df = pd.read_excel(Meta_data_table_xlsx, header=0)
    Meta_data_table_samples = Meta_data_table_df['Samples'].tolist()
    categories = Meta_data_table_df[meta_data_to_test].tolist()

    if len(set(Meta_data_table_df[meta_data_to_test])) == 1:
        sg.PopupError("The meta data has to differ between samples!", title="Error")
        raise RuntimeError

    if sorted(TaXon_table_samples) == sorted(Meta_data_table_samples):

        samples = Meta_data_table_samples
        OTU_abundances_dict = {}
        samples_metadata_list = []

        # remove samples that do not fit the format
        for i, sample in enumerate(samples):
            meta_data = str(Meta_data_table_df.loc[i][meta_data_to_test])
            samples_metadata_list.append(meta_data)

        #################################
        # Calculate Alpha diversity measurements (= observed_otus)

        observed_otus_dict = {}

        for i, sample in enumerate(samples):
            observed_otus = len([taxon for taxon in TaXon_table_df[sample].values.tolist() if taxon != 0])
            category = samples_metadata_list[i]
            if category not in observed_otus_dict.keys():
                observed_otus_dict[category] = [observed_otus]
            else:
                observed_otus_dict[category] = observed_otus_dict[category] + [observed_otus]

        ########################################
        # create the plot

        fig = go.Figure()
        for category in set(categories):
            fig.add_trace(go.Box(y=observed_otus_dict[category], name=category, marker_color=color1, marker_line_color=color2, marker_line_width=0.2, opacity=opacity_value))
        fig.update_layout(height=int(heigth), width=int(width), template=template, yaxis_title="# OTUs", showlegend=False)

        # finish script
        answer = sg.PopupYesNo('Show plot?', keep_on_top=True)
        if answer == "Yes":
            fig.show()

        bar_pdf = Path(str(path_to_outdirs) + "/" + "Alpha_diversity" + "/" + TaXon_table_xlsx.stem + "_" + meta_data_to_test + "_boxplot.pdf")
        bar_html = Path(str(path_to_outdirs) + "/" + "Alpha_diversity" + "/" + TaXon_table_xlsx.stem + "_" + meta_data_to_test + "_boxplot.html")
        fig.write_image(str(bar_pdf))
        fig.write_html(str(bar_html))

        sg.Popup("Alpha diversity estimate are found in", path_to_outdirs, "/Alpha_diversity/", title="Finished", keep_on_top=True)
        from taxontabletools.create_log import ttt_log
        ttt_log("alpha diversity boxplot", "analysis", TaXon_table_xlsx.name, bar_pdf.name, meta_data_to_test, path_to_outdirs)

    else:
        sg.PopupError("Error: The samples between the taxon table and meta table do not match!", keep_on_top=True)
