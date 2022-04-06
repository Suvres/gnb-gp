data = ModelData();

data = data.createModel("./sample_data/gender.csv", ...
              "gender");


data.save("./sample_data/model_data.csv");


%newData = ModelData();

%newData = newData.readCsv("./sample_data/model_data.csv");

tic
g = GNBSimple();
g = g.simpleComputeSampleData("./sample_data/sample.csv", data.model);
toc

stats_bar(g.statsTable)

