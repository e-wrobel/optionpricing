options = 'OW20A211150,OW20A211200,OW20A211250,OW20A211350,OW20A211450,OW20A211600,OW20A211650,OW20A211700,OW20A211750,OW20A211800,OW20A211850,OW20A211900,OW20A211925,OW20A211950,OW20A211975,OW20A212000,OW20A212025,OW20A212050,OW20A212075'

for option in options.split(','):
    print('\\begin{figure}[H]')
    print('\t\centering')
    print('\t\includegraphics[width = 1.2\linewidth]'+'{' + option + '.png}')
    print('\t\caption[Historical data for ' + option + ' option and WIG20 asset]{Historical data for ' + option + ' option and WIG20 asset}')
    print('\t\label{fig:' + option +'}')
    print('\end{figure}')
    print()