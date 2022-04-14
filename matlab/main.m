%data = ModelData();

%data = data.createModel("/home/suvres/Dokumenty/AGH/inzynierka/dane_ids/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv", ...
%              "Label");


%data.save("../model_data_ids.csv");


data = ModelData();

data = data.readCsv("../model_data_ids.csv");

tic
g = GNBSimple();
g = g.simpleComputeSampleData("/home/suvres/Dokumenty/AGH/inzynierka/dane_ids/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv", data.model);
toc

stats_bar(g.statsTable)

